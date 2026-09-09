import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENTS = PACKAGE / "skills" / "prepare-journal-manuscripts" / "components"
VALIDATOR = COMPONENTS / "statistics-reporting" / "scripts" / "validate_analysis_register.py"
EXAMPLE = COMPONENTS / "statistics-reporting" / "examples" / "analysis-register.example.json"


def valid_register() -> dict:
    return {
        "schema_version": 1,
        "study_id": "synthetic-study",
        "analyses": [
            {
                "analysis_id": "A1",
                "claim": "A synthetic comparison estimates a bounded difference.",
                "endpoint": "synthetic response",
                "comparison": "condition A versus condition B",
                "independent_unit": "independent synthetic specimen",
                "hierarchy": ["specimen", "technical reading"],
                "n_by_group": {"condition A": 6, "condition B": 6},
                "included_units": 12,
                "skipped_units": 1,
                "skip_reasons": ["one prespecified acquisition failure"],
                "paired_or_repeated": "unpaired",
                "dependence_handling": "not applicable: one record per specimen",
                "model_or_test": "prespecified two-group model",
                "assumptions_and_diagnostics": "defined in the synthetic protocol",
                "comparison_family": "one prespecified primary comparison",
                "multiplicity_strategy": "not applicable to one primary comparison",
                "effect_estimate": "reported with units in the manuscript",
                "uncertainty": "95% interval reported in the manuscript",
                "p_value_policy": "exact value reported when used",
                "exclusion_timing": "prespecified before outcome analysis",
                "computational_stochastic": True,
                "stochastic_design": {
                    "seed_role": "optimization variation",
                    "aggregation_unit": "paired seed-level difference",
                    "checkpoint_rule": "fixed on validation data",
                    "early_stopping_rule": "prespecified validation rule",
                    "comparison_budget": "same three seeds for both methods",
                    "selection_rule": "aggregate all registered seeds"
                },
                "sources": ["Methods: Statistical analysis", "Figure 2"]
            }
        ]
    }


def run(payload: dict, mode: str = "final") -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "register.json"
        target.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(target), "--mode", mode, "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )


class StatisticsValidatorTest(unittest.TestCase):
    def test_bundled_example_passes_final_mode(self):
        result = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(EXAMPLE), "--mode", "final", "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_complete_register_passes_final_mode(self):
        result = run(valid_register())
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_missing_independent_unit_and_skip_reason_fail(self):
        payload = valid_register()
        payload["analyses"][0]["independent_unit"] = ""
        payload["analyses"][0]["skip_reasons"] = []
        result = run(payload)
        self.assertEqual(1, result.returncode)
        rules = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("INDEPENDENT_UNIT", rules)
        self.assertIn("SKIP_ACCOUNTING", rules)

    def test_each_comparison_requires_group_denominators(self):
        payload = valid_register()
        del payload["analyses"][0]["n_by_group"]
        result = run(payload)
        self.assertEqual(1, result.returncode)
        self.assertIn("GROUP_DENOMINATORS", result.stdout)

    def test_stochastic_analysis_requires_selection_contract(self):
        payload = valid_register()
        del payload["analyses"][0]["stochastic_design"]["checkpoint_rule"]
        result = run(payload)
        self.assertEqual(1, result.returncode)
        self.assertIn("STOCHASTIC_SELECTION", result.stdout)

    def test_unresolved_placeholder_warns_in_working_and_fails_in_final(self):
        payload = deepcopy(valid_register())
        payload["analyses"][0]["effect_estimate"] = "AUTHOR_INPUT_NEEDED"
        working = run(payload, mode="working")
        final = run(payload, mode="final")
        self.assertEqual(0, working.returncode, working.stdout + working.stderr)
        self.assertEqual("PASS_WITH_WARNINGS", json.loads(working.stdout)["status"])
        self.assertEqual(1, final.returncode)
        self.assertIn("UNRESOLVED_FIELD", final.stdout)


if __name__ == "__main__":
    unittest.main()
