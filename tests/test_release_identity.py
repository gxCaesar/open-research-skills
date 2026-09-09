"""Keep the README, the index, the plugin manifests and the directories in agreement.

Four places name the skill set. Any one of them can drift, and a reader who trusts the
one that drifted is told the repository contains something it does not.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"


def indexed_names() -> set:
    data = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
    return {item["name"] for item in data["skills"]}


def directory_names() -> set:
    return {path.parent.name for path in ROOT.glob("skills/*/SKILL.md")}


def readme_names() -> set:
    """Skill names the README mentions in prose or in a path."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    return {name for name in directory_names() | indexed_names() if name in text}


class ReleaseIdentityTest(unittest.TestCase):
    def test_index_directories_and_readme_name_the_same_skills(self):
        indexed, directories, readme = indexed_names(), directory_names(), readme_names()
        self.assertEqual(indexed, directories, "index and skills/ disagree")
        self.assertEqual(indexed, readme, "README does not name every indexed skill")
        self.assertGreaterEqual(len(indexed), 10)

    def test_the_written_totals_match_the_index(self):
        """A prose count is the part that rots first, and only the totals are counts.

        Anchored on the exact sentences that state a total. A bare numeral scan would
        fire on "the five lenses" and on the section contrasting the original five
        entrypoints with the five added beside them, both of which are correct.
        """
        chinese = {5: "五", 10: "十", 11: "十一", 12: "十二"}
        english = {5: "five", 10: "ten", 11: "eleven", 12: "twelve"}
        total = len(indexed_names())
        self.assertIn(total, chinese, f"add the numerals for {total} entrypoints")

        claims = [
            ("README.md", "{n}个完整 skill"),
            ("README.md", "下文说明{n}项能力怎样用于真实科研"),
            ("README.md", "{n}份独立中文手册进一步展开"),
            ("README.md", "对{n}个名称分别执行"),
            ("README.md", "首页帮助选择，{n}份中文指南"),
            ("MAINTAINERS.md", "the {e} public entrypoints"),
        ]
        for name, template in claims:
            text = (ROOT / name).read_text(encoding="utf-8")
            right = template.format(n=chinese[total], e=english[total])
            with self.subTest(document=name, claim=right):
                self.assertIn(right, text)
            for other, numeral in chinese.items():
                if other == total:
                    continue
                wrong = template.format(n=numeral, e=english[other])
                with self.subTest(document=name, stale=wrong):
                    self.assertNotIn(wrong, text)

    def test_plugin_and_marketplace_manifests_agree(self):
        plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], marketplace["plugins"][0]["name"])
        self.assertEqual("./", marketplace["plugins"][0]["source"])
        for field in ("description", "version", "license", "homepage", "repository"):
            self.assertTrue(str(plugin.get(field, "")).strip(), field)
        self.assertTrue(str(marketplace.get("description", "")).strip())

    def test_the_readme_install_command_matches_the_manifest_names(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        expected = f"claude plugin install {plugin['name']}@{marketplace['name']}"
        self.assertIn(expected, readme)
        repository = plugin["repository"]
        slug = re.sub(r"^https://github\.com/", "", repository).removesuffix(".git")
        self.assertIn(f"claude plugin marketplace add {slug}", readme)


if __name__ == "__main__":
    unittest.main()
