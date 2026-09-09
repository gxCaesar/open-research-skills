"""Actual table mutations and exports for the advanced synthetic atlas."""

import csv
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

from pypdf import PdfReader

EXAMPLE = Path(__file__).resolve().parents[2] / "skills/build-scientific-visualizations/examples/spatial-multiomics-atlas"


def module():
    spec = importlib.util.spec_from_file_location("spatial_atlas", EXAMPLE / "render.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class AdvancedAtlasTest(unittest.TestCase):
    def test_real_missing_or_duplicate_assay_unit_is_rejected(self):
        for mutation in ("missing", "duplicate"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                copied = Path(tmp) / "data"
                shutil.copytree(EXAMPLE / "data", copied)
                target = copied / "assays.csv"
                with target.open(newline="", encoding="utf-8") as stream:
                    table = list(csv.DictReader(stream))
                if mutation == "missing":
                    table.pop(0)
                else:
                    table.append(table[0].copy())
                with target.open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(table[0]))
                    writer.writeheader(); writer.writerows(table)
                with self.assertRaisesRegex(ValueError, "missing|duplicate"):
                    module().read_data(copied)

    def test_complete_real_render_is_vector_and_at_declared_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = module().render(EXAMPLE / "data", Path(tmp))
            self.assertEqual(14, result["panels"])
            self.assertEqual(12, result["donors"])
            self.assertEqual(0, result["text_overflows"])
            page = PdfReader(Path(tmp) / "spatial-multiomics-atlas.pdf").pages[0]
            self.assertAlmostEqual(183, float(page.mediabox.width) * 25.4 / 72, places=2)
            self.assertAlmostEqual(170, float(page.mediabox.height) * 25.4 / 72, places=2)
            self.assertEqual(0, len(page.images))
            self.assertIn("SYNTHETIC", page.extract_text())


if __name__ == "__main__":
    unittest.main()
