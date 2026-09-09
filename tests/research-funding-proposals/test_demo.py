import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "writing-funding-proposals"
SNAPSHOT_AS_OF = "2024-02-29"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class FundingDemoTest(unittest.TestCase):
    def test_copied_skill_runs_complete_synthetic_demo_and_preserves_output_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            installed_skill = root / "installed-skill"
            shutil.copytree(SKILL, installed_skill)
            output = root / "synthetic-demo"
            demo = installed_skill / "examples" / "run_demo.py"

            completed = run_script(demo, str(output))

            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            self.assertIn("SYNTHETIC DEMO ONLY", completed.stdout)
            self.assertIn("Observed validator status: PASS", completed.stdout)
            self.assertIn(
                "Observed validator scope: record_completeness (record-only)",
                completed.stdout,
            )
            self.assertTrue((output / "project.json").is_file())

            sentinel = output / "do-not-overwrite.txt"
            sentinel.write_text("keep", encoding="utf-8")
            overwrite = run_script(demo, str(output))
            self.assertNotEqual(0, overwrite.returncode)
            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))

            inside_skill = installed_skill / "examples" / "generated-output"
            rejected_inside = run_script(demo, str(inside_skill))
            self.assertNotEqual(0, rejected_inside.returncode)
            self.assertFalse(inside_skill.exists())

            (output / "delivery" / "official-template.pdf").unlink()
            invalid = run_script(
                installed_skill / "scripts" / "validate_proposal_workspace.py",
                str(output),
                "--mode",
                "final",
                "--as-of",
                SNAPSHOT_AS_OF,
                "--json",
            )
            self.assertEqual(1, invalid.returncode)
            self.assertIn(
                "official template artifact_path must name an in-workspace regular file",
                invalid.stdout,
            )


if __name__ == "__main__":
    unittest.main()
