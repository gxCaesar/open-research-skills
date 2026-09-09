#!/usr/bin/env python3
"""Render canonical figure_spec.json panels with Matplotlib."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
from typing import Optional

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
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.text import Text
from matplotlib.transforms import Bbox
from PIL import Image


MM_PER_INCH = 25.4


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def color(colors: dict[str, str], value: Optional[str], fallback: str = "#000000") -> str:
    if value in {None, "none"}:
        return "none"
    return colors.get(value, value or fallback)


def image_extent(element: dict, image: Image.Image, panel_w: float, panel_h: float) -> tuple[float, float, float, float]:
    x, y, w, h = (element[key] for key in ["x", "y", "w", "h"])
    if element.get("fit", "contain") != "contain":
        return x, x + w, 1 - y - h, 1 - y
    image_aspect = image.width / image.height
    panel_aspect = panel_w / panel_h
    fitted_h = w * panel_aspect / image_aspect
    if fitted_h <= h:
        draw_w, draw_h = w, fitted_h
    else:
        draw_h = h
        draw_w = h * image_aspect / panel_aspect
    cx, cy_top = x + w / 2, y + h / 2
    return cx - draw_w / 2, cx + draw_w / 2, 1 - cy_top - draw_h / 2, 1 - cy_top + draw_h / 2


def add_text(ax, element: dict, colors: dict[str, str], family: str) -> Text:
    x, y, w, h = (element[key] for key in ["x", "y", "w", "h"])
    align, valign = element.get("align", "left"), element.get("valign", "center")
    xpos = {"left": x, "center": x + w / 2, "right": x + w}[align]
    ypos = {"top": 1 - y, "center": 1 - y - h / 2, "bottom": 1 - y - h}[valign]
    return ax.text(
        xpos,
        ypos,
        element.get("text", ""),
        ha=align,
        va=valign,
        fontsize=element["font_pt"],
        fontfamily=family,
        fontweight="bold" if element.get("bold") else "normal",
        color=color(colors, element.get("color", "ink")),
        linespacing=element.get("linespacing", 1.1),
        zorder=element.get("z", 20),
    )


def text_overflow_pt(artist: Text, bounds: Bbox, renderer) -> dict[str, float]:
    """Compare a drawn text artist with a display-coordinate box; allow 0.5 pt rounding.

    Call after ``figure.canvas.draw()``. Custom renderers may supply their own
    transformed boxes. This does not check other artists, page composition or
    exported PDF glyphs, and never changes the artist or its source text.
    """
    if not artist.get_visible() or not artist.get_text().strip():
        return {}
    actual = artist.get_window_extent(renderer)
    pixels_per_pt = renderer.points_to_pixels(1.0)
    distances = {
        "left": bounds.x0 - actual.x0,
        "right": actual.x1 - bounds.x1,
        "bottom": bounds.y0 - actual.y0,
        "top": actual.y1 - bounds.y1,
    }
    return {
        edge: round(distance / pixels_per_pt, 3)
        for edge, distance in distances.items()
        if distance / pixels_per_pt > 0.5
    }


def add_status(ax, element: dict, colors: dict[str, str], panel_w: float, panel_h: float) -> None:
    states = {
        "clean": ("teal_pale", "teal", "tick"),
        "exclude": ("coral_pale", "coral", "cross"),
        "doubt": ("gold_pale", "gold", "?"),
        "neutral": ("gray_pale", "guide", "line"),
    }
    fill, stroke, symbol = states[element["state"]]
    diameter_x = element["size"]
    diameter_y = diameter_x * panel_w / panel_h
    cx, cy = element["x"], 1 - element["y"]
    ax.add_patch(Ellipse((cx, cy), diameter_x, diameter_y, facecolor=color(colors, fill), edgecolor=color(colors, stroke), linewidth=0.7, zorder=20))
    if symbol == "tick":
        ax.plot([cx - 0.22 * diameter_x, cx - 0.05 * diameter_x, cx + 0.26 * diameter_x], [cy, cy - 0.18 * diameter_y, cy + 0.22 * diameter_y], color=color(colors, stroke), linewidth=0.8, zorder=21)
    elif symbol == "cross":
        ax.plot([cx - 0.20 * diameter_x, cx + 0.20 * diameter_x], [cy - 0.20 * diameter_y, cy + 0.20 * diameter_y], color=color(colors, stroke), linewidth=0.8, zorder=21)
        ax.plot([cx - 0.20 * diameter_x, cx + 0.20 * diameter_x], [cy + 0.20 * diameter_y, cy - 0.20 * diameter_y], color=color(colors, stroke), linewidth=0.8, zorder=21)
    elif symbol == "line":
        ax.plot([cx - 0.22 * diameter_x, cx + 0.22 * diameter_x], [cy, cy], color=color(colors, stroke), linewidth=0.8, zorder=21)
    else:
        ax.text(cx, cy, "?", ha="center", va="center", fontsize=6, fontweight="bold", color=color(colors, stroke), zorder=21)


def render_panel(root: Path, spec: dict, panel: dict, output_dir: Path, *, check_text_bounds: bool = False) -> dict:
    profile, colors = spec["journal_profile"], spec["style"]["colors"]
    panel_w, panel_h = panel["size_mm"]
    dpi = profile["dpi"]
    family = profile.get("font_family", "Arial")
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": [family, "Helvetica", "DejaVu Sans"], "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "savefig.bbox": None, "savefig.pad_inches": 0})
    fig, ax = plt.subplots(figsize=(panel_w / MM_PER_INCH, panel_h / MM_PER_INCH), dpi=dpi)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=color(colors, panel.get("background", "paper")), edgecolor="none", zorder=0))
    text_artists = []
    for element in panel.get("elements", []):
        kind = element["type"]
        if kind == "text":
            artist = add_text(ax, element, colors, family)
            text_artists.append((element, artist))
        elif kind == "round_rect":
            ax.add_patch(FancyBboxPatch(
                (element["x"], 1 - element["y"] - element["h"]), element["w"], element["h"],
                boxstyle=f"round,pad=0.003,rounding_size={element.get('radius', 0.012)}",
                facecolor=color(colors, element.get("fill", "paper")), edgecolor=color(colors, element.get("stroke", "hairline")),
                linewidth=element.get("stroke_pt", 0.7), alpha=element.get("alpha", 1.0), zorder=element.get("z", 2),
            ))
        elif kind == "image":
            record = spec["assets"][element["asset"]]
            path = root / record["path"]
            with Image.open(path) as pil:
                rgba = pil.convert("RGBA")
                extent = image_extent(element, rgba, panel_w, panel_h)
                ax.imshow(rgba, extent=extent, interpolation="lanczos", aspect="auto", zorder=element.get("z", 8))
        elif kind == "line":
            ax.plot(
                [element["x1"], element["x2"]],
                [1 - element["y1"], 1 - element["y2"]],
                color=color(colors, element.get("color", "ink")),
                linewidth=element.get("stroke_pt", 0.8),
                linestyle="--" if element.get("line_style", "solid") == "dashed" else "-",
                zorder=element.get("z", 10),
            )
        elif kind == "arrow":
            ax.add_patch(FancyArrowPatch(
                (element["x1"], 1 - element["y1"]), (element["x2"], 1 - element["y2"]),
                arrowstyle="-|>", mutation_scale=element.get("head_size", 8), color=color(colors, element.get("color", "ink")),
                linewidth=element.get("stroke_pt", 0.8),
                linestyle="--" if element.get("line_style", "solid") == "dashed" else "-",
                connectionstyle=f"arc3,rad={element.get('curve', 0)}", zorder=element.get("z", 10),
            ))
        elif kind == "status":
            add_status(ax, element, colors, panel_w, panel_h)
    report = {"checked": 0, "violations": []}
    if check_text_bounds:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for element, artist in text_artists:
            if not artist.get_text().strip():
                continue
            report["checked"] += 1
            box = Bbox.from_bounds(element["x"], 1 - element["y"] - element["h"], element["w"], element["h"])
            overflow = text_overflow_pt(artist, ax.transData.transform_bbox(box), renderer)
            if overflow:
                report["violations"].append({
                    "panel_id": panel["id"], "element_id": element["id"], "overflow_pt": overflow,
                })
        if report["violations"]:
            plt.close(fig)
            return report
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{spec['figure_id']}{panel['id']}"
    for extension in ["png", "pdf", "svg"]:
        fig.savefig(output_dir / f"{stem}.{extension}", dpi=dpi, facecolor="white")
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--panel")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--check-text-bounds", action="store_true",
        help="check actual text against its declared box before export; does not establish visual acceptance",
    )
    args = parser.parse_args()
    root = args.project.resolve()
    spec = load(root / "figure_spec.json")
    output_dir = args.output_dir.resolve() if args.output_dir else root / "outputs" / "panels"
    panels = [panel for panel in spec["panels"] if not args.panel or panel["id"] == args.panel]
    if not panels:
        raise SystemExit(f"panel not found: {args.panel}")
    report = {"status": "PASS", "scope": "declared_text_boxes", "checked": 0, "violations": []}
    for panel in panels:
        panel_report = render_panel(root, spec, panel, output_dir, check_text_bounds=args.check_text_bounds)
        report["checked"] += panel_report["checked"]
        report["violations"].extend(panel_report["violations"])
        if not args.check_text_bounds:
            print(f"PASS {panel['id']}")
    if args.check_text_bounds:
        if report["violations"]:
            report["status"] = "FAIL"
        elif not report["checked"]:
            report["status"] = "NOT_APPLICABLE"
        print(json.dumps(report))
        raise SystemExit(1 if report["violations"] else 0)


if __name__ == "__main__":
    main()
