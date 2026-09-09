import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
CORE = PACKAGE / "skills" / "build-scientific-visualizations" / "shared" / "figure-core"
INIT = CORE / "scripts" / "init_figure_project.py"
RENDER = CORE / "scripts" / "render_matplotlib.py"
CATALOG = CORE / "assets" / "diagram-styles.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def initialize(project, *selection):
    return subprocess.run(
        [sys.executable, "-B", str(INIT), str(project), "--figure-id", "style-test",
         "--layout-profile", "custom", "--page-width-mm", "180", "--dpi", "96",
         *selection],
        text=True, capture_output=True, check=False,
    )


class DiagramStyleSelectionTest(unittest.TestCase):
    def test_no_selection_preserves_legacy_style_and_palette(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            result = initialize(project)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(read_json(CORE / "assets" / "starter-spec.json")["style"],
                             read_json(project / "figure_spec.json")["style"])
            self.assertEqual(read_json(CORE / "assets" / "palette.json"),
                             read_json(project / "palette.json"))

    def test_each_palette_reaches_both_canonical_consumers(self):
        choices = [
            ("nature-pastel", "mist-blue"), ("nature-pastel", "sage-lilac"),
            ("nature-pastel", "lilac-sand"),
            ("conference-structured", "blue-orange"),
            ("conference-structured", "indigo-teal"),
            ("conference-structured", "plum-cyan"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for style_id, palette_id in choices:
                with self.subTest(palette=palette_id):
                    project = Path(tmp) / palette_id
                    result = initialize(project, "--diagram-style", style_id,
                                        "--palette", palette_id)
                    self.assertEqual(0, result.returncode, result.stderr)
                    style = read_json(project / "figure_spec.json")["style"]
                    self.assertEqual(style_id, style["diagram_style"])
                    self.assertEqual(palette_id, style["palette_id"])
                    expected = read_json(CATALOG)["palettes"][palette_id]["colors"]
                    for role, value in expected.items():
                        self.assertEqual(value, style["colors"][role])
                    self.assertEqual(style["colors"], read_json(project / "palette.json"))

    def test_style_default_and_palette_only_selection_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, args, expected_style, expected_palette in [
                ("default", ["--diagram-style", "nature-pastel"],
                 "nature-pastel", "mist-blue"),
                ("inferred", ["--palette", "indigo-teal"],
                 "conference-structured", "indigo-teal"),
            ]:
                project = Path(tmp) / name
                result = initialize(project, *args)
                self.assertEqual(0, result.returncode, result.stderr)
                style = read_json(project / "figure_spec.json")["style"]
                self.assertEqual(expected_style, style["diagram_style"])
                self.assertEqual(expected_palette, style["palette_id"])

    def test_wrong_family_and_unknown_palette_leave_no_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, args in [
                ("mismatch", ["--diagram-style", "nature-pastel", "--palette", "blue-orange"]),
                ("unknown", ["--palette", "not-a-palette"]),
            ]:
                project = Path(tmp) / name
                result = initialize(project, *args)
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(project.exists())

    def test_selection_does_not_overwrite_existing_figure(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "existing"
            first = initialize(project)
            self.assertEqual(0, first.returncode, first.stderr)
            paths = [project / "figure_spec.json", project / "palette.json"]
            before = [path.read_text(encoding="utf-8") for path in paths]
            result = initialize(project, "--palette", "sage-lilac")
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(before, [path.read_text(encoding="utf-8") for path in paths])

    def test_palette_choice_changes_actual_svg_without_changing_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            panels = []
            colours = []
            for palette_id in ["mist-blue", "blue-orange"]:
                project = Path(tmp) / palette_id
                result = initialize(project, "--palette", palette_id)
                self.assertEqual(0, result.returncode, result.stderr)
                spec = read_json(project / "figure_spec.json")
                panels.append(spec["panels"])
                expected = read_json(CATALOG)["palettes"][palette_id]["colors"]["primary_stroke"]
                colours.append(expected)
                rendered = subprocess.run(
                    [sys.executable, "-B", str(RENDER), str(project)],
                    text=True, capture_output=True, check=False,
                    env={**os.environ, "MPLCONFIGDIR": str(Path(tmp) / "mpl")},
                )
                self.assertEqual(0, rendered.returncode, rendered.stderr)
                svg = (project / "outputs" / "panels" / "style-testa.svg").read_text(encoding="utf-8")
                self.assertIn("stroke: " + expected.lower(), svg.lower())
            self.assertEqual(panels[0], panels[1])
            self.assertNotEqual(colours[0], colours[1])


if __name__ == "__main__":
    unittest.main()
