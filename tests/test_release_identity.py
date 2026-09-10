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


def readme_names(name: str = "README.md") -> set:
    """Skill names a README mentions in prose or in a path."""
    text = (ROOT / name).read_text(encoding="utf-8")
    return {skill for skill in directory_names() | indexed_names() if skill in text}


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

    def test_the_english_entry_point_names_the_same_skills(self):
        """An English reader landing here must not see a shorter list than a Chinese one."""
        self.assertEqual(indexed_names(), readme_names("README.en.md"))
        chinese = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertIn("README.en.md", chinese, "the Chinese README must link the English one")
        self.assertIn("README.md", english, "the English README must link back")
        plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertIn(f"claude plugin install {plugin['name']}@{marketplace['name']}", english)

    def test_every_command_in_a_guide_points_at_a_real_file(self):
        """A reader copies these lines. The repository checks the ones inside skills/ and
        never checked the ones in the guides, which are the ones a reader actually runs."""
        pattern = re.compile(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)")
        index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        checked = 0
        for item in index["skills"]:
            guide = ROOT / item["guide"]
            for relative in pattern.findall(guide.read_text(encoding="utf-8")):
                relative = relative.rstrip('".')
                checked += 1
                with self.subTest(guide=item["guide"], target=relative):
                    self.assertTrue((ROOT / "skills" / item["name"] / relative).exists(), relative)
        self.assertGreaterEqual(checked, 20, "the extractor found almost no commands")

    def test_every_skill_level_checker_is_shown_in_its_guide(self):
        """A skill that ships a checker and never shows the command has hidden it.

        All five guides written for the new entrypoints failed this when it was added:
        each skill bundled a validator and its manual never printed a way to run one.
        """
        pattern = re.compile(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)")
        index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        checked = 0
        for item in index["skills"]:
            skill = ROOT / "skills" / item["name"]
            checkers = sorted(
                path.relative_to(skill).as_posix()
                for glob in ("scripts/check_*.py", "scripts/validate_*.py")
                for path in skill.glob(glob)
            )
            if not checkers:
                continue
            guide = (ROOT / item["guide"]).read_text(encoding="utf-8")
            shown = {ref.rstrip('".') for ref in pattern.findall(guide)}
            for checker in checkers:
                checked += 1
                with self.subTest(skill=item["name"], checker=checker):
                    self.assertIn(checker, shown)
        self.assertGreaterEqual(checked, 7, "the sweep found almost no checkers")

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
