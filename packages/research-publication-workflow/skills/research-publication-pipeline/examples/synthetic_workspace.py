"""Build the complete synthetic workspace used by the runnable demonstration."""

import json
from pathlib import Path


EXAMPLE_SOURCE = '''import json
import sys
from pathlib import Path


def summarize(values):
    return {"count": len(values), "total": sum(values)}


if __name__ == "__main__":
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = summarize(payload["values"])
    Path(sys.argv[2]).write_text(json.dumps(result) + "\\n", encoding="utf-8")
    print(json.dumps(result))
'''

EXAMPLE_TEST = '''import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from example import summarize


class ExampleTest(unittest.TestCase):
    def test_uses_the_supplied_values(self):
        self.assertEqual({"count": 2, "total": 9}, summarize([4, 5]))

    def test_empty_input(self):
        self.assertEqual({"count": 0, "total": 0}, summarize([]))


if __name__ == "__main__":
    unittest.main()
'''

PUBLIC_RELEASE_FILES = {
    "README.md": (
        "# Synthetic public release\n\n"
        "This arithmetic example is not a scientific result. It needs only Python 3.9+ "
        "and its standard library; no package installation or network access is needed.\n\n"
        "From this directory, run:\n\n```bash\n"
        "python3 -B src/example.py examples/input.json result.json\n"
        "python3 -B tests/test_example.py\n```\n\n"
        "The first command writes result.json; the second runs two tests. "
        "See docs/expected-output.md. Keep generated outputs outside a release copy.\n"
    ),
    "requirements.txt": "# Standard-library example\n",
    "src/example.py": EXAMPLE_SOURCE,
    "examples/input.json": '{"values": [1, 2, 3]}\n',
    "docs/data.md": "# Data\n\nThe example input is synthetic and redistributable.\n",
    "docs/expected-output.md": (
        '# Expected output\n\nresult.json and stdout contain {"count": 3, "total": 6}.\n'
        "The test command runs two tests and reports OK. These values describe only "
        "the supplied synthetic arithmetic example.\n"
    ),
    "tests/test_example.py": EXAMPLE_TEST,
    "LICENSE": "Synthetic fixture licence.\n",
    "CITATION.cff": "cff-version: 1.2.0\ntitle: Synthetic fixture\n",
    "LIMITATIONS.md": "# Limitations\n\nThis fixture is not a scientific result.\n",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def populate_ready_workspace(root: Path, public_release: bool = False) -> None:
    """Fill an initialized workspace with an entirely synthetic passing record set."""
    write_json(
        root / "evidence" / "source-register.json",
        {
            "schema_version": 1,
            "sources": [
                {
                    "source_id": "S_DATA",
                    "kind": "dataset",
                    "locator": "https://example.org/synthetic-data",
                    "accessed_on": "2026-09-04",
                    "status": "VERIFIED",
                    "inspected_location": "versioned synthetic data record",
                    "scope": "joint variables and independent units",
                },
                {
                    "source_id": "S_PAPER",
                    "kind": "paper",
                    "locator": "https://example.org/synthetic-paper",
                    "accessed_on": "2026-09-04",
                    "status": "VERIFIED",
                    "inspected_location": "methods and matched evaluation table",
                    "scope": "nearest work and comparator",
                },
                {
                    "source_id": "S_RULE",
                    "kind": "official",
                    "locator": "https://example.org/synthetic-venue-rules",
                    "accessed_on": "2026-09-04",
                    "status": "VERIFIED",
                    "inspected_location": "main-track author instructions",
                    "scope": "venue and article type",
                },
                {
                    "source_id": "S_RESULT",
                    "kind": "project-result",
                    "locator": "results/final-comparison.json",
                    "accessed_on": "2026-09-04",
                    "status": "VERIFIED",
                    "inspected_location": "paired synthetic final comparison",
                    "scope": "final result claim",
                },
            ],
        },
    )

    project = read_json(root / "project.json")
    project.update(
        {
            "route": "top-cs",
            "current_stage": "handoff",
            "authority": {
                "status": "VERIFIED",
                "source_ids": ["S_RULE"],
                "conflicts": [],
            },
        }
    )
    write_json(root / "project.json", project)

    write_json(
        root / "intake" / "intake.json",
        {
            "schema_version": 1,
            "data_feasibility": {
                "status": "PASS",
                "required_joint_variables": ["input X", "outcome Y"],
                "coexistence_evidence": "X and Y coexist in every linkable synthetic specimen.",
                "independent_unit": "synthetic specimen",
                "independent_unit_count": 24,
                "data_source_ids": ["S_DATA"],
                "strongest_cheap_baseline": "ridge regression",
                "leakage_safe_split": "specimen-disjoint split",
            },
            "scoop": {
                "verdict": "ADJACENT",
                "contribution_lane": "sota-method",
                "searched_on": "2026-09-04",
                "closest_work_source_ids": ["S_PAPER"],
                "delta_from_closest_work": "The synthetic mechanism targets a documented error slice.",
                "matched_protocol_assessment": "The closest work does not test this mechanism under the matched split.",
            },
            "venue_fit": {
                "status": "PASS",
                "route": "top-cs",
                "target_venue": "Synthetic CS Venue",
                "article_type": "main track",
                "official_rule_source_ids": ["S_RULE"],
                "rules_checked_on": "2026-09-04",
                "rationale": "The primary claim is a transferable method claim.",
            },
            "hypothesis": {
                "hypothesis_id": "H1",
                "claim": "Mechanism M improves held-out prediction on the prespecified slice.",
                "endpoint": "synthetic response score",
                "direction": "higher",
                "minimum_effect": 0.02,
                "uncertainty_method": "paired specimen bootstrap interval",
                "validation_path": "held-out specimens in a second synthetic context",
                "kill_criterion": "Stop M after two frozen predicted-slice misses.",
            },
            "decision": {
                "status": "PASS",
                "kill_layer": "NONE",
                "action": "ADVANCE",
                "rationale": "Feasibility, adjacent prior art, and route fit are separately supported.",
            },
        },
    )

    write_json(
        root / "protocol" / "protocol.json",
        {
            "schema_version": 1,
            "status": "FROZEN",
            "frozen_on": "2026-09-04",
            "hypothesis_id": "H1",
            "contribution_lane": "sota-method",
            "dataset_versions": ["synthetic-data-v1"],
            "preprocessing": "Fit every transform on the training partition only.",
            "split": {
                "description": "specimen-disjoint development and locked-test partitions",
                "independent_unit": "synthetic specimen",
                "leakage_guard": "reject any repeated specimen identifier across partitions",
                "guard_test_status": "PASS",
            },
            "primary_metric": {
                "name": "synthetic score",
                "direction": "higher",
                "implementation": "fixed implementation in evaluation.py",
            },
            "baselines": [
                {
                    "baseline_id": "B_CHEAP",
                    "class": "cheap",
                    "name": "ridge regression",
                    "version_or_source": "frozen synthetic configuration",
                    "tuning_budget": "same development folds and trial count as the candidate",
                },
                {
                    "baseline_id": "B_STRONG",
                    "class": "recent-strong",
                    "name": "strong synthetic comparator",
                    "version_or_source": "S_PAPER",
                    "tuning_budget": "official configuration plus matched development allowance",
                },
            ],
            "uncertainty": {
                "unit": "synthetic specimen",
                "method": "paired specimen bootstrap interval",
            },
            "selection": {
                "development_metric": "mean synthetic score over all registered seeds",
                "seed_policy": "three prespecified seeds for every selectable configuration",
                "checkpoint_rule": "select on development data only",
                "baseline_tuning_parity": "equal search budget and information access",
            },
            "budgets": {"development_cycles": 3, "locked_test_accesses": 1},
            "locked_test": {
                "status": "SEALED",
                "custodian": "independent synthetic evaluator",
                "accesses_used": 0,
            },
            "allowed_changes": ["one registered load-bearing intervention per cycle"],
            "stop_rules": {
                "advance": "advance only when the predicted slice and aggregate floors pass",
                "revise": "revise one registered mechanism before its second slice miss",
                "pivot": "pivot to a different registered candidate after mechanism falsification",
                "stop": "stop only for closed headroom, exhausted budget, or lane-identical scoop",
            },
        },
    )

    write_json(
        root / "development" / "headroom.json",
        {
            "schema_version": 1,
            "status": "MEASURED",
            "task": "held-out synthetic response prediction",
            "strongest_representation": "fixed synthetic feature representation",
            "strongest_baseline_id": "B_STRONG",
            "metric_direction": "higher",
            "baseline_value": 0.60,
            "oracle_or_upper_bound": 0.80,
            "noise_floor": 0.01,
            "minimum_claimed_margin": 0.02,
            "measured_headroom": 0.20,
            "paired_independent_unit": "synthetic specimen",
            "conclusion": "OPEN",
            "evidence_source_ids": ["S_PAPER"],
            "result_locators": ["results/baseline-comparison.json"],
        },
    )

    write_json(
        root / "development" / "iteration-ledger.json",
        {
            "schema_version": 1,
            "construction_order": [
                "recipe_parity",
                "objective_alignment",
                "data_or_representation",
                "ensemble",
                "test_time_compute",
                "architecture",
            ],
            "rungs": [
                {"name": "recipe_parity", "status": "TRIED", "evidence": "official recipe reproduced"},
                {"name": "objective_alignment", "status": "TRIED", "evidence": "objective mismatch isolated"},
                {"name": "data_or_representation", "status": "UNTRIED", "evidence": ""},
                {"name": "ensemble", "status": "UNTRIED", "evidence": ""},
                {"name": "test_time_compute", "status": "UNTRIED", "evidence": ""},
                {"name": "architecture", "status": "UNTRIED", "evidence": ""},
            ],
            "registered_candidates": [
                {
                    "candidate_id": "C1",
                    "mechanism": "objective correction",
                    "failure_node": "objective mismatch",
                    "rung": "objective_alignment",
                    "predicted_slice": "low-signal specimens",
                    "matched_control": "parameter-matched unchanged objective",
                    "falsifier": "no improvement on the frozen low-signal slice",
                },
                {
                    "candidate_id": "C2",
                    "mechanism": "training-only representation correction",
                    "failure_node": "representation mismatch",
                    "rung": "data_or_representation",
                    "predicted_slice": "context-shifted specimens",
                    "matched_control": "same objective with the fixed representation",
                    "falsifier": "no improvement on the frozen context-shift slice",
                },
            ],
            "cycles": [],
        },
    )

    write_json(
        root / "claims" / "claim-register.json",
        {
            "schema_version": 1,
            "claims": [
                {
                    "claim_id": "CL1",
                    "claim_type": "RESULT",
                    "text": "Mechanism M improves the prespecified held-out slice.",
                    "status": "SUPPORTED",
                    "disposition": "INCLUDE",
                    "scope": "synthetic-data-v1, specimen-disjoint split, synthetic score",
                    "evidence_source_ids": ["S_RESULT"],
                    "result_locators": ["results/final-comparison.json:primary"],
                    "uncertainty": "paired 95% interval [0.03, 0.07]",
                    "limitations": ["synthetic fixture only"],
                    "observed": ["paired effect 0.05"],
                    "inferred": ["the mechanism may transfer to a second context"],
                    "not_run": ["prospective biological validation"],
                }
            ],
        },
    )

    write_json(
        root / "handoff" / "handoff.json",
        {
            "schema_version": 1,
            "terminal_outcome": "MANUSCRIPT",
            "final_evaluation": {
                "status": "PASS",
                "locked_test_accesses_used": 1,
                "protocol_match": "PASS",
                "strongest_comparator_id": "B_STRONG",
                "effect_estimate": 0.05,
                "confidence_interval": [0.03, 0.07],
                "independent_unit": "synthetic specimen",
                "result_locators": ["results/final-comparison.json"],
            },
            "external_validation": {
                "status": "NOT_APPLICABLE",
                "type": "top-CS breadth is represented by the second synthetic context",
                "result_locators": [],
            },
            "specialist_handoffs": {
                "abstract": "READY",
                "statistics": "READY",
                "data_availability": "READY",
                "figures": "READY",
                "venue_manuscript": "READY",
            },
            "public_release": {
                "path": "public-release",
                "status": "AUDITED" if public_release else "NOT_STARTED",
                "allowlist": sorted(PUBLIC_RELEASE_FILES) if public_release else [],
                "artifact_paths": (
                    {
                        "source": ["src/example.py"],
                        "dependency_spec": ["requirements.txt"],
                        "example": ["examples/input.json"],
                        "data_instructions": ["docs/data.md"],
                        "run_instructions": ["README.md"],
                        "expected_outputs": ["docs/expected-output.md"],
                        "tests": ["tests/test_example.py"],
                        "license": ["LICENSE"],
                        "citation": ["CITATION.cff"],
                        "limitations": ["LIMITATIONS.md"],
                    }
                    if public_release
                    else {}
                ),
                "rehearsal": (
                    {
                        "status": "PASS",
                        "checked_on": "2026-09-04",
                        "environment": "fresh temporary Python 3.9 environment",
                        "commands": [
                            {
                                "command": "python3 -B tests/test_example.py",
                                "exit_code": 0,
                                "observed_outputs": ["Ran 2 tests", "OK"],
                            }
                        ],
                        "not_run": [],
                    }
                    if public_release
                    else {
                        "status": "NOT_RUN",
                        "checked_on": "",
                        "environment": "",
                        "commands": [],
                        "not_run": ["fresh-unpack rehearsal"],
                    }
                ),
            },
            "external_action_status": "NOT_AUTHORIZED",
            "limitations": ["No external action is authorized by this record."],
            "not_run": ["repository push", "submission"],
        },
    )
    (root / "results").mkdir(exist_ok=True)
    write_json(root / "results" / "baseline-comparison.json", {"status": "synthetic"})
    write_json(root / "results" / "final-comparison.json", {"status": "synthetic"})
    if public_release:
        for relative, text in PUBLIC_RELEASE_FILES.items():
            target = root / "public-release" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
