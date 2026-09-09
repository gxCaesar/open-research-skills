"""Fresh-install behavior checks for the conference manuscript skill.

These tests catch a package that happens to work only because sibling package
directories remain present in the repository checkout.  Each case copies exactly the
public skill directory before it invokes a bundled command.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse


PACKAGE = Path(__file__).resolve().parents[1]
SKILL = PACKAGE / "skills" / "prepare-conference-manuscripts"


@contextmanager
def fresh_skill_copy() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        installed = Path(tmp) / "prepare-conference-manuscripts"
        shutil.copytree(SKILL, installed)
        yield installed


def run_python(script: Path, *args: str, input_text: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def words(count: int) -> str:
    return " ".join("word" for _ in range(count))


class IsolatedConferenceSkillTest(unittest.TestCase):
    def test_fresh_copy_includes_whole_paper_workflow_resources(self):
        """Break caught: an installed skill omits its linked whole-paper workflow resources."""
        with fresh_skill_copy() as skill:
            workflow = skill / "references" / "full-paper-workflow.md"
            deliverables = skill / "assets" / "full-paper-deliverables.md"

            self.assertTrue(workflow.is_file(), workflow)
            self.assertTrue(deliverables.is_file(), deliverables)

    def test_fresh_copy_runs_aaai_abstract_checker_on_known_good_and_bad_inputs(self):
        """Break caught: omitting the bundled abstract checker from an installed skill."""
        with fresh_skill_copy() as skill:
            checker = skill / "components" / "abstract" / "scripts" / "check_abstract.py"
            good = run_python(checker, "--venue", "aaai", input_text=words(160))
            bad = run_python(checker, "--venue", "aaai", input_text=words(149))

        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        self.assertIn("Add at least 1 word", bad.stdout)

    def test_fresh_copy_runs_iclr_abstract_checker_on_known_good_and_bad_inputs(self):
        """Break caught: an ICLR abstract check accidentally depends on another package."""
        with fresh_skill_copy() as skill:
            checker = skill / "components" / "abstract" / "scripts" / "check_abstract.py"
            good = run_python(checker, "--venue", "iclr", input_text=words(160))
            bad = run_python(
                checker,
                "--venue",
                "iclr",
                input_text=words(160) + " [12]",
            )

        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        self.assertIn("[12]", bad.stdout)

    def test_fresh_copy_statistics_validator_outputs_are_path_free(self):
        """Break caught: the analysis-register validator exposes installed or input paths."""
        with fresh_skill_copy() as skill:
            validator = (
                skill
                / "components"
                / "statistics-reporting"
                / "scripts"
                / "validate_analysis_register.py"
            )
            example = (
                skill
                / "components"
                / "statistics-reporting"
                / "examples"
                / "analysis-register.example.json"
            )
            self.assertTrue(validator.is_file(), validator)
            self.assertTrue(example.is_file(), example)
            good = run_python(validator, str(example), "--mode", "final", "--format", "json")
            payload = json.loads(example.read_text(encoding="utf-8"))
            payload["analyses"][0]["independent_unit"] = ""
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                bad_path = root / "bad-register.json"
                bad_path.write_text(json.dumps(payload), encoding="utf-8")
                bad = run_python(validator, str(bad_path), "--mode", "final", "--format", "json")
                missing = run_python(
                    validator,
                    str(root / "missing-register.json"),
                    "--mode",
                    "final",
                    "--format",
                    "json",
                )
                malformed_path = root / "malformed-register.json"
                malformed_path.write_text("{", encoding="utf-8")
                malformed = run_python(
                    validator,
                    str(malformed_path),
                    "--mode",
                    "final",
                    "--format",
                    "json",
                )
                non_utf8_path = root / "non-utf8-register.json"
                non_utf8_path.write_bytes(b"\xff")
                non_utf8 = run_python(
                    validator,
                    str(non_utf8_path),
                    "--mode",
                    "final",
                    "--format",
                    "json",
                )

        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertEqual(
            "analysis-register.example.json",
            json.loads(good.stdout)["target"],
            good.stdout + good.stderr,
        )
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        self.assertIn("INDEPENDENT_UNIT", bad.stdout)
        for label, result, basename, summary in (
            (
                "missing register",
                missing,
                "missing-register.json",
                "FileNotFoundError: No such file or directory",
            ),
            (
                "malformed register",
                malformed,
                "malformed-register.json",
                "invalid JSON at line 1, column 2",
            ),
            (
                "non-UTF-8 register",
                non_utf8,
                "non-utf8-register.json",
                "UnicodeDecodeError",
            ),
        ):
            with self.subTest(case=label):
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(basename, result.stderr)
                self.assertIn(summary, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                for forbidden in (str(root), "/private/tmp", "/Users"):
                    self.assertNotIn(forbidden, result.stderr)

    def test_task_local_generic_profile_uses_its_configured_style_rule(self):
        """Break caught: every non-AAAI profile is labeled as ICLR by the TeX audit."""
        with fresh_skill_copy() as skill, tempfile.TemporaryDirectory() as tmp:
            audit_tex = skill / "components" / "manuscript-core" / "scripts" / "audit_tex.py"
            template = skill / "components" / "venues" / "generic" / "references" / "venue-profile.template.json"
            self.assertTrue(audit_tex.is_file(), audit_tex)
            self.assertTrue(template.is_file(), template)
            profile = json.loads(template.read_text(encoding="utf-8"))
            self.assertEqual(0, profile["year"], "A generic template must not imply a real venue year.")
            self.assertTrue(
                all(
                    source_id.startswith("REPLACE_WITH_")
                    for source_ids in profile["rule_sources"].values()
                    for source_id in source_ids
                ),
                "Generic rule-source IDs must remain unmistakable placeholders.",
            )
            profile["venue"] = "Synthetic Computing Conference"
            profile["year"] = 2027
            profile["track"] = "Main track"
            profile["checked_on"] = "2026-09-04"
            profile["rule_sources"] = {
                "DOCUMENT_CLASS": ["SYNTHETIC_AUTHOR_GUIDE"],
                "SYNTHETIC_STYLE_CURRENT": ["SYNTHETIC_AUTHOR_GUIDE"],
                "ABSTRACT_REQUIRED": ["SYNTHETIC_AUTHOR_GUIDE"],
            }
            profile["tex_contract"].update(
                {
                    "document_class": "article",
                    "style_package": "synthetic2027",
                    "style_rule_id": "SYNTHETIC_STYLE_CURRENT",
                    "required_options": {"anonymous_submission": []},
                    "anonymous_stages": [],
                    "require_abstract": ["anonymous_submission"],
                }
            )
            root = Path(tmp)
            profile_path = root / "synthetic-profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            good_tex = root / "good.tex"
            good_tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            bad_tex = root / "bad.tex"
            bad_tex.write_text(
                r"""\documentclass{article}
\usepackage{wrongstyle}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            good = run_python(
                audit_tex,
                str(good_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            bad = run_python(
                audit_tex,
                str(bad_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(bad.stdout)["findings"]}
        self.assertIn("SYNTHETIC_STYLE_CURRENT", rule_ids)
        self.assertFalse(any(rule_id.startswith("ICLR_") for rule_id in rule_ids), rule_ids)

    def test_local_markdown_links_resolve_from_each_owning_document(self):
        """Break caught: moving a component leaves a broken local Markdown reference."""
        targets = []
        link = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
        documents = [PACKAGE / "README.md", *sorted(SKILL.rglob("*.md"))]
        for document in documents:
            for target in link.findall(document.read_text(encoding="utf-8")):
                target = target.strip().split(maxsplit=1)[0]
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                relative = parsed.path
                if relative:
                    targets.append((document, relative))

        self.assertTrue(targets, "Document local paths as Markdown links so an installer can verify them.")
        for document, relative in targets:
            with self.subTest(document=document, relative=relative):
                self.assertTrue((document.parent / relative).is_file())

    def test_readme_skill_dir_commands_name_reachable_local_tools(self):
        """Break caught: README commands assume the package checkout rather than an installation."""
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)", readme)
        self.assertTrue(targets, "README must give commands rooted at $SKILL_DIR.")
        with fresh_skill_copy() as skill:
            for relative in targets:
                with self.subTest(relative=relative):
                    self.assertTrue((skill / relative).is_file())


if __name__ == "__main__":
    unittest.main()
