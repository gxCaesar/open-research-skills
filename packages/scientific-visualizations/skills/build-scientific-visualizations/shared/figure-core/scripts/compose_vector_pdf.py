#!/usr/bin/env python3
"""Compose panel PDFs into a vector final figure from canonical placements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess

from pypdf import PageObject, PdfReader, PdfWriter, Transformation


MM_TO_PT = 72 / 25.4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--panel-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    spec = json.loads((root / "figure_spec.json").read_text(encoding="utf-8"))
    panel_dir = args.panel_dir.resolve() if args.panel_dir else root / "outputs" / "panels"
    output_dir = args.output_dir.resolve() if args.output_dir else root / "outputs" / "summary"
    output_dir.mkdir(parents=True, exist_ok=True)

    width_mm, height_mm = spec["composite"]["size_mm"]
    target = PageObject.create_blank_page(width=width_mm * MM_TO_PT, height=height_mm * MM_TO_PT)
    for placement in spec["composite"]["placements"]:
        panel_id = placement["panel"]
        source_path = panel_dir / f"{spec['figure_id']}{panel_id}.pdf"
        if not source_path.exists():
            raise SystemExit(f"missing panel PDF: {source_path}")
        source = PdfReader(source_path).pages[0]
        source_w = float(source.mediabox.width)
        source_h = float(source.mediabox.height)
        target_w = placement.get("w_mm", source_w / MM_TO_PT) * MM_TO_PT
        target_h = placement.get("h_mm", source_h / MM_TO_PT) * MM_TO_PT
        scale = min(target_w / source_w, target_h / source_h)
        x_pt = placement["x_mm"] * MM_TO_PT + (target_w - source_w * scale) / 2
        top_pt = placement["y_mm"] * MM_TO_PT + (target_h - source_h * scale) / 2
        y_pt = height_mm * MM_TO_PT - top_pt - source_h * scale
        target.merge_transformed_page(source, Transformation().scale(scale).translate(tx=x_pt, ty=y_pt))

    writer = PdfWriter(); writer.add_page(target)
    pdf_path = output_dir / f"{spec['figure_id']}_complete.pdf"
    with pdf_path.open("wb") as handle:
        writer.write(handle)

    if shutil.which("pdftocairo"):
        subprocess.run(["pdftocairo", "-svg", str(pdf_path), str(output_dir / f"{spec['figure_id']}_complete.svg")], check=True)
    if shutil.which("pdftoppm"):
        dpi = str(spec["journal_profile"]["dpi"])
        subprocess.run(["pdftoppm", "-png", "-r", dpi, "-singlefile", str(pdf_path), str(output_dir / f"{spec['figure_id']}_complete")], check=True)
    print(pdf_path)


if __name__ == "__main__":
    main()
