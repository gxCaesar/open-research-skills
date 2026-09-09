"""Check the run-cold-review-panel install unit, its declared modes and its public content."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "run-cold-review-panel"
MODE_ROW = re.compile(r"^\|\s*`([a-z][a-z-]+)`\s*\|[^|]+\|\s*`(references/[^`]+)`\s*\|\s*$", re.M)


def declared_modes(skill_root: Path) -> list[tuple[str, str]]:
    """Modes and their reading targets, taken from the SKILL.md selection table."""
    return MODE_ROW.findall((skill_root / "SKILL.md").read_text(encoding="utf-8"))


def missing_mode_targets(skill_root: Path) -> list[str]:
    """Reading targets a mode declares that an exact install would not contain."""
    findings = []
    for mode, target in declared_modes(skill_root):
        resolved = (skill_root / target).resolve()
        if not resolved.is_relative_to(skill_root.resolve()) or not resolved.is_file():
            findings.append(f"{mode} -> {target}")
    return findings


class ColdReviewPanelContractTest(unittest.TestCase):
    def test_one_complete_install_unit(self):
        self.assertEqual([SKILL / "SKILL.md"], list(SKILL.rglob("SKILL.md")))
        self.assertFalse(any(path.is_symlink() for path in SKILL.rglob("*")))
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())

    def test_every_declared_mode_has_a_reading_target(self):
        modes = declared_modes(SKILL)
        self.assertGreaterEqual(len(modes), 3, "the selection table did not parse")
        self.assertEqual([], missing_mode_targets(SKILL))

    def test_a_removed_reading_target_is_rejected(self):
        """The mode check must fail when an exact install would lack the target."""
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "run-cold-review-panel"
            shutil.copytree(SKILL, mutated)
            first = declared_modes(mutated)[0][1]
            (mutated / first).unlink()
            self.assertNotEqual([], missing_mode_targets(mutated))

    def test_documented_local_resources_resolve_inside_the_install_unit(self):
        for document in SKILL.rglob("*.md"):
            content = document.read_text(encoding="utf-8")
            for raw in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", content):
                target = raw.strip().split(maxsplit=1)[0].strip("<>")
                parsed = urlparse(target)
                if parsed.scheme or not parsed.path:
                    continue
                resolved = (document.parent / unquote(parsed.path)).resolve()
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(SKILL.resolve()), "link leaves installation")
                    self.assertTrue(resolved.exists(), "missing local resource")
            for relative in re.findall(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)", content):
                with self.subTest(document=document.relative_to(ROOT), command=relative):
                    self.assertTrue((SKILL / relative).exists(), "missing command target")

    def test_public_tree_scan(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "check_public_content.py"), str(SKILL)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
