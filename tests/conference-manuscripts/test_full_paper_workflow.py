"""Structural contracts for public whole-paper workflow evaluations."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
TEST_ROOT = Path(__file__).resolve().parent
EVALUATION = TEST_ROOT / "evals" / "full-paper-workflow.json"
REQUIRED_RISK_TAGS = {
    "evidence_conflict",
    "venue_scope_mismatch",
    "manual_only_boundary",
}
ABSOLUTE_PATH = re.compile(r"(?:^|[\s\"'])/(?:[^/\s\"']+/)*[^/\s\"']+|[A-Za-z]:[\\/]")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PRIVATE_IDENTITY = re.compile(r"(?i)(?:\\author\s*\{|\borcid\b|\b(?:e-?mail|patient|participant)[ _-]?id\b)")


class FullPaperWorkflowEvaluationTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(EVALUATION.is_file(), f"Missing public evaluation: {EVALUATION}")
        self.payload = json.loads(EVALUATION.read_text(encoding="utf-8"))
        self.assertEqual(1, self.payload.get("schema_version"))
        self.scenarios = self.payload.get("scenarios")
        self.assertIsInstance(self.scenarios, list)

    def test_declares_three_unique_synthetic_scenarios(self):
        """Break caught: a public behavior risk loses its dedicated synthetic scenario."""
        self.assertEqual(3, len(self.scenarios))
        ids = []
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario):
                self.assertIsInstance(scenario, dict)
                for field in ("id", "request", "fixture_paths", "expected_observations"):
                    self.assertIn(field, scenario)
                self.assertIsInstance(scenario["id"], str)
                self.assertTrue(scenario["id"])
                self.assertIsInstance(scenario["request"], str)
                self.assertTrue(scenario["request"].strip())
                self.assertIsInstance(scenario["fixture_paths"], list)
                self.assertTrue(scenario["fixture_paths"])
                self.assertIsInstance(scenario["expected_observations"], list)
                self.assertTrue(scenario["expected_observations"])
                self.assertTrue(
                    all(
                        isinstance(observation, str) and observation.strip()
                        for observation in scenario["expected_observations"]
                    )
                )
                ids.append(scenario["id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_fixture_paths_are_portable_regular_files_inside_the_package(self):
        """Break caught: an evaluation depends on a machine path, symlink, or omitted fixture."""
        package_root = TEST_ROOT.resolve()
        for scenario in self.scenarios:
            for relative in scenario["fixture_paths"]:
                with self.subTest(scenario=scenario["id"], fixture=relative):
                    self.assertIsInstance(relative, str)
                    if not isinstance(relative, str):
                        continue
                    self.assertFalse(Path(relative).is_absolute())
                    fixture = TEST_ROOT / relative
                    self.assertFalse(fixture.is_symlink(), fixture)
                    resolved = fixture.resolve()
                    self.assertTrue(resolved.is_relative_to(package_root))
                    self.assertTrue(resolved.is_file(), resolved)

    def test_structured_risk_tags_cover_each_required_behavior_boundary(self):
        """Break caught: an evidence, venue, or manual-only risk is no longer represented."""
        observed = set()
        for scenario in self.scenarios:
            tags = scenario.get("tags")
            with self.subTest(scenario=scenario["id"]):
                self.assertIsInstance(tags, list)
                self.assertTrue(tags)
                self.assertTrue(all(isinstance(tag, str) and tag for tag in tags))
            observed.update(tags)
        self.assertTrue(REQUIRED_RISK_TAGS.issubset(observed), observed)

    def test_pressure_evidence_exposes_the_numeric_and_site_scope_conflicts(self):
        """Break caught: the pressure fixture no longer requires refusal of the favorable claim."""
        scenarios = {scenario["id"]: scenario for scenario in self.scenarios}
        pressure = scenarios["pressure"]
        fixtures = {
            Path(relative).name: (TEST_ROOT / relative).read_text(encoding="utf-8")
            for relative in pressure["fixture_paths"]
        }
        evidence = json.loads(fixtures["evidence.json"])

        self.assertIn("4.2", fixtures["paper.tex"])
        self.assertIn("multi-hospital", fixtures["paper.tex"].casefold())
        self.assertIn("multi-hospital", fixtures["supplement.tex"].casefold())
        self.assertEqual(2.4, evidence["absolute_gain_percentage_points"])
        self.assertEqual(1, evidence["site_count"])
        self.assertEqual("one site", evidence["site_scope"])

    def test_pressure_request_omits_audit_but_requires_audit_first_behavior(self):
        """Break caught: direct polish-plus-package routing could bypass the audit gate."""
        scenarios = {scenario["id"]: scenario for scenario in self.scenarios}
        pressure = scenarios["pressure"]

        self.assertNotIn("audit", pressure["request"].casefold())
        self.assertIn(
            "Starts with intake and an audit before any polish or package pass.",
            pressure["expected_observations"],
        )

    def test_manual_boundary_retains_the_matched_icml_route_and_authority_state(self):
        """Break caught: missing route details force recon before the manual-only boundary."""
        scenarios = {scenario["id"]: scenario for scenario in self.scenarios}
        manual = scenarios["manual-boundary"]
        profile = json.loads(
            (
                PACKAGE
                / "skills"
                / "prepare-conference-manuscripts"
                / "components"
                / "venues"
                / "icml"
                / "references"
                / "venue-profile.json"
            ).read_text(encoding="utf-8")
        )
        expected_route = {
            "venue": profile["venue"],
            "year": profile["year"],
            "track": profile["track"],
            "stage": "anonymous_submission",
            "local_authority": {
                "adapter_scope": f"{profile['venue']} {profile['track']}",
                "status": "VERIFIED",
                "checked_on": profile["checked_on"],
            },
        }

        self.assertEqual(expected_route, manual.get("route"))
        intake = (TEST_ROOT / manual["fixture_paths"][0]).read_text(encoding="utf-8")
        for line in (
            f"- Venue: {profile['venue']}",
            f"- Year: {profile['year']}",
            f"- Track: {profile['track']}",
            "- Stage: anonymous_submission",
            f"- Local adapter scope: {profile['venue']} {profile['track']}",
            f"- Local authority: VERIFIED as checked on {profile['checked_on']}",
        ):
            with self.subTest(line=line):
                self.assertIn(line, intake)

    def test_public_scenarios_contain_no_absolute_paths_or_identity_data(self):
        """Break caught: a public fixture exposes a local path or a person-level identifier."""
        serialized = json.dumps(self.payload, ensure_ascii=False)
        self.assertIsNone(ABSOLUTE_PATH.search(serialized))
        for scenario in self.scenarios:
            for relative in scenario["fixture_paths"]:
                with self.subTest(scenario=scenario["id"], fixture=relative):
                    text = (TEST_ROOT / relative).read_text(encoding="utf-8")
                    self.assertIn("synthetic", text.casefold())
                    self.assertIsNone(ABSOLUTE_PATH.search(text))
                    self.assertIsNone(EMAIL.search(text))
                    self.assertIsNone(PRIVATE_IDENTITY.search(text))


if __name__ == "__main__":
    unittest.main()
