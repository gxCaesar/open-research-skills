#!/usr/bin/env python3
"""Run asset, raster, vector and packaging QA for a figure project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader

from project_contract import validate_v12_project

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional diagnostic dependency
    np = None


MM_TO_PT = 72 / 25.4
PPTX_NAMESPACES = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
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


def pixels(image: Image.Image):
    getter = getattr(image, "get_flattened_data", None)
    return getter() if getter else image.getdata()


def load_json_object(path: Path) -> dict[str, object]:
    """Return an object for QA reporting after the contract validator records parse errors."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def fonts_not_embedded(pdffonts_stdout: str):
    """Font names whose `emb` column is not yes, or None when no font rows were listed.

    The previous check looked for "TrueType" or "Type 1" anywhere in the output, which is
    the type column, not the embedding column: a PDF whose only font is
    `Helvetica / Type 1 / emb=no` reported as embedded.
    """
    rows = [line for line in pdffonts_stdout.splitlines()[2:] if line.strip()]
    if not rows:
        return None
    missing = []
    for row in rows:
        fields = row.split()
        if len(fields) < 5:
            continue
        if fields[-5].lower() != "yes":     # columns end: emb sub uni object ID
            missing.append(fields[0])
    return missing


def inspect_pptx(archive: zipfile.ZipFile) -> dict[str, object]:
    slide_names = sorted(
        name
        for name in archive.namelist()
        if name.startswith("ppt/slides/slide") and name.endswith(".xml")
    )
    texts: list[str] = []
    object_names: list[str] = []
    native_shapes = 0
    for slide_name in slide_names:
        root = ET.fromstring(archive.read(slide_name))
        texts.extend(node.text or "" for node in root.findall(".//a:t", PPTX_NAMESPACES))
        object_names.extend(
            node.attrib.get("name", "")
            for node in root.findall(".//p:cNvPr", PPTX_NAMESPACES)
        )
        native_shapes += len(root.findall(".//p:sp", PPTX_NAMESPACES))
    return {
        "slides": len(slide_names),
        "texts": texts,
        "object_names": object_names,
        "native_shapes": native_shapes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--pptx", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    spec = json.loads((root / "figure_spec.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "asset_manifest.json").read_text(encoding="utf-8"))
    delivery_mode = spec.get("delivery_mode", "panel_set")
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, object] = {}
    qa_dir = root / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    if delivery_mode not in {"composite", "panel_set"}:
        errors.append(f"invalid delivery_mode: {delivery_mode!r}")
    checks["delivery_mode"] = delivery_mode

    if spec.get("schema_version") == "1.2":
        ledger = json.loads((root / "content_ledger.json").read_text(encoding="utf-8"))
        contract_errors, contract_warnings, contract_checks = validate_v12_project(
            root,
            spec,
            ledger,
            manifest,
            stage="final",
        )
        errors.extend(contract_errors)
        warnings.extend(contract_warnings)
        blueprint = load_json_object(root / "layout_blueprint.json")
        venue = load_json_object(root / "venue_contract.json")
        review = load_json_object(root / "qa" / "layout_review.json")
        geometry_receipt_path = root / "qa" / "layout_proof.json"
        geometry_receipt = load_json_object(geometry_receipt_path) or None
        proof_stem = root / "outputs" / "layout" / f"{spec['figure_id']}_layout-proof"
        proof_paths = [proof_stem.with_suffix(".svg"), proof_stem.with_suffix(".png")]
        missing_proofs = [path.relative_to(root).as_posix() for path in proof_paths if not path.is_file()]
        if missing_proofs:
            errors.append("missing layout proof: " + ", ".join(missing_proofs))
        proof_png_size = None
        if proof_paths[1].is_file():
            try:
                with Image.open(proof_paths[1]) as proof_image:
                    proof_png_size = proof_image.size
                    proof_image.verify()
                expected_aspect = spec["composite"]["size_mm"][0] / spec["composite"]["size_mm"][1]
                actual_aspect = proof_png_size[0] / proof_png_size[1]
                if abs(actual_aspect - expected_aspect) / expected_aspect > 0.02:
                    errors.append("layout proof PNG aspect ratio does not match the composite page")
            except (OSError, UnidentifiedImageError):
                errors.append("layout proof PNG cannot be opened as a valid image")
        if proof_paths[0].is_file():
            proof_svg = proof_paths[0].read_text(encoding="utf-8", errors="ignore")
            if "<svg" not in proof_svg or not any(token in proof_svg for token in ("<path", "<rect", "<text")):
                errors.append("layout proof SVG has no inspectable vector content")
        checks["layout"] = {
            "proof_paths": [path.relative_to(root).as_posix() for path in proof_paths],
            "proofs_present": not missing_proofs,
            "proof_png_pixels": proof_png_size,
            "blueprint_revision": blueprint.get("blueprint_revision"),
            "reviewed_blueprint_revision": review.get("reviewed_blueprint_revision"),
            "ordered_panel_ids": review.get("ordered_panel_ids"),
            "selected_width_mm": venue.get("geometry", {}).get("selected_width_mm"),
            "geometry_receipt": geometry_receipt,
            "contract_checks": contract_checks,
        }

    annotation_checks = {}
    for panel in spec.get("panels", []):
        panel_id = panel["id"]
        panel_kind = panel.get("panel_kind")
        text_elements = [element for element in panel.get("elements", []) if element.get("type") == "text"]
        visible_strings = [str(element.get("text", "")).strip() for element in text_elements]
        visible_strings = [text for text in visible_strings if text]
        character_count = sum(len(text) for text in visible_strings)
        longest = max(visible_strings, key=len, default="")
        large_filled_cards = []
        full_panel_frames = []
        for element in panel.get("elements", []):
            if element.get("type") != "round_rect":
                continue
            fill = str(element.get("fill", "")).lower()
            area = element.get("w", 0) * element.get("h", 0)
            if fill not in {"", "none", "paper", "#ffffff", "white"} and area >= 0.06:
                large_filled_cards.append(element.get("id"))
            if element.get("w", 0) >= 0.92 and element.get("h", 0) >= 0.82:
                full_panel_frames.append(element.get("id"))
        text_limit, character_limit = TEXT_LIMITS.get(panel_kind, (18, 360))
        if len(visible_strings) > text_limit:
            warnings.append(
                f"panel {panel_id}: {len(visible_strings)} text objects exceed {panel_kind or 'legacy'} review limit {text_limit}"
            )
        if character_count > character_limit:
            warnings.append(
                f"panel {panel_id}: {character_count} visible characters exceed {panel_kind or 'legacy'} review limit {character_limit}"
            )
        if len(longest) > 72:
            warnings.append(f"panel {panel_id}: longest visible label has {len(longest)} characters")
        card_limit = 6 if panel_kind in METHOD_KINDS else 2
        if len(large_filled_cards) > card_limit:
            warnings.append(
                f"panel {panel_id}: {len(large_filled_cards)} large filled cards exceed open-layout review limit {card_limit}"
            )
        if full_panel_frames:
            warnings.append(f"panel {panel_id}: full-panel frames require semantic justification")
        annotation_checks[panel_id] = {
            "panel_kind": panel_kind or "legacy_unspecified",
            "text_objects": len(visible_strings),
            "visible_characters": character_count,
            "longest_label_characters": len(longest),
            "large_filled_cards": large_filled_cards,
            "full_panel_frames": full_panel_frames,
        }
    checks["annotation_density"] = annotation_checks

    asset_checks = {}
    for asset_id, record in spec.get("assets", {}).items():
        path = root / record["path"]
        if not path.exists():
            errors.append(f"missing asset: {asset_id}")
            continue
        registry = manifest.get("assets", {}).get(asset_id, {})
        requires_transparency = bool(
            record.get("requires_transparency", registry.get("requires_transparency", False))
        )
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            bbox = alpha.getbbox()
            border = list(pixels(alpha.crop((0, 0, rgba.width, 1)))) + list(pixels(alpha.crop((0, rgba.height - 1, rgba.width, rgba.height)))) + list(pixels(alpha.crop((0, 0, 1, rgba.height)))) + list(pixels(alpha.crop((rgba.width - 1, 0, rgba.width, rgba.height))))
            opaque_border = sum(value > 20 for value in border)
            visible = sum(value > 20 for value in pixels(alpha))
            visible_ratio = visible / (rgba.width * rgba.height)
            neon_green = sum(1 for r, g, b, a in pixels(rgba) if a > 20 and g > 150 and r < 100 and b < 100)
            if requires_transparency and "A" not in image.getbands():
                errors.append(f"{asset_id}: no alpha channel")
            if requires_transparency and opaque_border:
                errors.append(f"{asset_id}: {opaque_border} opaque border pixels")
            if requires_transparency and neon_green:
                errors.append(f"{asset_id}: {neon_green} possible chroma fringe pixels")
            if max(rgba.size) < 600: errors.append(f"{asset_id}: long edge below 600 px")
            if visible_ratio < 0.01: warnings.append(f"{asset_id}: very low visible-content ratio")
            asset_checks[asset_id] = {"size": rgba.size, "bbox": bbox, "visible_ratio": round(visible_ratio, 4), "requires_transparency": requires_transparency, "opaque_border": opaque_border if requires_transparency else None, "green_fringe": neon_green if requires_transparency else None}
        if record.get("kind") == "conceptual_ai":
            for key in ["prompt", "model", "generated_at"]:
                if not registry.get(key): warnings.append(f"{asset_id}: manifest missing {key}")
    checks["assets"] = asset_checks

    dpi = spec["journal_profile"]["dpi"]
    panel_checks = {}
    for panel in spec["panels"]:
        panel_id = panel["id"]
        stem = root / "outputs" / "panels" / f"{spec['figure_id']}{panel_id}"
        derivatives = [stem.with_suffix(ext) for ext in [".png", ".pdf", ".svg"]]
        present = [item for item in derivatives if item.exists()]
        missing = [str(item) for item in derivatives if not item.exists()]
        if delivery_mode == "composite" and not present:
            panel_checks[panel_id] = {"status": "not_required_for_composite"}
            continue
        if missing:
            errors.extend(f"missing panel output: {item}" for item in missing)
            continue
        with Image.open(stem.with_suffix(".png")) as image:
            expected = tuple(round(mm / 25.4 * dpi) for mm in panel["size_mm"])
            if any(abs(actual - target) > 2 for actual, target in zip(image.size, expected)):
                errors.append(f"panel {panel_id}: PNG size {image.size} != {expected}")
            actual_pixels = image.size
        pdf_page = PdfReader(stem.with_suffix(".pdf")).pages[0]
        pdf_size = (float(pdf_page.mediabox.width), float(pdf_page.mediabox.height))
        expected_pdf = tuple(mm * MM_TO_PT for mm in panel["size_mm"])
        if any(abs(actual - target) > 0.5 for actual, target in zip(pdf_size, expected_pdf)):
            errors.append(f"panel {panel_id}: PDF page size mismatch")
        svg_text = stem.with_suffix(".svg").read_text(encoding="utf-8", errors="ignore")
        if "<path" not in svg_text and "<text" not in svg_text:
            errors.append(f"panel {panel_id}: SVG has no vector content")
        panel_checks[panel_id] = {"png_pixels": actual_pixels, "pdf_points": pdf_size}
    checks["panels"] = panel_checks

    summary_pdf = root / "outputs" / "summary" / f"{spec['figure_id']}_complete.pdf"
    if summary_pdf.exists():
        page = PdfReader(summary_pdf).pages[0]
        actual = (float(page.mediabox.width), float(page.mediabox.height))
        expected = tuple(mm * MM_TO_PT for mm in spec["composite"]["size_mm"])
        if any(abs(a - e) > 0.5 for a, e in zip(actual, expected)): errors.append("summary PDF page size mismatch")
        # Record whether this ran, not only its result. Without Poppler the font check simply
        # does not happen, and a report that omits it is indistinguishable from one where the
        # fonts were fine -- the same shape as a check that reports zero because it never ran.
        fonts = "not_checked"
        if shutil.which("pdffonts"):
            result = subprocess.run(["pdffonts", str(summary_pdf)], capture_output=True, text=True, check=False)
            if result.returncode != 0:
                # A tool that failed reports nothing, and nothing used to read as "no fonts
                # detected" -- a run failure written down as a measurement.
                fonts = "check_failed"
                warnings.append(f"font check did not run: pdffonts exited {result.returncode}")
            else:
                unembedded = fonts_not_embedded(result.stdout)
                if unembedded is None:
                    fonts = "no_fonts_listed"
                    warnings.append("summary PDF lists no fonts")
                elif unembedded:
                    fonts = "not_embedded"
                    warnings.append("summary PDF has fonts that are not embedded: "
                                    + ", ".join(sorted(unembedded)))
                else:
                    fonts = "embedded"
        else:
            warnings.append("font embedding not checked: pdffonts not on PATH (install Poppler)")
        checks["summary"] = {"pdf_points": actual, "fonts": fonts}
    else:
        errors.append("missing vector summary PDF")

    summary_svg = root / "outputs" / "summary" / f"{spec['figure_id']}_complete.svg"
    if summary_svg.exists():
        svg_text = summary_svg.read_text(encoding="utf-8", errors="ignore")
        if "<path" not in svg_text and "<text" not in svg_text:
            errors.append("summary SVG has no vector content")
        checks.setdefault("summary", {})["svg_vector_content"] = "<path" in svg_text or "<text" in svg_text
    else:
        errors.append("missing vector summary SVG")

    summary_png = root / "outputs" / "summary" / f"{spec['figure_id']}_complete.png"
    if summary_png.exists():
        with Image.open(summary_png) as source:
            diagnostic = source.convert("RGB")
            diagnostic.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            diagnostic.convert("L").save(qa_dir / f"{spec['figure_id']}_complete_grayscale.png")
            if np is not None:
                array = np.asarray(diagnostic, dtype=np.float32) / 255.0
                matrix = np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]], dtype=np.float32)
                simulated = np.clip(array @ matrix.T, 0, 1)
                Image.fromarray((simulated * 255).astype(np.uint8)).save(qa_dir / f"{spec['figure_id']}_complete_deuteranopia.png")
            else:
                warnings.append("numpy unavailable; deuteranopia preview not generated")
    else:
        warnings.append("summary PNG unavailable; accessibility previews not generated")

    pptx = args.pptx.resolve() if args.pptx else root / "outputs" / "pptx" / f"{spec['figure_id']}_editable.pptx"
    pptx_required = bool(args.pptx or spec.get("editable_pptx", False))
    if pptx.exists():
        with zipfile.ZipFile(pptx) as archive:
            inventory = inspect_pptx(archive)
        slide_count = inventory["slides"]
        minimum = 1 if delivery_mode == "composite" else len(spec["panels"])
        if slide_count < minimum: errors.append(f"PPTX has {slide_count} slides; expected at least {minimum}")
        expected_text = [
            str(element.get("text", ""))
            for panel in spec.get("panels", [])
            for element in panel.get("elements", [])
            if element.get("type") == "text" and str(element.get("text", ""))
        ]
        actual_text = inventory["texts"]
        missing_text = [text for text in expected_text if text not in actual_text]
        if missing_text:
            errors.append(f"PPTX text inventory missing {len(missing_text)} canonical string(s): {missing_text[:3]}")
        expected_native_ids = [
            str(element.get("id"))
            for panel in spec.get("panels", [])
            for element in panel.get("elements", [])
            if element.get("type") != "image" and element.get("id")
        ]
        object_names = inventory["object_names"]
        missing_native = [element_id for element_id in expected_native_ids if element_id not in object_names]
        if missing_native:
            errors.append(f"PPTX is missing {len(missing_native)} named native object(s): {missing_native[:3]}")
        if expected_native_ids and inventory["native_shapes"] == 0:
            errors.append("PPTX contains no native editable shapes for canonical non-image elements")
        if delivery_mode == "panel_set" and spec.get("editable_pptx", False):
            for panel in spec.get("panels", []):
                individual = root / "outputs" / "pptx" / "individual" / f"{spec['figure_id']}{panel['id']}_editable.pptx"
                if not individual.exists():
                    errors.append(f"missing individual-panel PPTX: {individual}")
        checks["pptx"] = {
            "slides": slide_count,
            "native_shapes": inventory["native_shapes"],
            "canonical_text_strings": len(expected_text),
            "canonical_native_objects": len(expected_native_ids),
        }
    elif pptx_required:
        errors.append(f"PPTX not found: {pptx}")
    else:
        warnings.append("editable PPTX not requested; PPTX QA skipped")

    report = {"status": "PASS" if not errors else "FAIL", "errors": errors, "warnings": sorted(set(warnings)), "checks": checks}
    (qa_dir / "qa_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "errors": len(errors), "warnings": len(report["warnings"])}))
    if errors: raise SystemExit(1)


if __name__ == "__main__":
    main()
