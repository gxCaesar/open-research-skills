#!/usr/bin/env python3
"""Validate the canonical figure specification, ledger and asset registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from project_contract import is_regular_project_file, resolve_layout_profile, validate_v12_project


ELEMENT_TYPES = {"text", "round_rect", "image", "line", "arrow", "status"}
ASSET_KINDS = {"conceptual_ai", "data_render", "structure_render", "reference_image"}
EVIDENCE_ROLES = {"schematic", "claim_supporting", "decorative"}
STATUS_STATES = {"clean", "exclude", "doubt", "neutral"}
ANNOTATION_PROFILES = {"minimal", "method-readable"}
DELIVERY_MODES = {"composite", "panel_set"}
SOLID_ARROW_ROLES = {"primary", "sequence", "inference", "measured", "causal"}
DASHED_ARROW_ROLES = {"predicted", "prospective", "conditioning", "control", "parallel", "optional", "training_only"}
PANEL_KINDS = {
    "concept",
    "data",
    "result",
    "negative_result",
    "flowchart",
    "method",
    "model_architecture",
}
METHOD_KINDS = {"flowchart", "method", "model_architecture"}
TEXT_LIMITS = {
    "concept": (10, 220),
    "result": (10, 220),
    "data": (12, 240),
    "negative_result": (12, 240),
    "flowchart": (24, 420),
    "method": (24, 420),
    "model_architecture": (24, 420),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def caution(warnings: list[str], message: str) -> None:
    warnings.append(message)


def check_unit(errors: list[str], element_id: str, key: str, value: object) -> None:
    if not isinstance(value, (int, float)) or not 0 <= value <= 1:
        fail(errors, f"{element_id}: {key} must be in 0..1, got {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--stage", choices=["draft", "layout", "final"], default="draft")
    parser.add_argument(
        "--allow-missing-outputs",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    if args.allow_missing_outputs and args.stage != "final":
        parser.error("--allow-missing-outputs is only valid for the workflow's final pre-render check")
    root = args.project.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    required = [root / "figure_spec.json", root / "content_ledger.json", root / "asset_manifest.json"]
    for path in required:
        if not path.exists():
            fail(errors, f"missing {path.name}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)

    spec, ledger, manifest = (load(path) for path in required)
    schema_version = spec.get("schema_version")
    if schema_version not in {"1.0", "1.1", "1.2"}:
        fail(errors, "figure_spec.json: schema_version must be 1.0, 1.1, or 1.2")
    delivery_mode = spec.get("delivery_mode")
    if schema_version in {"1.1", "1.2"} and delivery_mode not in DELIVERY_MODES:
        fail(errors, f"figure_spec.json: delivery_mode must be one of {sorted(DELIVERY_MODES)}")
    elif schema_version == "1.0" and delivery_mode is None:
        caution(warnings, "legacy schema 1.0 has no delivery_mode; panel_set QA will be used")
    elif delivery_mode not in DELIVERY_MODES:
        fail(errors, f"figure_spec.json: invalid delivery_mode {delivery_mode!r}")
    if not isinstance(spec.get("editable_pptx", False), bool):
        fail(errors, "figure_spec.json: editable_pptx must be true or false")
    if spec.get("figure_id") != ledger.get("figure_id") or spec.get("figure_id") != manifest.get("figure_id"):
        fail(errors, "figure_id must match in specification, ledger and manifest")

    profile = spec.get("journal_profile", {})
    min_font = profile.get("min_font_pt", 5.0)
    if profile.get("dpi", 0) < 300:
        fail(errors, "journal_profile.dpi must be at least 300")
    page_width = profile.get("page_width_mm")
    if not isinstance(page_width, (int, float)) or page_width <= 0:
        fail(errors, "journal_profile.page_width_mm must be positive")

    layout_profile = spec.get("layout_profile")
    if layout_profile is not None and layout_profile != "custom":
        try:
            resolved_profile, profile_warnings = resolve_layout_profile(layout_profile)
        except ValueError as error:
            fail(errors, str(error))
        else:
            expected_width = resolved_profile["geometry"]["selected_width_mm"]
            if isinstance(page_width, (int, float)) and abs(page_width - expected_width) > 0.2:
                fail(
                    errors,
                    f"layout_profile {layout_profile} expects {expected_width:g} mm, got {page_width:g} mm",
                )
            if schema_version == "1.2":
                warnings.extend(profile_warnings)

    annotation_profile = spec.get("annotation_profile")
    if annotation_profile is not None and annotation_profile not in ANNOTATION_PROFILES:
        fail(errors, f"invalid annotation_profile {annotation_profile!r}")

    assets = spec.get("assets", {})
    registry = manifest.get("assets", {})
    for asset_id, record in assets.items():
        if record.get("kind") not in ASSET_KINDS:
            fail(errors, f"asset {asset_id}: invalid kind")
        if record.get("evidence_role") not in EVIDENCE_ROLES:
            fail(errors, f"asset {asset_id}: invalid evidence_role")
        if record.get("kind") == "conceptual_ai" and record.get("evidence_role") == "claim_supporting":
            fail(errors, f"asset {asset_id}: conceptual_ai cannot be claim_supporting")
        asset_path_value = record.get("path", "")
        asset_path = root / asset_path_value
        if asset_path.exists() and not is_regular_project_file(root, asset_path_value):
            fail(errors, f"asset {asset_id}: path must resolve to a regular non-symlink file within the project")
        elif not asset_path.exists():
            fail(errors, f"asset {asset_id}: missing file {asset_path}")
        if asset_id not in registry:
            fail(errors, f"asset {asset_id}: missing asset_manifest entry")

    panel_ids: list[str] = []
    element_ids: set[str] = set()
    for panel in spec.get("panels", []):
        panel_id = panel.get("id")
        if not panel_id or panel_id in panel_ids:
            fail(errors, f"invalid or duplicate panel id {panel_id!r}")
        panel_ids.append(panel_id)
        size = panel.get("size_mm", [])
        if len(size) != 2 or min(size) <= 0:
            fail(errors, f"panel {panel_id}: invalid size_mm")
        panel_kind = panel.get("panel_kind")
        if panel_kind is None:
            caution(warnings, f"panel {panel_id}: panel_kind is not declared")
        elif panel_kind not in PANEL_KINDS:
            fail(errors, f"panel {panel_id}: invalid panel_kind {panel_kind!r}")
        text_elements: list[dict] = []
        filled_cards: list[dict] = []
        for element in panel.get("elements", []):
            element_id = element.get("id")
            if not element_id or element_id in element_ids:
                fail(errors, f"panel {panel_id}: invalid or duplicate element id {element_id!r}")
            element_ids.add(element_id)
            element_type = element.get("type")
            if element_type not in ELEMENT_TYPES:
                fail(errors, f"{element_id}: unsupported type {element_type!r}")
                continue
            if element_type in {"text", "round_rect", "image"}:
                for key in ["x", "y", "w", "h"]:
                    check_unit(errors, element_id, key, element.get(key))
                if all(isinstance(element.get(key), (int, float)) for key in ["x", "y", "w", "h"]):
                    if element["x"] + element["w"] > 1 + 1e-9 or element["y"] + element["h"] > 1 + 1e-9:
                        fail(errors, f"{element_id}: element bounds exceed panel")
            if element_type in {"line", "arrow"}:
                for key in ["x1", "y1", "x2", "y2"]:
                    check_unit(errors, element_id, key, element.get(key))
                line_style = element.get("line_style", "solid")
                if line_style not in {"solid", "dashed"}:
                    fail(errors, f"{element_id}: line_style must be solid or dashed")
                if element_type == "arrow" and panel_kind in METHOD_KINDS and schema_version in {"1.1", "1.2"}:
                    role = element.get("role")
                    if role not in SOLID_ARROW_ROLES | DASHED_ARROW_ROLES:
                        fail(errors, f"{element_id}: flowchart-like arrow requires a valid semantic role")
                    elif role in SOLID_ARROW_ROLES and line_style != "solid":
                        fail(errors, f"{element_id}: {role} arrow must be solid")
                    elif role in DASHED_ARROW_ROLES and line_style != "dashed":
                        fail(errors, f"{element_id}: {role} arrow must be dashed")
                    redundancy = element.get("redundancy")
                    if not isinstance(redundancy, list) or not redundancy:
                        fail(errors, f"{element_id}: flowchart-like arrow requires non-colour redundancy")
            if element_type == "status":
                for key in ["x", "y", "size"]:
                    check_unit(errors, element_id, key, element.get(key))
                if element.get("state") not in STATUS_STATES:
                    fail(errors, f"{element_id}: invalid status state")
            if element_type == "text" and element.get("font_pt", 0) < min_font:
                fail(errors, f"{element_id}: font {element.get('font_pt')} pt is below {min_font} pt")
            if element_type == "text":
                text_elements.append(element)
            if element_type == "round_rect":
                fill = str(element.get("fill", "")).lower()
                area = element.get("w", 0) * element.get("h", 0)
                if fill not in {"", "none", "paper", "#ffffff", "white"} and area >= 0.06:
                    filled_cards.append(element)
                if element.get("w", 0) >= 0.92 and element.get("h", 0) >= 0.82:
                    caution(warnings, f"panel {panel_id}: full-panel frame {element_id} requires semantic justification")
            if element_type == "image" and element.get("asset") not in assets:
                fail(errors, f"{element_id}: unknown asset {element.get('asset')!r}")

        visible_strings = [str(element.get("text", "")).strip() for element in text_elements]
        visible_strings = [text for text in visible_strings if text]
        character_count = sum(len(text) for text in visible_strings)
        text_limit, character_limit = TEXT_LIMITS.get(panel_kind, (18, 360))
        if len(visible_strings) > text_limit:
            caution(
                warnings,
                f"panel {panel_id}: {len(visible_strings)} text objects exceed {panel_kind or 'legacy'} review limit {text_limit}",
            )
        if character_count > character_limit:
            caution(
                warnings,
                f"panel {panel_id}: {character_count} visible characters exceed {panel_kind or 'legacy'} review limit {character_limit}",
            )
        for text in visible_strings:
            if len(text) > 72:
                caution(warnings, f"panel {panel_id}: long visible label ({len(text)} characters): {text[:48]!r}")
        card_limit = 6 if panel_kind in METHOD_KINDS else 2
        if len(filled_cards) > card_limit:
            caution(
                warnings,
                f"panel {panel_id}: {len(filled_cards)} large filled cards exceed open-layout review limit {card_limit}",
            )

    ledger_panels = {panel.get("id") for panel in ledger.get("panels", [])}
    if set(panel_ids) != ledger_panels:
        fail(errors, f"panel IDs differ between specification {panel_ids} and ledger {sorted(ledger_panels)}")

    placement_panels = [item.get("panel") for item in spec.get("composite", {}).get("placements", [])]
    if len(placement_panels) != len(panel_ids) or set(placement_panels) != set(panel_ids):
        fail(errors, "composite placements must contain every panel exactly once")

    contract_checks: dict[str, object] = {}
    if schema_version == "1.2":
        contract_errors, contract_warnings, contract_checks = validate_v12_project(
            root,
            spec,
            ledger,
            manifest,
            stage=args.stage,
            allow_missing_outputs=args.allow_missing_outputs,
        )
        errors.extend(contract_errors)
        warnings.extend(contract_warnings)

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
    for warning in sorted(set(warnings)):
        print(f"WARNING {warning}", file=sys.stderr)
    print(
        json.dumps(
            {
                "status": "PASS",
                "panels": len(panel_ids),
                "elements": len(element_ids),
                "assets": len(assets),
                "warnings": len(set(warnings)),
                "contract_checks": contract_checks,
            }
        )
    )


if __name__ == "__main__":
    main()
