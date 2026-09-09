# Figure QA contract

## Scientific checks

- Match every label, symbol, arrow, value, and evidence state to the content ledger.
- Keep prospective, predicted, schematic, and observed elements distinguishable.
- Confirm that a crop retains every axis, legend, scale bar, and condition needed to
  interpret its panel claim.
- Reject any visual that implies a stronger mechanism or result than its source.

## Asset checks

For a processed bitmap, inspect crop, resolution, and unintended text. Enforce an alpha
channel, transparent border, and colour-fringe check only when the asset explicitly sets
`requires_transparency: true`; an opaque RGB micrograph is not a failed cutout. Record
source and evidence role. Real evidence keeps its provenance and never becomes a generic
decorative icon.

## Panel checks

- In `panel_set` mode, require PNG, PDF, and SVG for every panel.
- Confirm raster dimensions match physical size and DPI.
- Confirm PDF dimensions match the specification.
- Confirm SVG contains vector paths or text.
- Check minimum rendered font size, clipping, collisions, arrow attachment, and copy
  density.
- Inspect colour, grayscale, and a colour-vision-deficiency preview.

### Optional text-fit diagnostic

After changing labels or panel geometry, the canonical renderer can check actual
Matplotlib text extents against the declared text boxes before exporting each panel:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/render_matplotlib.py" <project> --check-text-bounds
```

The JSON result identifies each overflowing element and the excess in points, allowing
0.5 pt for rounding. A failing panel is not exported; existing outputs are left intact
and must not be mistaken for the failed attempt. The option never changes copy, wrapping
or font size. It is not run automatically by `run_workflow.py`.

Custom native renderers can import `text_overflow_pt(artist, bounds, renderer)` from
`render_matplotlib.py`. Call it after `figure.canvas.draw()` with a display-coordinate
Matplotlib `Bbox` and the matching canvas renderer. Register the actual text artists
and intended boxes; an empty registration proves nothing about a custom plot. This
diagnostic covers neither unregistered axes/legends, other-artist collisions, composite
rescaling nor PDF-backend glyph differences. Inspect the final export as above.

## Layout-proof checks

- Render panel boundaries, IDs, short evidence roles, reading path, legend ownership,
  and the anchor at the final page aspect ratio without scientific assets.
- Inspect question and reading-path legibility, anchor hierarchy, semantic grouping,
  whitespace, final-width allowance, shared encodings, and mechanical-grid risk.
- Record all checks in `qa/layout_review.json` and echo the current blueprint revision,
  ordered panel IDs, and selected venue width.
- Compare `qa/layout_proof.json` with the current composite size and resolved placement
  boxes.
- Treat `REVISE`, an incomplete check, a changed revision, panel-order drift, width
  drift, or geometry drift as a failed final-stage contract.

## Composite checks

- Compose from panel PDFs or a native vector scene, never from panel PNGs.
- Confirm the summary PDF page dimensions and embedded fonts.
- Confirm the summary SVG retains vector content.
- Inspect the complete page at its true aspect ratio and final print width.
- Inspect the whole composition before accepting isolated panels; a correct panel can
  still fail the page hierarchy or create a misleading cross-panel comparison.

## Source-data checks

- Require complete coverage for every data, result, negative-result, or
  claim-supporting image panel.
- Require each claim-supporting asset to bind `source_dataset_ids`; a controlled source
  cannot become externally eligible through the asset's own distribution label.
- Reconcile each visible quantitative mark with a declared portable file and plotting
  entrypoint.
- Record the independent unit, conditions, transformations, exclusions, missing values,
  estimate, and uncertainty.
- For images, record acquisition, channels, LUT, crop, registration, segmentation, and
  processing.
- Reject missing, undeclared, absolute, parent-traversing, or restricted raw files in a
  delivery candidate.

## PowerPoint checks

When `editable_pptx` is true or a PPTX is supplied, require native editable text,
arrows, dividers, and semantic marks; compare the visible text inventory with the
canonical specification; render every slide and inspect overflow. Schematics authored
through the default image-concept route require the native PPTX and its separate editing
check even when the brief did not name PowerPoint. A data-only figure, layout sketch or
explicitly chosen vector-only workflow does not acquire a PPTX requirement.

## Delivery checks

Packaging reruns full final validation and fresh QA against the current project; a stale
`qa/qa_report.json` cannot authorize delivery after a contract or output mutation. Package only
when the regenerated report is `PASS` with no errors and the schema-1.2 layout proof and review
match. A reviewer copy contains the public specification, venue and
blueprint contracts, audience-filtered source-data manifest, declared source files,
required outputs, and a plain file index. It excludes controlled raw objects, private
locators, undeclared files, internal drafting records, approval records, workflow state,
and agent metadata.
