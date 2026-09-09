import json
import subprocess
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENTS = PACKAGE / "skills" / "prepare-journal-manuscripts" / "components"
COMPONENT = COMPONENTS / "abstract"
CHECKER = COMPONENT / "scripts" / "check_abstract.py"


def words(count: int) -> str:
    return " ".join(["word"] * count)


class AbstractMergeTest(unittest.TestCase):
    def run_checker(self, text: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            input=text,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_contains_one_non_triggering_abstract_component(self):
        abstract_components = sorted(
            path.name
            for path in COMPONENTS.iterdir()
            if path.is_dir() and "abstract" in path.name
        ) if COMPONENTS.is_dir() else []
        self.assertEqual(["abstract"], abstract_components)
        self.assertTrue((COMPONENT / "guide.md").is_file())
        self.assertFalse((COMPONENT / "SKILL.md").exists())

    def test_aaai_preset_enforces_inclusive_150_to_200_word_window(self):
        for count in (150, 200):
            with self.subTest(count=count):
                result = self.run_checker(words(count), "--venue", "aaai")
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for count in (149, 201):
            with self.subTest(count=count):
                result = self.run_checker(words(count), "--venue", "aaai")
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_aaai_preset_rejects_citations(self):
        result = self.run_checker(words(160) + " [12]", "--venue", "aaai")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("[12]", result.stdout)

    def test_explicit_length_overrides_aaai_preset(self):
        result = self.run_checker(
            words(120),
            "--venue",
            "aaai",
            "--min-words",
            "100",
            "--max-words",
            "130",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_venue_roster_includes_aaai(self):
        result = self.run_checker("", "--venue", "list")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("aaai", result.stdout.split())

    def test_aaai_json_labels_preset_as_editorial_default(self):
        result = self.run_checker(words(160), "--venue", "aaai", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("editorial_default", payload["preset_kind"])


if __name__ == "__main__":
    unittest.main()
