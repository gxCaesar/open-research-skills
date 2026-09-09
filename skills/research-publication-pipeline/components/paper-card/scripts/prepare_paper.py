#!/usr/bin/env python3
"""Prepare a portable evidence bundle from a PDF or structured source map."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


SECTION_NAMES = {
    "abstract",
    "introduction",
    "background",
    "related work",
    "method",
    "methods",
    "methodology",
    "experiments",
    "experimental setup",
    "results",
    "discussion",
    "limitations",
    "conclusion",
    "conclusions",
    "references",
    "appendix",
}
PAGE_FIELDS = ("page", "page_number", "pdf_page")
POSITIVE_INTEGER = re.compile(r"^[1-9]\d*$")
CAPTION_PATTERNS = (
    re.compile(r"^\s*(Figure|Fig\.|Table)\s+((?:ED|S)?\d+[A-Za-z]?)\s*(?::|\|)\s*(.*)$", re.I),
    re.compile(r"^\s*(Fig\.)\s+((?:ED|S)?\d+)\s+(.+)$", re.I),
    re.compile(r"^\s*(Table)\s+((?:ED|S)\d+)\s+(.+)$", re.I),
)
EQUATION = re.compile(r"\((\d{1,3})\)\s*$")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a paper PDF or structured JSON source map."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--render-dir", type=Path)
    parser.add_argument("--render-dpi", type=int, default=110)
    return parser.parse_args(argv)


def clean_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in normalized.splitlines()).strip()


def verify_pdf_signature(path: Path) -> None:
    with path.open("rb") as handle:
        header = handle.read(1024)
    if b"%PDF-" not in header:
        raise RuntimeError("input has a .pdf suffix but no PDF header was found")


def heading_candidates(
    text: str,
    pdf_page: Optional[int],
    source_block_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for line in text.splitlines():
        value = " ".join(line.split()).strip(" :")
        lowered = value.casefold()
        numbered = re.match(r"^(?:\d+(?:\.\d+)*)\s+([A-Z][A-Za-z0-9 ,/&-]{2,80})$", value)
        if lowered not in SECTION_NAMES and numbered is None:
            continue
        record: Dict[str, Any] = {"title": value, "pdf_page": pdf_page}
        if source_block_id:
            record["source_block_id"] = source_block_id
        results.append(record)
    return results


def match_caption(line: str) -> Optional[re.Match]:
    for pattern in CAPTION_PATTERNS:
        match = pattern.match(line)
        if match is not None:
            return match
    return None


def collect_caption(lines: List[str], start: int) -> str:
    match = match_caption(lines[start])
    if match is None:
        return ""
    parts = [match.group(3).strip()]
    for line in lines[start + 1 : start + 4]:
        value = " ".join(line.split())
        if not value or match_caption(value) or value.casefold() in SECTION_NAMES:
            break
        if re.match(r"^[A-Z][A-Za-z ]{2,40}$", value) and not value.endswith("."):
            break
        parts.append(value)
    return " ".join(part for part in parts if part)


def evidence_from_units(units: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    inventory: Dict[str, List[Dict[str, Any]]] = {
        "figures": [],
        "tables": [],
        "equations": [],
    }
    seen = set()
    for unit in units:
        lines = str(unit.get("text", "")).splitlines()
        for index, line in enumerate(lines):
            caption = match_caption(line)
            if caption is not None:
                kind = "Table" if caption.group(1).casefold() == "table" else "Figure"
                number = caption.group(2)
                key = (kind, number.casefold())
                if key not in seen:
                    seen.add(key)
                    inventory["tables" if kind == "Table" else "figures"].append(
                        {
                            "id": f"{kind} {number}",
                            "caption": collect_caption(lines, index),
                            "pdf_page": unit.get("pdf_page"),
                            "source_block_id": unit.get("source_block_id"),
                        }
                    )
            equation = EQUATION.search(line)
            if equation is not None:
                number = equation.group(1)
                key = ("Equation", number)
                if key not in seen:
                    seen.add(key)
                    inventory["equations"].append(
                        {
                            "id": f"Equation {number}",
                            "context": " ".join(lines[max(0, index - 2) : index + 1]).strip(),
                            "pdf_page": unit.get("pdf_page"),
                            "source_block_id": unit.get("source_block_id"),
                        }
                    )
    return inventory


def flatten_source_map(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return []
    for key in ("blocks", "source_blocks", "items", "entries"):
        records = value.get(key)
        if isinstance(records, list):
            return [item for item in records if isinstance(item, dict)]
    return []


def source_text(block: Dict[str, Any]) -> str:
    value = (
        block.get("original")
        or block.get("source_text")
        or block.get("text")
        or block.get("content")
        or ""
    )
    return clean_text(str(value)) if value else ""


def page_locator(block: Dict[str, Any]) -> Tuple[Optional[int], str, Optional[str], Any]:
    field: Optional[str] = None
    value: Any = None
    for candidate in PAGE_FIELDS:
        if candidate not in block:
            continue
        field = candidate
        value = block[candidate]
        if value is not None and not (isinstance(value, str) and not value.strip()):
            break
    if field is None or value is None or (isinstance(value, str) and not value.strip()):
        return None, "missing", field, value
    if isinstance(value, bool):
        return None, "invalid", field, value
    if isinstance(value, int) and value > 0:
        return value, "verified", field, value
    if isinstance(value, float) and value.is_integer() and value > 0:
        return int(value), "verified", field, value
    if isinstance(value, str) and POSITIVE_INTEGER.fullmatch(value.strip()):
        return int(value.strip()), "verified", field, value
    return None, "invalid", field, value


def prepare_source_map(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped: Dict[int, List[str]] = defaultdict(list)
    located: List[Dict[str, Any]] = []
    unlocated: List[Dict[str, Any]] = []
    missing = 0
    invalid = 0

    for index, block in enumerate(flatten_source_map(data), start=1):
        text = source_text(block)
        if not text:
            continue
        page, state, field, value = page_locator(block)
        supplied_id = block.get("id") or block.get("block_id")
        record = {
            "id": str(supplied_id or (f"S{index:03d}" if state == "verified" else f"U{index:03d}")),
            "block_type": block.get("type"),
            "section": block.get("section") or block.get("section_title"),
            "text": text,
            "character_count": len(text),
            "locator_status": state,
            "locator_field": field,
            "locator_value": value,
        }
        if state == "verified" and page is not None:
            record["pdf_page"] = page
            located.append(record)
            grouped[page].append(text)
        else:
            unlocated.append(record)
            if state == "missing":
                missing += 1
            else:
                invalid += 1

    pages = [
        {
            "pdf_page": page,
            "text": clean_text("\n".join(grouped[page])),
            "character_count": len(clean_text("\n".join(grouped[page]))),
        }
        for page in sorted(grouped)
    ]
    structural_units: List[Dict[str, Any]] = [dict(item) for item in pages]
    structural_units.extend(
        {
            "pdf_page": item.get("pdf_page"),
            "source_block_id": item["id"],
            "text": item["text"],
        }
        for item in unlocated
    )
    sections: List[Dict[str, Any]] = []
    for item in located + unlocated:
        sections.extend(
            heading_candidates(
                item["text"], item.get("pdf_page"), item["id"]
            )
        )
        explicit = item.get("section")
        if explicit and not any(
            candidate["title"] == str(explicit)
            and candidate.get("source_block_id") == item["id"]
            for candidate in sections
        ):
            sections.append(
                {
                    "title": str(explicit),
                    "pdf_page": item.get("pdf_page"),
                    "source_block_id": item["id"],
                }
            )

    reliability = "reliable"
    if unlocated and located:
        reliability = "mixed"
    elif unlocated:
        reliability = "unavailable"
    bundle: Dict[str, Any] = {
        "schema_version": 1,
        "source_type": "source_map",
        "source_path": str(path.resolve()),
        "source_access": {"state": "local-file-readable"},
        "format_verification": {
            "declared": "json",
            "verified": "json",
            "method": "successful JSON parse",
        },
        "metadata": data.get("metadata", {}) if isinstance(data, dict) else {},
        "page_count": len(pages),
        "pages": pages,
        "located_blocks": located,
        "unlocated_blocks": unlocated,
        "locator_summary": {
            "verified_page_blocks": len(located),
            "missing_page_locator_blocks": missing,
            "invalid_page_locator_blocks": invalid,
            "page_locator_reliability": reliability,
        },
        "sections": sections,
        "evidence_inventory": evidence_from_units(structural_units),
        "rendered_pages_dir": None,
        "extraction": {
            "engine": "source-map-normalizer",
            "visual_pages_rendered": False,
            "confidence": "mixed",
        },
    }
    return bundle


def render_pdf(path: Path, render_dir: Path, dpi: int) -> None:
    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise RuntimeError("rendered pages requested but pdftoppm is unavailable")
    if dpi < 72:
        raise ValueError("render DPI must be at least 72")
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / "page"
    result = subprocess.run(
        [renderer, "-png", "-r", str(dpi), str(path), str(prefix)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftoppm could not render the PDF")


def prepare_pdf(path: Path, render_dir: Optional[Path], dpi: int) -> Dict[str, Any]:
    verify_pdf_signature(path)
    try:
        from pypdf import PdfReader
    except ImportError as error:
        raise RuntimeError("PDF input requires pypdf") from error
    try:
        reader = PdfReader(path)
        pages = []
        sections: List[Dict[str, Any]] = []
        for index, page in enumerate(reader.pages, start=1):
            text = clean_text(page.extract_text() or "")
            record = {
                "pdf_page": index,
                "text": text,
                "character_count": len(text),
            }
            pages.append(record)
            sections.extend(heading_candidates(text, index))
        metadata = {
            str(key).lstrip("/").casefold(): str(value)
            for key, value in (reader.metadata or {}).items()
            if value not in (None, "")
        }
    except Exception as error:
        raise RuntimeError(f"pypdf could not parse the PDF: {error}") from error
    if render_dir is not None:
        render_pdf(path, render_dir, dpi)
    return {
        "schema_version": 1,
        "source_type": "pdf",
        "source_path": str(path.resolve()),
        "source_access": {"state": "local-file-readable"},
        "format_verification": {
            "declared": "pdf",
            "verified": "pdf",
            "method": "PDF header plus pypdf parser open",
        },
        "metadata": metadata,
        "page_count": len(pages),
        "pages": pages,
        "located_blocks": [],
        "unlocated_blocks": [],
        "locator_summary": {
            "verified_page_blocks": 0,
            "missing_page_locator_blocks": 0,
            "invalid_page_locator_blocks": 0,
            "page_locator_reliability": "reliable",
        },
        "sections": sections,
        "evidence_inventory": evidence_from_units(pages),
        "rendered_pages_dir": str(render_dir.resolve()) if render_dir else None,
        "extraction": {
            "engine": "pypdf",
            "visual_pages_rendered": render_dir is not None,
            "confidence": "high" if pages and all(item["character_count"] >= 50 for item in pages) else "mixed",
        },
    }


def validate_bundle(bundle: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    pages = bundle.get("pages")
    page_count = bundle.get("page_count")
    unlocated = bundle.get("unlocated_blocks", [])
    if not isinstance(pages, list) or not isinstance(page_count, int) or len(pages) != page_count:
        errors.append("pages must contain exactly page_count records")
    source_type = bundle.get("source_type")
    if source_type == "pdf" and (not isinstance(page_count, int) or page_count < 1):
        errors.append("a PDF bundle must contain at least one page")
    text_units = (pages if isinstance(pages, list) else []) + (
        unlocated if isinstance(unlocated, list) else []
    )
    if not any(
        isinstance(item, dict) and int(item.get("character_count", 0)) >= 50
        for item in text_units
    ):
        errors.append("no source unit contains enough extractable text")
    metadata = bundle.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("title"):
        warnings.append("document title is unavailable")
    summary = bundle.get("locator_summary", {})
    missing = summary.get("missing_page_locator_blocks", 0) if isinstance(summary, dict) else 0
    invalid = summary.get("invalid_page_locator_blocks", 0) if isinstance(summary, dict) else 0
    if missing:
        warnings.append(f"{missing} source block(s) have no page locator")
    if invalid:
        warnings.append(f"{invalid} source block(s) have invalid page locators")
    inventory = bundle.get("evidence_inventory")
    if not isinstance(inventory, dict):
        errors.append("evidence_inventory must be an object")
    elif not any(inventory.get(key) for key in ("figures", "tables", "equations")):
        warnings.append("no figures, tables, or equations were detected")
    if errors:
        mode = "source-limited"
    elif source_type == "pdf":
        mode = "page-grounded"
    else:
        mode = "structure-grounded"
    return {
        "status": "invalid" if errors else ("valid_with_warnings" if warnings else "valid"),
        "errors": errors,
        "warnings": warnings,
        "recommended_locator_mode": mode,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    source = args.input.resolve()
    if not source.is_file():
        print(f"ERROR: input file does not exist: {source}", file=sys.stderr)
        return 2
    try:
        if source.suffix.casefold() == ".pdf":
            bundle = prepare_pdf(source, args.render_dir, args.render_dpi)
        elif source.suffix.casefold() == ".json":
            if args.render_dir is not None:
                raise ValueError("--render-dir is valid only for PDF input")
            bundle = prepare_source_map(source)
        else:
            raise ValueError("input must be a PDF or JSON source map")
        bundle["validation"] = validate_bundle(bundle)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote source bundle: {output}")
    print(f"Bundle validation: {bundle['validation']['status']}")
    print(f"Recommended locator mode: {bundle['validation']['recommended_locator_mode']}")
    for warning in bundle["validation"]["warnings"]:
        print(f"WARNING: {warning}")
    for error in bundle["validation"]["errors"]:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if bundle["validation"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
