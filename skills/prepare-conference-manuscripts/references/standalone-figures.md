# Standalone figures

Use this route when a manuscript or proposal task includes authorized figure production.
No other skill is required. Resolve scripts from the directory containing `SKILL.md`;
the local plotting and PPTX dependencies are declared in `requirements.txt`. Installation of software is
a separate environment action, not an automatic side effect of drafting.

## Default schematic workflow: concept, then editable PPTX

For new or redesigned method, architecture, flowchart, motivation and mechanism
schematics, use a destination-style GPT Image 2.5 concept followed by native editable
PPTX reconstruction. This default applies without a separate model or format request
and does not require the visualization skill to be installed.

1. Lock the scientific objects, labels, arrows, planned-versus-observed distinction and
   insertion dimensions. Apply current destination policy and confidentiality limits.
   Inspect relevant high-quality figure examples at their actual panel locations before
   composing the concept. Extract reading order, grouping, spatial hierarchy and label
   density; adapt those composition lessons to this study rather than copying biological
   claims, data, proprietary artwork or a merely relabelled layout. If examples cannot
   be inspected, state that limitation rather than claiming example-informed design.
2. Use an available image-generation tool directly for the conceptual layout. Select
   GPT Image 2.5 when the tool exposes that selector. A built-in image tool without a
   selector remains usable: report its actual backend as unverified/unknown rather than
   claiming a verified model identity or treating the missing selector as unavailable.
   Never fabricate measured panels or send restricted material to an external service.
3. Inspect the concept and reconstruct it with an available presentation tool or
   `python-pptx`: real text boxes, shapes, connectors and semantic groups at the final
   canvas. Do not place the whole concept image on a slide and call it editable.
   Keep any permitted raster illustration distinct from labels and scientific geometry.
4. Save a new PPTX, render it with an available presentation renderer, compare with the
   concept and inspect at final size. Edit one representative label or connector in a
   copy and verify it survives reopening/rendering. Deliver the native PPTX and the
   destination-required PDF/SVG/PNG exports, plus source-data plots and full legends.

If image generation really is unavailable or prohibited, record that step as `not_run`
and continue permitted native PPTX construction. If PPTX tools or its renderer are
unavailable, retain the editable local vector source and report the exact unrun format
or render; do not silently claim SVG satisfies PPTX. A narrower explicit user request
can select a simpler route. The absence of another skill is never a tool failure.

## Source-data plots and bounded native fallback

1. Bind each panel to its question, source artifact, exact labels, units and caption.
   Keep observed results separate from planned operations. Missing source data is a real
   evidence gap; a missing visualization skill is not.
2. Use the bundled `scripts/render_evidence_figure.py` for a small observation plot,
   or a native-vector fallback where the conditions above apply. It supports one to four
   panels and consumes source CSV
   values without aggregation and emits editable-text SVG, vector PDF and a PNG preview.
   SVG is an editable master, not a native PPTX. Keep the JSON specification and CSV with
   the source. It does not replace the default schematic-to-PPTX route when those
   tools are available.
3. For error bars, clustered summaries, images, heatmaps or denser layouts, create a
   project-local plotting script from the verified analysis outputs and the actual data
   modality. Reuse the project's native analysis library. Do not reinterpret seed
   repetitions as independent samples or compute new inferential quantities while
   formatting a frozen result. Use native shapes for schematics, source images for
   microscopy and data coordinates for spatial or molecular evidence.
4. Inspect the actual render at insertion size: text, symbols, arrows, panel labels,
   units, scales, colour and source-to-caption agreement. Rework the source and rerender
   only an observed defect. Deliver the master, exports, plotting source and final legend.
   A successful command does not certify publication-quality layout.

The helper accepts a JSON specification like this synthetic example. CSV paths resolve
beside the specification; replace the example input with approved real source data:

```json
{
  "width_mm": 180,
  "height_mm": 75,
  "panels": [
    {
      "kind": "plot",
      "title": "Synthetic observations",
      "source_csv": "observations.csv",
      "x": "dose",
      "y": "response",
      "xlabel": "Dose (arbitrary units)",
      "ylabel": "Response (arbitrary units)"
    },
    {
      "kind": "diagram",
      "title": "Planned analysis",
      "nodes": [
        {"id": "input", "label": "Observed inputs", "x": 0.2, "y": 0.5},
        {"id": "output", "label": "Planned output", "x": 0.8, "y": 0.5}
      ],
      "edges": [["input", "output"]]
    }
  ]
}
```

```csv
dose,response
0,1
1,2
2,4
```

```bash
python3 "$SKILL_DIR/scripts/render_evidence_figure.py" /path/to/figure.json /path/to/figure
```

Choose a new versioned output stem; existing figure exports are not overwritten.
The helper's 8 pt text and 9 pt panel letters are portable starting values, not a
Nature-family or other venue's final typography specification. Adapt the project-local
source to current venue typography and required canvas, then inspect the actual render.
Do not certify the starter output as a finished journal figure without that work.

The helper draws observations, not confidence intervals or fitted curves. It rejects
non-finite values instead of silently dropping them. It does not validate scientific
meaning, policy, permission or caption accuracy; those remain part of the task.

## Optional specialization

When `build-scientific-visualizations` is available, its specialist layouts, scientific
modality guidance and design helpers can enhance this same default workflow. It is not
a required installation and does not gate concept generation or native PPTX production.

Read-only scope, frozen-figure authority, source integrity, destination image policy,
confidentiality and external-service approval still apply. A policy prohibition cannot
be bypassed by using the local renderer.
