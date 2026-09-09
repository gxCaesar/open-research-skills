#!/usr/bin/env python3
"""Render a small source-data figure or native vector schematic, without another skill."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys


def render(spec_path, output):
    if any(output.with_suffix(suffix).exists() for suffix in (".svg", ".pdf", ".png")):
        raise FileExistsError("output exists; choose a new output stem to preserve the prior figure")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    panels = spec["panels"]
    if not 1 <= len(panels) <= 4:
        raise ValueError("use one to four panels; author a custom layout for denser figures")
    width, height = float(spec["width_mm"]), float(spec["height_mm"])
    if not all(math.isfinite(v) and v > 0 for v in (width, height)):
        raise ValueError("canvas dimensions must be positive and finite")
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42,
                         "font.size": 8, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, len(panels), squeeze=False,
                             figsize=(width / 25.4, height / 25.4), layout="constrained")
    try:
        for index, (ax, panel) in enumerate(zip(axes[0], panels)):
            ax.set_title(panel["title"], loc="left", fontsize=8)
            if panel["kind"] == "plot":
                source = spec_path.parent / panel["source_csv"]
                with source.open(newline="", encoding="utf-8") as stream:
                    rows = list(csv.DictReader(stream))
                x = [float(row[panel["x"]]) for row in rows]
                y = [float(row[panel["y"]]) for row in rows]
                if not x or not all(math.isfinite(v) for v in x + y):
                    raise ValueError("source values must be nonempty and finite")
                # Show observations only; do not silently aggregate units or infer uncertainty.
                ax.scatter(x, y, s=16, color="#0072B2", marker="o")
                ax.set_xlabel(panel["xlabel"])
                ax.set_ylabel(panel["ylabel"])
            elif panel["kind"] == "diagram":
                ax.set(xlim=(0, 1), ylim=(0, 1))
                ax.set_axis_off()
                nodes = {node["id"]: node for node in panel["nodes"]}
                if not nodes or len(nodes) != len(panel["nodes"]):
                    raise ValueError("diagram nodes need unique IDs")
                for node in nodes.values():
                    if not all(math.isfinite(node[k]) and 0 <= node[k] <= 1 for k in ("x", "y")):
                        raise ValueError("diagram coordinates must be finite and between 0 and 1")
                boxes = {}
                for node in nodes.values():
                    text = ax.text(node["x"], node["y"], node["label"], ha="center", va="center",
                                   bbox={"boxstyle": "round,pad=0.4", "facecolor": "#EAF2F8",
                                         "edgecolor": "#0072B2", "linewidth": 0.6})
                    boxes[node["id"]] = text.get_bbox_patch()
                for start, end in panel["edges"]:
                    a, b = nodes[start], nodes[end]
                    ax.annotate("", xy=(b["x"], b["y"]), xytext=(a["x"], a["y"]),
                                arrowprops={"arrowstyle": "->", "color": "#555555",
                                            "patchA": boxes[start], "patchB": boxes[end],
                                            "shrinkA": 2, "shrinkB": 2})
            else:
                raise ValueError("panel kind must be plot or diagram")
            if len(panels) > 1:
                ax.text(-0.10, 1.08, chr(97 + index), transform=ax.transAxes,
                        weight="bold", fontsize=9)
        output.parent.mkdir(parents=True, exist_ok=True)
        # Keep the declared canvas; no tight crop that changes insertion dimensions.
        for suffix in (".svg", ".pdf", ".png"):
            fig.savefig(output.with_suffix(suffix), dpi=300)
    finally:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON specification; CSV paths resolve beside it")
    parser.add_argument("output", type=Path, help="output stem for SVG, PDF, and PNG")
    args = parser.parse_args()
    try:
        render(args.spec.resolve(), args.output)
    except (ValueError, KeyError, TypeError, OSError, ImportError) as exc:
        print(f"figure failed: {exc}", file=sys.stderr)
        return 1
    print("Rendered SVG, PDF, and PNG; inspect at final size before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
