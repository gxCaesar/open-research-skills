"""Check the release package validator against a real package and one witness per rule.

The failing packages are built here rather than shipped. A directory demonstrating the
failures would contain absolute home paths and addresses, which the repository's own
content scan rejects, so shipping one would make the repository fail its own gate.
"""

import contextlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "release-research-artifacts"
CHECKER = SKILL / "scripts" / "check_release_package.py"
PACKAGE = SKILL / "examples" / "release-package"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_release_package", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


@contextlib.contextmanager
def copied_package(edit=None):
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "package"
        shutil.copytree(PACKAGE, target)
        if edit is not None:
            edit(target)
        yield target


def rules(root, mode="named"):
    findings, _ = checker.check(root, mode)
    return {rule for rule, _ in findings}


def edit_record(root, change):
    path = root / "RELEASED_FILES.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    change(record)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


class ReleasePackageTest(unittest.TestCase):
    def test_shipped_package_passes_in_both_modes(self):
        for mode in ("anonymized", "named"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    [sys.executable, "-B", str(CHECKER), str(PACKAGE), "--mode", mode],
                    text=True, capture_output=True, check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("failures=0", result.stdout)

    def test_the_shipped_package_reproduces_the_number_its_record_claims(self):
        """The record says what the verification run produced; the run has to agree."""
        result = subprocess.run(
            [sys.executable, "-B", str(PACKAGE / "src" / "reproduce.py")],
            cwd=PACKAGE, text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        record = json.loads((PACKAGE / "RELEASED_FILES.json").read_text(encoding="utf-8"))
        self.assertIn(result.stdout.strip(), record["verification"]["result"])

    def test_a_missing_package_directory_is_rejected(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(SKILL / "examples" / "absent-package")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("package_directory_missing", result.stdout)

    def test_a_deny_term_in_a_released_file_is_reported(self):
        with copied_package() as package, tempfile.TemporaryDirectory() as tmp:
            term = "synthetic" + "-private-project-name"
            (package / "README.md").write_text(f"built for {term}\n", encoding="utf-8")
            deny = Path(tmp) / "terms.txt"
            deny.write_text(term + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(package),
                 "--deny-term-file", str(deny)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("release_specific_term_in_released_file", result.stdout)
            self.assertIn("deny_terms=1", result.stdout)

    def test_every_declared_rule_has_a_witness(self):
        def unlink(name):
            return lambda root: (root / name).unlink()

        witnesses = {
            "release_record_missing": unlink("RELEASED_FILES.json"),
            "release_record_unreadable":
                lambda root: (root / "RELEASED_FILES.json").write_text("{", encoding="utf-8"),
            "release_record_missing_field":
                lambda root: edit_record(root, lambda r: r.pop("built_from_commit")),
            "verification_missing_field":
                lambda root: edit_record(root, lambda r: r["verification"].pop("command")),
            "verification_is_not_an_object":
                lambda root: edit_record(root, lambda r: r.update(verification="it ran")),
            "digest_algorithm_unavailable":
                lambda root: edit_record(root, lambda r: r.update(digest_algorithm="rot13")),
            "file_entry_is_not_an_object":
                lambda root: edit_record(root, lambda r: r["files"].append("LICENSE")),
            "file_entry_without_a_path":
                lambda root: edit_record(root, lambda r: r["files"].append({"bytes": 1})),
            "listed_path_escapes_the_package":
                lambda root: edit_record(root, lambda r: r["files"].append({"path": "../secret.txt"})),
            "listed_file_absent": lambda root: (root / "data" / "scores.csv").unlink(),
            "file_entry_without_a_size":
                lambda root: edit_record(root, lambda r: r["files"][0].pop("bytes")),
            "size_does_not_match_the_record":
                lambda root: (root / "README.md").write_text("short\n", encoding="utf-8"),
            "file_entry_without_a_digest":
                lambda root: edit_record(root, lambda r: r["files"][0].update(digest="")),
            "digest_does_not_match_the_record": lambda root: edit_record(
                root, lambda r: r["files"][0].update(digest="0" * 128)),
            "file_present_but_not_listed":
                lambda root: (root / "notes.txt").write_text("left over\n", encoding="utf-8"),
            # Nested on purpose. A root-only check passed this exact case, so the witness has
            # to sit where the checker used to be blind rather than where it always looked.
            "version_control_metadata_present":
                lambda root: (root / "src" / ".git").mkdir(parents=True),
            "build_cache_present":
                lambda root: (root / "src" / "__pycache__").mkdir(parents=True),
            "environment_specification_missing": unlink("requirements.txt"),
            "dependency_not_pinned":
                lambda root: (root / "requirements.txt").write_text("numpy\n", encoding="utf-8"),
            "licence_missing": unlink("LICENSE"),
            "citation_metadata_missing": unlink("CITATION.cff"),
            "persistent_identifier_missing":
                lambda root: edit_record(root, lambda r: r.pop("persistent_identifier")),
            "code_and_data_licences_not_stated_separately":
                lambda root: edit_record(root, lambda r: r.pop("data_licence")),
            "file_not_readable_as_text_and_not_inspected":
                lambda root: (root / "data" / "scores.csv").write_bytes(b"\xff\xfe\x00binary"),
            # Composed at runtime: the literal is what the repository's own content
            # scan rejects, so writing it out here would fail the public tree.
            "absolute_home_path_in_released_file": lambda root: (root / "README.md").write_text(
                "run it from /" + "Users" + "/someone/project\n", encoding="utf-8"),
            "email_address_in_released_file": lambda root: (root / "README.md").write_text(
                "questions to someone@example.org\n", encoding="utf-8"),
        }

        self.assertEqual(set(), rules(PACKAGE), "the shipped package must be silent")
        for rule, edit in witnesses.items():
            with self.subTest(rule=rule), copied_package(edit) as package:
                self.assertIn(rule, rules(package))

        source = CHECKER.read_text(encoding="utf-8")
        # Rules are emitted both as findings.append((...)) and as return [(...)]; a
        # pattern that sees only the first form silently under-reports the rule set.
        declared = set(re.findall(r'[(\[]\("([a-z_]+)"', source))
        # Reported by main() rather than by check(); covered by their own tests above.
        declared -= {"package_directory_missing", "release_specific_term_in_released_file",
                     "release_specific_term_in_a_filename"}
        self.assertEqual(set(), declared - set(witnesses), "rule with no witness")
        self.assertGreaterEqual(len(declared), 24, declared)


if __name__ == "__main__":
    unittest.main()
