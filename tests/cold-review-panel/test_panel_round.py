"""Check the panel round validator, and that every rule it declares can fire."""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "run-cold-review-panel"
CHECKER = SKILL / "scripts" / "check_panel_round.py"
CLEAN = SKILL / "examples" / "panel-round" / "clean.json"
KNOWN_BAD = SKILL / "examples" / "panel-round" / "known-bad.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_panel_round", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def rules(record) -> set:
    return {rule for rule, _ in checker.check(record)}


def mutate(base, edit):
    record = copy.deepcopy(base)
    edit(record)
    return record


class PanelRoundTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_clean_fixture_passes_through_the_command(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(CLEAN)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertIn("executed_artifact=1", result.stdout)

    def test_known_bad_fixture_fails(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        for rule in (
            "isolation_evidence_is_self_report",
            "manifest_contains_internal_material",
            "acceptance_probability_reported",
            "finding_not_adjudicated",
        ):
            self.assertIn(rule, result.stdout, rule)

    def test_unreadable_round_is_rejected_rather_than_skipped(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(SKILL / "examples" / "absent.json")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("round_unreadable", result.stdout)

    def test_self_report_detection_against_known_answers(self):
        """A model describing its own inputs is not an observation; the wording varies."""
        positives = (
            "each reviewer stated it had no other context",
            "the reviewers confirmed they saw only the manuscript",
            "model reports a clean context",
            "the agent asserted isolation",
            "the panel says nothing else was in scope",
        )
        negatives = (
            "directory listing of the reviewer package taken before dispatch",
            "listing of the dispatch directory, sizes included",
            "filesystem listing captured before the panel opened",
        )
        for text in positives:
            with self.subTest(text=text):
                self.assertTrue(checker.SELF_REPORT.search(text))
        for text in negatives:
            with self.subTest(text=text):
                self.assertIsNone(checker.SELF_REPORT.search(text))

    def test_every_declared_rule_has_a_witness(self):
        def drop(key):
            return lambda d: d.pop(key, None)

        witnesses = {
            "isolation_manifest_missing": drop("isolation_manifest"),
            "manifest_entry_without_a_path": lambda d: d["isolation_manifest"].append({"bytes": 1}),
            "manifest_entry_without_a_size": lambda d: d["isolation_manifest"][0].pop("bytes"),
            "manifest_contains_internal_material":
                lambda d: d["isolation_manifest"].append({"path": "project-plan.md", "bytes": 12}),
            "isolation_evidence_not_recorded": drop("isolation_evidence"),
            "isolation_evidence_is_self_report":
                lambda d: d.update(isolation_evidence="the reviewer stated it saw nothing else"),
            "round_has_no_reviewers": lambda d: d.update(reviewers=[]),
            "reviewer_is_not_an_object": lambda d: d["reviewers"].append("r-6"),
            "lens_not_recognised": lambda d: d["reviewers"][0].update(lens="everything"),
            "lens_not_covered": lambda d: d["reviewers"].pop(0),
            "model_family_not_recorded": lambda d: d["reviewers"][0].pop("model_family"),
            "reviewer_reported_no_findings": lambda d: d["reviewers"][0].update(findings=[]),
            "finding_is_not_an_object": lambda d: d["reviewers"][0]["findings"].append("f-99"),
            "finding_without_an_id": lambda d: d["reviewers"][0]["findings"][0].pop("id"),
            # Two independent reviewers numbering from the same start, which is what made a
            # single adjudication row cover five distinct findings.
            "finding_id_not_unique": lambda d: d["reviewers"][1]["findings"][0].update(
                id=d["reviewers"][0]["findings"][0]["id"]),
            "finding_missing_field": lambda d: d["reviewers"][0]["findings"][0].pop("location"),
            "no_reviewer_executed_the_artifact":
                lambda d: d["reviewers"][3].pop("executed_artifact"),
            "execution_claimed_without_commands": lambda d: d["reviewers"][3].pop("commands"),
            "command_without_a_command_line":
                lambda d: d["reviewers"][3]["commands"].append({"output": "ok"}),
            "command_without_recorded_output":
                lambda d: d["reviewers"][3]["commands"][0].pop("output"),
            "meta_review_missing": drop("meta_review"),
            "acceptance_probability_reported":
                lambda d: d["meta_review"].update(acceptance_probability=0.4),
            "adjudication_row_without_a_finding":
                lambda d: d["meta_review"]["adjudication"].append({"state": "confirmed"}),
            "adjudication_state_not_recognised":
                lambda d: d["meta_review"]["adjudication"][0].update(state="probably right"),
            "confirmed_finding_without_a_repair":
                lambda d: d["meta_review"]["adjudication"][0].pop("repair"),
            "finding_not_adjudicated": lambda d: d["meta_review"]["adjudication"].pop(0),
        }

        self.assertEqual(set(), rules(self.clean), "the clean fixture must be silent")
        for rule, edit in witnesses.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(mutate(self.clean, edit)))

        # Rules are emitted both as findings.append((...)) and as return [(...)];
        # a pattern that sees only the first form silently under-reports the set.
        declared = set(re.findall(r'[(\[]\("([a-z_]+)"', CHECKER.read_text(encoding="utf-8")))
        self.assertEqual(set(), declared - set(witnesses), "rule with no witness")
        self.assertGreaterEqual(len(declared), 25, declared)


if __name__ == "__main__":
    unittest.main()
