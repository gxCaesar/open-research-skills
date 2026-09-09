"""Check the survey ledger validator, and that every rule it declares can fire."""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "survey-and-audit-novelty"
CHECKER = SKILL / "scripts" / "check_survey_ledger.py"
CLEAN = SKILL / "examples" / "survey-ledger" / "clean.json"
KNOWN_BAD = SKILL / "examples" / "survey-ledger" / "known-bad.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_survey_ledger", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def rules(ledger) -> set:
    return {rule for rule, _ in checker.check(ledger)}


def mutate(base, edit):
    ledger = copy.deepcopy(base)
    edit(ledger)
    return ledger


class SurveyLedgerTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_clean_fixture_passes_through_the_command(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(CLEAN)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertIn("angles=8", result.stdout)

    def test_the_summary_breakdown_sums_to_the_scanned_total(self):
        """The denominator has to be visible, not asserted."""
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(CLEAN)],
            text=True, capture_output=True, check=False,
        )
        line = result.stdout.strip().splitlines()[-1]
        scanned = int(re.search(r"scanned=(\d+)", line).group(1))
        parts = dict(re.findall(r"(adjacent|identical|irrelevant|uncertain)=(\d+)", line))
        self.assertEqual(scanned, sum(int(v) for v in parts.values()), line)

    def test_known_bad_fixture_fails(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("disposition_denominator_open", result.stdout)
        self.assertIn("kill_without_layer", result.stdout)

    def test_unreadable_ledger_is_rejected_rather_than_skipped(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(SKILL / "examples" / "absent.json")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("ledger_unreadable", result.stdout)

    def test_every_declared_rule_has_a_witness(self):
        """A rule no mutation reaches is decoration. Adding one without a witness fails here."""
        def drop(key):
            return lambda d: d.pop(key, None)

        witnesses = {
            "lane_not_declared": drop("contribution_lane"),
            "lane_not_recognised": lambda d: d.update(contribution_lane="novel"),
            "lane_required_field_missing": drop("second_axis"),
            "joint_variable_audit_missing": drop("joint_variable_audit"),
            "joint_row_is_not_an_object": lambda d: d["joint_variable_audit"].append("corpus C"),
            "joint_row_missing_field": lambda d: d["joint_variable_audit"][0].pop("release"),
            "empty_intersection_without_next_move": lambda d: d["joint_variable_audit"][1].pop("disposition"),
            "too_few_search_angles": lambda d: d.__setitem__("search_angles", d["search_angles"][:3]),
            "angle_missing_framing": lambda d: d["search_angles"][0].update(framing=""),
            "angle_without_recorded_result": lambda d: d["search_angles"][0].pop("result"),
            "no_adversarial_angle": lambda d: [a.pop("adversarial", None) for a in d["search_angles"]],
            "ledger_has_no_candidates": lambda d: d.update(candidates=[]),
            "candidate_is_not_an_object": lambda d: d["candidates"].append("synthetic-doi-0005"),
            "candidate_missing_identifier": lambda d: d["candidates"][0].update(identifier=""),
            "candidate_missing_disposition": lambda d: d["candidates"][0].pop("disposition"),
            "disposition_not_recognised": lambda d: d["candidates"][0].update(disposition="maybe"),
            "kill_without_layer": lambda d: d["candidates"][2].pop("kill_layer"),
            "kill_layer_not_recognised": lambda d: d["candidates"][2].update(kill_layer="obvious"),
            "task_layer_kill_without_measurement": lambda d: d["candidates"][2].update(kill_layer="task"),
            "data_layer_kill_without_enumerated_sources": lambda d: d["candidates"][2].update(kill_layer="data"),
            "disposition_denominator_open": lambda d: d.update(candidates_examined=9),
            "scoop_verdict_not_recognised": lambda d: d.update(scoop_verdict="TAKEN"),
            "scoop_kill_without_an_identical_candidate":
                lambda d: d["candidates"][2].update(disposition="adjacent"),
            "venue_fit_not_recorded_separately": drop("venue_fit"),
            "venue_fit_stop_without_an_owner": lambda d: (
                d.update(scoop_verdict="ADJACENT"),
                d["candidates"][2].update(disposition="adjacent"),
                d["venue_fit"].update(recommendation="stop"),
                d["venue_fit"].pop("owner"),
            ),
            "repair_table_missing": drop("repair_table"),
            "kill_absent_from_repair_table": lambda d: d["repair_table"][0].update(kill="c-99"),
            "repair_row_without_a_verdict": lambda d: d["repair_table"][0].pop("reversible"),
        }

        self.assertEqual(set(), rules(self.clean), "the clean fixture must be silent")
        for rule, edit in witnesses.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(mutate(self.clean, edit)))

        declared = set(re.findall(r'findings\.append\(\("([a-z_]+)"', CHECKER.read_text(encoding="utf-8")))
        self.assertEqual(set(), declared - set(witnesses), "rule with no witness")
        self.assertGreaterEqual(len(declared), 25, declared)


if __name__ == "__main__":
    unittest.main()
