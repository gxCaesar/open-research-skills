"""Check the iteration ledger validator, and that every rule it declares can fire."""

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "develop-method-to-sota"
CHECKER = SKILL / "scripts" / "check_iteration_ledger.py"
CLEAN = SKILL / "examples" / "iteration-ledger" / "clean.json"
KNOWN_BAD = SKILL / "examples" / "iteration-ledger" / "known-bad.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_iteration_ledger", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def rules(ledger) -> set:
    return {rule for rule, _ in checker.check(ledger)}


class IterationLedgerTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_clean_fixture_passes_through_the_command(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(CLEAN)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertIn("scanned=3", result.stdout)

    def test_known_bad_fixture_fails_for_the_intended_reasons(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        for rule in (
            "void_from_single_seed",
            "construction_shape_repeats_a_kill",
            "iteration_missing_field",
            "order_out_of_range",
            "verdict_not_recognised",
            "architecture_before_lower_orders",
            "saturation_exit_without_measurement",
        ):
            self.assertIn(rule, result.stdout, rule)

    def test_unreadable_ledger_is_rejected_rather_than_skipped(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(SKILL / "examples" / "absent.json")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("ledger_unreadable", result.stdout)

    def test_every_declared_rule_can_fire(self):
        """A rule that no mutation reaches is decoration; each one gets a witness."""
        witnesses = {}

        empty = copy.deepcopy(self.clean)
        empty["iterations"] = []
        witnesses["ledger_has_no_iterations"] = empty

        not_object = copy.deepcopy(self.clean)
        not_object["iterations"][0] = "it-01"
        witnesses["iteration_is_not_an_object"] = not_object

        missing = copy.deepcopy(self.clean)
        missing["iterations"][0]["mechanism"] = ""
        witnesses["iteration_missing_field"] = missing

        bad_order = copy.deepcopy(self.clean)
        bad_order["iterations"][0]["order"] = 0
        witnesses["order_out_of_range"] = bad_order

        bad_verdict = copy.deepcopy(self.clean)
        bad_verdict["iterations"][0]["verdict"] = "looks good"
        witnesses["verdict_not_recognised"] = bad_verdict

        one_seed = copy.deepcopy(self.clean)
        one_seed["iterations"][1]["control"]["seeds"] = [11]
        witnesses["void_from_single_seed"] = one_seed

        bad_arm = copy.deepcopy(self.clean)
        bad_arm["iterations"][0]["control"] = "same run without the reweighting"
        witnesses["control_is_not_an_arm"] = bad_arm

        renamed = copy.deepcopy(self.clean)
        del renamed["iterations"][2]["differs_from_prior"]
        witnesses["construction_shape_repeats_a_kill"] = renamed

        architecture = copy.deepcopy(self.clean)
        for entry in architecture["iterations"]:
            entry["order"] = 6
        witnesses["architecture_before_lower_orders"] = architecture

        bad_exit = copy.deepcopy(self.clean)
        bad_exit["exit"]["number"] = 4
        witnesses["exit_not_recognised"] = bad_exit

        saturated = copy.deepcopy(self.clean)
        saturated["exit"] = {"number": 1}
        witnesses["saturation_exit_without_measurement"] = saturated

        self.assertEqual(set(), rules(self.clean), "the clean fixture must be silent")
        for rule, ledger in witnesses.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(ledger))

    def test_the_witness_set_covers_every_rule_the_checker_emits(self):
        """Adding a rule without a witness must break this test."""
        emitted = set()
        for path in (CLEAN, KNOWN_BAD):
            emitted |= rules(json.loads(path.read_text(encoding="utf-8")))
        source = CHECKER.read_text(encoding="utf-8")
        declared = set(
            line.split('("', 1)[1].split('"', 1)[0]
            for line in source.splitlines()
            if 'findings.append(("' in line
        )
        declared.add("ledger_unreadable")
        self.assertGreaterEqual(len(declared), 10, declared)
        covered = {
            "ledger_has_no_iterations", "iteration_is_not_an_object",
            "iteration_missing_field", "order_out_of_range", "verdict_not_recognised",
            "void_from_single_seed", "control_is_not_an_arm",
            "construction_shape_repeats_a_kill", "architecture_before_lower_orders",
            "exit_not_recognised", "saturation_exit_without_measurement",
            "ledger_unreadable",
        }
        self.assertEqual(set(), declared - covered, "rule with no witness")


if __name__ == "__main__":
    unittest.main()
