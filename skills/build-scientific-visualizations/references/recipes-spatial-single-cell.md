# Spatial and single-cell input-to-panel recipes

Use after choosing the scientific question in `domain-visualization-selection.md`.
These are plotting handoffs, not authorization to change preprocessing or inference.
Accept an existing AnnData/MuData/SpatialData object or export equivalent tidy tables;
the file extension does not establish compatible sample identities.

## Minimal inputs

| Input | Columns or equivalent fields | Grain and missingness |
|---|---|---|
| Cells/spots | `cell_id, specimen_id, section_id, condition, cell_type, x, y, coordinate_unit, included` | One object per row; preserve excluded counts and duplicated-barcode mapping |
| Assay values | `cell_id, feature_id, assay, value, layer, normalization` | Define raw counts versus normalized/log/scaled values; unmeasured is not zero |
| Specimen metadata | `specimen_id, donor_id, batch, condition, time, pairing_id` | This determines aggregation and independent units |
| Registration/ROI | `section_id, image_id, x0, y0, width, height, transform, pixel_size` | Bounds and transforms must use an explicit coordinate system |
| Cross-modal mapping | `unit_id, assay, observation_id, relationship` | Distinguish same cell, same specimen, adjacent section and computational alignment |

Before merging modalities, report input observations, unique keys, matched units,
unmatched units in each assay and final complete units. A repeated barcode from two
libraries is not the same cell. Adjacent sections are not paired cells. An inner join
can be useful, but its resulting population must be visible.

## Three useful page patterns

**Tissue → ROI → quantitative effect.** Keep the overview's physical aspect ratio and
draw the ROI in its original coordinates. Derive the crop from those bounds, not by
an independently chosen thumbnail. Display a scale bar only with calibration. Reuse
one display mapping for matched acquisitions; a normalized or independently exposed
view needs its own local key. Compute cell/spot summaries inside each specimen before
forming specimen-level contrasts. An ROI should be selected by a stated rule, not
because its signal is visually strong.

**Identity → state → abundance.** Use an embedding only as context. Lock cell-type
order across embedding keys, marker matrix and abundance summaries. Marker dot area
can encode detection fraction and colour mean expression; define threshold, layer,
whether zeros enter the mean, and any feature scaling. These choices are explicit in
the [Scanpy dotplot API](https://scanpy.readthedocs.io/en/stable/generated/scanpy.pl.dotplot.html)
(opened 2026-09-09). Give both size and colour keys. Place specimen-level state or
composition estimates nearby so pooled cell density is not mistaken for replication.

**Matched assays → concordance → null.** Align by the declared unit first, aggregate
within it, then plot paired effects for each assay. Raw RNA, protein and accessibility
intensities do not share units: use separate scales or explicitly defined standardized
effects. A common feature order is useful even when colourbars are separate. Put
cross-assay scatter beside a pairing/null control appropriate to the experimental
design; randomizing cells across donors is not a donor-level null.

## Plotting recipe

```python
# Paired summaries are supplied by the analysis, with one row per donor and condition.
wide = donor_summary.pivot(index="donor_id", columns="condition", values="estimate")
complete = wide.dropna(subset=["control", "perturbed"])
changes = complete["perturbed"] - complete["control"]
# Resample independent donors, carrying all their paired/repeated observations together.
# Do not use pooled cell count as n or silently impute a missing condition.
ax.plot([0, 1], complete[["control", "perturbed"]].to_numpy().T, color="0.75")
```

Reserve a long-label column for marker/pathway names; do not rotate thirty labels into
microscopic text. A marker matrix can occupy a wide band while its embedding stays
small. Use vector scatter and matrix cells for modest datasets. If millions of points
require selective rasterization, disclose that only the point layer is raster, retain
vector labels and axes, and verify final resolution. Do not call that export all-vector.

The [18-panel example](../examples/multimodal-18-panel/README.md) implements these
relationships using synthetic tables and Matplotlib alone. Its latent coordinates
are generated directly, not claimed to be UMAP or a validated multi-omic integration.
