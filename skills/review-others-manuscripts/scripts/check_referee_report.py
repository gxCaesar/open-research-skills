#!/usr/bin/env python3
"""Check a referee report for the shapes that make it unusable to an editor.

Reads one JSON report record and prints findings as `rule_id: location`. Exits 1 when
any finding is reported.

The checks are structural. They cannot tell whether an objection is correct. They
establish that every finding is located and answerable, that severity is not inflated,
that the editor-facing recommendation matches the author-facing one, that the
confidentiality position was taken rather than assumed, and that a revision round was
judged against the manuscript rather than against the response letter.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODES = {"initial-review", "revision-round", "editorial-prescreen"}
SEVERITIES = ("fatal", "major", "minor", "taste")
HIGH = {"fatal", "major"}
RECOMMENDATIONS = {
    "accept", "minor-revision", "major-revision", "reject",
    "proceed-to-review", "return-for-missing-element", "redirect", "decline-on-scope",
}
PRESCREEN_RECOMMENDATIONS = {
    "proceed-to-review", "return-for-missing-element", "redirect", "decline-on-scope",
}
# A prescreen that judges these has answered a referee question.
REFEREE_GROUNDS = re.compile(r"\b(novel\w*|import\w*|significan\w*|correct\w*|impact\w*)\b", re.I)
REVISION_COLUMNS = ("requested", "letter_claims", "manuscript_now", "resolved")


def blank(value) -> bool:
    return value in (None, "", [], {})


def check(report: dict) -> list:
    findings = []

    mode = report.get("mode")
    if mode not in MODES:
        findings.append(("mode_not_recognised", "mode"))

    # --- confidentiality position --------------------------------------------
    if "competing_interest" not in report:
        findings.append(("competing_interest_not_declared", "competing_interest"))
    elif report.get("competing_interest") and blank(report.get("competing_interest_reason")):
        findings.append(("competing_interest_without_a_reason", "competing_interest_reason"))

    tools = report.get("external_tools")
    if tools is None:
        findings.append(("external_tool_use_not_recorded", "external_tools"))
    elif isinstance(tools, list):
        for index, tool in enumerate(tools):
            where = f"external_tools[{index}]"
            if not isinstance(tool, dict) or blank(tool.get("name")):
                findings.append(("external_tool_without_a_name", where))
            elif blank(tool.get("policy_basis")):
                findings.append(("external_tool_without_policy_basis", f"{where}.policy_basis"))

    # --- findings -------------------------------------------------------------
    items = report.get("findings")
    if not isinstance(items, list):
        items = []
        findings.append(("report_has_no_findings_list", "findings"))
    severity_counts = {name: 0 for name in SEVERITIES}
    for index, item in enumerate(items):
        where = f"findings[{index}]"
        if not isinstance(item, dict):
            findings.append(("finding_is_not_an_object", where))
            continue
        name = item.get("id", where)
        for field in ("location", "statement", "request"):
            if blank(item.get(field)):
                findings.append(("finding_missing_field", f"{name}.{field}"))
        severity = item.get("severity")
        if severity not in SEVERITIES:
            findings.append(("severity_not_recognised", f"{name}.severity"))
            continue
        severity_counts[severity] += 1
        if item.get("kind") == "taste" and severity in HIGH:
            findings.append(("taste_finding_raised_above_minor", f"{name}.severity"))
        if severity == "fatal" and blank(item.get("consequence")):
            findings.append(("fatal_finding_without_a_consequence", f"{name}.consequence"))

    # --- recommendation -------------------------------------------------------
    recommendation = report.get("recommendation")
    if recommendation not in RECOMMENDATIONS:
        findings.append(("recommendation_not_recognised", "recommendation"))
    editor = report.get("to_editor")
    if not isinstance(editor, dict) or blank(editor.get("recommendation")):
        findings.append(("editor_facing_recommendation_missing", "to_editor.recommendation"))
    elif editor.get("recommendation") != recommendation:
        findings.append(("editor_and_author_recommendations_disagree", "to_editor.recommendation"))
    if recommendation == "reject" and not any(
        isinstance(i, dict) and i.get("severity") in HIGH for i in items
    ):
        findings.append(("reject_without_a_located_high_severity_finding", "recommendation"))

    # --- mode-specific --------------------------------------------------------
    if mode == "revision-round":
        table = report.get("revision_table")
        if not isinstance(table, list) or not table:
            findings.append(("revision_table_missing", "revision_table"))
            table = []
        for index, row in enumerate(table):
            where = f"revision_table[{index}]"
            if not isinstance(row, dict):
                findings.append(("revision_row_is_not_an_object", where))
                continue
            for column in REVISION_COLUMNS:
                if column not in row:
                    findings.append(("revision_point_missing_column", f"{where}.{column}"))
            if row.get("resolved") and blank(row.get("manuscript_now")):
                findings.append(("point_closed_without_a_manuscript_change", f"{where}.manuscript_now"))

    if mode == "editorial-prescreen":
        if recommendation in RECOMMENDATIONS and recommendation not in PRESCREEN_RECOMMENDATIONS:
            findings.append(("prescreen_used_a_referee_recommendation", "recommendation"))
        grounds = report.get("grounds")
        if not isinstance(grounds, list) or not grounds:
            findings.append(("prescreen_without_grounds", "grounds"))
            grounds = []
        for index, ground in enumerate(grounds):
            where = f"grounds[{index}]"
            if not isinstance(ground, dict) or blank(ground.get("statement")):
                findings.append(("prescreen_ground_without_a_statement", where))
                continue
            if blank(ground.get("basis")):
                findings.append(("prescreen_ground_without_a_citable_basis", f"{where}.basis"))
            if REFEREE_GROUNDS.search(str(ground.get("statement"))):
                findings.append(("prescreen_judged_a_referee_question", f"{where}.statement"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"FAIL report_unreadable: {args.report} ({error})")
        print("scanned=0 failures=1")
        return 1
    findings = check(report)
    for rule, location in findings:
        print(f"FAIL {rule}: {location}")
    items = [i for i in (report.get("findings") or []) if isinstance(i, dict)]
    counts = {name: sum(1 for i in items if i.get("severity") == name) for name in SEVERITIES}
    print(
        f"scanned={len(items)} failures={len(findings)} "
        + " ".join(f"{name}={count}" for name, count in counts.items())
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
