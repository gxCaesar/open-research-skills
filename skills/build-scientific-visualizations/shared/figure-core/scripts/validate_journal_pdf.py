#!/usr/bin/env python3
"""Validate one-page journal-figure PDF geometry against a dated profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import List

from project_contract import (
    caption_word_count,
    load_venue_profiles,
    profile_height_limit,
    resolve_layout_profile,
)

try:
    from pypdf import PdfReader
except ImportError as error:  # pragma: no cover - dependency guidance
    raise SystemExit("validate_journal_pdf.py requires pypdf") from error


MM_TO_PT = 72 / 25.4


def parse_args() -> argparse.Namespace:
    registry = load_venue_profiles()
    profile_names = sorted(set(registry["profiles"]) | set(registry["legacy_aliases"]))
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    geometry = parser.add_mutually_exclusive_group(required=True)
    geometry.add_argument("--profile", choices=profile_names)
    geometry.add_argument("--expected-width-mm", type=float)
    geometry.add_argument("--venue-contract", type=Path)
    parser.add_argument("--max-height-mm", type=float)
    parser.add_argument("--caption-file", type=Path)
    parser.add_argument("--tolerance-mm", type=float, default=0.2)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if args.tolerance_mm < 0:
        parser.error("--tolerance-mm must be non-negative")
    return args


def main() -> int:
    args = parse_args()
    reader = PdfReader(args.pdf)
    errors: List[str] = []
    if len(reader.pages) != 1:
        errors.append(f"expected one page, found {len(reader.pages)}")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) / MM_TO_PT
    height_mm = float(page.mediabox.height) / MM_TO_PT

    warnings: List[str] = []
    contract = None
    if args.profile:
        contract, warnings = resolve_layout_profile(args.profile)
    elif args.venue_contract:
        contract = json.loads(args.venue_contract.read_text(encoding="utf-8"))
    geometry = contract.get("geometry", {}) if contract else {}
    expected_width = (
        float(geometry["selected_width_mm"])
        if contract
        else args.expected_width_mm
    )
    max_height = args.max_height_mm
    words = None
    if args.caption_file is not None:
        words = caption_word_count(args.caption_file.read_text(encoding="utf-8"))
    caption_limits = geometry.get("caption_height_limits", [])
    if contract is not None and caption_limits and words is None:
        errors.append("the selected venue profile requires --caption-file for caption-dependent height validation")
    if contract is not None and caption_limits and words is not None:
        max_height = profile_height_limit(contract, words)
        if max_height is None:
            errors.append(
                f"caption has {words} words; the selected profile has no 300-word-or-longer height allowance"
            )
    elif contract is not None and max_height is None:
        fixed_height = geometry.get("max_height_mm")
        max_height = float(fixed_height) if fixed_height is not None else None

    if abs(width_mm - expected_width) > args.tolerance_mm:
        errors.append(
            f"width {width_mm:.3f} mm differs from expected {expected_width:.3f} mm "
            f"by more than {args.tolerance_mm:.3f} mm"
        )
    if max_height is not None and height_mm - max_height > args.tolerance_mm:
        errors.append(
            f"height {height_mm:.3f} mm exceeds maximum {max_height:.3f} mm "
            f"by more than {args.tolerance_mm:.3f} mm"
        )

    result = {
        "status": "FAIL" if errors else "PASS",
        "profile": args.profile or (contract or {}).get("profile_id"),
        "pages": len(reader.pages),
        "width_mm": round(width_mm, 3),
        "height_mm": round(height_mm, 3),
        "expected_width_mm": expected_width,
        "max_height_mm": max_height,
        "caption_words": words,
        "tolerance_mm": args.tolerance_mm,
        "errors": errors,
        "warnings": warnings,
    }
    for warning in warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    if args.as_json:
        print(json.dumps(result, sort_keys=True))
    else:
        for error in errors:
            print(f"ERROR {error}")
        print(
            f"Status: {result['status']} | {width_mm:.3f} x {height_mm:.3f} mm | "
            f"caption_words={words}"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
