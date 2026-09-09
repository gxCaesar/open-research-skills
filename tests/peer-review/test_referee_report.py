"""Check the referee report validator, and that every rule it declares can fire."""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "review-others-manuscripts"
CHECKER = SKILL / "scripts" / "check_referee_report.py"
CLEAN = SKILL / "examples" / "referee-report" / "clean.json"
KNOWN_BAD = SKILL / "examples" / "referee-report" / "known-bad.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_referee_report", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def rules(report) -> set:
    return {rule for rule, _ in checker.check(report)}


def mutate(base, edit):
    report = copy.deepcopy(base)
    edit(report)
    return report


def as_revision(report, rows):
    report["mode"] = "revision-round"
    report["revision_table"] = rows


class RefereeReportTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_clean_fixture_passes_through_the_command(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(CLEAN)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertIn("fatal=1", result.stdout)

    def test_known_bad_fixture_fails(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        for rule in (
            "taste_finding_raised_above_minor",
            "editor_and_author_recommendations_disagree",
            "prescreen_judged_a_referee_question",
        ):
            self.assertIn(rule, result.stdout, rule)

    def test_unreadable_report_is_rejected_rather_than_skipped(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(SKILL / "examples" / "absent.json")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("report_unreadable", result.stdout)

    def test_a_clean_revision_round_is_silent(self):
        report = mutate(self.clean, lambda d: as_revision(d, [
            {"point": "p-01", "requested": "split on donor and re-run",
             "letter_claims": "the split was rebuilt on donor",
             "manuscript_now": "Section 3.1 now describes a donor-level split and Table 2 is re-run",
             "resolved": True},
            {"point": "p-02", "requested": "recompute intervals over donors",
             "letter_claims": "explained in the response",
             "manuscript_now": "", "resolved": False},
        ]))
        self.assertEqual(set(), rules(report))

    def test_every_declared_rule_has_a_witness(self):
        def drop(key):
            return lambda d: d.pop(key, None)

        def prescreen(**changes):
            def edit(d):
                d["mode"] = "editorial-prescreen"
                d["recommendation"] = "proceed-to-review"
                d["to_editor"]["recommendation"] = "proceed-to-review"
                d["grounds"] = [{"statement": "the topic is in scope", "basis": "aims and scope page"}]
                for key, value in changes.items():
                    d[key] = value
            return edit

        witnesses = {
            "mode_not_recognised": lambda d: d.update(mode="skim"),
            "competing_interest_not_declared": drop("competing_interest"),
            "competing_interest_without_a_reason": lambda d: d.update(competing_interest=True),
            "external_tool_use_not_recorded": drop("external_tools"),
            "external_tool_without_a_name": lambda d: d["external_tools"].append({"policy_basis": "x"}),
            "external_tool_without_policy_basis":
                lambda d: d["external_tools"].append({"name": "a hosted assistant"}),
            "report_has_no_findings_list": lambda d: d.update(findings="see below"),
            "finding_is_not_an_object": lambda d: d["findings"].append("p-05"),
            "finding_missing_field": lambda d: d["findings"][0].pop("location"),
            "severity_not_recognised": lambda d: d["findings"][0].update(severity="critical"),
            "taste_finding_raised_above_minor": lambda d: d["findings"][3].update(severity="major"),
            "fatal_finding_without_a_consequence": lambda d: d["findings"][0].pop("consequence"),
            "recommendation_not_recognised": lambda d: d.update(recommendation="revise"),
            "editor_facing_recommendation_missing": drop("to_editor"),
            "editor_and_author_recommendations_disagree":
                lambda d: d["to_editor"].update(recommendation="reject"),
            "reject_without_a_located_high_severity_finding": lambda d: (
                d.update(recommendation="reject"),
                d["to_editor"].update(recommendation="reject"),
                [f.update(severity="minor") for f in d["findings"]],
            ),
            "revision_table_missing": lambda d: d.update(mode="revision-round"),
            "revision_row_is_not_an_object": lambda d: as_revision(d, ["p-01"]),
            "revision_point_missing_column":
                lambda d: as_revision(d, [{"point": "p-01", "requested": "x"}]),
            "point_closed_without_a_manuscript_change": lambda d: as_revision(d, [
                {"point": "p-01", "requested": "x", "letter_claims": "explained in the response",
                 "manuscript_now": "", "resolved": True}
            ]),
            "prescreen_used_a_referee_recommendation":
                lambda d: (prescreen()(d), d.update(recommendation="major-revision")),
            "prescreen_without_grounds": lambda d: (prescreen()(d), d.update(grounds=[])),
            "prescreen_ground_without_a_statement":
                lambda d: (prescreen()(d), d["grounds"].append({"basis": "policy"})),
            "prescreen_ground_without_a_citable_basis":
                lambda d: (prescreen()(d), d["grounds"].append({"statement": "the file set is incomplete"})),
            "prescreen_judged_a_referee_question":
                lambda d: (prescreen()(d), d["grounds"].append(
                    {"statement": "the contribution is not novel enough", "basis": "editor judgement"})),
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
