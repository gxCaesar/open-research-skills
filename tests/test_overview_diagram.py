"""The README's skill map is a copy of skill-index.json, so something must keep it honest.

A diagram that names ten skills is documentation with the same failure mode as a hand-copied
index: rename or add a skill and the picture is silently wrong, and a reader trusts a picture
more than prose. These tests fail in that case instead.
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "build_overview_diagram.py"
OUT = ROOT / "assets" / "overview"
VARIANTS = ("skill-map-zh.svg", "skill-map-zh-dark.svg",
            "skill-map-en.svg", "skill-map-en-dark.svg")


def hyphenated_text_names(svg: str) -> set:
    """Skill-shaped names taken from element text, not from whitespace-split markup."""
    return {m.strip() for m in re.findall(r">\s*([a-z][a-z0-9]*(?:-[a-z0-9]+){2,})\s*<", svg)}


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
        """The mirror. A diagram may not invent an entry point either.

        The first version of this split the SVG on whitespace and filtered the pieces. Every
        skill name in the file is the text content of an element, so each piece looked like
        `>survey-and-audit-novelty</text>` and no filter it applied could ever match: thirteen
        tokens entered the loop and none reached an assertion. A test that cannot fail is the
        thing this repository exists to catch, so the extractor is now checked as well.
        """
        declared = declared_skills()
        for variant in VARIANTS:
            names = hyphenated_text_names((OUT / variant).read_text(encoding="utf-8"))
            # Equality, not containment. A subset check passes when the diagram adds a name
            # the index never declared, which is exactly what this test is named for.
            with self.subTest(variant=variant):
                self.assertEqual(declared, names)

    def test_the_extractor_would_catch_an_invented_name(self):
        """Without this, the mirror above could quietly go back to asserting nothing."""
        svg = (OUT / VARIANTS[0]).read_text(encoding="utf-8")
        planted = svg.replace(">survey-and-audit-novelty<", ">invented-skill-name<", 1)
        self.assertNotEqual(svg, planted, "the planted marker did not apply")
        found = hyphenated_text_names(planted)
        self.assertIn("invented-skill-name", found)
        self.assertNotIn("invented-skill-name", declared_skills())

    def test_the_generator_refuses_when_it_disagrees_with_the_index(self):
        """Run it against a mutated index and require a non-zero exit.

        This used to assert only that two error strings appeared in the source. Replacing
        the generator's `if drawn != declared:` with `if False:` left every test in this
        file green, and the generator then happily emitted four diagrams that disagreed
        with the index.
        """
        index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        index["skills"].append({"name": "invented-skill-entry", "entrypoint": "x", "guide": "y"})
        with tempfile.TemporaryDirectory() as tmp:
            bad_index = Path(tmp) / "skill-index.json"
            bad_index.write_text(json.dumps(index), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(GENERATOR), "--out", tmp, "--index", str(bad_index)],
                capture_output=True, text=True, cwd=str(ROOT))
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("diagram/index disagree", result.stdout)
            self.assertFalse(list(Path(tmp).glob("*.svg")), "it wrote diagrams anyway")

    def test_the_generator_refuses_a_caption_that_would_overflow(self):
        """Also run rather than grepped: the width guard is what keeps captions inside cards."""
        source = GENERATOR.read_text(encoding="utf-8")
        long_caption = "Is this direction still open?"
        self.assertIn(long_caption, source, "anchor caption moved; update this test")
        with tempfile.TemporaryDirectory() as tmp:
            patched = Path(tmp) / "gen.py"
            patched.write_text(
                source.replace(long_caption, "x" * 200).replace(
                    "ROOT = Path(__file__).resolve().parent.parent",
                    f"ROOT = Path({str(ROOT)!r})"),
                encoding="utf-8")
            result = subprocess.run([sys.executable, str(patched), "--out", tmp],
                                    capture_output=True, text=True, cwd=str(ROOT))
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("caption overflows its card", result.stdout)

    def test_regenerating_reproduces_the_committed_files(self):
        """Regenerate somewhere else. Regenerating in place destroyed an uncommitted edit
        to an SVG and only then reported that it differed."""
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(GENERATOR), "--out", tmp],
                                    capture_output=True, text=True, cwd=str(ROOT))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            for name in VARIANTS:
                with self.subTest(variant=name):
                    self.assertEqual((OUT / name).read_bytes(),
                                     (Path(tmp) / name).read_bytes(),
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
