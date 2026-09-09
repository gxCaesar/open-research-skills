import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "build-scientific-visualizations"
EXPECTED_SKILLS = {"build-scientific-visualizations"}
EXPECTED_MODES = {
    "layout-sketch",
    "flowchart",
    "compound-figure",
    "conference-figure-set",
    "journal-figure-set",
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


def markdown_links(text):
    return set(re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", text))


class ScientificFiguresPackageContractTest(unittest.TestCase):
    def test_package_exposes_one_skill_entrypoint(self):
        observed = {
            path.parent.name for path in SKILL.rglob("SKILL.md")
        }
        self.assertEqual(EXPECTED_SKILLS, observed)

    def test_entrypoint_routes_all_five_modes(self):
        skill = PACKAGE / "skills" / "build-scientific-visualizations" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        for mode in EXPECTED_MODES:
            self.assertIn(f"`{mode}`", text)

    def test_shared_core_is_not_a_fourth_skill(self):
        core = SKILL / "shared" / "figure-core"
        self.assertTrue(core.is_dir())
        self.assertFalse((core / "SKILL.md").exists())

    def test_modes_are_skill_local_non_triggering_components(self):
        for name in ("flowchart", "compound-figure", "journal-figure-set"):
            component = SKILL / "components" / name
            self.assertTrue((component / "guide.md").is_file(), name)
            self.assertFalse((component / "SKILL.md").exists(), name)

    def test_nature_family_evidence_arcs_are_source_located_and_routed(self):
        component = SKILL / "components" / "journal-figure-set"
        reference = component / "references" / "nature-family-evidence-arcs.md"
        self.assertTrue(reference.is_file())

        guide = (component / "guide.md").read_text(encoding="utf-8")
        self.assertIn("nature-family-evidence-arcs.md", guide)
        self.assertIn("DOI/PDF-page-supported empirical precedents", guide)

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
        self.assertGreaterEqual(len(rows), 9)
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

    def test_colour_redundancy_has_a_measurement_image_contract(self):
        palette = (
            SKILL
            / "components"
            / "journal-figure-set"
            / "references"
            / "palette-and-accessibility.md"
        ).read_text(encoding="utf-8")
        contract = (
            SKILL / "shared" / "figure-core" / "references" / "visual-contract.md"
        ).read_text(encoding="utf-8")
        for text in (palette, contract):
            normalized = " ".join(text.split())
            self.assertIn("measurement images", normalized)
            self.assertIn("local channel key", normalized)
            self.assertIn("synthetic hatches or markers", normalized)

    def test_package_contains_no_symlinks(self):
        links = [str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)

    def test_entrypoint_directly_routes_new_decision_references(self):
        links = markdown_links((SKILL / "SKILL.md").read_text(encoding="utf-8"))
        for path in (
            "references/page-blueprint-contract.md",
            "references/domain-visualization-selection.md",
            "references/source-data-contract.md",
        ):
            self.assertIn(path, links)
            self.assertTrue((SKILL / path).is_file())

    def test_long_new_references_have_contents_and_no_nested_required_read(self):
        entry_links = markdown_links((SKILL / "SKILL.md").read_text(encoding="utf-8"))
        for relative in (
            "references/page-blueprint-contract.md",
            "references/domain-visualization-selection.md",
            "references/source-data-contract.md",
        ):
            path = SKILL / relative
            text = path.read_text(encoding="utf-8")
            if len(text.splitlines()) > 100:
                self.assertIn("## Contents", text, relative)
            self.assertIn(relative, entry_links)
            self.assertNotRegex(
                text.casefold(),
                r"(?:must|required to)\s+read[^\n]*\.md",
                relative,
            )

    def test_documented_commands_exist_and_match_cli_help(self):
        targets = set()
        for markdown in SKILL.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            targets.update(re.findall(r"\$SKILL_DIR/([^\s\"']+\.py)", text))
        self.assertTrue(targets)
        for relative in sorted(targets):
            with self.subTest(script=relative):
                script = SKILL / relative
                self.assertTrue(script.is_file(), relative)
                result = subprocess.run(
                    [sys.executable, "-B", str(script), "--help"],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_geometry_profiles_name_scope_authority_and_checked_date(self):
        profiles = json.loads(
            (
                SKILL
                / "shared"
                / "figure-core"
                / "assets"
                / "venue-profiles.json"
            ).read_text(encoding="utf-8")
        )["profiles"]
        verified = [profile for profile in profiles.values() if profile["authority_status"] == "verified"]
        self.assertTrue(verified)
        for profile in verified:
            self.assertTrue(profile["journal"])
            self.assertTrue(profile["article_type"])
            self.assertTrue(profile["submission_stage"])
            self.assertRegex(profile["authority"]["url"], r"^https://")
            self.assertRegex(profile["authority"]["checked_date"], r"^20\d{2}-\d{2}-\d{2}$")
            self.assertGreater(profile["geometry"]["selected_width_mm"], 0)

    def test_bundled_flowchart_examples_use_schema_12_cross_references(self):
        flowchart = json.loads(
            (SKILL / "components" / "flowchart" / "assets" / "flowchart-spec.json").read_text(
                encoding="utf-8"
            )
        )
        ledger = json.loads(
            (SKILL / "components" / "flowchart" / "assets" / "content-ledger.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("1.2", flowchart["schema_version"])
        self.assertEqual("1.2", ledger["schema_version"])
        self.assertEqual(flowchart["figure_id"], ledger["figure_id"])
        claim_ids = {claim["id"] for claim in ledger["claims"]}
        diagram = flowchart["flowcharts"][0]
        for stage in diagram["stages"]:
            self.assertIn(stage["content_anchor"], claim_ids)
            self.assertTrue(stage["visual_element_ids"])
        for edge in diagram["edges"]:
            self.assertIn(edge["content_anchor"], claim_ids)
            self.assertTrue(edge["visual_element_ids"])


if __name__ == "__main__":
    unittest.main()
