import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "skills" / "research-publication-pipeline"
EXAMPLE = SKILL / "examples" / "perturbation-comparison"


class PerturbationComparisonTest(unittest.TestCase):
    def run_analysis(self, example, scores, output, cwd):
        return subprocess.run(
            [sys.executable, "-B", str(example / "analyze_scores.py"),
             "--scores", str(scores), "--output", str(output)],
            cwd=cwd, text=True, capture_output=True, check=False,
        )

    def test_six_real_rows_and_isolated_install_produce_paired_results(self):
        """Catch reversed differences, dropped losses and checkout-only imports."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copied = root / "installed-skill"
            shutil.copytree(SKILL, copied)
            for name, example in (
                ("checkout", EXAMPLE),
                ("installed", copied / "examples" / "perturbation-comparison"),
            ):
                with self.subTest(location=name):
                    output = root / name
                    result = self.run_analysis(example, example / "scores.csv", output, root)
                    self.assertEqual(0, result.returncode, result.stderr)
                    summary = json.loads((output / "summary.json").read_text())
                    self.assertEqual(6, summary["tasks"])
                    self.assertEqual((4, 2, 0), (summary["wins"], summary["losses"], summary["ties"]))
                    self.assertAlmostEqual(0.005, summary["mean_difference"])
                    with (output / "differences.csv").open(newline="") as stream:
                        rows = list(csv.DictReader(stream))
                    self.assertEqual(["task-1", "task-2", "task-3", "task-4", "task-5", "task-6"],
                                     [row["task"] for row in rows])
                    self.assertEqual([0.02, 0.01, -0.01, 0.02, 0.01, -0.02],
                                     [float(row["difference"]) for row in rows])
                    self.assertIn("synthetic", (output / "summary.md").read_text().lower())

    def test_uniform_scores_do_not_generate_a_mixed_direction_claim(self):
        """Catch a canned mixed-result interpretation on all-positive or tied inputs."""
        cases = (
            ("positive", "task,baseline,candidate\na,0.2,0.3\nb,0.4,0.6\n",
             (2, 0, 0), "每项候选分数均高于基线"),
            ("tied", "task,baseline,candidate\na,0.2,0.2\nb,0.4,0.4\n",
             (0, 0, 2), "所有任务分数均相等"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, text, counts, conclusion in cases:
                with self.subTest(input=name):
                    scores = root / (name + ".csv")
                    scores.write_text(text)
                    output = root / name
                    result = self.run_analysis(EXAMPLE, scores, output, root)
                    self.assertEqual(0, result.returncode, result.stderr)
                    summary = json.loads((output / "summary.json").read_text())
                    self.assertEqual(counts, (summary["wins"], summary["losses"], summary["ties"]))
                    brief = (output / "summary.md").read_text()
                    self.assertNotIn("混合方向", brief)
                    self.assertIn(conclusion, brief)
                    self.assertIn("synthetic", brief.lower())

    def test_duplicate_or_nonfinite_row_is_rejected_before_output_creation(self):
        """Catch counting a repeated task or accepting NaN as a valid score."""
        original = (EXAMPLE / "scores.csv").read_text()
        mutations = {
            "duplicate": original.replace("task-6,", "task-1,"),
            "nonfinite": original.replace("0.64", "nan"),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, text in mutations.items():
                with self.subTest(mutation=name):
                    scores = root / (name + ".csv")
                    scores.write_text(text)
                    output = root / name
                    result = self.run_analysis(EXAMPLE, scores, output, root)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(name, result.stderr.lower())
                    self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        """Catch an accidental overwrite of an earlier analysis."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "previous"
            output.mkdir()
            summary = output / "summary.json"
            summary.write_text("previous result\n")
            result = self.run_analysis(EXAMPLE, EXAMPLE / "scores.csv", output, root)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("exist", result.stderr.lower())
            self.assertEqual("previous result\n", summary.read_text())
            self.assertEqual(["summary.json"], [path.name for path in output.iterdir()])


if __name__ == "__main__":
    unittest.main()
