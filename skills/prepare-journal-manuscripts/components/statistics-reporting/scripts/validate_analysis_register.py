#!/usr/bin/env python3
"""Validate a claim-to-analysis register without choosing statistical methods."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


UNRESOLVED = re.compile(
    r"(?:AUTHOR_INPUT_NEEDED|\bTBD\b|\bTODO\b|"
    r"\[(?:replace|insert|unknown|required|test|model|unit|value|version)[^\]]*\])",
    re.I,
)
DEPENDENT_DESIGNS = {"paired", "repeated", "nested", "mixed"}
STOCHASTIC_FIELDS = {
    "seed_role",
    "aggregation_unit",
    "checkpoint_rule",
    "early_stopping_rule",
    "comparison_budget",
    "selection_rule",
}


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    parser.add_argument("--mode", choices=["working", "final"], default="working")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args(argv)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add(
    findings: List[Dict[str, Any]],
    rule_id: str,
    severity: str,
    location: str,
    message: str,
) -> None:
    findings.append(
        {
            "rule_id": rule_id,
            "severity": severity,
            "location": location,
            "message": message,
        }
    )


def unresolved_values(value: Any, location: str = "$") -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            results.extend(unresolved_values(item, f"{location}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            results.extend(unresolved_values(item, f"{location}[{index}]"))
    elif isinstance(value, str) and UNRESOLVED.search(value):
        results.append((location, value))
    return results


def validate(payload: Any, mode: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    if not isinstance(payload, dict):
        add(findings, "ROOT_OBJECT", "error", "$", "The register must be a JSON object.")
        return findings
    if payload.get("schema_version") != 1:
        add(findings, "SCHEMA_VERSION", "error", "schema_version", "schema_version must be 1.")
    if not text(payload.get("study_id")):
        add(findings, "STUDY_ID", "error", "study_id", "study_id must be non-empty text.")
    analyses = payload.get("analyses")
    if not isinstance(analyses, list) or not analyses:
        add(findings, "ANALYSES", "error", "analyses", "analyses must be a non-empty list.")
        analyses = []

    observed_ids = set()
    required_text = (
        "analysis_id",
        "claim",
        "endpoint",
        "comparison",
        "independent_unit",
        "paired_or_repeated",
        "dependence_handling",
        "model_or_test",
        "assumptions_and_diagnostics",
        "comparison_family",
        "multiplicity_strategy",
        "effect_estimate",
        "uncertainty",
        "p_value_policy",
        "exclusion_timing",
    )
    for index, analysis in enumerate(analyses):
        base = f"analyses[{index}]"
        if not isinstance(analysis, dict):
            add(findings, "ANALYSIS_OBJECT", "error", base, "Each analysis must be an object.")
            continue
        for key in required_text:
            if not text(analysis.get(key)):
                rule = "INDEPENDENT_UNIT" if key == "independent_unit" else "REQUIRED_FIELD"
                add(findings, rule, "error", f"{base}.{key}", f"{key} must be non-empty text.")
        analysis_id = analysis.get("analysis_id")
        if text(analysis_id):
            if analysis_id in observed_ids:
                add(findings, "DUPLICATE_ID", "error", f"{base}.analysis_id", "analysis_id must be unique.")
            observed_ids.add(analysis_id)

        hierarchy = analysis.get("hierarchy")
        if not isinstance(hierarchy, list) or not hierarchy or any(not text(item) for item in hierarchy):
            add(findings, "ANALYSIS_HIERARCHY", "error", f"{base}.hierarchy", "hierarchy must name each sampling or measurement level.")

        n_by_group = analysis.get("n_by_group")
        if (
            not isinstance(n_by_group, dict)
            or not n_by_group
            or any(
                not text(group)
                or not isinstance(count, int)
                or isinstance(count, bool)
                or count < 1
                for group, count in n_by_group.items()
            )
        ):
            add(
                findings,
                "GROUP_DENOMINATORS",
                "error",
                f"{base}.n_by_group",
                "n_by_group must give a positive independent-unit count for each compared group or condition.",
            )

        included = analysis.get("included_units")
        skipped = analysis.get("skipped_units")
        if not isinstance(included, int) or isinstance(included, bool) or included < 1:
            add(findings, "DENOMINATOR", "error", f"{base}.included_units", "included_units must be a positive integer.")
        if not isinstance(skipped, int) or isinstance(skipped, bool) or skipped < 0:
            add(findings, "DENOMINATOR", "error", f"{base}.skipped_units", "skipped_units must be a non-negative integer.")
        reasons = analysis.get("skip_reasons")
        if not isinstance(reasons, list) or any(not text(item) for item in reasons):
            add(findings, "SKIP_ACCOUNTING", "error", f"{base}.skip_reasons", "skip_reasons must be a list of non-empty strings.")
        elif isinstance(skipped, int) and skipped > 0 and not reasons:
            add(findings, "SKIP_ACCOUNTING", "error", f"{base}.skip_reasons", "Every skipped unit needs a reason.")
        elif skipped == 0 and reasons:
            add(findings, "SKIP_ACCOUNTING", "warning", f"{base}.skip_reasons", "Reasons are listed although skipped_units is zero.")

        design = str(analysis.get("paired_or_repeated", "")).casefold()
        if design in DEPENDENT_DESIGNS and not text(analysis.get("dependence_handling")):
            add(findings, "DEPENDENCE_HANDLING", "error", f"{base}.dependence_handling", "Dependent observations require an explicit analysis treatment.")
        if analysis.get("interaction_claim") is True and not text(analysis.get("interaction_test")):
            add(findings, "INTERACTION_TEST", "error", f"{base}.interaction_test", "An interaction claim requires a direct interaction analysis.")

        if analysis.get("computational_stochastic") is True:
            stochastic = analysis.get("stochastic_design")
            if not isinstance(stochastic, dict):
                add(findings, "STOCHASTIC_SELECTION", "error", f"{base}.stochastic_design", "A stochastic analysis requires its run-selection contract.")
            else:
                missing = sorted(key for key in STOCHASTIC_FIELDS if not text(stochastic.get(key)))
                if missing:
                    add(
                        findings,
                        "STOCHASTIC_SELECTION",
                        "error",
                        f"{base}.stochastic_design",
                        "Missing stochastic design fields: " + ", ".join(missing) + ".",
                    )

        sources = analysis.get("sources")
        if not isinstance(sources, list) or not sources or any(not text(item) for item in sources):
            add(findings, "SOURCE_POINTER", "error", f"{base}.sources", "Each analysis needs at least one manuscript or protocol pointer.")

    unresolved_severity = "error" if mode == "final" else "warning"
    for location, _ in unresolved_values(payload):
        add(
            findings,
            "UNRESOLVED_FIELD",
            unresolved_severity,
            location,
            "Replace or explicitly resolve this placeholder before final mode.",
        )
    return findings


def report(payload: Any, mode: str, target: Path) -> Dict[str, Any]:
    findings = validate(payload, mode)
    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "tool": "validate_analysis_register.py",
        "target": str(target.resolve()),
        "mode": mode,
        "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "limitations": [
            "Schema validity does not establish that a statistical method is appropriate.",
            "The tool does not read raw data, recompute results, or verify manuscript claims.",
        ],
    }


def render_markdown(result: Dict[str, Any]) -> str:
    lines = [
        "# Analysis-register validation",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {result['errors']}",
        f"- Warnings: {result['warnings']}",
    ]
    for item in result["findings"]:
        lines.append(
            f"- [{item['severity']}] `{item['rule_id']}` at `{item['location']}`: {item['message']}"
        )
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        payload = json.loads(args.register.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    result = report(payload, args.mode, args.register)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
