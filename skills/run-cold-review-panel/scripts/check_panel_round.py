#!/usr/bin/env python3
"""Check one cold-review round for the things that make a panel worthless.

Reads one JSON round record and reports findings as `rule_id: location`. Exits 1 when
any finding is reported.

The checks are structural. They cannot tell whether a finding is correct. What they
establish is that the isolation was recorded as an observation rather than as a
reviewer's statement about itself, that somebody actually executed the artifact, that
every finding reached adjudication, and that the round does not claim to predict a
decision it cannot see.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LENSES = {
    "claim-support",
    "method-correctness",
    "comparison-fairness",
    "reproducibility",
    "significance",
}
STATES = {"confirmed", "unsupported", "underdetermined"}
# Material that repairs a reviewer's misreading before it can be observed.
INTERNAL = re.compile(
    r"(plan|charter|survey|ledger|postmortem|correspondence|response|draft-v\d|"
    r"internal|meta-review|previous-round)",
    re.IGNORECASE,
)
# A model describing its own inputs produces a description, not an observation.
SELF_REPORT = re.compile(
    r"\b(reviewers?|models?|agents?|panel)\b[^.]{0,24}?"
    r"\b(stat\w*|say\w*|said|claim\w*|report\w*|assert\w*|confirm\w*|told)\b",
    re.IGNORECASE,
)


def blank(value) -> bool:
    return value in (None, "", [], {})


def check(record: dict) -> list:
    findings = []

    # --- isolation ------------------------------------------------------------
    manifest = record.get("isolation_manifest")
    if not isinstance(manifest, list) or not manifest:
        findings.append(("isolation_manifest_missing", "isolation_manifest"))
        manifest = []
    for index, entry in enumerate(manifest):
        where = f"isolation_manifest[{index}]"
        if not isinstance(entry, dict) or blank(entry.get("path")):
            findings.append(("manifest_entry_without_a_path", where))
            continue
        if entry.get("bytes") is None:
            findings.append(("manifest_entry_without_a_size", f"{where}.bytes"))
        if INTERNAL.search(str(entry.get("path"))):
            findings.append(("manifest_contains_internal_material", f"{where}:{entry['path']}"))

    evidence = record.get("isolation_evidence")
    if blank(evidence):
        findings.append(("isolation_evidence_not_recorded", "isolation_evidence"))
    elif SELF_REPORT.search(str(evidence)):
        findings.append(("isolation_evidence_is_self_report", "isolation_evidence"))

    # --- reviewers ------------------------------------------------------------
    reviewers = record.get("reviewers")
    if not isinstance(reviewers, list) or not reviewers:
        findings.append(("round_has_no_reviewers", "reviewers"))
        reviewers = []

    seen_lenses = set()
    finding_ids = []
    executed = 0
    for index, reviewer in enumerate(reviewers):
        where = f"reviewers[{index}]"
        if not isinstance(reviewer, dict):
            findings.append(("reviewer_is_not_an_object", where))
            continue
        name = reviewer.get("id", where)
        lens = reviewer.get("lens")
        if lens not in LENSES:
            findings.append(("lens_not_recognised", f"{name}.lens"))
        else:
            seen_lenses.add(lens)
        if blank(reviewer.get("model_family")):
            findings.append(("model_family_not_recorded", f"{name}.model_family"))

        reviewer_findings = reviewer.get("findings")
        if not isinstance(reviewer_findings, list) or not reviewer_findings:
            findings.append(("reviewer_reported_no_findings", f"{name}.findings"))
            reviewer_findings = []
        for position, item in enumerate(reviewer_findings):
            spot = f"{name}.findings[{position}]"
            if not isinstance(item, dict):
                findings.append(("finding_is_not_an_object", spot))
                continue
            if blank(item.get("id")):
                findings.append(("finding_without_an_id", spot))
            else:
                finding_ids.append(item["id"])
            for field in ("location", "statement", "would_resolve"):
                if blank(item.get(field)):
                    findings.append(("finding_missing_field", f"{spot}.{field}"))

        if reviewer.get("executed_artifact"):
            executed += 1
            commands = reviewer.get("commands")
            if not isinstance(commands, list) or not commands:
                findings.append(("execution_claimed_without_commands", f"{name}.commands"))
                commands = []
            for position, command in enumerate(commands):
                spot = f"{name}.commands[{position}]"
                if not isinstance(command, dict) or blank(command.get("command")):
                    findings.append(("command_without_a_command_line", spot))
                elif "output" not in command:
                    findings.append(("command_without_recorded_output", f"{spot}.output"))

    for lens in sorted(LENSES - seen_lenses):
        findings.append(("lens_not_covered", f"reviewers:{lens}"))
    if reviewers and executed == 0:
        findings.append(("no_reviewer_executed_the_artifact", "reviewers"))

    # --- adjudication ---------------------------------------------------------
    meta = record.get("meta_review")
    if not isinstance(meta, dict):
        findings.append(("meta_review_missing", "meta_review"))
        meta = {}
    if "acceptance_probability" in meta:
        findings.append(("acceptance_probability_reported", "meta_review.acceptance_probability"))

    adjudication = meta.get("adjudication")
    if not isinstance(adjudication, list):
        adjudication = []
    adjudicated = {}
    for index, row in enumerate(adjudication):
        where = f"meta_review.adjudication[{index}]"
        if not isinstance(row, dict) or blank(row.get("finding")):
            findings.append(("adjudication_row_without_a_finding", where))
            continue
        state = row.get("state")
        if state not in STATES:
            findings.append(("adjudication_state_not_recognised", f"{where}.state"))
            continue
        adjudicated[row["finding"]] = row
        if state == "confirmed" and blank(row.get("repair")):
            findings.append(("confirmed_finding_without_a_repair", f"{where}.repair"))

    for identifier in finding_ids:
        if identifier not in adjudicated:
            findings.append(("finding_not_adjudicated", f"meta_review:{identifier}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("round_record", type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.round_record.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"FAIL round_unreadable: {args.round_record} ({error})")
        print("scanned=0 failures=1")
        return 1
    findings = check(record)
    for rule, location in findings:
        print(f"FAIL {rule}: {location}")
    reviewers = record.get("reviewers") or []
    total = sum(len(r.get("findings") or []) for r in reviewers if isinstance(r, dict))
    executed = sum(1 for r in reviewers if isinstance(r, dict) and r.get("executed_artifact"))
    print(
        f"scanned={len(reviewers)} failures={len(findings)} "
        f"reported_findings={total} executed_artifact={executed} "
        f"manifest_entries={len(record.get('isolation_manifest') or [])}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
