"""Check the code-inventory validator, and that every rule it declares can fire."""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENT = (
    PACKAGE / "skills" / "prepare-journal-manuscripts" / "components" / "code-availability"
)
CHECKER = COMPONENT / "scripts" / "validate_code_inventory.py"
CLEAN = COMPONENT / "examples" / "code-inventory.example.json"
KNOWN_BAD = COMPONENT / "examples" / "code-inventory.known-bad.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("validate_code_inventory", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def rules(payload, mode="final") -> set:
    return {item["rule_id"] for item in checker.validate(payload, mode)}


def mutate(base, edit):
    payload = copy.deepcopy(base)
    edit(payload)
    return payload


class CodeAvailabilityTest(unittest.TestCase):
    def setUp(self):
        self.clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    def test_shipped_example_passes_in_both_modes(self):
        for mode in ("working", "final"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    [sys.executable, "-B", str(CHECKER), str(CLEAN), "--mode", mode],
                    text=True, capture_output=True, check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_known_bad_example_fails_at_final(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD), "--mode", "final"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        report = json.loads(result.stdout)
        self.assertEqual("FAIL", report["status"])
        found = {item["rule_id"] for item in report["findings"]}
        for rule in (
            "custom_code_not_applicable",
            "repository_without_archive",
            "statement_promises_rather_than_provides",
            "unresolved_placeholder",
        ):
            self.assertIn(rule, found, rule)

    def test_an_unarchived_repository_is_a_warning_while_drafting_and_an_error_at_final(self):
        """The rule changes severity by mode; a single-mode test would miss half of it."""
        payload = mutate(self.clean, lambda d: d["components"][0].update(
            access_route="public_repository", repository="Synthetic Host",
            identifier="https://example.org/synthetic/repo"))
        for mode, severity in (("working", "warning"), ("final", "error")):
            with self.subTest(mode=mode):
                findings = {
                    item["rule_id"]: item["severity"]
                    for item in checker.validate(payload, mode)
                }
                self.assertEqual(severity, findings.get("repository_without_archive"))

    def test_a_promise_is_rejected_however_it_is_phrased(self):
        for phrasing in (
            "Code will be made available upon publication.",
            "Analysis code is available on reasonable request.",
            "The repository will be released after publication.",
            "Scripts are coming soon.",
        ):
            with self.subTest(phrasing=phrasing):
                payload = mutate(self.clean, lambda d, p=phrasing: d.update(statement=p))
                self.assertIn("statement_promises_rather_than_provides", rules(payload))
        for phrasing in (
            "All custom analysis code is archived at https://doi.org/10.0000/synthetic-code.1 "
            "(C1, v1.0.0, Apache-2.0). C2 and C3 are described in the Methods.",
            "Every component below is deposited with a persistent identifier: C1, C2, C3.",
        ):
            with self.subTest(accepted=phrasing):
                payload = mutate(self.clean, lambda d, p=phrasing: d.update(statement=p))
                self.assertNotIn("statement_promises_rather_than_provides", rules(payload))

    def test_every_declared_rule_has_a_witness(self):
        def drop(key):
            return lambda d: d.pop(key, None)

        witnesses = {
            "inventory": lambda d: None,  # replaced below; the payload itself is not an object
            "schema_version": lambda d: d.update(schema_version=2),
            "journal": drop("journal"),
            "components": lambda d: d.update(components=[]),
            "component": lambda d: d["components"].append("C4"),
            "component_id": lambda d: d["components"][1].update(component_id="C1"),
            "description": lambda d: d["components"][0].update(description=""),
            "supports": lambda d: d["components"][0].update(supports=[]),
            "origin": lambda d: d["components"][0].update(origin="borrowed"),
            "access_route": lambda d: d["components"][0].update(access_route="somewhere"),
            "custom_code_not_applicable": lambda d: d["components"][0].update(access_route="not_applicable"),
            "not_applicable_reason": lambda d: d["components"][2].update(
                origin="reused", access_route="not_applicable"),
            "version_or_commit": lambda d: d["components"][0].update(version_or_commit=""),
            "identifier": lambda d: d["components"][0].update(identifier=""),
            "repository": lambda d: d["components"][0].update(
                access_route="public_repository", repository=""),
            "repository_without_archive": lambda d: d["components"][0].update(
                access_route="public_repository", repository="Synthetic Host"),
            "licence": lambda d: d["components"][0].update(licence=""),
            "environment": lambda d: d["components"][0].pop("environment"),
            "environment_runtime": lambda d: d["components"][0]["environment"].pop("interpreter_or_runtime"),
            "citation": lambda d: d["components"][1].update(citation=""),
            "third_party": lambda d: d["components"][2].update(conditions=""),
            "request_route": lambda d: d["components"][2].update(access_route="justified_request"),
            "request_route_at_final": lambda d: d["components"][2].update(access_route="justified_request"),
            "statement": lambda d: d.pop("statement"),
            "statement_promises_rather_than_provides": lambda d: d.update(
                statement="Code will be made available upon reasonable request."),
            "statement_omits_component": lambda d: d.update(statement="Code is deposited."),
            "unresolved_placeholder": lambda d: d["components"][0].update(licence="[replace with a licence]"),
        }

        self.assertEqual(set(), rules(self.clean), "the shipped example must be silent")
        for rule, edit in witnesses.items():
            with self.subTest(rule=rule):
                if rule == "inventory":
                    self.assertIn(rule, rules(["not", "an", "object"]))
                    continue
                self.assertIn(rule, rules(mutate(self.clean, edit)))

        declared = set(re.findall(r'add\(findings, "([a-z_]+)"', CHECKER.read_text(encoding="utf-8")))
        self.assertEqual(set(), declared - set(witnesses), "rule with no witness")
        self.assertGreaterEqual(len(declared), 26, declared)


if __name__ == "__main__":
    unittest.main()
