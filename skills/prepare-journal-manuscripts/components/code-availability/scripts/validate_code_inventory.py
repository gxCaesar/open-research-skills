#!/usr/bin/env python3
"""Validate code-to-claim and availability-route records.

Journals ask what a reader needs in order to re-run the analysis behind a claim. This
checks that the record answers that question: every component that a conclusion depends
on has a route, an identifier that can outlive a repository, a licence that permits the
reuse the statement implies, and enough environment detail to install it.

It cannot confirm that an identifier resolves, that a repository is public, that the
licence is the author's to grant, or that the code reproduces anything.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROUTES = {
    "archived_with_identifier",
    "public_repository",
    "within_paper_or_supplement",
    "reused_public",
    "third_party_restricted",
    "justified_request",
    "not_applicable",
}
ORIGINS = {"custom", "reused", "third_party", "mixed"}
DURABLE = {"archived_with_identifier", "reused_public", "within_paper_or_supplement"}
UNRESOLVED = re.compile(
    r"(?:AUTHOR_INPUT_NEEDED|\bTBD\b|\bTODO\b|"
    r"\[(?:replace|insert|unknown|required|repository|identifier|doi|commit|"
    r"licen[cs]e|reason|contact|version|environment|journal|article)[^\]]*\])",
    re.I,
)
# The statement that promises rather than provides. Journals increasingly reject it, and
# a reader cannot act on it at all.
PROMISE = re.compile(
    r"(?:will be (?:made )?(?:available|released|deposited|shared)"
    r"|available (?:up)?on (?:reasonable )?request"
    r"|upon publication|after publication|in due course|coming soon)",
    re.I,
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--mode", choices=["working", "final"], default="working")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args(argv)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(text(item) for item in value)


def add(findings: List[Dict[str, Any]], rule_id: str, severity: str, location: str, message: str) -> None:
    findings.append({"rule_id": rule_id, "severity": severity, "location": location, "message": message})


def validate(payload: Any, mode: str) -> List[Dict[str, Any]]:  # noqa: C901 - one rule per branch
    findings: List[Dict[str, Any]] = []
    final = mode == "final"
    if not isinstance(payload, dict):
        add(findings, "inventory", "error", "inventory", "top-level value must be an object")
        return findings

    if payload.get("schema_version") != 1:
        add(findings, "schema_version", "error", "schema_version", "must equal 1")
    for key in ("journal", "article_type", "policy_checked_on"):
        if not text(payload.get(key)):
            add(findings, key, "error", key, "must be non-empty text")

    components = payload.get("components")
    if not isinstance(components, list) or not components:
        add(findings, "components", "error", "components", "must be a non-empty list")
        components = []

    seen: set = set()
    for index, component in enumerate(components):
        where = f"components[{index}]"
        if not isinstance(component, dict):
            add(findings, "component", "error", where, "must be an object")
            continue
        name = component.get("component_id") if text(component.get("component_id")) else where
        if not text(component.get("component_id")):
            add(findings, "component_id", "error", f"{where}.component_id", "must be non-empty text")
        elif component["component_id"] in seen:
            add(findings, "component_id", "error", f"{where}.component_id", "must be unique")
        else:
            seen.add(component["component_id"])

        if not text(component.get("description")):
            add(findings, "description", "error", f"{name}.description", "must be non-empty text")
        if not text_list(component.get("supports")):
            add(findings, "supports", "error", f"{name}.supports",
                "must list the claims, figures or tables this code produces")

        origin = component.get("origin")
        if origin not in ORIGINS:
            add(findings, "origin", "error", f"{name}.origin",
                f"must be one of: {', '.join(sorted(ORIGINS))}")

        route = component.get("access_route")
        if route not in ROUTES:
            add(findings, "access_route", "error", f"{name}.access_route",
                f"must be one of: {', '.join(sorted(ROUTES))}")
            continue

        if route == "not_applicable":
            if origin == "custom":
                add(findings, "custom_code_not_applicable", "error", f"{name}.access_route",
                    "custom code that supports a claim cannot be exempt; choose a real route")
            if not text(component.get("not_applicable_reason")):
                add(findings, "not_applicable_reason", "error", f"{name}.not_applicable_reason",
                    "must say why no code underlies this claim")
            continue

        if route in {"archived_with_identifier", "public_repository", "reused_public"}:
            if not text(component.get("version_or_commit")):
                add(findings, "version_or_commit", "error", f"{name}.version_or_commit",
                    "must pin the exact version, tag or commit a reader should obtain")
        if route in {"archived_with_identifier", "reused_public"} and not text(component.get("identifier")):
            add(findings, "identifier", "error", f"{name}.identifier",
                "must give the persistent identifier of the archived version")
        if route == "public_repository":
            if not text(component.get("repository")):
                add(findings, "repository", "error", f"{name}.repository", "must name the host")
            if not text(component.get("identifier")):
                add(findings, "identifier", "error", f"{name}.identifier", "must give the repository URL")
            severity = "error" if final else "warning"
            if not text(component.get("archived_identifier")):
                add(findings, "repository_without_archive", severity, f"{name}.archived_identifier",
                    "a repository URL is a moving target; deposit the exact version and record its "
                    "persistent identifier")
        if route in DURABLE | {"public_repository"} and not text(component.get("licence")):
            add(findings, "licence", "error", f"{name}.licence",
                "released code needs a licence; without one a reader may read it and not run it")
        if route in {"archived_with_identifier", "public_repository", "within_paper_or_supplement"}:
            environment = component.get("environment")
            if not isinstance(environment, dict) or not text(environment.get("specification")):
                add(findings, "environment", "error", f"{name}.environment.specification",
                    "name the pinned environment file a reader installs from")
            elif final and not text(environment.get("interpreter_or_runtime")):
                add(findings, "environment_runtime", "warning", f"{name}.environment.interpreter_or_runtime",
                    "record the interpreter or runtime version the released environment was verified on")
        if route == "reused_public" and not text(component.get("citation")):
            add(findings, "citation", "error", f"{name}.citation", "reused code must be cited")
        if route == "third_party_restricted":
            for key in ("controller", "conditions", "available_without_it"):
                if not text(component.get(key)):
                    add(findings, "third_party", "error", f"{name}.{key}",
                        "restricted third-party code needs its controller, the conditions, and what a "
                        "reader can still do without it")
        if route == "justified_request":
            for key in ("contact_route", "eligibility", "response_window"):
                if not text(component.get(key)):
                    add(findings, "request_route", "error", f"{name}.{key}",
                        "a request route needs a durable contact, who qualifies, and how long a reply takes")
            if final:
                add(findings, "request_route_at_final", "warning", f"{name}.access_route",
                    "a request route is the weakest available answer; confirm the journal accepts it for "
                    "code central to the conclusions")

    statement = payload.get("statement")
    if statement is not None and not text(statement):
        add(findings, "statement", "error", "statement", "must be non-empty text when present")
    elif text(statement):
        if PROMISE.search(statement):
            add(findings, "statement_promises_rather_than_provides",
                "error" if final else "warning", "statement",
                "the statement promises future availability; a reader cannot act on it")
        if final:
            for component in components:
                if not isinstance(component, dict):
                    continue
                handles = [component.get(key) for key in ("component_id", "identifier", "repository")]
                handles = [handle for handle in handles if text(handle)]
                if handles and not any(handle in statement for handle in handles):
                    add(findings, "statement_omits_component", "warning", "statement",
                        f"the statement names none of {handles} for this component")
    elif final:
        add(findings, "statement", "error", "statement", "final mode requires the statement text")

    if final:
        rendered = json.dumps(payload, ensure_ascii=False)
        if UNRESOLVED.search(rendered):
            add(findings, "unresolved_placeholder", "error", "inventory",
                "resolve every placeholder before final mode")
    return findings


def build_report(payload: Any, mode: str, target: Path) -> Dict[str, Any]:
    findings = validate(payload, mode)
    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "tool": "validate_code_inventory.py",
        "target": str(target.resolve()),
        "mode": mode,
        "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "limitations": [
            "The validator does not confirm that an identifier resolves or that a repository is public.",
            "The validator cannot establish licence rights, export controls, or journal compliance.",
            "Running the code is the only way to learn whether it reproduces anything.",
        ],
    }


def render_markdown(result: Dict[str, Any]) -> str:
    lines = [
        "# Code-inventory validation",
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
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    result = build_report(payload, args.mode, args.inventory)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
