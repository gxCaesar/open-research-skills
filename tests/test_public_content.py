import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_public_content.py"
DECK = (
    ROOT / "skills"
    / "build-scientific-visualizations" / "assets" / "design-templates"
    / "diagram-style-library.pptx"
)


class PublicContentTest(unittest.TestCase):
    def test_actual_public_tree_passes(self):
        result = self.run_checker(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def run_checker(
        self, root: Path, deny_term_file: Optional[Path] = None
    ) -> subprocess.CompletedProcess:
        command = [sys.executable, str(CHECKER), str(root)]
        if deny_term_file is not None:
            command.extend(["--deny-term-file", str(deny_term_file)])
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_clean_public_tree_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "skills" / "safe"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("# Safe public workflow\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("failures=0", result.stdout)

    def test_missing_candidate_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "missing"
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("candidate_root", result.stdout)

    def test_root_level_macos_private_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Read " + "/" + "Users" + "/example-user/private-note.md\n",
                encoding="utf-8",
            )
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("absolute_macos_user_path", result.stdout)

    def test_extensionless_text_is_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Dockerfile").write_text(
                "COPY " + "/" + "Users" + "/example-user/private-token /app/token\n",
                encoding="utf-8",
            )
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("absolute_macos_user_path", result.stdout)

    def test_linux_private_path_and_private_account_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "guide.md"
            target.write_text(
                "Read "
                + "/"
                + "home"
                + "/example-user/private-note.md and ~/"
                + ".ssh"
                + "/config\n",
                encoding="utf-8",
            )
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("absolute_linux_home_path", result.stdout)
            self.assertIn("private_account_path", result.stdout)

    def test_external_release_specific_deny_term_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "candidate"
            root.mkdir()
            private_term = "internal" + "-machine-42"
            (root / "README.md").write_text(private_term + "\n", encoding="utf-8")
            deny_file = Path(tmp) / "deny-terms.txt"
            deny_file.write_text(private_term + "\n", encoding="utf-8")
            result = self.run_checker(root, deny_file)
            self.assertEqual(1, result.returncode)
            self.assertIn("release_specific_term", result.stdout)

    def test_deny_term_in_filename_is_redacted_from_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "candidate"
            root.mkdir()
            private_term = "synthetic" + "-private-identity-canary"
            (root / (private_term.upper() + ".md")).write_text("example\n", encoding="utf-8")
            deny_file = Path(tmp) / "private-terms.txt"
            deny_file.write_text(private_term + "\n", encoding="utf-8")
            result = self.run_checker(root, deny_file)
            self.assertEqual(1, result.returncode)
            self.assertIn("release_specific_term", result.stdout)
            self.assertNotIn(private_term, result.stdout.casefold())
            self.assertIn("[redacted].md", result.stdout)

    def test_internal_control_filename_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "pipeline-" + "state.json"
            (root / name).write_text("{}\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("internal_control_artifact", result.stdout)

    def test_agent_instruction_filename_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "AG" + "ENTS.md"
            (root / name).write_text("internal instructions\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("internal_control_artifact", result.stdout)

    def test_author_created_integrity_side_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            phrase = "Publish the check" + "sum manifest with the release.\n"
            (root / "instructions.md").write_text(phrase, encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("integrity_side_record", result.stdout)

    def test_symlink_is_rejected_without_following_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.md"
            target.write_text("safe\n", encoding="utf-8")
            os.symlink(target.name, root / "linked.md")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("symlink", result.stdout)

    def test_nested_repository_metadata_is_rejected(self):
        """The candidate's own root metadata may exist locally; vendored metadata may not."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "skills" / "example" / ".git"
            nested.mkdir(parents=True)
            (nested / "config").write_text("synthetic repository metadata\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("internal_control_artifact", result.stdout)

    def test_finder_metadata_is_rejected_even_when_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".DS_Store").write_bytes(b"\x00\x00synthetic Finder record")
            result = self.run_checker(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("operating_system_metadata", result.stdout)

    def test_clean_real_pptx_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copyfile(DECK, root / DECK.name)
            result = self.run_checker(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("failures=0", result.stdout)

    def mutate_deck(self, destination: Path, member: str, change) -> None:
        """Change one real OOXML part, preserving the other archive members."""
        with ZipFile(DECK) as source, ZipFile(destination, "w") as output:
            self.assertIn(member, source.namelist())
            for info in source.infolist():
                content = source.read(info)
                if info.filename == member:
                    content = change(content)
                output.writestr(info, content)

    def test_pptx_private_paths_in_slide_notes_and_relationships_are_rejected(self):
        private_path = "/" + "Users" + "/example-user/private-note.md"
        cases = (
            ("ppt/slides/slide1.xml", "t"),
            ("ppt/notesSlides/notesSlide1.xml", "t"),
            ("ppt/_rels/presentation.xml.rels", "Relationship"),
        )
        for member, tag in cases:
            with self.subTest(member=member), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)

                def inject(content):
                    document = ET.fromstring(content)
                    element = next(e for e in document.iter() if e.tag.rsplit("}", 1)[-1] == tag)
                    if tag == "Relationship":
                        element.set("Target", "file://" + private_path)
                        element.set("TargetMode", "External")
                    else:
                        element.text = private_path
                    return ET.tostring(document, encoding="utf-8")

                self.mutate_deck(root / "example.pptx", member, inject)
                result = self.run_checker(root)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("absolute_macos_user_path", result.stdout)
                self.assertIn(member, result.stdout)
                self.assertNotIn(private_path, result.stdout)

    def test_pptx_core_metadata_respects_deny_terms_and_xml_encoding(self):
        private_term = "synthetic" + "-private-identity-canary"
        for encoding in ("utf-8", "utf-16"):
            with self.subTest(encoding=encoding), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "candidate"
                root.mkdir()
                deny_file = Path(tmp) / "private-terms.txt"
                deny_file.write_text(private_term + "\n", encoding="utf-8")

                def inject(content):
                    document = ET.fromstring(content)
                    creator = document.find("{http://purl.org/dc/elements/1.1/}creator")
                    self.assertIsNotNone(creator)
                    creator.text = private_term
                    return ET.tostring(document, encoding=encoding)

                self.mutate_deck(root / "example.pptx", "docProps/core.xml", inject)
                result = self.run_checker(root, deny_file)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("release_specific_term", result.stdout)
                self.assertIn("docProps/core.xml", result.stdout)
                self.assertNotIn(private_term, result.stdout)

    def test_unreadable_pptx_is_rejected_instead_of_silently_skipped(self):
        for kind in ("invalid_archive", "invalid_xml"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                destination = root / "example.pptx"
                if kind == "invalid_archive":
                    destination.write_bytes(b"not an office archive")
                else:
                    self.mutate_deck(destination, "docProps/core.xml", lambda _: b"<unfinished")
                result = self.run_checker(root)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("unreadable_pptx", result.stdout)

    def test_current_repository_candidate_is_clean(self):
        result = self.run_checker(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("failures=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
