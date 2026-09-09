#!/usr/bin/env python3
"""Inspect PDF geometry, page count, and anonymous-review metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import List

from profile_contract import path_free_exception_summary, readiness_error

try:
    from pypdf import PdfReader
except ImportError as error:  # pragma: no cover - dependency guidance
    raise SystemExit("audit_pdf.py requires pypdf") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args()


def finding(
    number: int,
    rule_id: str,
    priority: str,
    observed: str,
    expected: str,
    action: str,
    location: str,
    sources: List[str],
) -> dict:
    impacts = {
        "PDF_PAGE_SIZE": "The rendered paper can be rejected or print incorrectly.",
        "PDF_TOTAL_PAGE_LIMIT": "The submission exceeds a hard page limit.",
        "PDF_FILE_SIZE": "The submission can be rejected because the PDF exceeds the configured file-size limit.",
        "PDF_AUTHOR_METADATA": "Document properties can reveal identity during double-blind review.",
    }
    return {
        "id": f"PDF-{number:03d}",
        "rule_id": rule_id,
        "basis": "official_hard_rule",
        "priority": priority,
        "status": "observed",
        "location": location,
        "observed": observed,
        "expected": expected,
        "impact": impacts[rule_id],
        "minimal_action": action,
        "verification": "Rebuild from the current official template and rerun PDF plus visual inspection.",
        "sources": sources,
    }


def format_decimal_mb(value: float) -> str:
    if value and abs(value) < 0.000001:
        return f"{value:.3g} MB"
    formatted = f"{value:.6f}".rstrip("0").rstrip(".")
    return f"{formatted or '0'} MB"


def audit(pdf_path: Path, profile: dict, stage: str) -> dict:
    reader = PdfReader(pdf_path)
    contract = profile["pdf_contract"]
    display_path = pdf_path.name
    findings: List[dict] = []
    width = float(contract["page_width_points"])
    height = float(contract["page_height_points"])
    tolerance = float(contract.get("page_tolerance_points", 2.0))
    geometry = []
    for index, page in enumerate(reader.pages, start=1):
        actual_width = float(page.mediabox.width)
        actual_height = float(page.mediabox.height)
        geometry.append(
            {
                "page": index,
                "width_points": round(actual_width, 3),
                "height_points": round(actual_height, 3),
            }
        )
        normal = abs(actual_width - width) <= tolerance and abs(actual_height - height) <= tolerance
        rotated = abs(actual_width - height) <= tolerance and abs(actual_height - width) <= tolerance
        if not (normal or rotated):
            findings.append(
                finding(
                    len(findings) + 1,
                    "PDF_PAGE_SIZE",
                    "P1",
                    f"Page {index} is {actual_width:.2f} x {actual_height:.2f} points.",
                    f"Every page is {width:.2f} x {height:.2f} points, allowing rotation.",
                    "Restore the official paper size and rebuild without document-level scaling.",
                    f"{display_path}:page {index}",
                    list(profile.get("rule_sources", {}).get("PDF_PAGE_SIZE", [])),
                )
            )

    maximum = contract.get("max_total_pages", {}).get(stage)
    if maximum is not None and len(reader.pages) > int(maximum):
        findings.append(
            finding(
                len(findings) + 1,
                "PDF_TOTAL_PAGE_LIMIT",
                "P0",
                f"The PDF contains {len(reader.pages)} pages.",
                f"The stage profile permits at most {maximum} total pages.",
                "Reduce content within the official format and rebuild; do not shrink the template.",
                display_path,
                list(profile.get("rule_sources", {}).get("PDF_TOTAL_PAGE_LIMIT", [])),
            )
        )

    max_file_size_mb = contract.get("max_file_size_mb", {}).get(stage)
    if max_file_size_mb is not None:
        file_size_mb = pdf_path.stat().st_size / 1_000_000
        if file_size_mb > float(max_file_size_mb):
            findings.append(
                finding(
                    len(findings) + 1,
                    "PDF_FILE_SIZE",
                    "P0",
                    f"The PDF file size is {format_decimal_mb(file_size_mb)}.",
                    f"The stage profile permits at most {format_decimal_mb(float(max_file_size_mb))}.",
                    "Reduce the submission artifact within the configured limit and rebuild without lowering content quality through template changes.",
                    display_path,
                    list(profile.get("rule_sources", {}).get("PDF_FILE_SIZE", [])),
                )
            )

    metadata = reader.metadata or {}
    author = str(metadata.get("/Author", "") or "").strip()
    if stage in contract.get("anonymous_stages", []) and author:
        findings.append(
            finding(
                len(findings) + 1,
                "PDF_AUTHOR_METADATA",
                "P0",
                f"PDF Author metadata is populated: {author!r}.",
                "Author metadata is empty in anonymous-review PDFs.",
                "Clear identifying metadata, rebuild, and inspect all document properties.",
                display_path,
                list(profile.get("rule_sources", {}).get("PDF_AUTHOR_METADATA", [])),
            )
        )

    limitations = [
        "A total PDF page count cannot locate a main-text, reference, or appendix boundary.",
        "Metadata and geometry checks do not prove visible anonymity or layout quality.",
        "Font embedding and clipping require a rendered inspection and, when available, a font-report tool.",
    ]
    return {
        "schema_version": 1,
        "tool": "audit_pdf.py",
        "venue": profile["venue"],
        "stage": stage,
        "target": display_path,
        "page_count": len(reader.pages),
        "geometry": geometry,
        "findings": findings,
        "limitations": limitations,
    }


def render_markdown(report: dict) -> str:
    lines = [
        f"# {report['venue']} PDF audit",
        "",
        f"- Stage: `{report['stage']}`",
        f"- Pages: {report['page_count']}",
        f"- Findings: {len(report['findings'])}",
    ]
    for item in report["findings"]:
        lines.extend(
            [
                "",
                f"## {item['id']} — {item['rule_id']}",
                "",
                f"- Observed: {item['observed']}",
                f"- Expected: {item['expected']}",
                f"- Action: {item['minimal_action']}",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except OSError as error:
        print(
            f"error: could not read profile {args.profile.name or 'profile'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    except json.JSONDecodeError as error:
        print(
            f"error: invalid profile {args.profile.name or 'profile'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if not isinstance(profile, dict):
        print(
            f"error: invalid profile {args.profile.name or 'profile'}: expected a JSON object",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if profile.get("schema_version") != 1 or args.stage not in profile.get("allowed_stages", []):
        print("error: unsupported profile or stage", file=sys.stderr)
        raise SystemExit(2)
    profile_error = readiness_error(profile, require_pdf_geometry=True)
    if profile_error:
        print(f"error: incomplete profile: {profile_error}", file=sys.stderr)
        raise SystemExit(2)
    try:
        report = audit(args.pdf.resolve(), profile, args.stage)
    except OSError as error:
        print(
            f"error: could not read PDF artifact {args.pdf.name or 'input'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    except (ValueError, KeyError):
        print("error: profile contract could not be applied", file=sys.stderr)
        raise SystemExit(2)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    raise SystemExit(1 if report["findings"] else 0)


if __name__ == "__main__":
    main()
