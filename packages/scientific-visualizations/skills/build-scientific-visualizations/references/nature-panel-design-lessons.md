# Panel design lessons from inspected figure pages

Use when designing a Nature-family flowchart or compound figure, especially microscopy,
spatial/proteomic measurements or interventions. These are paraphrased observations and
conditional design lessons, not author-file templates or current publisher requirements.
PDF pages are one-based file pages. Reopen the original before relying on its details.

## Contents

- [Four inspected displays](#four-inspected-displays)
- [Turn a precedent into a design decision](#turn-a-precedent-into-a-design-decision)
- [Keep the caption and source data attached to the design](#keep-the-caption-and-source-data-attached-to-the-design)
- [Inspect the resulting page](#inspect-the-resulting-page)

## Four inspected displays

### diaTracer: make the transformation legible

Observed: [10.1038/s41467-024-55448-8](https://doi.org/10.1038/s41467-024-55448-8),
PDF p. 3, Fig. 1. The upper region depicts measured data dimensions, feature tracing,
precursor–fragment grouping and a resulting spectrum. The lower region connects the
output to downstream analysis. Additional DDA library data enter through a separate
branch. The caption explicitly makes the hybrid-library route conditional on DDA data.

Design lesson: allocate visual emphasis to the new transformation. Show a scientific
object changing across a stage when that is more informative than a software box.
Separate optional extra inputs from the standard path and identify the receiving
operation. Keep evidence states in the semantic contract: an explanatory spectrum
glyph is schematic unless drawn from a declared measurement. Redraw in the current
project's notation; do not copy the exemplar's logos, background or thresholds.

Use this pattern when the reader needs the input/output transformation to understand
the method. A mechanism diagram instead needs evidence-supported relationships; do
not turn its nodes into a software pipeline for visual convenience.

### HCC / TIMES: connect anatomical context to a quantitative claim

Observed: [10.1038/s41586-025-08668-x](https://doi.org/10.1038/s41586-025-08668-x),
PDF p. 5, Fig. 3. Whole-slide views flank channel-separated ROI strips with explicit
crop links. A scoring schematic follows the image block. Distributions, survival
curves, feature comparison and ROC curves occupy the lower region at different widths.

Design lesson: preserve the whole-tissue → compartment → ROI relationship before
showing the analytic summary. Give the measured image enough area to resolve the
relevant anatomy; give long labels their own allowance. Assign equal scales to genuinely
matched image comparisons and preserve channel/condition identity across the crops.
Document justified display differences rather than silently equalizing unlike assays.

The radial scoring display in this paper is an observed choice, not a default. A
coefficient strip, dot plot or small table may make a new score easier to compare.
Choose by the intended comparison and actual score definition. Never invent weights
or aggregate on the test set to reproduce the appearance of a published display.

### TEN: organize evidence by experiment and timing

Observed: [10.1038/s41586-024-08061-0](https://doi.org/10.1038/s41586-024-08061-0),
PDF p. 7, Fig. 5. The fourteen panels combine co-culture design, image fields, time
courses, mouse treatment schedules, histology and quantified outcomes. Panel c
distinguishes treatment before induction from treatment after induction. Panel k
introduces another model rather than reusing the earlier schedule. The legend defines
sampling and tests for specific panel groups. PDF p. 8, Fig. 6 instead uses a patient
course with aligned photographs and treatment timing.

Design lesson: place a model's design beside its evidence, retain the timing contrast,
and group each experiment before linking across experimental systems. Use a shared
time axis for aligned events when supported by the source. A sparse terminal figure
is appropriate when one longitudinal observation is its entire evidential job.

Do not fill a chosen panel count with extra plots. Do not combine fields, wells, mice
and patients under one n. Show repeated measurements and independent samples in ways
that remain distinguishable. A patient photograph series illustrates that patient's
course; its layout cannot establish a treatment effect or represent the full cohort.

### CyLinter: make apparent structure answer to raw evidence

Observed: [10.1038/s41592-024-02328-0](https://doi.org/10.1038/s41592-024-02328-0),
PDF p. 4, Fig. 2. Embedding, silhouette and marker heatmap occupy the top band. Tissue
examples show artifact-associated clusters in a middle band. Cell galleries and
intensity distributions supply further interpretation below. The final gallery is
explicitly contrast-adjusted; the legend describes per-channel/per-image adjustment.

Design lesson: connect an embedding or cluster score to the originating tissue and
marker distributions when claiming biological identity or QC quality. Keep the same
cluster identifiers through all views. An attractive embedding alone cannot establish
that a cluster is biological. Label image annotations separately from acquired channels.

Contrast-adjusted galleries can illustrate morphology, but independent rescaling
removes a common intensity scale. Such images cannot silently support a quantitative
intensity comparison. Preserve the processing record and raw-data quantification, and
verify the destination journal's current image policy before creating comparable views.

## Turn a precedent into a design decision

Choose the closest scientific relationship above, then adapt its principle inside the
existing page blueprint. Use the current question, data shape and independent unit to
choose the anchor and groups. Reuse the blueprint's rationale fields; no extra form is
needed. Preserve useful relationships rather than reproducing panel coordinates.

For a dense page, sketch plausible groupings before detailed rendering if the anchor
is uncertain. Prefer the arrangement in which a reader can find the condition, source
measurement, decisive comparison and necessary qualification with fewer visual jumps.
Equal small multiples remain appropriate for matched comparisons. Unequal area is
justified by information and legibility, not by a desire to appear less regular.

## Keep the caption and source data attached to the design

Assemble the panel facts alongside the blueprint: panel ID, source dataset, specimen
and ROI relation, measured or schematic status, condition, time, unit, transformation,
and the definition of a mark. Keep those facts in the existing source-data and content
records. Draft short panel descriptions early enough to expose missing denominators,
conflicting condition labels or an unexplained crop before rendering.

Spatial data need a recoverable specimen → section → ROI → cell relationship when
those levels exist. Proteomic summaries need the actual aggregation and filtering level
(for example precursor, peptide, protein, run or specimen). Preserve missingness and
normalization choices used to compute the plotted values. Do not infer independence
from the number of cells, ions or fields visible in a plot.

For manuscript handoff, supply the figure and its existing panel facts to the manuscript
skill. The manuscript owns the final legend in context; the figure and legend must agree
on labels, representative views, scales, n and uncertainty. Do not require installation
of another skill to produce a self-contained figure and factual legend draft.

## Inspect the resulting page

After the layout proof, inspect the detailed figure at final insertion width. Check
whether the distinguishing structure remains visible inside the image, whether crop
links and arrowheads resolve, and whether a comparison can be read without searching
across distant legends. A placeholder layout cannot establish these details.

Use the current scene and data to repair the problem: enlarge the relevant ROI, simplify
redundant labels, relocate the legend, or change the grouping. Do not enlarge an observed
effect, suppress an unfavorable condition, or independently stretch image intensities
to improve the story. Record only concrete remaining defects; automated checks do not
grade scientific communication or publisher acceptance.
