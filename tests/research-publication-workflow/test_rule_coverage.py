"""Pin the validator's rule coverage so the unwitnessed set can shrink but not grow."""

import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "scripts" / "check_rule_coverage.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("check_rule_coverage", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = load_tool()

# The ceiling is written out here rather than read from the tool. Deriving it from the set
# it is meant to bound made the assertion unfailable, which is how it was written first:
# `frozenset(tool.UNWITNESSED)` compared against `set(tool.UNWITNESSED)` is always empty.
# The list stood at 27 and reached zero by writing the missing mutations. It stays at zero.
UNWITNESSED_CEILING: frozenset = frozenset()


class RuleCoverageTest(unittest.TestCase):
    def test_every_declared_rule_is_witnessed_or_listed(self):
        declared = tool.declared_rules()
        accounted = set(tool.WITNESSES) | set(tool.UNWITNESSED)
        self.assertEqual(set(), declared - accounted, "rule neither witnessed nor listed")
        self.assertEqual(set(), accounted - declared, "listed rule the validator cannot emit")

    def test_the_unwitnessed_set_does_not_grow(self):
        self.assertEqual(set(), set(tool.UNWITNESSED) - UNWITNESSED_CEILING)

    def test_every_rule_the_validator_can_emit_has_a_witness(self):
        """Zero is the current answer; a rule added without one has to change this line."""
        self.assertEqual({}, tool.UNWITNESSED)
        self.assertEqual(tool.declared_rules(), set(tool.WITNESSES))

    def test_each_unwitnessed_rule_would_carry_a_reason(self):
        """The escape hatch still has a contract, even while nothing uses it."""
        for rule, reason in tool.UNWITNESSED.items():
            with self.subTest(rule=rule):
                self.assertGreater(len(reason.strip()), 20, rule)

    def test_a_rule_without_a_witness_is_reported_as_unaccounted(self):
        """The reconciliation arithmetic has to notice a gap, not just print a total."""
        declared = tool.declared_rules()
        witnessed = set(tool.WITNESSES) - {"SPLIT_CONTRACT"}
        unaccounted = declared - witnessed - set(tool.UNWITNESSED)
        self.assertEqual({"SPLIT_CONTRACT"}, unaccounted)

    def test_the_command_reports_a_closed_reconciliation(self):
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL)], text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Nothing unaccounted", result.stdout)
        counts = dict(re.findall(r"(declared|witnessed|unwitnessed)=(\d+)", result.stdout))
        self.assertEqual(
            int(counts["declared"]),
            int(counts["witnessed"]) + int(counts["unwitnessed"]),
            result.stdout,
        )

    def test_the_witness_runner_can_fail(self):
        """A runner that always passes reports the same thing as a healthy one."""
        validator = tool.load_validator()
        target, public_release, _ = tool.WITNESSES["SPLIT_CONTRACT"]
        unchanged = tool.run_witness(validator, "SPLIT_CONTRACT", target, public_release,
                                     lambda project: None)
        self.assertEqual(set(), unchanged, "the base project must validate cleanly")
        mutated = tool.run_witness(validator, "SPLIT_CONTRACT", *tool.WITNESSES["SPLIT_CONTRACT"])
        self.assertIn("SPLIT_CONTRACT", mutated)


if __name__ == "__main__":
    unittest.main()
