"""Give every rule of the data-inventory validator a witness that makes it fire.

A rule nothing can make fire could stop working with the suite still green. Fourteen of
this validator's seventeen rules had no witness anywhere in the repository when this file
was written.
"""

import ast
import copy
import importlib.util
import json
import re
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENT = PACKAGE / "skills" / "prepare-journal-manuscripts" / "components" / "data-availability"
CHECKER = COMPONENT / "scripts" / "validate_data_inventory.py"
CLEAN = COMPONENT / "examples" / "data-inventory.example.json"
REPORTERS = {"add", "require_text", "require_enum"}


def load_checker():
    spec = importlib.util.spec_from_file_location("validate_data_inventory", CHECKER)
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


def with_second(route, **fields):
    """Append a second dataset on a given route, so route-specific rules can be reached."""
    def edit(payload):
        extra = copy.deepcopy(payload["datasets"][0])
        extra["dataset_id"] = "D2"
        extra["access_route"] = route
        extra.update(fields)
        payload["datasets"].append(extra)
    return edit


WITNESSES = {
        "ROOT_OBJECT": None,
        "SCHEMA_VERSION": lambda d: d.update(schema_version=2),
        "AUTHORITY": lambda d: d.update(journal=""),
        "DATASETS": lambda d: d.update(datasets=[]),
        "DATASET_OBJECT": lambda d: d["datasets"].append("D9"),
        "DATASET_IDENTITY": lambda d: d["datasets"][0].update(description=""),
        "DUPLICATE_ID": with_second("public_repository", dataset_id="D1"),
        "ORIGIN": lambda d: d["datasets"][0].update(origin="invented"),
        "ACCESS_ROUTE": lambda d: d["datasets"][0].update(access_route="somewhere"),
        "CLAIM_MAPPING": lambda d: d["datasets"][0].update(supports=[]),
        "PUBLIC_REPOSITORY": lambda d: d["datasets"][0].update(identifier=""),
        "CONTROLLED_ACCESS": with_second("controlled_access", restrictions={}),
        "REUSED_PUBLIC": with_second("reused_public", citation="", version_or_access_date=""),
        "THIRD_PARTY_ACCESS": with_second("third_party_restricted", restrictions={}),
        "REQUEST_ACCESS": with_second("justified_request", restrictions={}),
        "NOT_APPLICABLE": with_second("not_applicable"),
        "UNRESOLVED_FIELD": lambda d: d["datasets"][0].update(
            identifier="[replace with the identifier]"),
}


class DataInventoryCoverageTest(unittest.TestCase):
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
        self.assertGreaterEqual(len(declared), 17, declared)

    def test_a_missing_witness_would_be_reported(self):
        """The reconciliation has to detect a gap, not only recount a matching pair."""
        incomplete = set(WITNESSES) - {"ACCESS_ROUTE"}
        self.assertEqual({"ACCESS_ROUTE"}, declared_rules() - incomplete)


if __name__ == "__main__":
    unittest.main()
