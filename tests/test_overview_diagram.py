"""The README's skill map is a copy of skill-index.json, so something must keep it honest.

A diagram that names ten skills is documentation with the same failure mode as a hand-copied
index: rename or add a skill and the picture is silently wrong, and a reader trusts a picture
more than prose. These tests fail in that case instead.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "build_overview_diagram.py"
OUT = ROOT / "assets" / "overview"
VARIANTS = ("skill-map-zh.svg", "skill-map-zh-dark.svg",
            "skill-map-en.svg", "skill-map-en-dark.svg")


def declared_skills() -> set:
    data = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
    return {entry["name"] for entry in data["skills"]}


class OverviewDiagramTest(unittest.TestCase):
    def test_every_declared_skill_appears_in_every_variant(self):
        for variant in VARIANTS:
            svg = (OUT / variant).read_text(encoding="utf-8")
            for name in declared_skills():
                with self.subTest(variant=variant, skill=name):
                    self.assertIn(name, svg)

    def test_no_variant_names_a_skill_the_index_does_not_declare(self):
        """The mirror. A diagram may not invent an entry point either."""
        declared = declared_skills()
        for variant in VARIANTS:
            svg = (OUT / variant).read_text(encoding="utf-8")
            for name in set(svg.split()) & {w for w in svg.split() if w.count("-") >= 2}:
                cleaned = name.strip('">,<')
                if cleaned.startswith(("skill-map", "http", "font-", "text-", "stroke-")):
                    continue
                if cleaned.replace("-", "").isalpha() and cleaned.count("-") >= 2:
                    if cleaned in {"open-research-skills"}:
                        continue
                    with self.subTest(variant=variant, token=cleaned):
                        self.assertIn(cleaned, declared)

    def test_the_generator_refuses_when_it_disagrees_with_the_index(self):
        """A generator that cannot fail would let the two drift apart quietly."""
        source = GENERATOR.read_text(encoding="utf-8")
        self.assertIn("FAIL diagram/index disagree", source)
        self.assertIn("FAIL caption overflows its card", source)

    def test_regenerating_reproduces_the_committed_files(self):
        before = {name: (OUT / name).read_bytes() for name in VARIANTS}
        result = subprocess.run([sys.executable, str(GENERATOR)],
                                capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for name in VARIANTS:
            with self.subTest(variant=name):
                self.assertEqual(before[name], (OUT / name).read_bytes(),
                                 f"{name} differs from what the generator produces")

    def test_no_style_or_script_element_survives_githubs_sanitiser(self):
        """GitHub strips <style> and <script> from Markdown-rendered SVG."""
        for variant in VARIANTS:
            svg = (OUT / variant).read_text(encoding="utf-8")
            with self.subTest(variant=variant):
                self.assertNotIn("<style", svg)
                self.assertNotIn("<script", svg)


if __name__ == "__main__":
    unittest.main()
