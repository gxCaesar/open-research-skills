#!/usr/bin/env python3
"""Validate the portable review-report contract used by manuscript skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Dict, List, Optional, Sequence
from urllib.parse import urlparse

from profile_contract import path_free_exception_summary


PRIORITIES = {"P0", "P1", "P2"}
BASES = {
    "official_hard_rule",
    "official_guidance",
    "manuscript_fact",
    "scientific_judgment",
    "inference",
}
SOURCE_STATUSES = {"VERIFIED", "UNVERIFIED", "COULD_NOT_OPEN", "NOT_FOUND"}
MODES = {"diagnose", "revise", "final_audit"}
FINDING_KEYS = {
    "id",
    "basis",
    "priority",
    "status",
    "location",
    "observed",
    "expected",
    "impact",
    "minimal_action",
    "verification",
    "sources",
}


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args(argv)


def nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add(errors: List[dict], location: str, message: str) -> None:
    errors.append({"location": location, "message": message})


def validate(report: object) -> List[dict]:
    errors: List[dict] = []
    if not isinstance(report, dict):
        add(errors, "$", "The report must be a JSON object.")
        return errors

    if report.get("schema_version") != 1:
        add(errors, "schema_version", "schema_version must be 1.")
    for key in ("venue", "stage"):
        if not nonempty_text(report.get(key)):
            add(errors, key, f"{key} must be non-empty text.")
    year = report.get("year")
    if not isinstance(year, int) or isinstance(year, bool) or year < 2000:
        add(errors, "year", "year must be a four-digit integer.")
    if report.get("mode") not in MODES:
        add(errors, "mode", f"mode must be one of {sorted(MODES)}.")

    artifacts = report.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        add(errors, "artifacts", "artifacts must be a non-empty list.")
    else:
        for index, artifact in enumerate(artifacts):
            location = f"artifacts[{index}]"
            if not isinstance(artifact, dict):
                add(errors, location, "artifact must be an object.")
                continue
            if not nonempty_text(artifact.get("path")):
                add(errors, f"{location}.path", "path must be non-empty text.")
            if artifact.get("status") not in {"observed", "not_run", "failed", "inferred"}:
                add(errors, f"{location}.status", "artifact status is invalid.")

    source_ids: Dict[str, str] = {}
    source_statuses: Dict[str, str] = {}
    sources = report.get("sources")
    if not isinstance(sources, list):
        add(errors, "sources", "sources must be a list.")
    else:
        for index, source in enumerate(sources):
            location = f"sources[{index}]"
            if not isinstance(source, dict):
                add(errors, location, "source must be an object.")
                continue
            source_id = source.get("source_id")
            if not nonempty_text(source_id):
                add(errors, f"{location}.source_id", "source_id must be non-empty text.")
            elif source_id in source_ids:
                add(errors, f"{location}.source_id", f"duplicate source_id {source_id!r}.")
            else:
                source_ids[source_id] = location
            url = source.get("url")
            parsed = urlparse(url) if isinstance(url, str) else None
            if parsed is None or parsed.scheme not in {"https", "http"} or not parsed.netloc:
                add(errors, f"{location}.url", "url must be an absolute HTTP(S) URL.")
            checked_on = source.get("checked_on")
            if not nonempty_text(checked_on):
                add(errors, f"{location}.checked_on", "checked_on must be non-empty text.")
            if source.get("status") not in SOURCE_STATUSES:
                add(errors, f"{location}.status", "source status is invalid.")
            elif nonempty_text(source_id):
                source_statuses[source_id] = source["status"]

    findings = report.get("findings")
    finding_ids = set()
    if not isinstance(findings, list):
        add(errors, "findings", "findings must be a list.")
    else:
        for index, finding in enumerate(findings):
            location = f"findings[{index}]"
            if not isinstance(finding, dict):
                add(errors, location, "finding must be an object.")
                continue
            missing = sorted(FINDING_KEYS - set(finding))
            if missing:
                add(errors, location, f"missing required fields: {', '.join(missing)}.")
            finding_id = finding.get("id")
            if not nonempty_text(finding_id):
                add(errors, f"{location}.id", "id must be non-empty text.")
            elif finding_id in finding_ids:
                add(errors, f"{location}.id", f"duplicate finding id {finding_id!r}.")
            else:
                finding_ids.add(finding_id)
            priority = finding.get("priority")
            basis = finding.get("basis")
            if priority not in PRIORITIES:
                add(errors, f"{location}.priority", "priority must be P0, P1, or P2.")
            if basis not in BASES:
                add(errors, f"{location}.basis", "basis is invalid.")
            if finding.get("status") not in {"observed", "inferred"}:
                add(errors, f"{location}.status", "finding status must be observed or inferred.")
            for key in (
                "location",
                "observed",
                "expected",
                "impact",
                "minimal_action",
                "verification",
            ):
                if not nonempty_text(finding.get(key)):
                    add(errors, f"{location}.{key}", f"{key} must be non-empty text.")
            cited = finding.get("sources")
            if not isinstance(cited, list):
                add(errors, f"{location}.sources", "sources must be a list of source ids.")
                cited = []
            for source_id in cited:
                if source_id not in source_ids:
                    add(errors, f"{location}.sources", f"unknown source id {source_id!r}.")
            if basis in {"official_hard_rule", "official_guidance"} and not cited:
                add(errors, f"{location}.sources", "official claims require at least one source id.")
            if priority == "P0" and (basis == "inference" or finding.get("status") != "observed"):
                add(
                    errors,
                    location,
                    "P0 findings must be observed and cannot use inference as their basis.",
                )
            if priority == "P0":
                unverified = [
                    source_id
                    for source_id in cited
                    if source_id in source_statuses
                    and source_statuses[source_id] != "VERIFIED"
                ]
                if unverified:
                    add(
                        errors,
                        f"{location}.sources",
                        "P0 findings cannot rely on unverified official sources.",
                    )

    limitations = report.get("limitations")
    if not isinstance(limitations, list) or any(not nonempty_text(item) for item in limitations):
        add(errors, "limitations", "limitations must be a list of non-empty strings.")
    return errors


def render_markdown(result: dict) -> str:
    lines = [
        "# Review report validation",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {len(result['errors'])}",
    ]
    for error in result["errors"]:
        lines.append(f"- `{error['location']}`: {error['message']}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(
            f"error: could not read review report {args.report.name}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        return 2
    errors = validate(report)
    result = {
        "schema_version": 1,
        "tool": "validate_review_report.py",
        "target": args.report.name,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
