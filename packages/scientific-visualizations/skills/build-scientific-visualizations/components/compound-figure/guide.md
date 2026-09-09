# Compound-Figure Mode Reference

Build one complete figure from a single canonical scene. Keep measured evidence,
source-derived images, schematic explanation, and optional conceptual artwork visibly
distinct. A compact open-white layout is the default, not a substitute for the
scientific reading path.

## Ownership boundary

- Select this mode for one complete compound figure or graphical abstract.
- Select `flowchart` for one standalone workflow, mechanism, or model diagram.
- Select `journal-figure-set` to coordinate all main, Extended Data, and Supplementary
  figures in one manuscript.

When a compound figure contains a flowchart-like panel, apply the flowchart semantic
arrow and notation rules to that panel before composing the full figure.
For new or redesigned conceptual method, architecture, motivation or mechanism panels,
also use the default [image concept to editable PPTX route](../../references/image-concept-to-vector.md).
Keep measured panels on their real-data route and combine source-faithful vector exports
at the approved page geometry; do not generate the evidence-bearing composite as an image.

## Shared implementation

Resolve `../../shared/figure-core/` relative to this guide. That directory is the
only implementation of project initialization, schema validation, Matplotlib rendering,
vector composition, QA, and reviewer packaging. Read these shared references before
authoring:

- `references/figure-spec-schema.md`
- `references/scientific-integrity-rules.md`
- `references/layout-and-annotation-profiles.md`
- `references/visual-contract.md`
- `references/qa-contract.md`

Keep the package directory intact so these relative paths remain valid.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## 1. Establish the content contract

Read the manuscript passage, caption, prior figure, analysis outputs, plotting code, and
source images that establish the figure. Complete `content_ledger.json` before drawing.
For every panel record:

- the exact claim and source anchor;
- required objects, comparisons, labels, and controls;
- whether each element is observed, predicted, prospective, schematic, or decorative;
- any wet-lab or real-data boundary;
- prohibited implications and the decisive control.

Do not choose between scientifically different interpretations for visual convenience.
If the source does not resolve a claim, mark the uncertainty or request the minimum
clarification before placing that claim-bearing element.

## 2. Initialize the venue and project contracts

Choose the current venue width before layout. Use a dated profile that names its
journal, article type, submission stage, source URL, and checked date. The old
`nature-single`, `nature-protocols`, and `nature-double` aliases remain readable but are
unverified and cannot pass a final journal-submission gate. Current destination-journal
instructions override the bundled snapshots.

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <project> \
  --figure-id <id> --mode compound-figure --layout-profile <dated-profile> \
  --annotation-profile minimal --delivery-mode composite
```

Use `figure_spec.json` as the only source of visible copy, coordinates, dimensions,
colours, and asset placement. Use `panel_set` only when separately reusable panels are
required. Make a disposable layout-only sketch first when panel hierarchy or reading
order is unclear; do not treat that sketch as evidence or a submission artifact.

## 3. Design the visual argument

Assign each panel one primary evidence role: design or schematic, measurement, summary
or result, control, outcome, or negative result. Record flowchart, method, and model
architecture as design subtypes when applicable. Use a claim-led title, a clear reading
path, and the smallest label set needed to decode the evidence. The visual should expose
the question, comparison, direction, and principal readout; the caption supplies sample,
statistical, treatment, scale, and boundary details.

Keep category identity redundant in grayscale: pair colour with marker, line style,
hatch, shape, or a direct label in charts and diagrams. For channel-based measurement
images, use a local channel key, direct labels, or separate channel views; do not overlay
synthetic chart marks on the measured field. Use filled regions only when they encode a
real group, compartment, or state. Author at final physical size and never rely on
`bbox_inches="tight"` to repair geometry.

## 4. Design the complete page before drawing panels

For dense figures, apply [dense compound design](../../references/dense-compound-design.md).
It provides three-scale design, space budgeting, an illustrative eighteen-panel
allocation and whole-page review. Panel count alone is not a reason to omit evidence.

State the one page question, narrative job, and decision unlocked. Choose a visual
anchor from evidential importance and legibility. Group panels by scientific transition,
then assign relative area, preferred aspect, shared scales, legend ownership, and the
reading path in `layout_blueprint.json`.

Do not start with a uniform card grid. Equal sizes are valid only when they express a
matched scientific comparison; record `uniform_size_rationale` for four or more equal
panels. Microscopy, spectra, structures, longitudinal data, and dense labels often need
different areas. Use whitespace, alignment, shared axes, and short group labels to make
the argument visible without decorative containers.

For Nature-family figures, consult the HCC, TEN and CyLinter cases in
[panel design lessons](../../references/nature-panel-design-lessons.md) when the page
combines tissue context, experimental schedules, image fields and quantitative plots.
Draft the panel descriptions alongside the blueprint so units, crop relationships and
model-specific comparisons influence space allocation before detailed drawing.

Run the layout phase before adding scientific assets:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
```

Inspect the whole proof at final physical width. Record a matching `PASS` review only
after the anchor, reading path, whitespace, encodings, text/image allowance, mechanical
grid risk, and semantic coverage all pass.

If the brief explicitly names twelve panel roles but supplies no images or values, still
encode those twelve bounded roles and their unequal evidence bands in the ledger and
blueprint. Use unresolved placeholders in the layout proof and stop before detailed
rendering. Do not leave a one-panel initializer that contradicts the requested page, and
do not invent an image field, protein value, pathway result, control outcome, or effect
direction to populate it.

## 5. Register assets and source data without changing their evidential role

Register every imported or generated asset in both `figure_spec.json` and
`asset_manifest.json`. A claim-supporting crop records its source figure, panel or page,
transformation, retained scientific elements, omitted elements, and crop review result.
Quantitative plots, microscopy, structures, and experimental images come from real
analysis artifacts; a schematic stand-in cannot silently replace them.

Bind every data-bearing panel to `source_data_manifest.json`. Numeric records name the
independent unit, variables, conditions, transformations, exclusions, missing values,
estimates, uncertainty, portable file, and plotting entrypoint. Image records preserve
acquisition, channels, LUT, crop, registration, segmentation, and processing. Controlled
objects remain pointers with access conditions and a stable request route.

For a mixed-access composite, declare the full image-bearing output for `author` only.
Create a separately labelled quantitative-only reviewer output when that is scientifically useful,
then list only that reduced view under the reviewer audience in `delivery_outputs`. The packager
does not infer that a rendered composite is safe from the access class of its individual assets.

Use native vectors for reconstructed schematics and source-derived graphics for evidence.
Concept generation follows the default schematic route above; any generated asset
embedded in the final figure is conceptual only and subject to current venue policy. Never use
them to fabricate a structure, molecule, measurement, specimen, or experimental result.
Keep generation details in the author workspace and include a disclosure only when the
actual use and current policy require one.

## 6. Validate and render

Run the final phase only after the layout review passes:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase final
```

The canonical PDF must be composed from vector panels or a native vector scene, never
from PNG panels. Produce SVG and a high-resolution PNG alongside the PDF. If the project
has a native composite renderer, use `run_workflow.py --direct-composite` so the shared
workflow does not regenerate it.

Deliver native editable PowerPoint for schematic panels authored through the default
route; render and inspect every delivered slide separately. This does not require
rebuilding measured panels in PowerPoint. A PowerPoint copy of the complete mixed
figure is optional when not requested; its canonical manuscript PDF/SVG remains required.

## 7. Inspect the rendered figure

For each schematic panel, apply
[rendered schematic refinement](../../references/visual-refinement.md) before final
acceptance. Judge local improvements within the complete compound layout; measured
panels keep their data and image content unchanged.

Open the full composition at its real aspect ratio and final physical width. Check:

- claim fidelity, panel order, and evidence-versus-schematic boundaries;
- type size, font embedding, clipping, collisions, and arrow attachment;
- axes, legends, scale bars, condition labels, and image-crop context;
- grayscale and colour-vision-deficiency previews;
- exact page geometry and retained vector content;
- whether warnings in `qa/qa_report.json` have a written disposition.

Schema success is not visual acceptance. Preserve the last accepted version and compare
revisions at the same width. Do not deliver with an unresolved error or high-severity
visual defect.

## 8. Package the handoff

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/package_deliverables.py" <project>
```

Deliver the vector PDF/SVG, inspection PNG, layout proof, canonical specification,
content ledger, venue and blueprint contracts, source-data manifest, palette, asset
inventory, and concise QA report. Include the native editable PPTX for schematic panels
authored through the default route. Include other panel derivatives, explicitly
distributable processed assets, disclosure text or notebooks when used or requested.
The reviewer handoff includes only declared reviewer-eligible source files
and excludes controlled raw objects, private locators, drafting prompts, agent metadata,
approvals, workflow state, and internal integrity records.
