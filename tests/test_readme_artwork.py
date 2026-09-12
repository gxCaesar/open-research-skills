"""Check the skill maps readers actually see, including their editable slide source."""
from __future__ import annotations

import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parent.parent
NS = {
    "svg": "http://www.w3.org/2000/svg",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


class ImageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        field = {"img": "src", "source": "srcset"}.get(tag)
        value = dict(attrs).get(field, "") if field else ""
        if "skill-map-" in value:
            self.paths.append(Path(value))


class ReadmeArtworkTest(unittest.TestCase):
    def declared_skills(self):
        index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        return {entry["name"] for entry in index["skills"]}

    def referenced_maps(self):
        paths = []
        for readme, lang in (("README.md", "zh"), ("README.en.md", "en")):
            parser = ImageReferences()
            parser.feed((ROOT / readme).read_text(encoding="utf-8"))
            expected = {
                Path(f"assets/readme-artwork/skill-map-{lang}-v2{suffix}.png")
                for suffix in ("", "-dark")
            }
            self.assertEqual(expected, set(parser.paths), readme)
            paths.extend(ROOT / path for path in parser.paths)
        return paths

    def assert_skill_set(self, svg):
        labels = svg.findall(".//svg:text[@data-skill]", NS)
        names = [label.attrib["data-skill"] for label in labels]
        self.assertEqual(self.declared_skills(), set(names))
        self.assertEqual(len(names), len(set(names)), "duplicate skill labels")
        return labels

    def test_readme_maps_match_index_and_editable_slide(self):
        for png in self.referenced_maps():
            with self.subTest(image=png.name):
                self.assertTrue(png.is_file(), str(png))
                svg = ET.parse(png.with_suffix(".svg")).getroot()
                labels = self.assert_skill_set(svg)
                # Dark previews share the same editable source as the light preview.
                pptx = png.with_name(png.stem.removesuffix("-dark") + ".pptx")
                with zipfile.ZipFile(pptx) as archive:
                    slides = [name for name in archive.namelist()
                              if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)]
                    self.assertEqual(1, len(slides), str(pptx))
                    slide = ET.fromstring(archive.read(slides[0]))
                self.assertEqual([], slide.findall(".//p:pic", NS), str(pptx))
                editable_text = {
                    node.text for node in slide.findall(".//p:sp//a:t", NS)
                    if node.text
                }
                for label in labels:
                    text = "".join(label.itertext()).strip()
                    self.assertTrue(text, label.attrib["data-skill"])
                    self.assertIn(text, editable_text, str(pptx))

    def test_real_map_rejects_a_missing_or_invented_skill(self):
        for png in self.referenced_maps():
            original = ET.parse(png.with_suffix(".svg")).getroot()
            self.assert_skill_set(original)
            for mutation in ("missing", "invented"):
                with self.subTest(image=png.name, mutation=mutation):
                    svg = copy.deepcopy(original)
                    label = svg.find(".//svg:text[@data-skill]", NS)
                    if mutation == "missing":
                        del label.attrib["data-skill"]
                    else:
                        label.set("data-skill", "invented-skill-entry")
                    with self.assertRaises(AssertionError):
                        self.assert_skill_set(svg)


if __name__ == "__main__":
    unittest.main()
