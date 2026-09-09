import re
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "prepare-journal-manuscripts"
EXPECTED = {"prepare-journal-manuscripts"}
EXPECTED_MODES = {
    "recon",
    "draft",
    "audit",
    "polish",
    "editor-pack",
    "cover-letter",
    "revision-response",
    "final-package",
}
EXPECTED_COMPONENTS = {
    "abstract",
    "statistics-reporting",
    "data-availability",
}


def precedent_rows(path):
    text = path.read_text(encoding="utf-8")
    section = text.split("## Source-located precedent index", 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("|")]
    headers = [cell.strip() for cell in rows[0].strip("|").split("|")]
    return [
        dict(zip(headers, [cell.strip() for cell in row.strip("|").split("|")]))
        for row in rows[2:]
    ]


class JournalManuscriptPackageContractTest(unittest.TestCase):
    def test_exact_approved_skill_entrypoints(self):
        observed = {
            path.parent.name for path in SKILL.rglob("SKILL.md")
        }
        self.assertEqual(EXPECTED, observed)

    def test_every_skill_has_openai_metadata(self):
        for name in EXPECTED:
            self.assertTrue((PACKAGE / "skills" / name / "agents" / "openai.yaml").is_file())

    def test_entrypoint_routes_journal_lifecycle_modes(self):
        skill = PACKAGE / "skills" / "prepare-journal-manuscripts" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        for mode in EXPECTED_MODES:
            self.assertIn(f"`{mode}`", text)

    def test_writing_capabilities_are_non_triggering_components(self):
        for name in EXPECTED_COMPONENTS:
            component = SKILL / "components" / name
            self.assertTrue((component / "guide.md").is_file(), name)
            self.assertFalse((component / "SKILL.md").exists(), name)

    def test_paper_card_is_not_owned_by_journal_package(self):
        self.assertFalse((SKILL / "components" / "paper-card").exists())
        self.assertFalse((PACKAGE / "skills" / "research-paper-card").exists())

    def test_sampled_nature_family_shapes_are_optional_and_source_located(self):
        reference = SKILL / "references" / "nature-family-article-shapes.md"
        self.assertTrue(reference.is_file())

        entrypoint = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        drafting = (SKILL / "references" / "drafting-and-polish.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("nature-family-article-shapes.md", entrypoint)
        self.assertIn("nature-family-article-shapes.md", drafting)

        text = reference.read_text(encoding="utf-8")
        for phrase in (
            "Observed in the sampled papers",
            "Editorial heuristic",
            "Official requirement",
            "PDF page",
            "Counterexamples",
        ):
            self.assertIn(phrase, text)

        rows = precedent_rows(reference)
        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(len(rows), len({row["ID"] for row in rows}))
        for row in rows:
            match = re.fullmatch(
                r"\[(10\.1038/[A-Za-z0-9.-]+)\]\(https://doi\.org/(10\.1038/[A-Za-z0-9.-]+)\)",
                row["DOI"],
            )
            self.assertIsNotNone(match, row)
            self.assertEqual(match.group(1), match.group(2))
            self.assertRegex(row["PDF pages"], r"^\d+(?:-\d+)?(?:; \d+(?:-\d+)?)*$")
            self.assertRegex(row["Locator"], r"(?:Fig|ED|section)")

        for shape in ("computational-method", "discovery-mechanism", "translational"):
            self.assertGreaterEqual(
                sum(row["Shape"] == shape for row in rows),
                2,
                shape,
            )

        for paragraph in text.split("\n\n"):
            if "Observed in the sampled papers" in paragraph:
                self.assertNotRegex(paragraph.casefold(), r"\b(?:commonly|often|usually|most)\b")

        ids = {row["ID"].strip("`") for row in rows}
        for paragraph in text.split("\n\n"):
            if re.search(
                r"(?:in this sample|the sample includes|one supplied|complete supplied pdf)",
                paragraph,
                flags=re.IGNORECASE,
            ):
                self.assertTrue(
                    any(f"`{record_id}`" in paragraph for record_id in ids),
                    f"sample-specific empirical prose lacks an indexed record: {paragraph}",
                )

    def test_package_contains_no_symlinks(self):
        links = [str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)


if __name__ == "__main__":
    unittest.main()
