#!/usr/bin/env python3
"""Validate dataset-to-claim and availability-route records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


ROUTES = {
    "public_repository",
    "controlled_access",
    "within_paper_or_supplement",
    "reused_public",
    "third_party_restricted",
    "justified_request",
    "not_applicable",
}
ORIGINS = {"generated", "reused", "third_party", "mixed", "none"}
UNRESOLVED = re.compile(
    r"(?:AUTHOR_INPUT_NEEDED|\bTBD\b|\bTODO\b|"
    r"\[(?:replace|insert|unknown|required|repository|identifier|accession|doi|"
    r"licen[cs]e|reason|contact|version|file|dataset|journal|article)[^\]]*\])",
    re.I,
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--mode", choices=["working", "final"], default="working")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args(argv)


def path_free_exception_summary(error: BaseException) -> str:
    """Describe a read failure without repeating the caller's absolute path."""
    if isinstance(error, json.JSONDecodeError):
        return f"invalid JSON at line {error.lineno}, column {error.colno}"
    if isinstance(error, OSError):
        return f"{type(error).__name__}: {error.strerror}" if error.strerror else type(error).__name__
    return type(error).__name__


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(text(item) for item in value)


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


def require_text(
    record: Dict[str, Any],
    keys: Sequence[str],
    findings: List[Dict[str, Any]],
    rule_id: str,
    base: str,
) -> None:
    missing = [key for key in keys if not text(record.get(key))]
    if missing:
        add(
            findings,
            rule_id,
            "error",
            base,
            "Missing route fields: " + ", ".join(missing) + ".",
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


def validate_files(value: Any, findings: List[Dict[str, Any]], base: str, rule_id: str) -> None:
    if not isinstance(value, list) or not value:
        add(findings, rule_id, "error", f"{base}.files", "At least one exact deposited or article-hosted file is required.")
        return
    for index, item in enumerate(value):
        location = f"{base}.files[{index}]"
        if not isinstance(item, dict):
            add(findings, rule_id, "error", location, "Each file must be an object.")
            continue
        require_text(item, ("name", "role", "format"), findings, rule_id, location)


def validate(payload: Any, mode: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    if not isinstance(payload, dict):
        add(findings, "ROOT_OBJECT", "error", "$", "The inventory must be a JSON object.")
        return findings
    if payload.get("schema_version") != 1:
        add(findings, "SCHEMA_VERSION", "error", "schema_version", "schema_version must be 1.")
    for key in ("journal", "article_type", "policy_checked_on"):
        if not text(payload.get(key)):
            add(findings, "AUTHORITY", "error", key, f"{key} must be non-empty text.")
    datasets = payload.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        add(findings, "DATASETS", "error", "datasets", "datasets must be a non-empty list.")
        datasets = []

    observed_ids = set()
    for index, dataset in enumerate(datasets):
        base = f"datasets[{index}]"
        if not isinstance(dataset, dict):
            add(findings, "DATASET_OBJECT", "error", base, "Each dataset must be an object.")
            continue
        require_text(dataset, ("dataset_id", "description"), findings, "DATASET_IDENTITY", base)
        dataset_id = dataset.get("dataset_id")
        if text(dataset_id):
            if dataset_id in observed_ids:
                add(findings, "DUPLICATE_ID", "error", f"{base}.dataset_id", "dataset_id must be unique.")
            observed_ids.add(dataset_id)
        origin = dataset.get("origin")
        route = dataset.get("access_route")
        if origin not in ORIGINS:
            add(findings, "ORIGIN", "error", f"{base}.origin", f"origin must be one of {sorted(ORIGINS)}.")
        if route not in ROUTES:
            add(findings, "ACCESS_ROUTE", "error", f"{base}.access_route", f"access_route must be one of {sorted(ROUTES)}.")
            continue

        supports = dataset.get("supports")
        if route == "not_applicable":
            if origin != "none":
                add(findings, "NOT_APPLICABLE", "error", f"{base}.origin", "not_applicable requires origin 'none'.")
            if supports not in ([], None):
                add(findings, "NOT_APPLICABLE", "error", f"{base}.supports", "not_applicable cannot claim to support a result.")
            require_text(dataset, ("reason",), findings, "NOT_APPLICABLE", base)
            continue
        if not text_list(supports):
            add(findings, "CLAIM_MAPPING", "error", f"{base}.supports", "List each claim, figure, or table supported by this dataset.")

        if route == "public_repository":
            require_text(
                dataset,
                ("repository", "identifier", "licence", "citation"),
                findings,
                "PUBLIC_REPOSITORY",
                base,
            )
            validate_files(dataset.get("files"), findings, base, "PUBLIC_FILES")
        elif route == "controlled_access":
            require_text(dataset, ("repository",), findings, "CONTROLLED_ACCESS", base)
            restrictions = dataset.get("restrictions")
            if not isinstance(restrictions, dict):
                add(findings, "CONTROLLED_ACCESS", "error", f"{base}.restrictions", "Controlled access requires a restrictions object.")
            else:
                require_text(
                    restrictions,
                    ("reason", "controller", "request_route", "conditions"),
                    findings,
                    "CONTROLLED_ACCESS",
                    f"{base}.restrictions",
                )
                metadata_public = restrictions.get("metadata_public")
                if not isinstance(metadata_public, bool):
                    add(findings, "CONTROLLED_ACCESS", "error", f"{base}.restrictions.metadata_public", "metadata_public must be true or false.")
                elif metadata_public and not text(dataset.get("identifier")):
                    add(findings, "CONTROLLED_ACCESS", "error", f"{base}.identifier", "Public discovery metadata require a stable record identifier.")
                elif not metadata_public and not text(restrictions.get("metadata_unavailable_reason")):
                    add(findings, "CONTROLLED_ACCESS", "error", f"{base}.restrictions.metadata_unavailable_reason", "Explain why no public discovery record can be provided.")
        elif route == "within_paper_or_supplement":
            validate_files(dataset.get("files"), findings, base, "EMBEDDED_FILES")
        elif route == "reused_public":
            require_text(
                dataset,
                ("repository", "identifier", "version_or_access_date", "citation"),
                findings,
                "REUSED_PUBLIC",
                base,
            )
        elif route == "third_party_restricted":
            restrictions = dataset.get("restrictions")
            if not isinstance(restrictions, dict):
                add(findings, "THIRD_PARTY_ACCESS", "error", f"{base}.restrictions", "Third-party data require access terms.")
            else:
                require_text(
                    restrictions,
                    ("owner", "reason", "request_route", "permission_condition", "shareable_derivatives"),
                    findings,
                    "THIRD_PARTY_ACCESS",
                    f"{base}.restrictions",
                )
        elif route == "justified_request":
            restrictions = dataset.get("restrictions")
            if not isinstance(restrictions, dict):
                add(findings, "REQUEST_ACCESS", "error", f"{base}.restrictions", "Request-based access requires a durable process.")
            else:
                require_text(
                    restrictions,
                    ("reason", "responsible_group", "eligibility", "conditions", "contact_route"),
                    findings,
                    "REQUEST_ACCESS",
                    f"{base}.restrictions",
                )

    severity = "error" if mode == "final" else "warning"
    for location, _ in unresolved_values(payload):
        add(
            findings,
            "UNRESOLVED_FIELD",
            severity,
            location,
            "Replace or explicitly resolve this placeholder before final mode.",
        )
    return findings


def build_report(payload: Any, mode: str, target: Path) -> Dict[str, Any]:
    findings = validate(payload, mode)
    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "tool": "validate_data_inventory.py",
        "target": target.name,
        "mode": mode,
        "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "limitations": [
            "The validator does not confirm that an identifier resolves or that files are accessible.",
            "The validator cannot establish consent, licence rights, ethics approval, or journal compliance.",
        ],
    }


def render_markdown(result: Dict[str, Any]) -> str:
    lines = [
        "# Data-inventory validation",
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
        payload = json.loads(args.inventory.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: could not read data inventory {args.inventory.name}: "
              f"{path_free_exception_summary(error)}", file=sys.stderr)
        return 2
    result = build_report(payload, args.mode, args.inventory)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
