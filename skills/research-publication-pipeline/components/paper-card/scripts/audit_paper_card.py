#!/usr/bin/env python3
"""Audit a fixed-section Paper Card against its evidence bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence


SECTION = re.compile(r"^##\s+(\d{2})\b.*$", re.M)
POINTER = re.compile(r"\[Paper:\s*([^\]]+)\]", re.I)
BLOCK_ID = re.compile(r"\b[SU]\d{3,}\b", re.I)
LOCATOR_MODES = ("page-grounded", "structure-grounded", "source-limited")
SOURCE_LIMITED = ("abstract", "metadata", "user-provided excerpt")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", required=True, type=Path)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--locator-mode", required=True, choices=LOCATOR_MODES)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args(argv)


def finding(level: str, rule_id: str, message: str, **details: Any) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "level": level,
        "rule_id": rule_id,
        "message": message,
    }
    if details:
        result["details"] = details
    return result


def section_text(card: str, number: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(number)}\b[^\n]*\n(.*?)(?=^##\s+\d{{2}}\b|\Z)",
        card,
        re.M | re.S,
    )
    return match.group(1) if match else ""


def evidence_mentioned(card: str, item_id: str) -> bool:
    match = re.match(r"^(Figure|Table|Equation)\s+((?:ED|S)?\d+[A-Za-z]?)$", item_id, re.I)
    if match is None:
        return item_id.casefold() in card.casefold()
    kind, number = match.groups()
    aliases = {
        "figure": [f"Figure {number}", f"Fig. {number}", f"图 {number}", f"图{number}"],
        "table": [f"Table {number}", f"表 {number}", f"表{number}"],
        "equation": [f"Equation {number}", f"Eq. {number}", f"公式 {number}", f"公式{number}"],
    }
    lowered = card.casefold()
    return any(alias.casefold() in lowered for alias in aliases[kind.casefold()])


def audit(card: str, bundle: Optional[Dict[str, Any]], locator_mode: str) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    observed_sections = SECTION.findall(card)
    expected_sections = [f"{number:02d}" for number in range(1, 17)]
    if observed_sections == expected_sections:
        findings.append(finding("pass", "SECTIONS_01_16", "Sections 01--16 occur once and in order."))
    else:
        findings.append(
            finding(
                "error",
                "SECTIONS_01_16",
                "Sections 01--16 must occur once and in order.",
                expected=expected_sections,
                observed=observed_sections,
            )
        )

    if re.search(r"^##\s+(?:17|18)\b", card, re.M):
        findings.append(finding("error", "FORBIDDEN_SECTION", "Sections 17 and 18 are outside the card contract."))

    preamble = card.split("## 01", 1)[0]
    header_lines = [line for line in preamble.splitlines() if line.lstrip().startswith(">")]
    if len(header_lines) < 7:
        findings.append(finding("error", "STATUS_HEADER", "The evidence-status header needs seven fields."))
    if locator_mode.casefold() not in preamble.casefold():
        findings.append(finding("error", "LOCATOR_DECLARATION", "The header does not declare the selected locator mode."))

    pointers = POINTER.findall(card)
    if not pointers:
        findings.append(finding("error", "PAPER_POINTER_REQUIRED", "No [Paper: ...] source pointer was found."))
    page_pointers = [
        pointer
        for pointer in pointers
        if re.search(r"\bPDF\s+pp?\.\s*\d", pointer, re.I)
    ]
    ambiguous_pages = [
        pointer
        for pointer in pointers
        if re.search(r"\bpp?\.\s*\d", pointer, re.I)
        and not re.search(r"\bPDF\s+pp?\.\s*\d", pointer, re.I)
    ]
    if locator_mode == "page-grounded":
        if bundle is None:
            findings.append(finding("error", "BUNDLE_REQUIRED", "Page-grounded mode requires a source bundle."))
        if not page_pointers:
            findings.append(finding("error", "PAGE_POINTER_REQUIRED", "Page-grounded mode requires an explicit PDF page pointer."))
        if ambiguous_pages:
            findings.append(finding("error", "AMBIGUOUS_PAGE_POINTER", "Page pointers must identify PDF page indices.", pointers=ambiguous_pages))
        if bundle is not None and page_pointers:
            available_pages = {
                item.get("pdf_page")
                for item in bundle.get("pages", [])
                if isinstance(item, dict) and isinstance(item.get("pdf_page"), int)
            }
            invalid_pages = set()
            for pointer in page_pointers:
                for match in re.finditer(
                    r"\bPDF\s+pp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?",
                    pointer,
                    re.I,
                ):
                    start = int(match.group(1))
                    end = int(match.group(2) or start)
                    if start not in available_pages:
                        invalid_pages.add(start)
                    if end not in available_pages:
                        invalid_pages.add(end)
            if invalid_pages:
                findings.append(
                    finding(
                        "error",
                        "PAGE_POINTER_RANGE",
                        "A cited PDF page is absent from the source bundle.",
                        pages=sorted(invalid_pages),
                    )
                )
    elif page_pointers or ambiguous_pages:
        findings.append(
            finding(
                "error",
                "PAGE_POINTER_FORBIDDEN",
                f"{locator_mode} mode cannot use page-number pointers.",
                pointers=page_pointers + ambiguous_pages,
            )
        )

    inventory: Dict[str, Any] = {}
    if bundle is None:
        findings.append(
            finding(
                "warning",
                "SOURCE_INVENTORY_UNAVAILABLE",
                "No source bundle was supplied; display and block coverage were not checked.",
            )
        )
    else:
        inventory = bundle.get("evidence_inventory", {})
        if not isinstance(inventory, dict):
            findings.append(finding("error", "INVALID_INVENTORY", "evidence_inventory must be an object."))
            inventory = {}
        for key, label in (("figures", "figure"), ("tables", "table"), ("equations", "equation")):
            items = inventory.get(key, [])
            if not isinstance(items, list):
                findings.append(finding("error", "INVALID_INVENTORY", f"{key} must be a list."))
                continue
            missing = [
                str(item.get("id", ""))
                for item in items
                if isinstance(item, dict)
                and item.get("id")
                and not evidence_mentioned(card, str(item["id"]))
            ]
            if missing:
                findings.append(
                    finding(
                        "error",
                        f"{label.upper()}_COVERAGE",
                        f"Not every inventoried {label} appears in the Paper Card.",
                        missing=missing,
                    )
                )
        records = []
        for key in ("located_blocks", "unlocated_blocks"):
            value = bundle.get(key, [])
            if isinstance(value, list):
                records.extend(item for item in value if isinstance(item, dict))
        available = {str(item["id"]).upper() for item in records if item.get("id")}
        cited = {
            block.upper()
            for pointer in pointers
            for block in BLOCK_ID.findall(pointer)
        }
        unknown = sorted(cited - available)
        if unknown:
            findings.append(
                finding(
                    "error",
                    "UNKNOWN_SOURCE_BLOCK",
                    "A source-block pointer is absent from the source bundle.",
                    unknown=unknown,
                )
            )

    if locator_mode == "source-limited":
        invalid = [
            pointer
            for pointer in pointers
            if not any(scope in pointer.casefold() for scope in SOURCE_LIMITED)
        ]
        if invalid:
            findings.append(
                finding(
                    "error",
                    "SOURCE_LIMITED_SCOPE",
                    "Source-limited pointers may use only Abstract, Metadata, or User-provided excerpt.",
                    pointers=invalid,
                )
            )

    author_limitations = section_text(card, "12")
    critical_analysis = section_text(card, "13")
    if "[Analysis]" in author_limitations:
        findings.append(
            finding(
                "error",
                "LIMITATION_PROVENANCE",
                "Section 12 mixes agent analysis with author-acknowledged limitations.",
            )
        )
    if critical_analysis and "[Analysis]" not in critical_analysis:
        findings.append(
            finding(
                "warning",
                "ANALYSIS_LABEL",
                "Section 13 should label agent-derived criticism as [Analysis].",
            )
        )

    ideas = section_text(card, "16").casefold()
    for rule_id, terms in (
        ("IDEA_STATUS", ("innovation status", "创新状态")),
        ("IDEA_VALIDATION", ("validation", "如何验证")),
        ("IDEA_FAILURE", ("failure mode", "failure modes", "可能失败")),
    ):
        if not any(term.casefold() in ideas for term in terms):
            findings.append(finding("warning", rule_id, "Section 16 is missing a required idea field."))

    errors = sum(item["level"] == "error" for item in findings)
    warnings = sum(item["level"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "summary": {
            "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
            "errors": errors,
            "warnings": warnings,
        },
        "metrics": {
            "locator_mode": locator_mode,
            "sections": observed_sections,
            "paper_pointer_count": len(pointers),
        },
        "findings": findings,
    }


def print_text(report: Dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        f"Audit status: {summary['status']} "
        f"(warnings={summary['warnings']}, errors={summary['errors']})"
    )
    for item in report["findings"]:
        print(f"{item['level'].upper():7} {item['rule_id']}: {item['message']}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if not args.card.is_file():
        print("ERROR: --card must identify an existing file", file=sys.stderr)
        return 2
    if args.bundle is not None and not args.bundle.is_file():
        print("ERROR: --bundle must identify an existing file", file=sys.stderr)
        return 2
    if args.locator_mode == "page-grounded" and args.bundle is None:
        print("ERROR: page-grounded mode requires --bundle", file=sys.stderr)
        return 2
    try:
        card = args.card.read_text(encoding="utf-8")
        bundle = json.loads(args.bundle.read_text(encoding="utf-8")) if args.bundle else None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    report = audit(card, bundle, args.locator_mode)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_text(report)
    if args.report is not None:
        output = args.report.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
