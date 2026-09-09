import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE / "skills"
EXPECTED_MODES = {
    "survey",
    "plan",
    "pilot",
    "develop",
    "monitor",
    "freeze",
    "claim-lock",
    "handoff",
    "public-release",
}


def table_first_column_after_heading(text, heading):
    section = text.split(heading, 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("|")]
    return {
        row.strip("|").split("|", 1)[0].strip().strip("`")
        for row in rows[2:]
    }


class PublicationWorkflowPackageContractTest(unittest.TestCase):
    def test_package_exposes_one_publication_skill(self):
        observed = {
            path.name
            for path in SKILLS.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        } if SKILLS.is_dir() else set()
        self.assertEqual({"research-publication-pipeline"}, observed)

    def test_skill_has_portable_workspace_tools_and_references(self):
        skill = SKILLS / "research-publication-pipeline"
        required = [
            "scripts/init_publication_project.py",
            "scripts/validate_publication_project.py",
            "examples/run_demo.py",
            "examples/README.md",
            "examples/synthetic_workspace.py",
            "references/intake-and-routing.md",
            "references/protocol-headroom-and-development.md",
            "references/evidence-claims-and-handoff.md",
            "references/survey-and-planning.md",
            "references/exemplar-corpus-calibration.md",
            "references/pilot-and-monitoring.md",
            "references/frozen-evaluation.md",
            "references/public-code-release.md",
            "assets/templates/project.json",
            "assets/templates/source-register.json",
            "assets/templates/intake.json",
            "assets/templates/protocol.json",
            "assets/templates/headroom.json",
            "assets/templates/iteration-ledger.json",
            "assets/templates/claim-register.json",
            "assets/templates/handoff.json",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((skill / relative).is_file())

    def test_entrypoint_routes_the_full_publication_lifecycle(self):
        text = (SKILLS / "research-publication-pipeline" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for mode in EXPECTED_MODES:
            self.assertIn(f"`{mode}`", text)

    def test_skill_documents_its_synthetic_demonstration_boundary(self):
        skill = SKILLS / "research-publication-pipeline"
        documentation = (skill / "examples" / "README.md").read_text(encoding="utf-8")
        entrypoint = (skill / "SKILL.md").read_text(encoding="utf-8")
        for text in (documentation, entrypoint):
            self.assertIn("run_demo.py", text)
            self.assertIn("synthetic", text.lower())
            self.assertIn("locked-test", text)

    def test_absorbed_workflow_safeguards_are_explicit(self):
        skill = SKILLS / "research-publication-pipeline"
        text = "\n".join(
            (skill / "references" / name).read_text(encoding="utf-8")
            for name in (
                "survey-and-planning.md",
                "pilot-and-monitoring.md",
                "frozen-evaluation.md",
                "public-code-release.md",
            )
        )
        for phrase in (
            "bounded search budget",
            "retrainability",
            "current incumbent",
            "known-answer",
            "lockbox exposure",
            "logical conjunction",
            "fresh unpack",
        ):
            self.assertIn(phrase, text)

    def test_exemplar_corpus_calibration_is_routed_and_transfer_safe(self):
        skill = SKILLS / "research-publication-pipeline"
        reference = skill / "references" / "exemplar-corpus-calibration.md"
        self.assertTrue(reference.is_file())

        entrypoint = (skill / "SKILL.md").read_text(encoding="utf-8")
        survey = (skill / "references" / "survey-and-planning.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("exemplar-corpus-calibration.md", entrypoint)
        self.assertIn("exemplar-corpus-calibration.md", survey)

        text = reference.read_text(encoding="utf-8")
        for phrase in (
            "corpus census",
            "publication_form",
            "source completeness",
            "Observed pattern",
            "Editorial judgement",
            "Official requirement",
            "PDF page",
            "counterexample",
            "private paths",
        ):
            self.assertIn(phrase.casefold(), text.casefold())

        census_fields = table_first_column_after_heading(
            text, "## 1. Freeze the calibration question and denominator"
        )
        self.assertTrue(
            {
                "Source identity",
                "publication_form",
                "Contribution shape",
                "Source completeness",
                "Coverage",
                "Validation",
                "Disposition",
            }.issubset(census_fields)
        )
        matrix_fields = table_first_column_after_heading(
            text, "## 4. Build a cross-paper evidence matrix"
        )
        self.assertTrue(
            {
                "Source",
                "Stratum",
                "Locator",
                "Observed role",
                "Proposed pattern",
                "Quality basis",
                "Counterevidence",
                "Confidence",
            }.issubset(matrix_fields)
        )
        transfer_fields = table_first_column_after_heading(
            text, "## 6. Transfer only bounded decisions"
        )
        self.assertTrue(
            {
                "Target",
                "Pattern and use condition",
                "Evidence",
                "Counterexample",
                "Stronger rejected rule",
                "Policy boundary",
                "Source boundary",
            }.issubset(transfer_fields)
        )
        self.assertIn("at least two independent source locators", text)

    def test_paper_card_is_a_non_triggering_pipeline_component(self):
        component = SKILLS / "research-publication-pipeline" / "components" / "paper-card"
        self.assertTrue((component / "guide.md").is_file())
        self.assertTrue((component / "scripts" / "prepare_paper.py").is_file())
        self.assertTrue((component / "scripts" / "audit_paper_card.py").is_file())
        self.assertFalse((component / "SKILL.md").exists())
        skill_text = (SKILLS / "research-publication-pipeline" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("components/paper-card/guide.md", skill_text)

    def test_package_contains_no_symlinks_or_private_control_artifacts(self):
        links = [str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)
        forbidden = {
            "pipeline-state.json",
            "compute-preflight.json",
            "execution-receipt.json",
            "delegated-decision-receipt.json",
            "release-manifest.json",
        }
        observed = {path.name for path in PACKAGE.rglob("*")}
        self.assertTrue(forbidden.isdisjoint(observed))


if __name__ == "__main__":
    unittest.main()
