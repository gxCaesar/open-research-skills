# Spatial multiomics atlas: advanced compound example

An original **14-panel synthetic figure**, designed as an unequal editorial composition
instead of a repeated chart grid. A large spatial anchor connects to exact ROI views;
a tall donor-by-assay matrix sits beside paired summaries and a wide boundary profile.
The lower panels retain locus context, cell composition, an invariant control, a
sign-flip null and boundary-width sensitivity.

[Vector PDF](preview/spatial-multiomics-atlas.pdf) ·
[Editable SVG](preview/spatial-multiomics-atlas.svg) ·
[PNG preview](preview/spatial-multiomics-atlas.png)

All 17,280 cells, 12 paired donor identifiers, abundance values and locus tracks are
artificial. These are plotted coordinate tables, **not microscopy, measured specimens,
an experimentally validated atlas or a discovery claim**. The synthetic intervention
and spatial programs are inserted by the generator to exercise the visual design.

## Reproduce

From the repository root, using the dependencies in the skill's `requirements.txt`:

```bash
python3 skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/render.py \
  --output /path/to/new-atlas-output
```

The script reads the bundled CSV files and exports PDF, SVG and 300-dpi PNG. It resolves
the skill's existing font-bounds helper relative to its own file, so a copied skill
directory also works from another working directory. No other skill, image model,
account, downloaded dataset or GPU is required. Editing the Python scene and rerunning
preserves editable vector marks/text; no PowerPoint handoff is claimed for this example.

To recreate the original inputs in a new directory:

```bash
python3 skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/generate.py \
  /path/to/new-synthetic-tables
python3 skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/render.py \
  --data /path/to/new-synthetic-tables --output /path/to/new-atlas-output
```

## Inputs and invariants

| Table | Grain | Contents |
|---|---|---|
| `data/cells.csv` | One synthetic cell within donor and condition | State, x/y coordinates, radial offset and six molecular values |
| `data/assays.csv` | One donor-condition-feature measurement | Ten arbitrary-unit assay summaries; complete C/P pairs |
| `data/tracks.csv` | One assay-condition-position bin | Three artificial locus tracks, explicitly not a genome assembly |
| `data/regions.csv` | One selected field/ROI | Exact donor, condition and crop coordinates |

Cross-assay comparisons join explicit donor IDs, never array positions. The reader
rejects duplicate, non-finite, missing or unmatched assay units before plotting and
requires both cell conditions for each donor. This is an example for its documented
data schema, not a general assay-import or missing-data analysis package.

The [legend](legend.md) specifies each transformation, independent unit, display scale
and null. In particular, the marker matrix scales by full cell-level feature variation
so tiny invariant-control differences are not exaggerated. Assay changes use their own
control donor SD before sharing a colour scale; they are not comparable concentrations.

## Dimensions and limitations

The canvas is **183 × 170 mm**, with 5–6.2 pt body labels, 8 pt panel letters and an
8 pt educational heading. The dimensions use the scope of the
[Nature figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
(opened 2026-09-09), not a universal Nature-family specification. This teaching
example does not assert that its long explanatory legend is ready for a particular
submission; verify the exact journal, article type and stage for a real manuscript.
Arial is used when installed; the renderer reports a DejaVu Sans fallback otherwise.

The PDF/SVG keep plots and colourbars vector, and PDF fonts are embedded. PNG is only
a preview. Page text bounds are checked automatically; scientific interpretation,
within-panel overlaps and final-size readability still require rendered inspection.
