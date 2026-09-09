#!/usr/bin/env python3
"""Render a placeholder-only whole-page proof before scientific assets are drawn."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "scientific-figure-mpl")
)
os.environ.setdefault(
    "XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "scientific-figure-cache")
)
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
Path(os.environ["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)

import matplotlib as mpl

mpl.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from project_contract import layout_geometry_record, validate_v12_project


MM_PER_INCH = 25.4
GROUP_FILLS = ("#E8F0F5", "#E9F3F1", "#F7ECEA", "#F3F0E7", "#EEF0F2")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a schema-1.2 page blueprint without loading scientific assets."
    )
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    spec = load(root / "figure_spec.json")
    if spec.get("schema_version") != "1.2":
        raise SystemExit("render_layout_proof.py requires a schema 1.2 project")
    ledger = load(root / "content_ledger.json")
    manifest = load(root / "asset_manifest.json")
    errors, warnings, _ = validate_v12_project(
        root,
        spec,
        ledger,
        manifest,
        stage="layout",
    )
    if errors:
        raise SystemExit("layout proof validation failed:\n" + "\n".join(errors))

    blueprint = load(root / "layout_blueprint.json")
    geometry = layout_geometry_record(spec, blueprint)
    width_mm, height_mm = geometry["composite_size_mm"]

    panels = {panel["id"]: panel for panel in spec.get("panels", [])}
    blueprint_panels = {panel["id"]: panel for panel in blueprint.get("panels", [])}
    path_order = {
        group_id: index
        for index, group_id in enumerate(blueprint.get("reading_path", []), start=1)
    }
    group_colors = {
        group_id: GROUP_FILLS[index % len(GROUP_FILLS)]
        for index, group_id in enumerate(blueprint.get("reading_path", []))
    }
    placements = geometry["placements"]
    if len(placements) != len(panels):
        raise SystemExit("figure_spec.json: every panel requires exactly one composite placement")

    figure, axis = plt.subplots(figsize=(width_mm / MM_PER_INCH, height_mm / MM_PER_INCH))
    figure.patch.set_facecolor("white")
    axis.set_xlim(0, width_mm)
    axis.set_ylim(height_mm, 0)
    axis.set_aspect("equal", adjustable="box")
    axis.axis("off")

    anchor_id = blueprint.get("visual_anchor", {}).get("panel_id")
    for placement in placements:
        panel_id = placement.get("panel")
        panel = panels.get(panel_id)
        blueprint_panel = blueprint_panels.get(panel_id)
        if panel is None or blueprint_panel is None:
            raise SystemExit(f"layout proof: unknown placed panel {panel_id}")
        x_mm = placement.get("x_mm")
        y_mm = placement.get("y_mm")
        panel_width = placement["w_mm"]
        panel_height = placement["h_mm"]
        group_id = blueprint_panel.get("group_id")
        fill = group_colors.get(group_id, "#F4F5F6")
        linewidth = 1.4 if panel_id == anchor_id else 0.75
        edge = "#466B82" if panel_id == anchor_id else "#8A949D"
        axis.add_patch(
            Rectangle(
                (x_mm, y_mm),
                panel_width,
                panel_height,
                facecolor=fill,
                edgecolor=edge,
                linewidth=linewidth,
            )
        )
        role = str(blueprint_panel.get("evidence_role", "unspecified")).replace("_", " ")
        priority = str(blueprint_panel.get("priority", "supporting")).replace("_", " ")
        reading_position = path_order.get(group_id, "?")
        axis.text(
            x_mm + min(2.5, panel_width * 0.06),
            y_mm + min(4.0, panel_height * 0.16),
            panel_id,
            ha="left",
            va="top",
            fontsize=8.0,
            fontweight="bold",
            color="#2E3540",
        )
        axis.text(
            x_mm + panel_width / 2,
            y_mm + panel_height / 2,
            f"path {reading_position}: {group_id}\n{role}\n{priority}",
            ha="center",
            va="center",
            fontsize=6.0,
            color="#4D5863",
            linespacing=1.3,
        )
        if blueprint_panel.get("legend_owner") == panel_id:
            axis.text(
                x_mm + panel_width - min(2.5, panel_width * 0.06),
                y_mm + min(3.5, panel_height * 0.14),
                "legend",
                ha="right",
                va="top",
                fontsize=5.0,
                color="#69737E",
            )

    output = root / "outputs" / "layout"
    output.mkdir(parents=True, exist_ok=True)
    stem = output / f"{spec['figure_id']}_layout-proof"
    figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    figure.savefig(stem.with_suffix(".svg"), format="svg", facecolor="white")
    figure.savefig(stem.with_suffix(".png"), format="png", dpi=220, facecolor="white")
    plt.close(figure)
    qa_dir = root / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "layout_proof.json").write_text(
        json.dumps(geometry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "figure_id": spec["figure_id"],
                "blueprint_revision": blueprint["blueprint_revision"],
                "outputs": [
                    stem.with_suffix(".svg").relative_to(root).as_posix(),
                    stem.with_suffix(".png").relative_to(root).as_posix(),
                ],
                "warnings": warnings,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
