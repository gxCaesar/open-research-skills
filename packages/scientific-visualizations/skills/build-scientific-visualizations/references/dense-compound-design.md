# Designing a dense compound figure

Use for many panels/insets, heterogeneous evidence, long labels or nested comparisons.
A request for 12, 18 or 24 panels calls for deliberate page design; these are not
thresholds or recommended counts. Keep all required scientific content in the plan.
Do not default to fewer panels or a uniform grid.

## Contents

- [Evidence basis](#evidence-basis)
- [Design at three scales](#design-at-three-scales)
- [Budget space before rendering](#budget-space-before-rendering)
- [An eighteen-panel planning example](#an-eighteen-panel-planning-example)
- [Coordinate domain views](#coordinate-domain-views)
- [Render and review together](#render-and-review-together)
- [Real-image construction case](#real-image-construction-case)
- [Resolve density without losing evidence](#resolve-density-without-losing-evidence)

## Evidence basis

Observed in [TEN](https://doi.org/10.1038/s41586-024-08061-0), PDF p. 7, Fig. 5:
fourteen lettered panels combine co-culture, treatment schedules, mouse models, images
and outcomes with different widths and internal subdivisions. The adjacent patient
course, Fig. 6 on p. 8, is sparse. In
[CyLinter](https://doi.org/10.1038/s41592-024-02328-0), PDF p. 4, Fig. 2, fifteen
lettered panels use bands for summaries, artifact examples and cell galleries; many
tiles belong inside one panel. In
[HCC/TIMES](https://doi.org/10.1038/s41586-025-08668-x), PDF p. 5, Fig. 3, six
lettered panels contain multiple whole-slide views, channel strips and analytic views.

Inference: letter count does not measure visual load. A large panel can contain many
views; a small statistical panel can carry a decisive control. These are layout
observations, not publisher rules or coordinates to copy.

## Design at three scales

**Whole page:** state the question and dominant evidence. Choose the anchor that must
remain interpretable, then establish the reading route through the answer.

**Evidence groups:** organize by experimental model, biological scale or inferential
dependency. Keep each group's design, measurement and control close enough to compare.
Horizontal bands, a large anchor with side comparisons, or a central map with linked
margins may work. Choose from the evidence relations rather than a preferred shape.

**Panels and internal views:** assign panel IDs to independently referenced comparisons.
An ROI gallery may use specimen/channel labels under one letter. Do not promote every
thumbnail to a panel to meet a count or hide unrelated outcomes under one letter to
claim a crowded page is simple. Track internal views in the existing scene and source
records, not an additional manifest.

Align comparison axes, condition order and repeated objects within groups. Different
groups may need different dimensions. Reserve whitespace for a scientific transition;
avoid arbitrary blank corridors and a decorative box around every panel. Keep one
dominant entry point and supporting local anchors where needed.

## Budget space before rendering

Obtain available width and height from the selected venue contract, including
caption-dependent limits when applicable. For each region budget its letter, title,
axes/ticks, scale/channel key, legend and actual marks. The useful plotting rectangle
is what remains after these allowances.

For example, four panels in an illustrative 183 mm canvas with 2 mm outer margins and
3 mm inter-panel gutters have 42.5 mm each before axes and labels. Six have about
27.3 mm each. These are arithmetic examples, not current journal rules or proof that
a particular plot fits.

Use actual label lengths and source-image aspect ratios in a text-fit/layout sketch.
Protect a gene/pathway label column rather than budgeting it like a two-condition dot
plot. Protect the discriminating feature in microscopy and ticks/trajectories in time
courses. Plan the full page before final plots; independent panel sizes cannot decide it.

When hierarchy is uncertain, compare two materially different sketches, such as
experiment bands versus an anatomical anchor with adjacent comparisons. Choose by
reading order, comparability and final-size legibility. Do not require a second sketch
when the design choice is already resolved.

Put the selected design in the existing blueprint and coordinates in `figure_spec.json`.
The standard layout proof is a structural scaffold; it does not test real axes, labels,
image resolution or scientific readability. Inspect these during detailed rendering.

## An eighteen-panel planning example

This original illustrative allocation is not a published figure or required template.
It assumes the study supports the question "Does the spatial signal remain credible
from tissue measurement through independent and functional validation?" If those parts
do not belong to one claim, use separate figures and explain the scientific division.

| Group | Panels and distinct jobs | Allocation principle |
|---|---|---|
| Establish measurement | a, tissue overview; b, linked ROI/channel views; c, specimen/region sampling design | Wide anatomical anchor, smaller aligned context views |
| Quantify the signal | d, specimen abundance contrast; e, intensity distribution; f, spatial enrichment; g, distance profile | Matched condition order; shared value scales only when valid |
| Test independent performance | h, cohort-level effect; i, calibration; j, strongest matched comparator; k, failure slice | Space for labels and uncertainty; failure slice adjacent to gains |
| Test functional support | l, perturbation schedule; m, endpoint; n, orthogonal measurement; o, decisive null/control | Schedule introduces this experiment's samples, timing and controls |
| Delimit interpretation | p, cohort sensitivity; q, exclusion sensitivity; r, scope boundary | Compact summaries only when labels and uncertainty remain legible |

There are 3 + 4 + 4 + 4 + 3 = 18 IDs. Each needs an existing-contract record and source
coverage. Rows need not have equal height or equal columns. A long-label plot may span
a wider region; a matrix may replace repeated charts only if it preserves comparisons
and uncertainty.

Use this allocation to reason about area, not to invent effects, perturbations or
controls. If only roles are supplied, retain them as unresolved placeholders, render
the layout-only proof and state the missing sources. Do not mark absent evidence as
measured to pass final validation. Prefer the user's actual roles over this example.

## Coordinate domain views

| Evidence combination | Design choice | Preserve |
|---|---|---|
| Tissue, ROIs and cell/compartment values | Linked crop boxes, enlarged fields and nearby specimen summaries | Specimen → section → ROI → cell relation; descriptive versus inferential unit |
| Proteomic coverage, abundance and pathways | Separate coverage/missingness from abundance effects; use declared pathway order | Precursor/peptide/protein level, normalization, universe and missing values |
| Method, benchmark, ablation and failures | Enlarge the non-obvious transformation; align comparisons and keep failures beside gains | Input budget, split, metric direction, comparator, uncertainty unit |
| Perturbation, images and longitudinal outcome | Each model's schedule grouped with images and endpoint | Assignment, time, unit, control and repeated measures |
| Structure, contacts and functional assays | Source-derived structure beside contact detail and assay evidence | Coordinates, residue identity, prediction status and measured function |

Use semantic colours consistently with labels/markers/line styles as needed. Shared
category identity does not justify sharing an intensity scale. Keep channel keys local
if a distant global legend makes decoding difficult. A compact repeated key can be
better than excessive visual travel.

## Render and review together

Freeze the blueprint and common typography, encodings and spacing before final panel
production. Build panels against their allocated rectangles and assemble an early
whole-page rendering. Iterate the composite rather than approving eighteen isolated
plots and hoping they fit later.

Inspect the full-page route, each group's comparability and final-size details in one
review. Check missing labels, distant context, crop-link endpoints and panel letters.
Zoom to diagnose defects, but judge readability at actual insertion size.

Draft the legend alongside the composite. Reconcile per-panel n, image processing,
scale, uncertainty and source data during assembly. A long legend can change the
permitted height; recheck the existing venue contract before finalizing. Changed
groups or placements invalidate the previous review under the existing rules.

## Real-image construction case

An original descriptive exercise used [BBBC039v1](https://bbbc.broadinstitute.org/BBBC039):
the first twelve training-list fields in source order, with 1,287 decoded annotated
nuclei. Eighteen panels combined full images, linked crops, a fixed Otsu foreground
comparison, field summaries, nuclear distributions, a long-label descriptor matrix
and a sampling diagram on a custom 183 x 190 mm canvas. No field was removed for
quality. This was figure construction, not a held-out segmentation benchmark or a
biological-effect estimate.

The first detailed rendering exposed problems absent from its blank page sketch:

| Observed issue | Transferable repair |
|---|---|
| A long confusion-matrix row label ran outside the page despite an ample panel rectangle | Budget the row-denominator label separately from the matrix; inspect the actual exported text, not only the enclosing rectangle |
| Connecting F01–F12 formed apparent trajectories although the field IDs were unordered | Connect the two measurements within each field; do not invent a sequence between unrelated fields |
| Precision/recall points occupied one corner of a full 0–1 scatter plot | Use explicit tighter axis limits that retain every point; a scatter plot need not inherit a zero-based bar-chart convention |
| Open coral points were ambiguous beside panels using coral for the diagnostic field | Read the producer: these points encoded boundary-touching nuclei. Add a local shape-and-text key; shared colour alone cannot define the variable |
| Computed heatmaps were raster images inside otherwise vector exports | Draw matrix cells as vector meshes or rectangles; a PDF extension does not prove that plots are vector |

The descriptor matrix retained full labels, including "Median nucleus mean raw
intensity", with a separate label column and an explicit within-descriptor display
scale. The image example was the first selected field, while the diagnostic example
was deterministically the lowest-IoU field, not an asserted representative. All image
views shared a declared display mapping; measurements used original intensities.

The sampling diagram also needed two views: all image pixels include background,
whereas only reference-foreground pixels belong inside annotated nuclei. Keep these
denominators distinct from field-level summaries. No micrometre calibration was
available, so none was invented. These are concrete construction lessons, not fixed
panel counts, font sizes or analysis recipes for another study.

## Resolve density without losing evidence

First remove redundant labels and decorative containers, consolidate genuinely shared
legends, and reallocate area. Consider common axes or matrices where they improve the
actual comparison. Keep independent units and uncertainty visible.

If required content still cannot fit, identify the exact panels and readability
constraint. Propose a scientific split or main/Extended Data division that preserves
the claim and decisive control, respecting the user's deliverable and current venue
rules. Do not silently remove panels, bury negative evidence, shrink type below the
required size or flatten into a bitmap. Success means the evidence can be read.
