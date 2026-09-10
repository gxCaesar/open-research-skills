"""Check the handover-pack validator, and that every rule it declares can fire.

The two rules about machine-specific paths are witnessed here rather than in a shipped
fixture: a file containing a literal absolute home path would make the repository fail
its own content scan, so those strings are composed at runtime.
"""

import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPONENT = (
    ROOT / "skills" / "research-publication-pipeline" / "components" / "project-handover"
)
CHECKER = COMPONENT / "scripts" / "validate_handover_pack.py"
CLEAN = COMPONENT / "examples" / "handover-pack.example.json"
KNOWN_BAD = COMPONENT / "examples" / "handover-pack.known-bad.json"
HOME_PREFIX = "/" + "Users" + "/someone/"
LINUX_PREFIX = "/" + "home" + "/someone/"


def load_checker():
    spec = importlib.util.spec_from_file_location("validate_handover_pack", CHECKER)
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


class ProjectHandoverTest(unittest.TestCase):
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

    def test_known_bad_example_fails(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), str(KNOWN_BAD), "--mode", "final"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        found = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        for rule in (
            "run_layout_escapes_the_project",
            "environment_not_pinned",
            "answer_defers_to_the_author",
            "rehearsal_by_the_author",
        ):
            self.assertIn(rule, found, rule)

    def test_a_machine_specific_command_is_rejected(self):
        """Composed at runtime; the literal is what the content scan rejects."""
        payload = mutate(self.clean, lambda d: d["tasks"][0].update(
            command=f"bash {HOME_PREFIX}project/run.sh"))
        self.assertEqual({"command_names_one_machine"}, rules(payload))
        payload = mutate(self.clean, lambda d: d["run_layout"].update(
            root=f"{LINUX_PREFIX}experiments"))
        self.assertEqual({"run_layout_escapes_the_project"}, rules(payload))

    def test_deferring_to_the_author_is_rejected_however_it_is_phrased(self):
        for phrasing in (
            "ask me and I will tell you whether the number looks right",
            "contact the author if the score differs",
            "check with me before continuing",
            "I will send the expected value",
        ):
            with self.subTest(phrasing=phrasing):
                payload = mutate(self.clean, lambda d, p=phrasing: d["tasks"][0].update(done_when=p))
                self.assertIn("answer_defers_to_the_author", rules(payload))
        for phrasing in (
            "results/metrics.json exists and dev_score is within the recorded noise floor",
            "the slice counts sum to the evaluation set size printed by the script",
        ):
            with self.subTest(accepted=phrasing):
                payload = mutate(self.clean, lambda d, p=phrasing: d["tasks"][0].update(done_when=p))
                self.assertNotIn("answer_defers_to_the_author", rules(payload))

    def test_a_rehearsal_by_the_author_does_not_count(self):
        payload = mutate(self.clean, lambda d: d["rehearsal"].update(performed_by=d["prepared_by"]))
        self.assertIn("rehearsal_by_the_author", rules(payload))

    def test_a_missing_rehearsal_is_a_warning_while_drafting_and_an_error_at_final(self):
        payload = mutate(self.clean, lambda d: d.pop("rehearsal"))
        severities = {
            mode: {item["rule_id"]: item["severity"] for item in checker.validate(payload, mode)}
            for mode in ("working", "final")
        }
        self.assertEqual("warning", severities["working"]["rehearsal"])
        self.assertEqual("error", severities["final"]["rehearsal"])

    def test_every_declared_rule_has_a_witness(self):
        witnesses = {
            "pack": None,  # handled separately: the payload itself is not an object
            "schema_version": lambda d: d.update(schema_version=2),
            "project": lambda d: d.pop("project"),
            "run_layout": lambda d: d.pop("run_layout"),
            "run_layout_field": lambda d: d["run_layout"].update(log_directory=""),
            "run_layout_escapes_the_project": lambda d: d["run_layout"].update(root="../outside"),
            "layout_not_written_before_launch": lambda d: d["run_layout"].pop("written_before_launch"),
            "environment": lambda d: d.pop("environment"),
            "environment_field": lambda d: d["environment"].update(create_command=""),
            "environment_not_pinned": lambda d: d["environment"].update(pinned=False),
            "data_access": lambda d: d.pop("data_access"),
            "data_route": lambda d: d["data_access"].update(route="wherever"),
            "data_obtainability": lambda d: d["data_access"].update(obtainable_by_receiver=""),
            "tasks": lambda d: d.update(tasks=[]),
            "task": lambda d: d["tasks"].append("T3"),
            "task_id": lambda d: d["tasks"][1].update(task_id="T1"),
            "task_field": lambda d: d["tasks"][0].update(command=""),
            "command_names_one_machine": lambda d: d["tasks"][0].update(
                command=f"bash {HOME_PREFIX}run.sh"),
            "command_assumes_the_authors_hosts": lambda d: d["tasks"][0].update(
                command="ssh gpubox 'bash run.sh'"),
            "answer_defers_to_the_author": lambda d: d["tasks"][0].update(done_when="ask me"),
            "do_not_change": lambda d: d.pop("do_not_change"),
            "rehearsal": lambda d: d.pop("rehearsal"),
            "rehearsal_field": lambda d: d["rehearsal"].update(outcome=""),
            "rehearsal_by_the_author": lambda d: d["rehearsal"].update(performed_by=d["prepared_by"]),
            "unresolved_placeholder": lambda d: d["tasks"][0].update(goal="[replace with the goal]"),
        }

        self.assertEqual(set(), rules(self.clean), "the shipped example must be silent")
        for rule, edit in witnesses.items():
            with self.subTest(rule=rule):
                if edit is None:
                    self.assertIn(rule, rules(["not", "an", "object"]))
                    continue
                self.assertIn(rule, rules(mutate(self.clean, edit)))

        declared = set(re.findall(r'add\(findings, "([a-z_]+)"', CHECKER.read_text(encoding="utf-8")))
        self.assertEqual(set(), declared - set(witnesses), "rule with no witness")
        self.assertGreaterEqual(len(declared), 24, declared)


if __name__ == "__main__":
    unittest.main()
