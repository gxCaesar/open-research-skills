"""Check the repository's install unit and usable local documentation targets."""

from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "prepare-journal-manuscripts"


class RepositoryContractTest(unittest.TestCase):
    def test_one_complete_install_unit(self):
        entries = list(SKILL.rglob("SKILL.md"))
        self.assertEqual([SKILL / "SKILL.md"], entries)
        for name in ("LICENSE", "NOTICE", "THIRD_PARTY.md", "README.md", "MAINTAINERS.md"):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertFalse(any(path.is_symlink() for path in SKILL.rglob("*")))

    def test_documented_local_resources_resolve_inside_the_install_unit(self):
        skill = SKILL
        documents = list(skill.rglob("*.md"))
        for document in documents:
            content = document.read_text(encoding="utf-8")
            for raw in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", content):
                target = raw.strip().split(maxsplit=1)[0].strip("<>")
                parsed = urlparse(target)
                if parsed.scheme or not parsed.path:
                    continue
                resolved = (document.parent / unquote(parsed.path)).resolve()
                boundary = skill if document.is_relative_to(skill) else ROOT
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(boundary), "link leaves installation")
                    self.assertTrue(resolved.exists(), "missing local resource")
            if document.is_relative_to(skill):
                for relative in re.findall(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)", content):
                    with self.subTest(document=document.relative_to(ROOT), command=relative):
                        self.assertTrue((skill / relative).resolve().is_relative_to(skill))
                        self.assertTrue((skill / relative).exists(), "missing command target")

    def test_public_tree_scan(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "check_public_content.py"), str(SKILL)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
