#!/usr/bin/env python3
"""Check an exploratory iteration ledger for the claims it is not entitled to make.

Reads one JSON ledger and reports findings as `rule_id: location`. Exits 1 when any
finding is reported. The checks are mechanical; none of them establishes that a
component works, only that the ledger does not assert more than it recorded.

Construction shapes are compared after case, punctuation and spacing are removed, so
a rename is caught and a rephrasing is not. Semantic deduplication stays with the
author; the checker only enforces that a repeat was acknowledged.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "id",
    "order",
    "construction_shape",
    "mechanism",
    "predicted_slice",
    "treatment",
    "control",
    "verdict",
)
VERDICTS = {"supported", "void", "inconclusive"}
ORDERS = range(1, 7)
EXITS = {1, 2, 3}


def normalise(shape: str) -> str:
    """Collapse a construction shape so that renaming alone does not create a new one."""
    return " ".join(re.sub(r"[^a-z0-9]+", " ", shape.casefold()).split())


def seeds_of(arm: Any) -> list:
    return list(arm.get("seeds", [])) if isinstance(arm, dict) else []


def check(ledger: dict) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    iterations = ledger.get("iterations")
    if not isinstance(iterations, list) or not iterations:
        return [("ledger_has_no_iterations", "iterations")]

    killed: dict[str, str] = {}
    order_six: list[str] = []
    lower_orders: set[int] = set()

    for index, entry in enumerate(iterations):
        where = f"iterations[{index}]"
        if not isinstance(entry, dict):
            findings.append(("iteration_is_not_an_object", where))
            continue
        name = entry.get("id", where)

        for field in REQUIRED_FIELDS:
            if entry.get(field) in (None, "", [], {}):
                findings.append(("iteration_missing_field", f"{name}.{field}"))

        order = entry.get("order")
        if order not in ORDERS:
            findings.append(("order_out_of_range", f"{name}.order"))
        elif order == 6:
            order_six.append(name)
        else:
            lower_orders.add(order)

        verdict = entry.get("verdict")
        if verdict is not None and verdict not in VERDICTS:
            findings.append(("verdict_not_recognised", f"{name}.verdict"))

        treatment_seeds = seeds_of(entry.get("treatment"))
        control_seeds = seeds_of(entry.get("control"))
        if verdict == "void" and (len(treatment_seeds) < 2 or len(control_seeds) < 2):
            findings.append(("void_from_single_seed", f"{name}.verdict"))

        if entry.get("control") is not None and not isinstance(entry.get("control"), dict):
            findings.append(("control_is_not_an_arm", f"{name}.control"))

        shape = normalise(str(entry.get("construction_shape", "")))
        if shape and shape in killed and not entry.get("differs_from_prior"):
            findings.append(("construction_shape_repeats_a_kill", f"{name}.construction_shape"))
        if shape and verdict == "void":
            killed.setdefault(shape, name)

    if len(order_six) > 1 and len(lower_orders) < 2:
        findings.append(("architecture_before_lower_orders", f"iterations:{order_six[1]}"))

    exit_claim = ledger.get("exit")
    if exit_claim is not None:
        if exit_claim.get("number") not in EXITS:
            findings.append(("exit_not_recognised", "exit.number"))
        elif exit_claim.get("number") == 1:
            for field in ("headroom", "noise_floor", "oracle_arm"):
                if exit_claim.get(field) in (None, "", [], {}):
                    findings.append(("saturation_exit_without_measurement", f"exit.{field}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"FAIL ledger_unreadable: {args.ledger} ({error})")
        print("scanned=0 failures=1")
        return 1
    findings = check(ledger)
    for rule, location in findings:
        print(f"FAIL {rule}: {location}")
    scanned = len(ledger.get("iterations") or [])
    print(f"scanned={scanned} failures={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
