# Nature-family evidence-arc calibration

Use this reference when planning a journal-wide figure sequence from published
Nature-family exemplars. It records how a bounded sample assembled visual evidence. It
does not define a house style, a required figure count, or a current submission rule.

## Read the evidence labels literally

- **Observed in the sampled papers** means that the display and its role were inspected
  in the supplied publisher PDF at the locator shown.
- **Editorial heuristic** means a conditional design choice inferred from those
  observations. Reject it when the manuscript's evidence demands another sequence.
- **Official requirement** means a current rule from the exact journal and article type.
  This reference establishes none; verify current geometry, file, image, and policy
  requirements from first-party instructions.

The calibration corpus contained 51 publisher PDFs and 1,042 PDF pages. It was heavily
weighted toward Nature Methods (23 PDFs) and Nature Communications (16); three papers
were from Nature and nine from other Nature-family titles. Forty-two inputs were
Articles, one was a Brief Communication, and the remainder were Comment, News,
Editorial, or source-limited material. Only research articles with a complete source
boundary were used for evidence-arc inference.

Use the locator form `DOI | PDF page | figure or Extended Data | observed visual job`.
PDF page is the one-based page index in the inspected file. Re-open the source before
reusing a precedent. A cited Supplementary item that was not supplied remains
`not assessed`.

## Source-located precedent index

Every empirical example used below has one canonical record here. Page ranges are
one-based indices in the inspected PDF.

| ID | Shape | DOI | PDF pages | Locator | Observed role |
|---|---|---|---|---|---|
| `visual-method-gaston` | computational-method | [10.1038/s41592-024-02503-3](https://doi.org/10.1038/s41592-024-02503-3) | 2; 10; 20 | Fig. 1; Fig. 6; ED Fig. 1 | system and downstream tasks, closing tissue application, and matched ED comparison |
| `visual-method-banksy` | computational-method | [10.1038/s41588-024-01664-3](https://doi.org/10.1038/s41588-024-01664-3) | 3; 9; 21 | Fig. 1; Fig. 6; ED Fig. 1 | feature augmentation, closing scale/runtime, and detailed ED concept |
| `visual-discovery-liver` | discovery-mechanism | [10.1038/s41586-025-08885-4](https://doi.org/10.1038/s41586-025-08885-4) | 2; 6; 12 | Fig. 1; Fig. 4; ED Fig. 1 | acquisition and patient evidence, closing morphology analysis, and ED quality control |
| `visual-discovery-aging` | discovery-mechanism | [10.1038/s43587-025-00823-3](https://doi.org/10.1038/s43587-025-00823-3) | 3; 11; 13 | Fig. 1; Fig. 7; Fig. 8 | localization, in-vivo perturbation, and closing molecular synthesis |
| `visual-translational-ten` | translational | [10.1038/s41586-024-08061-0](https://doi.org/10.1038/s41586-024-08061-0) | 2; 7; 8 | Fig. 1; Fig. 5; Fig. 6 | cohort and measurement, 14-panel preclinical intervention, and single-panel patient course |
| `visual-translational-hcc` | translational | [10.1038/s41586-025-08668-x](https://doi.org/10.1038/s41586-025-08668-x) | 3; 5; 7; 9 | Fig. 1; Fig. 3; Fig. 4; Fig. 5 | spatial association, score, cellular interpretation, and mouse perturbation |
| `visual-density-neighbourhoods` | density-counterexample | [10.1038/s41592-023-02124-2](https://doi.org/10.1038/s41592-023-02124-2) | 17 | ED Fig. 1 | two-panel robustness display with open space |
| `visual-algorithm-dlvpm` | framing-counterexample | [10.1038/s42256-025-01052-4](https://doi.org/10.1038/s42256-025-01052-4) | 2 | Fig. 1 | sparse two-panel algorithm schematic |
| `visual-comment-roadmap` | publication-form | [10.1038/s41592-024-02542-w](https://doi.org/10.1038/s41592-024-02542-w) | 1-3 | section structure; Figs. 1-2 | Comment uses framing and roadmap graphics rather than an experimental evidence arc |
| `visual-packaging-diatracer` | packaging-counterexample | [10.1038/s41467-024-55448-8](https://doi.org/10.1038/s41467-024-55448-8) | 1-14 | section structure; Figs. 1-7 | complete supplied PDF exposes main figures but no ED caption block |

## Plan a figure sequence by decisions, not by count

For every display, record two separate fields:

- `narrative_job`: orient, define the problem, explain the design, establish a
  comparison, test a mechanism, validate, delimit scope, or show an outcome;
- `decision_unlocked`: the next inference or experiment that becomes justified if this
  display supports its claim.

Then assign each panel a primary evidence role: `design`, `measurement`, `summary`,
`control`, `outcome`, or `negative result`. A schematic can explain input ->
transformation -> output, but it cannot take the role of a measurement or control.

## Conditional evidence arcs

### Computational method or analysis system

**Observed in the sampled papers:** in `visual-method-gaston` and
`visual-method-banksy`, Fig. 1 made the transformation interpretable, middle figures
tested concrete tasks, and the closing figure added a distinct application or scale
test. Their located ED examples expanded comparison or conceptual detail.

- `visual-method-gaston`: system -> tissue applications -> closing additional tissue,
  with an early matched comparison in ED.
- `visual-method-banksy`: feature augmentation -> biological tasks -> closing
  scale/runtime, with detailed conceptual explanation in ED.

**Editorial heuristic:** use a workflow-led Fig. 1 when the reader must understand the
information boundary before judging results. Let later figures answer different failure
or generalization questions. Do not repeat architecture diagrams after the data path is
clear, and do not turn a list of datasets into a visual argument.

### Biological discovery or mechanism

**Observed in the sampled papers:** in `visual-discovery-liver` and
`visual-discovery-aging`, the opening figure combined acquisition or localization with
the first biological evidence. Later displays supplied morphology-guided analysis,
in-vivo perturbation, or mechanistic synthesis.

- `visual-discovery-liver`: acquisition plus patient protein evidence ->
  morphology-guided analysis, with cohort/data quality in ED.
- `visual-discovery-aging`: localization and proximity labelling -> pathway evidence ->
  in-vivo perturbation -> molecular synthesis.

**Editorial heuristic:** mix schematic, image, quantitative summary, control, and
outcome panels only when their spatial groups preserve that evidence order. A closing
model summarizes demonstrated links and visibly marks conjectural ones; it does not
complete a missing causal step.

### Translational prediction or intervention

**Observed in the sampled papers:** in `visual-translational-ten` and
`visual-translational-hcc`, the first figure established the cohort, measurement
boundary, or initial spatial association. Middle figures developed a pathway or score,
and the closing figure showed the strongest completed animal or patient endpoint.

- `visual-translational-ten`: cohort and acquisition -> molecular comparison ->
  preclinical inhibition -> single-panel patient course.
- `visual-translational-hcc`: spatial association -> score -> cellular interpretation
  -> mouse perturbation.

**Editorial heuristic:** make cohort identity, independent unit, development-versus-
validation role, and intervention status visible at the display where they matter. The
last figure need not be dense: its job is the strongest terminal evidence, not a visual
summary of every preceding panel.

## Compose heterogeneous evidence without a collage

When a compound figure combines design, measurement images, quantitative summaries,
controls, and outcomes, preserve a readable evidence path with alignment, spacing,
thin dividers, repeated condition order, or short group labels. Panel letters identify
references; they do not create hierarchy by themselves.

High panel density is not automatically a defect. `visual-translational-ten` uses 14
panels to join cell, mouse, and treatment evidence, while
`visual-density-neighbourhoods` is a two-panel robustness display with much more open
space. Use whitespace to separate semantic groups and protect the visual anchor, not to
imitate an assumed Nature look or dilute necessary evidence.

The figure should identify its question, compared conditions, direction, and principal
readout without requiring the caption. The caption then supplies independent units,
sample counts, uncertainty and statistical tests, treatment details, scale, channel
definitions, exclusions, and boundaries that do not fit safely inside the graphic.

## Place main, Extended Data, and Supplementary evidence by function

Main versus Extended Data is an argumentative placement decision, not a chart-type or
panel-count distinction. Put the load-bearing claim path and any qualifier that changes
its meaning in main. Calibration, robustness, additional sites or cohorts, detailed
diagnostics, and explanatory expansions may sit outside main when the article form
supports that packaging and the main claim remains interpretable and honest.

The located examples show both packaging routes: `visual-method-gaston` and
`visual-method-banksy` include ED, while the complete supplied PDF for
`visual-packaging-diatracer` exposes no ED caption block. This contrast rejects a
universal packaging rule; it does not estimate frequency and is not evidence that other
supplementary material was absent.

## Counterexamples and stopping rules

- `visual-algorithm-dlvpm` shows that a pure algorithm schematic can be the correct
  Fig. 1 when the mathematical data path is the first unresolved issue; it is not a
  default for every computational biology paper.
- `visual-comment-roadmap` provides framing rather than an experimental evidence
  contract. Do not use a Comment's text-heavy conceptual layout to structure a research
  Article.
- Accepted papers vary in arrow weight, box style, density, and whitespace. Acceptance
  proves that a paper exists, not that every visual choice should be copied.
- Publisher-composed article pages cannot establish the size, font, or editable geometry
  of the authors' original figure files. Use current Official requirement and inspect the
  actual submission artifact at final insertion size.
- Exclude a PDF from pattern counts when its filename identifier, metadata, visible
  title, page continuity, or article completeness conflict. Record the mismatch instead
  of guessing which source is authoritative.

Stop using an exemplar as soon as its publication form, contribution shape, evidence
type, or decision sequence diverges from the current manuscript. The current evidence
contract outranks resemblance to an accepted figure.
