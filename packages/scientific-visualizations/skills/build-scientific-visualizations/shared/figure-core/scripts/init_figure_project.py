#!/usr/bin/env python3
"""Initialize a single-source scientific figure project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from project_contract import load_venue_profiles, resolve_layout_profile


SKILL_ROOT = Path(__file__).resolve().parent.parent
MODES = {
    "layout-sketch",
    "flowchart",
    "compound-figure",
    "conference-figure-set",
    "journal-figure-set",
}


def parse_args() -> argparse.Namespace:
    registry = load_venue_profiles()
    profiles = sorted(set(registry["profiles"]) | set(registry["legacy_aliases"]) | {"custom"})
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--page-width-mm", type=float)
    parser.add_argument(
        "--layout-profile",
        choices=profiles,
        default="nature-double",
    )
    parser.add_argument("--mode", choices=sorted(MODES), default="compound-figure")
    parser.add_argument("--annotation-profile", choices=["minimal", "method-readable"], default="minimal")
    parser.add_argument("--delivery-mode", choices=["composite", "panel_set"], default="composite")
    parser.add_argument("--dpi", type=int, default=500)
    parser.add_argument("--diagram-style", help="Optional diagram family from assets/diagram-styles.json")
    parser.add_argument("--palette", help="Palette ID; infers the family when --diagram-style is absent")
    return parser.parse_args()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_diagram_style(style_id: str | None, palette_id: str | None) -> dict | None:
    if style_id is None and palette_id is None:
        return None
    catalog = json.loads((SKILL_ROOT / "assets" / "diagram-styles.json").read_text(encoding="utf-8"))
    if style_id is not None and style_id not in catalog["styles"]:
        raise SystemExit(f"unknown diagram style: {style_id}")
    if palette_id is not None and palette_id not in catalog["palettes"]:
        raise SystemExit(f"unknown diagram palette: {palette_id}")
    if palette_id is None:
        palette_id = catalog["styles"][style_id]["default_palette"]
    palette = catalog["palettes"][palette_id]
    if style_id is not None and style_id != palette["style_id"]:
        raise SystemExit(f"palette {palette_id} belongs to {palette['style_id']}, not {style_id}")
    colors = json.loads((SKILL_ROOT / "assets" / "palette.json").read_text(encoding="utf-8"))
    colors.update(catalog["neutrals"])
    colors.update(palette["colors"])
    return {"diagram_style": palette["style_id"], "palette_id": palette_id, "colors": colors}


def main() -> None:
    args = parse_args()
    root = args.output.resolve()
    diagram_style = resolve_diagram_style(args.diagram_style, args.palette)
    if diagram_style is not None and (root / "figure_spec.json").exists():
        raise SystemExit("style selection requires a new project; existing figure_spec.json was not changed")
    layout_profile = args.layout_profile
    if layout_profile == "custom":
        if args.page_width_mm is None or args.page_width_mm <= 0:
            raise SystemExit("custom layout requires a positive --page-width-mm")
        page_width_mm = args.page_width_mm
        venue_contract = {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "profile_id": "custom",
            "target_context": "custom",
            "journal": None,
            "article_type": "custom",
            "submission_stage": "custom",
            "authority": {
                "title": "Author-defined custom canvas",
                "url": None,
                "checked_date": None,
                "scope": "Custom geometry; not a publisher requirement.",
            },
            "authority_status": "custom",
            "geometry": {"selected_width_mm": page_width_mm, "max_height_mm": None},
            "technical": {
                "font_family": "Arial",
                "text_range_pt": [5.0, 8.0],
                "min_resolution_dpi": args.dpi,
                "colour_space": "RGB",
                "preferred_formats": ["PDF", "SVG", "PNG"],
            },
        }
    else:
        venue_contract, profile_warnings = resolve_layout_profile(layout_profile)
        expected = venue_contract["geometry"]["selected_width_mm"]
        if args.page_width_mm is not None and abs(args.page_width_mm - expected) > 0.001:
            raise SystemExit(
                f"layout profile {layout_profile} fixes width at {expected:g} mm; "
                "use --layout-profile custom for another width"
            )
        page_width_mm = expected
        venue_contract["schema_version"] = "1.2"
        venue_contract["figure_id"] = args.figure_id
        for warning in profile_warnings:
            print(f"WARNING {warning}", file=sys.stderr)
    for relative in [
        "assets/source",
        "assets/processed",
        "assets/manifest",
        "outputs/panels",
        "outputs/layout",
        "outputs/summary",
        "outputs/notebooks",
        "outputs/pptx/individual",
        "qa",
        "qa/private",
        "scripts",
        "source-data/files",
        "dist",
    ]:
        (root / relative).mkdir(parents=True, exist_ok=True)

    starter = json.loads((SKILL_ROOT / "assets" / "starter-spec.json").read_text(encoding="utf-8"))
    starter["figure_id"] = args.figure_id
    starter["delivery_mode"] = args.delivery_mode
    starter["mode"] = args.mode
    starter["editable_pptx"] = False
    starter["layout_profile"] = layout_profile
    starter["annotation_profile"] = args.annotation_profile
    starter["journal_profile"]["page_width_mm"] = page_width_mm
    starter["journal_profile"]["dpi"] = args.dpi
    starter["panels"][0]["id"] = "a"
    if args.mode == "flowchart":
        starter["panels"][0]["panel_kind"] = "flowchart"
        starter["panels"][0]["title"] = "Replace with a source-anchored method stage"
        starter["panels"][0]["elements"][1]["text"] = "Replace with a source-anchored method stage"
    starter["panels"][0]["size_mm"][0] = page_width_mm
    starter["composite"]["size_mm"][0] = page_width_mm
    if diagram_style is not None:
        starter["style"] = diagram_style
        for element in starter["panels"][0]["elements"]:
            if element["id"] == "a-divider":
                element["color"] = "primary_stroke"
    write_json(root / "figure_spec.json", starter)

    write_json(
        root / "content_ledger.json",
        {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "source_files": [],
            "claims": [
                {
                    "id": "claim-a",
                    "panel_id": "a",
                    "claim": "Replace with the source-anchored panel claim.",
                    "source_anchors": [],
                    "evidence_status": "schematic",
                    "prohibited_implications": [],
                }
            ],
            "panels": [
                {
                    "id": "a",
                    "claim_ids": ["claim-a"],
                    "claim": "Replace with the source-anchored panel claim.",
                    "source_anchors": [],
                    "required_objects": [],
                    "evidence_status": "schematic",
                    "wet_data": None,
                    "decisive_control": None,
                    "prohibited_implications": [],
                }
            ],
        },
    )
    write_json(
        root / "asset_manifest.json",
        {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "assets": {},
            "ai_disclosure_required": False,
        },
    )
    write_json(root / "venue_contract.json", venue_contract)
    write_json(
        root / "layout_blueprint.json",
        {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "blueprint_revision": 1,
            "mode": args.mode,
            "question": "What inference must this complete figure support?",
            "narrative_job": "Replace with the scientific job of the complete page.",
            "decision_unlocked": "Replace with the decision supported by the complete page.",
            "reading_path": ["primary-evidence"],
            "visual_anchor": {
                "panel_id": "a",
                "reason": "The starter panel is the only declared evidence unit.",
            },
            "groups": [
                {
                    "id": "primary-evidence",
                    "panels": ["a"],
                    "role": "design",
                    "emphasis": "primary",
                }
            ],
            "panels": [
                {
                    "id": "a",
                    "group_id": "primary-evidence",
                    "evidence_role": "design",
                    "priority": "anchor",
                    "preferred_aspect": "wide",
                    "shared_scale_group": None,
                    "legend_owner": "a",
                    "source_data_required": False,
                }
            ],
            "shared_scale_groups": [],
            "layout_rationale": "The starter uses one full-width schematic panel; revise before claim-bearing drawing.",
        },
    )
    write_json(
        root / "source_data_manifest.json",
        {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "datasets": [],
            "delivery_outputs": [
                {
                    "path": f"outputs/layout/{args.figure_id}_layout-proof.svg",
                    "audiences": ["author"],
                    "content_scope": "layout_proof",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/layout/{args.figure_id}_layout-proof.png",
                    "audiences": ["author"],
                    "content_scope": "layout_proof",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/summary/{args.figure_id}_complete.pdf",
                    "audiences": ["author"],
                    "content_scope": "complete_figure",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/summary/{args.figure_id}_complete.svg",
                    "audiences": ["author"],
                    "content_scope": "complete_figure",
                    "contains_controlled_visual_content": False,
                },
            ],
            "panels": [
                {
                    "panel_id": "a",
                    "coverage": "not_applicable",
                    "dataset_ids": [],
                    "supports": [],
                    "reason": "Starter panel is a non-claim-bearing schematic placeholder.",
                }
            ],
        },
    )
    write_json(
        root / "qa" / "layout_review.json",
        {
            "schema_version": "1.2",
            "figure_id": args.figure_id,
            "status": "REVISE",
            "reviewed_blueprint_revision": 1,
            "ordered_panel_ids": ["a"],
            "selected_width_mm": page_width_mm,
            "checks": {
                "question_and_reading_path": "not_reviewed",
                "anchor_and_hierarchy": "not_reviewed",
                "grouping_and_whitespace": "not_reviewed",
                "final_width_allowance": "not_reviewed",
                "shared_encodings": "not_reviewed",
                "mechanical_grid_risk": "not_reviewed",
                "semantic_coverage": "not_reviewed"
            },
            "notes": "Review the layout proof and change status to PASS only after all checks pass."
        },
    )
    if args.mode == "flowchart":
        write_json(
            root / "flowchart_spec.json",
            {
                "schema_version": "1.2",
                "figure_id": args.figure_id,
                "flowcharts": [
                    {
                        "flowchart_id": "method-a",
                        "panel_id": "a",
                        "stages": [
                            {
                                "id": "starter-stage",
                                "semantic_role": "schematic_stage",
                                "label": "Replace with a source-anchored method stage",
                                "content_anchor": "claim-a",
                                "visual_element_ids": ["a-title", "a-status"],
                                "formula_refs": [],
                                "pictogram": {
                                    "kind": "generic-placeholder",
                                    "meaning": "schematic stage placeholder",
                                    "evidence_status": "schematic",
                                    "source_anchor": "claim-a"
                                }
                            }
                        ],
                        "edges": [],
                        "formulas": [],
                    }
                ],
            },
        )
    (root / "source-data" / "README.md").write_text(
        "# Figure source data\n\nPlace only declared, reviewer-safe portable files in `files/`.\n",
        encoding="utf-8",
    )
    if diagram_style is None:
        shutil.copy2(SKILL_ROOT / "assets" / "palette.json", root / "palette.json")
    else:
        write_json(root / "palette.json", diagram_style["colors"])
    print(root)


if __name__ == "__main__":
    main()
