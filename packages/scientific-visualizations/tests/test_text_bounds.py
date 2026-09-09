"""Exercise actual rendered text, rather than declared scene rectangles."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "skills/build-scientific-visualizations/shared/figure-core/scripts"


def scene(text, width=0.18, height=0.1):
    return {
        "figure_id": "bounds",
        "journal_profile": {"dpi": 300, "font_family": "DejaVu Sans"},
        "style": {"colors": {"paper": "#FFFFFF", "ink": "#222222"}},
        "assets": {},
        "panels": [{
            "id": "a", "size_mm": [60, 40],
            "elements": [{
                "type": "text", "id": "descriptor", "x": 0.1, "y": 0.2,
                "w": width, "h": height, "text": text, "font_pt": 7.5,
            }],
        }],
    }


class CanonicalTextBoundsTest(unittest.TestCase):
    def run_renderer(self, root, spec, *args):
        (root / "figure_spec.json").write_text(json.dumps(spec), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "render_matplotlib.py"), str(root), *args],
            capture_output=True, text=True, check=False,
        )

    def test_opt_in_check_rejects_actual_overflow_before_export(self):
        """Ignoring actual glyph width must fail even when the declared box fits."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_renderer(
                root, scene("Independent observations across experimental conditions"),
                "--check-text-bounds",
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("FAIL", report["status"])
            self.assertEqual(1, report["checked"])
            self.assertEqual("a", report["violations"][0]["panel_id"])
            self.assertEqual("descriptor", report["violations"][0]["element_id"])
            self.assertGreater(report["violations"][0]["overflow_pt"]["right"], 20)
            self.assertFalse((root / "outputs/panels/boundsa.pdf").exists())

    def test_wrapped_text_with_room_passes_without_changing_copy(self):
        """Blanket rejection of all text or forced shrinking must not count as a fix."""
        text = "Independent observations\nacross experimental conditions"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = scene(text, width=0.85, height=0.5)
            result = self.run_renderer(root, spec, "--check-text-bounds")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("PASS", report["status"])
            self.assertEqual(1, report["checked"])
            self.assertEqual([], report["violations"])
            saved = json.loads((root / "figure_spec.json").read_text(encoding="utf-8"))
            self.assertEqual(text, saved["panels"][0]["elements"][0]["text"])
            self.assertEqual(7.5, saved["panels"][0]["elements"][0]["font_pt"])
            self.assertTrue((root / "outputs/panels/boundsa.svg").is_file())
            font_sizes = []
            page = PdfReader(root / "outputs/panels/boundsa.pdf").pages[0]
            extracted = page.extract_text(visitor_text=lambda text, cm, tm, font, size: font_sizes.append(size) if text.strip() else None)
            self.assertIn("Independent observations", extracted)
            self.assertIn("experimental conditions", extracted)
            self.assertEqual({7.5}, set(font_sizes))

    def test_multiline_height_is_checked_too(self):
        """A width-only check must not accept a multiline label taller than its box."""
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_renderer(
                Path(tmp), scene("First line\nSecond line\nThird line", width=0.8, height=0.025),
                "--check-text-bounds",
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            overflow = report["violations"][0]["overflow_pt"]
            self.assertGreater(overflow["top"], 0)
            self.assertGreater(overflow["bottom"], 0)

    def test_default_export_remains_compatible(self):
        """An opt-in diagnostic must not silently become a new mandatory gate."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_renderer(root, scene("Independent observations across experimental conditions"))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((root / "outputs/panels/boundsa.pdf").is_file())

    def test_no_registered_text_is_not_a_passing_text_review(self):
        """An empty text inventory must not claim that text was checked."""
        spec = scene("")
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_renderer(Path(tmp), spec, "--check-text-bounds")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("NOT_APPLICABLE", report["status"])
            self.assertEqual(0, report["checked"])

    def test_native_artist_with_transformed_axes_uses_the_same_check(self):
        """Ignoring axes transforms breaks reuse outside full-panel canonical axes."""
        module_spec = importlib.util.spec_from_file_location("native_bounds", SCRIPTS / "render_matplotlib.py")
        native = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(native)
        fig = native.plt.figure(figsize=(3, 2), dpi=100)
        self.addCleanup(native.plt.close, fig)
        ax = fig.add_axes([0.2, 0.15, 0.7, 0.7])
        ax.set_xlim(10, 20)
        artist = ax.text(0.02, 0.9, "Baseline observations", transform=ax.transAxes, va="top", fontsize=8)
        fig.canvas.draw()
        backend = fig.canvas.get_renderer()
        narrow = ax.transAxes.transform_bbox(native.Bbox.from_bounds(0.02, 0.5, 0.1, 0.4))
        roomy = ax.transAxes.transform_bbox(native.Bbox.from_bounds(0.02, 0.5, 0.9, 0.4))
        self.assertGreater(native.text_overflow_pt(artist, narrow, backend)["right"], 20)
        self.assertEqual({}, native.text_overflow_pt(artist, roomy, backend))
        self.assertEqual("Baseline observations", artist.get_text())
        self.assertEqual(8, artist.get_fontsize())


if __name__ == "__main__":
    unittest.main()
