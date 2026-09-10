#!/usr/bin/env python3
"""Create a validated figure handoff with a plain file index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any
import zipfile

from PIL import Image
from pypdf import PdfReader

from project_contract import (
    declared_output_files,
    declared_source_files,
    is_private_locator,
    is_regular_project_file,
)


AUTHOR_TOP_LEVEL = [
    "figure_spec.json",
    "content_ledger.json",
    "asset_manifest.json",
    "palette.json",
    "venue_contract.json",
    "layout_blueprint.json",
    "source_data_manifest.json",
    "flowchart_spec.json",
    "AI_DISCLOSURE.txt",
]
REVIEWER_TOP_LEVEL = [
    "figure_spec.json",
    "content_ledger.json",
    "asset_manifest.json",
    "palette.json",
    "venue_contract.json",
    "layout_blueprint.json",
    "source_data_manifest.json",
    "flowchart_spec.json",
    "AI_DISCLOSURE.txt",
]
ALLOWED_SUFFIXES = {
    ".png",
    ".pdf",
    ".svg",
    ".pptx",
    ".ipynb",
    ".json",
    ".txt",
    ".md",
    ".py",
    ".mjs",
    ".csv",
    ".tsv",
    ".xlsx",
}
IGNORED_NAMES = {".DS_Store", "__pycache__"}
INTERNAL_NAME_PARTS = {"prompt", "approval", "pipeline_state", "agent_instruction", "automation_trace"}
PUBLIC_TEXT_PATTERNS = [
    re.compile(r'"prompt(?:_record)?"\s*:', re.IGNORECASE),
    re.compile(r"approval[ _-]?receipt", re.IGNORECASE),
    re.compile(r"pipeline[ _-]?state", re.IGNORECASE),
    re.compile(r"agent[ _-]?instruction", re.IGNORECASE),
    re.compile("sha" + "256", re.IGNORECASE),
    re.compile("check" + "sum", re.IGNORECASE),
    re.compile(r"/(?:Users|home|private/var)/"),
    re.compile(r"[A-Za-z]:\\(?:Users|Documents)\\", re.IGNORECASE),
]


def clean_public_json(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            lowered = key.lower()
            if lowered in {"prompt", "prompt_record"} or "sha" + "256" in lowered or "check" + "sum" in lowered:
                continue
            cleaned[key] = clean_public_json(item)
        return cleaned
    if isinstance(value, list):
        return [clean_public_json(item) for item in value]
    return value


def include(relative: Path, audience: str, delivery_mode: str, include_panel_derivatives: bool) -> bool:
    if any(part in IGNORED_NAMES for part in relative.parts):
        return False
    if relative.name.endswith(".inspect.ndjson") or relative.suffix not in ALLOWED_SUFFIXES:
        return False
    lowered_parts = [part.lower() for part in relative.parts]
    if audience in {"reviewer", "public"} and any(
        any(term in part for term in INTERNAL_NAME_PARTS) for part in lowered_parts
    ):
        return False
    if delivery_mode == "composite" and not include_panel_derivatives:
        if len(relative.parts) >= 2 and relative.parts[0:2] == ("outputs", "panels"):
            return False
        if len(relative.parts) >= 3 and relative.parts[0:3] == ("outputs", "pptx", "individual"):
            return False
    return True


def require_project_ready(root: Path, spec: dict[str, Any]) -> None:
    if spec.get("schema_version") == "1.2":
        figure_id = spec["figure_id"]
        proof_paths = [
            root / "outputs" / "layout" / f"{figure_id}_layout-proof.svg",
            root / "outputs" / "layout" / f"{figure_id}_layout-proof.png",
        ]
        if any(not path.is_file() for path in proof_paths):
            raise SystemExit("layout proof is required before packaging")

    validator = subprocess.run(
        [
            sys.executable,
            "-B",
            str(Path(__file__).resolve().parent / "validate_figure_project.py"),
            str(root),
            "--stage",
            "final",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if validator.returncode != 0:
        details = (validator.stderr + validator.stdout).strip()
        raise SystemExit("full final validation failed before packaging:\n" + details)

    qa_run = subprocess.run(
        [
            sys.executable,
            "-B",
            str(Path(__file__).resolve().parent / "qa_figure.py"),
            str(root),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if qa_run.returncode != 0:
        qa_path = root / "qa" / "qa_report.json"
        details = []
        if qa_path.is_file():
            try:
                qa_payload = json.loads(qa_path.read_text(encoding="utf-8"))
                details.extend(str(error) for error in qa_payload.get("errors", []))
            except (OSError, json.JSONDecodeError):
                pass
        if not details:
            details.append((qa_run.stderr + qa_run.stdout).strip() or "QA process failed")
        raise SystemExit("fresh QA failed before packaging:\n" + "\n".join(details))
    qa_path = root / "qa" / "qa_report.json"
    if not qa_path.is_file():
        raise SystemExit("qa/qa_report.json is required before packaging")
    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    if qa.get("status") != "PASS" or qa.get("errors"):
        raise SystemExit("qa_report.json must be PASS with no errors before packaging")

    figure_id = spec["figure_id"]
    required = [
        root / "outputs" / "summary" / f"{figure_id}_complete.pdf",
        root / "outputs" / "summary" / f"{figure_id}_complete.svg",
    ]
    if spec.get("editable_pptx", False):
        required.append(root / "outputs" / "pptx" / f"{figure_id}_editable.pptx")
    if spec.get("delivery_mode", "panel_set") == "panel_set":
        for panel in spec.get("panels", []):
            panel_id = panel["id"]
            stem = root / "outputs" / "panels" / f"{figure_id}{panel_id}"
            required.extend(stem.with_suffix(suffix) for suffix in (".png", ".pdf", ".svg"))
            if spec.get("editable_pptx", False):
                required.append(root / "outputs" / "pptx" / "individual" / f"{figure_id}{panel_id}_editable.pptx")
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("required delivery files are missing:\n" + "\n".join(missing))


def source_manifest_for_audience(payload: dict[str, Any], audience: str) -> dict[str, Any]:
    """Return a delivery view without records unavailable to the audience."""

    eligible = {
        dataset.get("id")
        for dataset in payload.get("datasets", [])
        if isinstance(dataset, dict) and audience in dataset.get("audiences", [])
    }
    result = clean_public_json(payload)
    result["datasets"] = [
        dataset
        for dataset in result.get("datasets", [])
        if dataset.get("id") in eligible
    ]
    result["delivery_outputs"] = [
        record
        for record in result.get("delivery_outputs", [])
        if audience in record.get("audiences", [])
    ]
    for panel in result.get("panels", []):
        original_ids = panel.get("dataset_ids", [])
        panel["dataset_ids"] = [dataset_id for dataset_id in original_ids if dataset_id in eligible]
        if panel.get("coverage") in {"complete", "partial"} and not panel["dataset_ids"]:
            raise SystemExit(
                f"source-data panel {panel.get('panel_id')} has no {audience}-eligible dataset"
            )
    return result


def asset_is_eligible(
    record: dict[str, Any],
    audience: str,
    source_manifest: dict[str, Any],
) -> bool:
    distribution = record.get("distribution")
    if distribution == "controlled_access":
        return False
    if audience == "author":
        return True
    audiences = record.get("audiences", [])
    eligible_distributions = {"public", "shareable"}
    if audience == "reviewer":
        eligible_distributions.add("reviewer")
    if audience not in audiences and distribution not in eligible_distributions:
        return False
    source_ids = record.get("source_dataset_ids", [])
    if record.get("evidence_role") == "claim_supporting" and not source_ids:
        return False
    datasets = {
        dataset.get("id"): dataset
        for dataset in source_manifest.get("datasets", [])
        if isinstance(dataset, dict) and dataset.get("id")
    }
    for dataset_id in source_ids:
        dataset = datasets.get(dataset_id)
        if dataset is None or dataset.get("availability") in {"controlled_access", "not_applicable"}:
            return False
        if audience not in dataset.get("audiences", []):
            return False
    return True


def figure_spec_for_audience(
    payload: dict[str, Any],
    asset_manifest: dict[str, Any],
    source_manifest: dict[str, Any],
    audience: str,
) -> dict[str, Any]:
    """Remove file locators for assets not distributed to this audience."""

    result = clean_public_json(payload)
    registry = asset_manifest.get("assets", {})
    for asset_id, record in result.get("assets", {}).items():
        manifest_record = registry.get(asset_id, {})
        if not asset_is_eligible(manifest_record, audience, source_manifest):
            record.pop("path", None)
            record["delivery_status"] = f"not_included_for_{audience}"
    return result


def asset_manifest_for_audience(
    payload: dict[str, Any],
    source_manifest: dict[str, Any],
    audience: str,
) -> dict[str, Any]:
    """Remove file locators for assets not distributed to this audience."""

    result = clean_public_json(payload)
    for record in result.get("assets", {}).values():
        if not asset_is_eligible(record, audience, source_manifest):
            record.pop("path", None)
    return result


def declared_asset_files(
    root: Path,
    spec: dict[str, Any],
    asset_manifest: dict[str, Any],
    source_manifest: dict[str, Any],
    audience: str,
) -> list[Path]:
    """Select only explicitly distributable schema-1.2 processed assets."""

    result = []
    registry = asset_manifest.get("assets", {})
    for asset_id, spec_record in spec.get("assets", {}).items():
        record = registry.get(asset_id, {})
        if not asset_is_eligible(record, audience, source_manifest):
            continue
        path_value = record.get("path") or spec_record.get("path")
        if not isinstance(path_value, str):
            continue
        path = Path(path_value)
        if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "assets":
            raise SystemExit(f"asset {asset_id}: unsafe project-relative path {path_value!r}")
        source = root / path
        if source.exists() and not is_regular_project_file(root, path_value):
            raise SystemExit(
                f"asset {asset_id}: path must resolve to a regular non-symlink file within the project"
            )
        if source.is_file():
            result.append(source)
    return result


def scan_external_copy(output: Path, source_manifest: dict[str, Any]) -> None:
    findings = []
    output_records = {
        record.get("path"): record
        for record in source_manifest.get("delivery_outputs", [])
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }
    text_suffixes = {
        ".json",
        ".txt",
        ".md",
        ".py",
        ".mjs",
        ".ipynb",
        ".svg",
        ".csv",
        ".tsv",
    }

    def inspect_text(label: str, text: str) -> None:
        if is_private_locator(text):
            findings.append(f"{label}: private locator")
            return
        for pattern in PUBLIC_TEXT_PATTERNS:
            if pattern.search(text):
                findings.append(f"{label}: prohibited internal metadata")
                return

    def inspect_zip(path: Path, relative: str) -> None:
        try:
            with zipfile.ZipFile(path) as archive:
                for member in archive.namelist():
                    if member.endswith((".xml", ".rels", ".txt", ".csv", ".tsv")):
                        inspect_text(
                            f"{relative}:{member}",
                            archive.read(member).decode("utf-8", errors="ignore"),
                        )
        except zipfile.BadZipFile:
            findings.append(f"{relative}: invalid ZIP-based document")

    def inspect_pdf(path: Path, relative: str) -> None:
        inspect_text(relative, path.read_bytes().decode("latin-1", errors="ignore"))
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                findings.append(f"{relative}: encrypted PDF cannot be externally audited")
                return
            metadata = reader.metadata or {}
            inspect_text(f"{relative}:metadata", "\n".join(str(value) for value in metadata.values()))
            if getattr(reader, "attachments", None):
                findings.append(f"{relative}: embedded PDF attachment is not allowed")
            for page_number, page in enumerate(reader.pages, start=1):
                if output_records.get(relative, {}).get("content_scope") == "quantitative_only":
                    try:
                        if len(page.images) > 0:
                            findings.append(
                                f"{relative}: quantitative-only PDF must not contain image XObjects"
                            )
                    except Exception as error:
                        findings.append(
                            f"{relative}: could not audit PDF image objects ({type(error).__name__})"
                        )
                for annotation_ref in page.get("/Annots", []):
                    annotation = annotation_ref.get_object()
                    inspect_text(
                        f"{relative}:page-{page_number}-annotation",
                        str(annotation),
                    )
        except Exception as error:  # pypdf exposes several parse-specific exception types
            findings.append(f"{relative}: unreadable PDF ({type(error).__name__})")

    def inspect_png(path: Path, relative: str) -> None:
        try:
            with Image.open(path) as image:
                metadata_text = "\n".join(
                    str(value) for value in image.info.values() if isinstance(value, (str, bytes))
                )
                inspect_text(f"{relative}:metadata", metadata_text)
        except Exception as error:
            findings.append(f"{relative}: unreadable PNG ({type(error).__name__})")

    for path in output.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(output).as_posix()
        if path.suffix in text_suffixes:
            text = path.read_text(encoding="utf-8", errors="ignore")
            inspect_text(relative, text)
            if (
                path.suffix == ".svg"
                and output_records.get(relative, {}).get("content_scope") == "quantitative_only"
                and re.search(r"<(?:[A-Za-z0-9_-]+:)?image\b", text, flags=re.IGNORECASE)
            ):
                findings.append(f"{relative}: quantitative-only SVG must not contain image elements")
        elif path.suffix in {".pptx", ".xlsx"}:
            inspect_zip(path, relative)
        elif path.suffix == ".pdf":
            inspect_pdf(path, relative)
        elif path.suffix == ".png":
            inspect_png(path, relative)
    if findings:
        raise SystemExit("external-facing package is not clean:\n" + "\n".join(findings))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--audience", choices=["author", "reviewer", "public"], default="author")
    parser.add_argument("--include-panel-derivatives", action="store_true")
    args = parser.parse_args()
    root = args.project.resolve()
    spec = json.loads((root / "figure_spec.json").read_text(encoding="utf-8"))
    require_project_ready(root, spec)
    schema_12 = spec.get("schema_version") == "1.2"
    asset_manifest = json.loads((root / "asset_manifest.json").read_text(encoding="utf-8"))
    source_manifest = (
        json.loads((root / "source_data_manifest.json").read_text(encoding="utf-8"))
        if schema_12
        else None
    )

    output = args.output.resolve() if args.output else root / "dist" / f"{spec['figure_id']}_{args.audience}_delivery"
    if output.exists() and not args.overwrite:
        raise SystemExit(f"output exists; pass --overwrite to replace it: {output}")
    # --overwrite calls rmtree, so refuse any target that contains the project it is packaging.
    # Pointing --output at the project, or at its parent, deleted the source and every sibling
    # beside it, and only then failed with "source data does not exist". A delete whose blast
    # radius is decided by an unchecked argument is not an option flag.
    if output == root or output in root.parents:
        raise SystemExit(
            f"refusing to write the package into {output}: it contains the project at {root}. "
            "--overwrite deletes the output directory first, which would delete the source.")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    top_level = AUTHOR_TOP_LEVEL if args.audience == "author" else REVIEWER_TOP_LEVEL
    candidates: list[Path] = []
    for name in top_level:
        path = root / name
        if path.exists():
            candidates.append(path)
    directories: list[Path] = []
    if not schema_12:
        directories.insert(0, root / "assets" / "processed")
    else:
        candidates.extend(
            declared_asset_files(
                root,
                spec,
                asset_manifest,
                source_manifest or {},
                args.audience,
            )
        )
        if source_manifest is not None:
            try:
                candidates.extend(declared_source_files(root, source_manifest, audience=args.audience))
            except ValueError as error:
                raise SystemExit(str(error)) from error
            if args.audience in {"reviewer", "public"}:
                try:
                    candidates.extend(
                        declared_output_files(root, source_manifest, audience=args.audience)
                    )
                except ValueError as error:
                    raise SystemExit(str(error)) from error
            source_readme = root / "source-data" / "README.md"
            if source_readme.is_file():
                candidates.append(source_readme)
    if args.audience == "author":
        directories.extend([root / "outputs", root / "scripts", root / "qa"])
    for directory in directories:
        if directory.exists():
            candidates.extend(
                path
                for path in directory.rglob("*")
                if path.is_file()
                and include(
                    path.relative_to(root),
                    args.audience,
                    spec.get("delivery_mode", "panel_set"),
                    args.include_panel_derivatives,
                )
            )

    file_index = []
    for source in sorted(set(candidates)):
        relative = source.relative_to(root)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if args.audience in {"reviewer", "public"} and source.suffix == ".json":
            payload = json.loads(source.read_text(encoding="utf-8"))
            if relative == Path("source_data_manifest.json"):
                payload = source_manifest_for_audience(payload, args.audience)
            elif relative == Path("asset_manifest.json"):
                payload = asset_manifest_for_audience(
                    payload,
                    source_manifest or {},
                    args.audience,
                )
            elif relative == Path("figure_spec.json"):
                payload = figure_spec_for_audience(
                    payload,
                    asset_manifest,
                    source_manifest or {},
                    args.audience,
                )
            else:
                payload = clean_public_json(payload)
            target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            shutil.copy2(source, target)
        file_index.append({"path": relative.as_posix(), "size_bytes": target.stat().st_size})

    (output / "delivery_index.json").write_text(
        json.dumps({"figure_id": spec["figure_id"], "audience": args.audience, "files": file_index}, indent=2) + "\n",
        encoding="utf-8",
    )
    if args.audience in {"reviewer", "public"}:
        try:
            scan_external_copy(output, source_manifest or {})
        except SystemExit:
            shutil.rmtree(output)
            raise
    print(output)


if __name__ == "__main__":
    main()
