"""Give every rule of the analysis-register validator a witness that makes it fire.

Eleven of its fifteen rules had no witness anywhere in the repository when this file was
written. The conference and journal copies of this script are byte-identical, asserted in
tests/test_bundled_script_hygiene.py, so witnessing one covers both.
"""

import ast
import copy
import importlib.util
import json
import re
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENT = PACKAGE / "skills" / "prepare-journal-manuscripts" / "components" / "statistics-reporting"
CHECKER = COMPONENT / "scripts" / "validate_analysis_register.py"
CLEAN = COMPONENT / "examples" / "analysis-register.example.json"
REPORTERS = {"add", "require_text", "require_enum"}


def load_checker():
    spec = importlib.util.spec_from_file_location("validate_analysis_register", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def declared_rules() -> set:
    rules = set()
    for node in ast.walk(ast.parse(CHECKER.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", "")
            if name in REPORTERS:
                for argument in node.args:
                    if isinstance(argument, ast.Constant) and isinstance(argument.value, str) \
                       and re.fullmatch(r"[A-Z][A-Z_]{3,}", argument.value):
                        rules.add(argument.value)
    return rules


def rules(payload, mode="final") -> set:
    return {item["rule_id"] for item in checker.validate(payload, mode)}


def mutate(base, edit):
    payload = copy.deepcopy(base)
    edit(payload)
    return payload


def duplicate_analysis(payload):
    extra = copy.deepcopy(payload["analyses"][0])
    payload["analyses"].append(extra)


WITNESSES = {
    "ROOT_OBJECT": None,
    "SCHEMA_VERSION": lambda d: d.update(schema_version=2),
    "STUDY_ID": lambda d: d.update(study_id=""),
    "ANALYSES": lambda d: d.update(analyses=[]),
    "ANALYSIS_OBJECT": lambda d: d["analyses"].append("A9"),
    "DUPLICATE_ID": duplicate_analysis,
    "ANALYSIS_HIERARCHY": lambda d: d["analyses"][0].update(hierarchy=[]),
    "DENOMINATOR": lambda d: d["analyses"][0].update(included_units=0),
    "GROUP_DENOMINATORS": lambda d: d["analyses"][0].update(
        n_by_group={"condition A": 0, "condition B": 6}),
    "SKIP_ACCOUNTING": lambda d: d["analyses"][0].update(skip_reasons=[""]),
    "DEPENDENCE_HANDLING": lambda d: d["analyses"][0].update(
        paired_or_repeated="repeated", dependence_handling=""),
    "INTERACTION_TEST": lambda d: d["analyses"][0].update(interaction_claim=True),
    # The example already declares a full stochastic design, so the witness removes it
    # rather than turning the flag on, which changes nothing.
    "STOCHASTIC_SELECTION": lambda d: d["analyses"][0].pop("stochastic_design"),
    "SOURCE_POINTER": lambda d: d["analyses"][0].update(sources=[]),
    "UNRESOLVED_FIELD": lambda d: d["analyses"][0].update(claim="[replace with the claim]"),
}


class AnalysisRegisterCoverageTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_the_shipped_example_is_silent(self):
        self.assertEqual(set(), rules(self.clean))

    def test_every_declared_rule_has_a_witness(self):
        for rule, edit in WITNESSES.items():
            with self.subTest(rule=rule):
                payload = ["not", "an", "object"] if edit is None else mutate(self.clean, edit)
                self.assertIn(rule, rules(payload))

        declared = declared_rules()
        self.assertEqual(set(), declared - set(WITNESSES), "rule with no witness")
        self.assertEqual(set(), set(WITNESSES) - declared, "witness for a rule that is gone")
        self.assertGreaterEqual(len(declared), 15, declared)

    def test_a_missing_witness_would_be_reported(self):
        incomplete = set(WITNESSES) - {"DENOMINATOR"}
        self.assertEqual({"DENOMINATOR"}, declared_rules() - incomplete)

    def test_the_conference_copy_reports_the_same_rules(self):
        """The two copies are asserted byte-identical elsewhere; this is the behavioural half."""
        twin = (PACKAGE / "skills" / "prepare-conference-manuscripts" / "components"
                / "statistics-reporting" / "scripts" / "validate_analysis_register.py")
        spec = importlib.util.spec_from_file_location("twin_validate_analysis_register", twin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for rule, edit in WITNESSES.items():
            with self.subTest(rule=rule):
                payload = ["not", "an", "object"] if edit is None else mutate(self.clean, edit)
                self.assertIn(rule, {item["rule_id"] for item in module.validate(payload, "final")})


if __name__ == "__main__":
    unittest.main()
