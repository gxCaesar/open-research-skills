"""Exercise figure construction with only one installed skill present."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "prepare-journal-manuscripts"


class StandaloneFigureTests(unittest.TestCase):
    def test_isolated_source_plot_and_editable_diagram(self):
        """Break caught: missing local renderer or flattening diagram text into pixels."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "only-installed-skill"
            shutil.copytree(SKILL, skill)
            (root / "data.csv").write_text("dose,response\n0,1\n1,2\n2,4\n", encoding="utf-8")
            spec = {
                "width_mm": 180, "height_mm": 75,
                "panels": [
                    {"kind": "plot", "title": "Synthetic observations",
                     "source_csv": "data.csv", "x": "dose", "y": "response",
                     "xlabel": "Dose (arbitrary units)", "ylabel": "Response (arbitrary units)"},
                    {"kind": "diagram", "title": "Planned analysis",
                     "nodes": [{"id": "input", "label": "Observed inputs", "x": 0.2, "y": 0.5},
                               {"id": "output", "label": "Planned output", "x": 0.8, "y": 0.5}],
                     "edges": [["input", "output"]]},
                ],
            }
            path = root / "figure.json"
            path.write_text(json.dumps(spec), encoding="utf-8")
            env = dict(os.environ, MPLCONFIGDIR=str(root / "mpl"))
            command = [sys.executable, "-B", str(skill / "scripts/render_evidence_figure.py"),
                       str(path), str(root / "output")]
            run = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)
            self.assertTrue((root / "output.pdf").read_bytes().startswith(b"%PDF"))
            self.assertTrue((root / "output.png").read_bytes().startswith(b"\x89PNG"))
            tree = ET.parse(root / "output.svg")
            texts = [node.text for node in tree.iter() if node.tag.endswith("}text")]
            self.assertIn("Observed inputs", texts)
            self.assertIn("Planned output", texts)
            self.assertFalse(any(node.tag.endswith("}image") for node in tree.iter()))
            # A different source must change the actual plot, not merely the report.
            def marker_positions(svg):
                group = next(node for node in svg.iter() if node.attrib.get("id") == "PathCollection_1")
                return [(node.attrib["x"], node.attrib["y"]) for node in group.iter()
                        if node.tag.endswith("}use")]
            first = marker_positions(tree)
            protected = (root / "output.svg").read_bytes()
            overwrite = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
            self.assertNotEqual(0, overwrite.returncode)
            self.assertEqual(protected, (root / "output.svg").read_bytes())
            (root / "data.csv").write_text("dose,response\n0,1\n1,3\n2,4\n", encoding="utf-8")
            updated = subprocess.run(command[:-1] + [str(root / "output2")], cwd=root, env=env,
                                     capture_output=True, text=True)
            self.assertEqual(0, updated.returncode, updated.stderr)
            changed = ET.parse(root / "output2.svg")
            second = marker_positions(changed)
            self.assertNotEqual(first, second)
            # Non-finite scientific values must fail rather than disappear from the plot.
            (root / "data.csv").write_text("dose,response\n0,1\n1,nan\n", encoding="utf-8")
            bad = subprocess.run(command[:-1] + [str(root / "bad")], cwd=root, env=env,
                                 capture_output=True, text=True)
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("finite", bad.stderr)
            self.assertFalse((root / "bad.pdf").exists())


if __name__ == "__main__":
    unittest.main()
