#!/usr/bin/env python3
"""Check a survey and novelty ledger for claims it did not earn.

Reads one JSON ledger and reports findings as `rule_id: location`. Exits 1 when any
finding is reported.

The checks are arithmetic and structural. None of them decides whether a direction is
novel; they establish that the disposition arithmetic closes, that a kill names the layer
it lands on, and that a stop recommendation is attributed to the verdict that produced it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LANES = {"discovery", "sota-method", "benchmark"}
LANE_FIELDS = {
    "discovery": ("falsifier",),
    "sota-method": ("task", "second_axis"),
    "benchmark": ("named_gap", "why_existing_suites_miss_it"),
}
DISPOSITIONS = {"identical", "adjacent", "irrelevant", "uncertain"}
LAYERS = {"framing", "data", "task"}
EMPTY_MOVES = {"widen", "relax", "assemble", "stop"}
MINIMUM_ANGLES = 6


def path_free_exception_summary(error: BaseException) -> str:
    """Describe a read failure without repeating the caller's absolute path."""
    if isinstance(error, json.JSONDecodeError):
        return f"invalid JSON at line {error.lineno}, column {error.colno}"
    if isinstance(error, OSError):
        return f"{type(error).__name__}: {error.strerror}" if error.strerror else type(error).__name__
    return type(error).__name__


def blank(value) -> bool:
    return value in (None, "", [], {})


def check(ledger: dict) -> list:
    findings = []

    lane = ledger.get("contribution_lane")
    if blank(lane):
        findings.append(("lane_not_declared", "contribution_lane"))
    elif lane not in LANES:
        findings.append(("lane_not_recognised", "contribution_lane"))
    else:
        for field in LANE_FIELDS[lane]:
            if blank(ledger.get(field)):
                findings.append(("lane_required_field_missing", f"{lane}.{field}"))

    # --- joint random-variable audit -----------------------------------------
    joint = ledger.get("joint_variable_audit")
    if not isinstance(joint, list) or not joint:
        findings.append(("joint_variable_audit_missing", "joint_variable_audit"))
        joint = []
    for index, row in enumerate(joint):
        where = f"joint_variable_audit[{index}]"
        if not isinstance(row, dict):
            findings.append(("joint_row_is_not_an_object", where))
            continue
        for field in ("source", "release", "checked_on", "joint_count"):
            if blank(row.get(field)) and row.get(field) != 0:
                findings.append(("joint_row_missing_field", f"{where}.{field}"))
        if row.get("joint_count") == 0 and row.get("disposition") not in EMPTY_MOVES:
            findings.append(("empty_intersection_without_next_move", f"{where}.disposition"))

    # --- search angles --------------------------------------------------------
    angles = ledger.get("search_angles")
    if not isinstance(angles, list):
        angles = []
    if len(angles) < MINIMUM_ANGLES:
        findings.append(("too_few_search_angles", f"search_angles:{len(angles)}"))
    for index, angle in enumerate(angles):
        where = f"search_angles[{index}]"
        if not isinstance(angle, dict) or blank(angle.get("framing")):
            findings.append(("angle_missing_framing", where))
        elif "result" not in angle:
            findings.append(("angle_without_recorded_result", f"{where}.result"))
    if angles and not any(
        isinstance(a, dict) and a.get("adversarial") for a in angles
    ):
        findings.append(("no_adversarial_angle", "search_angles"))

    # --- candidates and the disposition ledger --------------------------------
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        findings.append(("ledger_has_no_candidates", "candidates"))
        candidates = []
    kills = []
    for index, entry in enumerate(candidates):
        where = f"candidates[{index}]"
        if not isinstance(entry, dict):
            findings.append(("candidate_is_not_an_object", where))
            continue
        name = entry.get("id", where)
        if blank(entry.get("identifier")):
            findings.append(("candidate_missing_identifier", f"{name}.identifier"))
        disposition = entry.get("disposition")
        if blank(disposition):
            findings.append(("candidate_missing_disposition", f"{name}.disposition"))
            continue
        if disposition not in DISPOSITIONS:
            findings.append(("disposition_not_recognised", f"{name}.disposition"))
            continue
        if disposition == "identical":
            kills.append(name)
            layer = entry.get("kill_layer")
            if blank(layer):
                findings.append(("kill_without_layer", f"{name}.kill_layer"))
            elif layer not in LAYERS:
                findings.append(("kill_layer_not_recognised", f"{name}.kill_layer"))
            elif layer == "task":
                for field in ("headroom", "noise_floor"):
                    if blank(entry.get(field)):
                        findings.append(("task_layer_kill_without_measurement", f"{name}.{field}"))
            elif layer == "data" and blank(entry.get("sources_checked")):
                findings.append(("data_layer_kill_without_enumerated_sources", f"{name}.sources_checked"))

    declared_total = ledger.get("candidates_examined")
    if declared_total is not None and declared_total != len(candidates):
        findings.append(("disposition_denominator_open", "candidates_examined"))

    # --- verdicts -------------------------------------------------------------
    scoop = ledger.get("scoop_verdict")
    if scoop not in {"IDENTICAL", "ADJACENT", "UNCERTAIN"}:
        findings.append(("scoop_verdict_not_recognised", "scoop_verdict"))
    if scoop == "IDENTICAL" and not kills:
        findings.append(("scoop_kill_without_an_identical_candidate", "scoop_verdict"))

    venue = ledger.get("venue_fit")
    if not isinstance(venue, dict) or blank(venue.get("reason")):
        findings.append(("venue_fit_not_recorded_separately", "venue_fit"))
    elif venue.get("recommendation") == "stop" and scoop != "IDENTICAL" and blank(
        venue.get("owner")
    ):
        findings.append(("venue_fit_stop_without_an_owner", "venue_fit.owner"))

    # --- repair table over one's own kills ------------------------------------
    if kills:
        repair = ledger.get("repair_table")
        if not isinstance(repair, list) or not repair:
            findings.append(("repair_table_missing", "repair_table"))
        else:
            covered = {row.get("kill") for row in repair if isinstance(row, dict)}
            for name in kills:
                if name not in covered:
                    findings.append(("kill_absent_from_repair_table", f"repair_table:{name}"))
            for index, row in enumerate(repair):
                if isinstance(row, dict) and "reversible" not in row:
                    findings.append(("repair_row_without_a_verdict", f"repair_table[{index}].reversible"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"FAIL ledger_unreadable: {args.ledger.name} "
              f"({path_free_exception_summary(error)})")
        print("scanned=0 failures=1")
        return 1
    findings = check(ledger)
    for rule, location in findings:
        print(f"FAIL {rule}: {location}")
    candidates = ledger.get("candidates") or []
    angles = ledger.get("search_angles") or []
    sources = ledger.get("joint_variable_audit") or []
    breakdown = {name: 0 for name in sorted(DISPOSITIONS)}
    for entry in candidates:
        if isinstance(entry, dict) and entry.get("disposition") in breakdown:
            breakdown[entry["disposition"]] += 1
    print(
        f"scanned={len(candidates)} failures={len(findings)} "
        f"angles={len(angles)} sources={len(sources)} "
        + " ".join(f"{name}={count}" for name, count in breakdown.items())
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
