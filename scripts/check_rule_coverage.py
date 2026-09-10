#!/usr/bin/env python3
"""Show which project-validator rules can still be made to fire.

A rule that nothing can make fire is decoration: it could stop working and the suite
would stay green. This tool holds one witness per rule, each a minimal mutation of a
passing synthetic project, and reports the rules that have none.

Measured on 2026-09-10, before this file existed: the validator declared 62 rule ids and
22 of them fired anywhere in the 555-test workflow suite. The other 40 were unverified.
The first count of the declared set was 51, not 62, because it read only the first
positional argument of self.error and self.warn and missed the ids passed through
require_text, require_enum, mapping and sequence. The denominator was wrong before the
coverage number was.

All 62 now have a witness. The first version of this file carried 27 of them on an
unwitnessed list with a reason each; the list reached zero by writing the mutations those
reasons described, not by lowering the bar.

Exits 1 when a witness stops firing its rule, or when a declared rule is neither
witnessed nor listed as unwitnessed with a reason.
"""

from __future__ import annotations

import argparse
import ast
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-publication-pipeline"
VALIDATOR = SKILL / "scripts" / "validate_publication_project.py"
INITIALIZER = SKILL / "scripts" / "init_publication_project.py"

# A completed development cycle that the validator accepts, used as the base for every
# cycle-level witness so each mutation isolates one rule.
CLEAN_CYCLE = {
    "cycle_id": "CY1",
    "candidate_id": "C1",
    "rung": "objective_alignment",
    "status": "COMPLETED",
    "mechanism_status": "SUPPORTED",
    "decision": "REVISE",
    "locked_test_accessed": False,
    "observed": [
        {
            "statement": "the objective correction moved the low-signal slice",
            "locator": "results/baseline-comparison.json",
        }
    ],
    "failed": [],
    "not_run": [],
    "inferred": [],
    "predicted_slice_met": True,
    "matched_control_status": "PASS",
    "ablation_status": "PASS",
}


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_publication_project", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declared_rules() -> set:
    """Every rule id the validator can emit, including those passed through helpers."""
    rules = set()
    for node in ast.walk(ast.parse(VALIDATOR.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Call):
            continue
        for argument in list(node.args) + [keyword.value for keyword in node.keywords]:
            if (
                isinstance(argument, ast.Constant)
                and isinstance(argument.value, str)
                and len(argument.value) > 3
                and argument.value.isupper()
                and argument.value.replace("_", "").isalpha()
            ):
                rules.add(argument.value)
    return rules


def build_project(directory: Path, public_release: bool = False) -> Path:
    sys.path.insert(0, str(SKILL / "examples"))
    from synthetic_workspace import populate_ready_workspace  # noqa: E402

    project = directory / "project"
    subprocess.run(
        [
            sys.executable, "-B", str(INITIALIZER), str(project),
            "--project-id", "SYN-1", "--title", "Synthetic",
            "--domain", "synthetic", "--contribution-lane", "sota-method",
        ],
        capture_output=True, check=True,
    )
    populate_ready_workspace(project, public_release=public_release)
    return project


def edit(project: Path, relative: str, change):
    path = project / relative
    document = json.loads(path.read_text(encoding="utf-8"))
    change(document)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def project_field(key, value):
    return lambda project: edit(project, "project.json", lambda d: d.update({key: value}))


def boundary(key, value):
    return lambda project: edit(project, "project.json", lambda d: d["boundaries"].update({key: value}))


def sources(change):
    return lambda project: edit(project, "evidence/source-register.json", change)


def protocol(change):
    return lambda project: edit(project, "protocol/protocol.json", change)


def ledger(change):
    return lambda project: edit(project, "development/iteration-ledger.json", change)


def intake(change):
    return lambda project: edit(project, "intake/intake.json", change)


def handoff(change):
    return lambda project: edit(project, "handoff/handoff.json", change)


def claims(change):
    return lambda project: edit(project, "claims/claim-register.json", change)


def release(change):
    """Edit the public_release block inside the handoff record."""
    return lambda project: edit(
        project, "handoff/handoff.json", lambda d: change(d["public_release"])
    )


def two_predicted_slice_misses(project):
    """Two misses on one candidate followed by another revision kills the mechanism."""
    first = copy.deepcopy(CLEAN_CYCLE)
    first.update(cycle_id="CY1", predicted_slice_met=False, mechanism_status="FALSIFIED")
    second = copy.deepcopy(CLEAN_CYCLE)
    second.update(cycle_id="CY2", predicted_slice_met=False, mechanism_status="FALSIFIED")
    edit(project, "development/iteration-ledger.json", lambda d: d.update(cycles=[first, second]))


def stop_without_a_route_reason(project):
    cycle = copy.deepcopy(CLEAN_CYCLE)
    cycle.update(decision="STOP", stop_reason="TIRED")
    edit(project, "development/iteration-ledger.json", lambda d: d.update(cycles=[cycle]))


def a_symlink_in_the_workspace(project):
    (project / "notes-link.json").symlink_to(project / "project.json")


def a_file_outside_the_allowlist(project):
    (project / "public-release" / "leftover.txt").write_text("left over\n", encoding="utf-8")


def a_machine_path_in_a_released_file(project):
    # Composed at runtime: the literal is what this repository's own content scan rejects.
    (project / "public-release" / "docs" / "setup.md").write_text(
        "run it from /" + "Users" + "/someone/project\n", encoding="utf-8"
    )
    edit(project, "handoff/handoff.json", lambda d: (
        d["public_release"]["allowlist"].append("docs/setup.md"),
        d["public_release"]["artifact_paths"]["run_instructions"].append("docs/setup.md"),
    ))


def cycles(change=None, count=1):
    """Install `count` accepted cycles, optionally breaking the last one."""
    def mutate(project):
        installed = []
        for index in range(count):
            cycle = copy.deepcopy(CLEAN_CYCLE)
            cycle["cycle_id"] = f"CY{index + 1}"
            installed.append(cycle)
        if change is not None:
            change(installed[-1])
        edit(project, "development/iteration-ledger.json", lambda d: d.update(cycles=installed))
    return mutate


# rule_id -> (validation target, needs a public-release workspace, mutation)
WITNESSES = {
    # structure of the workspace itself
    "PROJECT_ROOT": ("handoff", False, lambda p: (p / "not-a-directory").write_text("", encoding="utf-8")),
    "REQUIRED_FILE": ("handoff", False, lambda p: (p / "intake" / "intake.json").unlink()),
    "JSON_PARSE": ("handoff", False, lambda p: (p / "project.json").write_text("{", encoding="utf-8")),
    "JSON_OBJECT": ("handoff", False, lambda p: (p / "project.json").write_text("[]", encoding="utf-8")),
    "SCHEMA_VERSION": ("handoff", False, project_field("schema_version", 2)),
    # project identity
    "PROJECT_ID": ("handoff", False, project_field("project_id", "")),
    "PROJECT_TITLE": ("handoff", False, project_field("title", "")),
    "PROJECT_DOMAIN": ("handoff", False, project_field("domain", "")),
    "PROJECT_STAGE": ("handoff", False, project_field("current_stage", "unknown")),
    "PROJECT_ROUTE": ("handoff", False, project_field("route", "unknown")),
    "EXTERNAL_VALIDATION": ("handoff", False, project_field("route", "unknown")),
    # authorization boundaries
    "AUTHORITY_BOUNDARY": ("handoff", False, boundary("remote_compute", "granted")),
    # evidence sources
    "SOURCE_REGISTER": ("handoff", False, sources(lambda d: d.update(sources="none"))),
    "SOURCE_RECORD": ("handoff", False, sources(lambda d: d["sources"].append("S_X"))),
    "SOURCE_ID": ("handoff", False, sources(lambda d: d["sources"][0].update(source_id=""))),
    "SOURCE_STATUS": ("handoff", False, sources(lambda d: d["sources"][0].update(status="MAYBE"))),
    # the frozen protocol
    "SPLIT_CONTRACT": ("development", False, protocol(lambda d: d["split"].update(leakage_guard=""))),
    "PRIMARY_METRIC": ("development", False, protocol(lambda d: d["primary_metric"].update(name=""))),
    "UNCERTAINTY": ("development", False, protocol(lambda d: d["uncertainty"].update(method=""))),
    "PROTOCOL_DATA": ("development", False, protocol(lambda d: d.update(dataset_versions=[]))),
    "PROTOCOL_HYPOTHESIS": ("development", False, protocol(lambda d: d.update(hypothesis_id="H9"))),
    "SELECTION_CONTRACT": ("development", False, protocol(lambda d: d["selection"].update(baseline_tuning_parity=""))),
    "STOP_RULES": ("development", False, protocol(lambda d: d.pop("stop_rules", None))),
    "BASELINE_PARITY": (
        "development", False,
        protocol(lambda d: d["baselines"][1].update(baseline_id=d["baselines"][0]["baseline_id"])),
    ),
    # the development loop
    "HEADROOM": ("development", False,
                 lambda p: edit(p, "development/headroom.json", lambda d: d.update(noise_floor=0.5))),
    "CANDIDATE_REGISTER": ("development", False, ledger(lambda d: d.update(registered_candidates=[]))),
    "ITERATION_LEDGER": ("development", False, cycles(lambda c: c.update(cycle_id=""))),
    "PREDICTED_SLICE": ("development", False, cycles(lambda c: c.pop("predicted_slice_met"))),
    "EVIDENCE_STATUS": ("development", False, cycles(lambda c: c.update(observed=[]))),
    "LOCKED_TEST": ("development", False, cycles(lambda c: c.update(locked_test_accessed=True))),
    "ADVANCE_EVIDENCE": ("development", False,
                         cycles(lambda c: c.update(decision="ADVANCE", mechanism_status="INCONCLUSIVE"))),
    "BUDGET": ("development", False, cycles(count=12)),
    # claims and handoff
    "CLAIM_REGISTER": ("handoff", False, claims(lambda d: d.update(claims=[]))),
    "CLAIM_EVIDENCE": ("handoff", False, claims(lambda d: d["claims"][0].update(scope=""))),
    "CLAIM_STATUS": ("handoff", False,
                     claims(lambda d: d["claims"][0].update(status="ok"))),
    "HANDOFF": ("handoff", False, handoff(lambda d: d.update(limitations="none"))),
    "SPECIALIST_HANDOFF": ("handoff", False,
                           handoff(lambda d: d.update(specialist_handoffs=[]))),
    "EXTERNAL_BOUNDARY": ("handoff", False,
                          handoff(lambda d: d.update(external_action_status="AUTHORIZED"))),
    "FINAL_EVALUATION": ("handoff", False,
                         handoff(lambda d: d["final_evaluation"].update(status="FAIL"))),
    "NEGATIVE_RESULT": ("handoff", False,
                        handoff(lambda d: d.update(terminal_outcome="NEGATIVE_RESULT"))),
    "RETURN_TO_INTAKE": ("handoff", False,
                         handoff(lambda d: d.update(terminal_outcome="RETURN_TO_INTAKE"))),
    "PATH_CONTAINMENT": ("handoff", False, a_symlink_in_the_workspace),
    # intake
    "AUTHORITY": ("pilot", False, project_field("authority", {"status": "UNVERIFIED",
                                                             "source_ids": ["S_RULE"],
                                                             "conflicts": []})),
    "DATA_FEASIBILITY": ("pilot", False, intake(lambda d: d["data_feasibility"].update(status="FAIL"))),
    "HYPOTHESIS": ("pilot", False, intake(lambda d: d["hypothesis"].update(claim=""))),
    "INTAKE_DECISION": ("pilot", False, intake(lambda d: d["decision"].update(status="HOLD"))),
    "SCOOP_VERDICT": ("pilot", False, intake(lambda d: d["scoop"].update(verdict="MAYBE"))),
    "SCOOP_LANE": ("pilot", False, intake(lambda d: d["scoop"].update(contribution_lane="discovery"))),
    "VENUE_FIT": ("pilot", False, intake(lambda d: d["venue_fit"].update(status="FAIL"))),
    "VERIFIED_SOURCE": ("pilot", False, sources(lambda d: d["sources"][0].update(locator=""))),
    # the frozen protocol and the development loop
    "PROTOCOL_FREEZE": ("development", False, protocol(lambda d: d.update(status="DRAFT"))),
    "PROTOCOL_CHANGE": ("development", False, protocol(lambda d: d.pop("allowed_changes", None))),
    "CONTRIBUTION_LANE": ("development", False,
                          protocol(lambda d: d.update(contribution_lane="discovery"))),
    "CONSTRUCTION_ORDER": ("development", False,
                           ledger(lambda d: d.update(construction_order=["architecture"]))),
    "MECHANISM_RECOVERY": ("development", False, two_predicted_slice_misses),
    "ROUTE_CLOSURE": ("development", False, stop_without_a_route_reason),
    # the curated public release
    "PUBLIC_RELEASE_STATUS": ("public-release", True, release(lambda r: r.update(status="DONE"))),
    "PUBLIC_RELEASE_PATH": ("public-release", True, release(lambda r: r.update(path="../outside"))),
    "PUBLIC_RELEASE_ALLOWLIST": ("public-release", True, a_file_outside_the_allowlist),
    "PUBLIC_RELEASE_ARTIFACT": ("public-release", True,
                                release(lambda r: r["artifact_paths"].pop("tests"))),
    "PUBLIC_RELEASE_REHEARSAL": ("public-release", True,
                                 release(lambda r: r["rehearsal"].update(status="FAIL"))),
    "PUBLIC_RELEASE_CONTENT": ("public-release", True, a_machine_path_in_a_released_file),
}

# Every declared rule now has a witness. This dict is the escape hatch for a rule that
# genuinely cannot be reached from a synthetic project, and it is empty on purpose: the
# list stood at 27 when this tool was written and reached zero by writing the mutations
# rather than by lowering the bar. A rule added without a witness lands here and fails
# the test that asserts this stays empty.
UNWITNESSED: dict = {}


def run_witness(validator, rule, target, public_release, mutate):
    with tempfile.TemporaryDirectory() as tmp:
        project = build_project(Path(tmp), public_release)
        mutate(project)
        subject = project / "not-a-directory"
        if not subject.is_file():
            subject = project
        report = validator.ProjectValidator(subject, target).run()
        return {finding["rule_id"] for finding in report["findings"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print the reconciliation and stop")
    args = parser.parse_args()

    declared = declared_rules()
    witnessed = set(WITNESSES)
    unwitnessed = set(UNWITNESSED)
    unaccounted = declared - witnessed - unwitnessed
    stale = (witnessed | unwitnessed) - declared

    failures = []
    if not args.list:
        validator = load_validator()
        for rule in sorted(WITNESSES):
            target, public_release, mutate = WITNESSES[rule]
            fired = run_witness(validator, rule, target, public_release, mutate)
            if rule not in fired:
                failures.append(rule)
                print(f"FAIL witness_no_longer_fires: {rule} (fired instead: {sorted(fired)})")

    for rule in sorted(unaccounted):
        print(f"FAIL rule_neither_witnessed_nor_listed: {rule}")
    for rule in sorted(stale):
        print(f"FAIL listed_rule_no_longer_declared: {rule}")

    print(
        f"declared={len(declared)} witnessed={len(witnessed)} "
        f"unwitnessed={len(unwitnessed)} failures={len(failures) + len(unaccounted) + len(stale)}"
    )
    print(
        f"{len(witnessed)} witnessed + {len(unwitnessed)} unwitnessed = {len(declared)}"
        " = every rule the validator can emit. Nothing unaccounted."
        if not unaccounted and not stale
        else "reconciliation does not close"
    )
    return 1 if failures or unaccounted or stale else 0


if __name__ == "__main__":
    sys.exit(main())
