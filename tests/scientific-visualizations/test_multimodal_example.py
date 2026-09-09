"""Protect donor pairing and the public example's real exported artifacts."""

import csv
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader


EXAMPLE = Path(__file__).resolve().parents[2] / "skills/build-scientific-visualizations/examples/multimodal-18-panel"


def module():
    path = EXAMPLE / "render.py"
    spec = importlib.util.spec_from_file_location("multimodal_example", path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class MultimodalExampleTest(unittest.TestCase):
    def test_pairing_uses_ids_not_row_order_and_reports_incomplete_units(self):
        rows = [
            {"donor": "B", "condition": "perturbed", "rna": "7"},
            {"donor": "A", "condition": "control", "rna": "2"},
            {"donor": "C", "condition": "control", "rna": "100"},
            {"donor": "B", "condition": "control", "rna": "3"},
            {"donor": "A", "condition": "perturbed", "rna": "3"},
        ]
        ids, changes, excluded = module().paired_values(rows, "rna")
        self.assertEqual(["A", "B"], ids)
        self.assertEqual([1.0, 4.0], list(changes))
        self.assertEqual(1, excluded)

    def test_duplicate_unit_condition_cannot_silently_change_weight(self):
        rows = [{"donor": "A", "condition": "control", "rna": "2"}] * 2
        with self.assertRaisesRegex(ValueError, "duplicate"):
            module().paired_values(rows, "rna")

    def test_disjoint_missing_assays_cannot_silently_mispair_real_example(self):
        """Equal-length RNA/ATAC arrays can represent different donor populations."""
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            shutil.copytree(EXAMPLE / "data", data)
            assay_path = data / "assays.csv"
            with assay_path.open(newline="", encoding="utf-8") as stream:
                table = list(csv.DictReader(stream))
            for row in table:
                if row["condition"] == "perturbed" and row["donor"] == "D01":
                    row["rna"] = ""
                if row["condition"] == "perturbed" and row["donor"] == "D02":
                    row["atac"] = ""
            with assay_path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(table[0]))
                writer.writeheader()
                writer.writerows(table)
            output = Path(tmp) / "output"
            with self.assertRaisesRegex(ValueError, "fixed demonstration.*missing"):
                module().render(data, output, font="DejaVu Sans")
            self.assertFalse(output.exists())

    def test_real_render_preserves_physical_page_and_vector_marks(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = module().render(EXAMPLE / "data", Path(tmp), font="DejaVu Sans")
            self.assertEqual(18, report["panels"])
            self.assertEqual(8, report["paired_units"])
            self.assertEqual(0, report["text_overflows"])
            page = PdfReader(Path(tmp) / "multimodal-18-panel.pdf").pages[0]
            self.assertAlmostEqual(183, float(page.mediabox.width) * 25.4 / 72, places=2)
            self.assertAlmostEqual(235, float(page.mediabox.height) * 25.4 / 72, places=2)
            self.assertEqual(0, len(page.images))
            self.assertIn("SYNTHETIC", page.extract_text())
            self.assertGreater((Path(tmp) / "multimodal-18-panel.png").stat().st_size, 1000)
            self.assertNotIn("<image", (Path(tmp) / "multimodal-18-panel.svg").read_text())


if __name__ == "__main__":
    unittest.main()
