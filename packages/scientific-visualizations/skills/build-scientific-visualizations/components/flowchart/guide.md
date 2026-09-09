# Flowchart Mode Reference

Build one standalone diagram whose pictograms, labels, and arrows communicate the
scientific logic at final print size. Treat every visible mark as claim bearing.

## Ownership boundary

- Select this mode for one flowchart, method schematic, mechanism workflow, or model
  architecture diagram.
- Select `compound-figure` when the diagram is one panel within a complete figure.
- Select `journal-figure-set` for a complete main, Extended Data, and Supplementary set.

## Shared core

The skill-local implementation is `../../shared/figure-core/`, resolved relative to
this guide. Read its `references/visual-contract.md` and
`references/scientific-integrity-rules.md` before drawing. Use its initializer,
validator, renderer, compositor, and QA scripts for the final scene.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

Use `assets/content-ledger.json` and `assets/flowchart-spec.json` as schema examples when
the project has no equivalent source of truth. The initialized project files remain the
working authority.

## 1. Lock the scientific content

Read the manuscript passage, caption, existing figure, plotting code, and cited source
artifacts that establish the diagram. For each stage, record:

- the claim and exact source anchor;
- required object, label, input, and output;
- evidence state: observed, predicted, prospective, hypothesis, or schematic;
- prohibited implication and decisive control;
- whether a displayed object is real evidence or a stand-in.

When two plausible interpretations change the scientific claim or arrow direction, do
not choose by visual preference. Surface the exact conflict before authoring that mark.

When the brief names semantic states or paths but omits their scientific details, retain
every named state in the schema instead of reverting to the one-stage starter. Use only
the supplied category wording, mark its source anchor unresolved, and connect only the
direction explicitly stated by the brief. In particular, keep training-only influence
outside the deployment chain and keep prospective validation visually distinct. This is
a semantic layout scaffold, not permission to invent an assay, model, result, or causal
arrow.

## 2. Lock geometry and notation

Use the target venue's current physical width and minimum rendered type size. Select a
dated profile that names the exact source and submission stage, or use an explicit
custom width without presenting it as a journal rule. Author at final size. Do not crop
with `bbox_inches="tight"` or rely on a document-level resize.

Create a notation registry for every symbol and equation. Copy notation from the
manuscript or derivation; do not add pseudo-mathematics to make a node look technical.
Long equations belong in a separate strip below a thin divider.

## 3. Design nodes and arrows

Use a short noun phrase, a mechanism-specific vector pictogram, and at most one
necessary symbol, threshold, or output per stage. A generic triangle or decorative icon
does not explain a scientific stage.

Arrow roles are semantic:

- solid: primary sequence, measured flow, inference, or source-established causality;
- dashed: conditioning, prediction, prospective work, control, optional branch, or
  training-only influence.

Give every arrow a non-colour cue such as line style and a nearby label. Do not use
colour alone for identity. Avoid ambiguous crossings and arrowheads that attach to the
wrong label or node. `flowchart_spec.json` must bind every semantic stage and edge to
existing visible element IDs and a content-ledger claim. Every visible flowchart arrow
is covered by exactly one semantic edge. Edge endpoints and formula references must
resolve; direction, causality, and training-only status are never inferred from position.

For a Nature-family method diagram, the diaTracer case in
[panel design lessons](../../references/nature-panel-design-lessons.md) illustrates
how a domain object changes through a method and where optional inputs enter. Adapt
the relationship to the current method and use its own notation and evidence states.

Use real plots, microscopy, structures, and quantitative outputs for evidence. A
schematic object may explain a concept but cannot stand in for measured evidence unless
the artwork or caption identifies it as schematic. Keep each pictogram's
`evidence_status` compatible with its anchored content-ledger claim: schematic and
decorative symbols may explain any status, but measured/observed, inferred/predicted,
prospective/hypothesis, training-only, and unresolved states cannot promote one another.

## 4. Prove the whole-page composition

For every new or redesigned diagram, use the default
[image concept to editable PPTX route](../../references/image-concept-to-vector.md)
and inspect the [design templates](../../references/design-template-library.md).
Develop the visual direction before detailed reconstruction. A complete generated
concept is an intermediate reference, not source authority or final editable artwork.
For two source-informed visual grammars and six selectable palettes, use
[diagram style profiles](../../references/diagram-style-profiles.md). The selected
grammar guides composition; a palette change alone is not a layout redesign.

Before detailed pictograms, choose the page question, anchor stage or panel, semantic
groups, relative area, and reading path in `layout_blueprint.json`. Render the
placeholder-only proof. A horizontal row of equal cards is not a default; use it only
when sequence and equal emphasis are scientifically accurate. Embedded method panels
take their area from the complete compound-page argument.

Review the proof at final physical width and complete `qa/layout_review.json`. Do not
draw claim-bearing details while that record is `REVISE` or stale.

## 5. Build from one scene

Initialize a vector project, then replace the placeholder panel with the approved
flowchart scene:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <project> \
  --figure-id <id> --mode flowchart --layout-profile <dated-profile> \
  --annotation-profile method-readable --delivery-mode composite

python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
# Inspect the proof, then record a matching PASS layout review.
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase final
```

For the shared renderer, keep all visible copy and geometry in `figure_spec.json`.
For the default native PPTX schematic route, retain its authoritative presentation
scene and existing scientific content record, then validate and inspect the actual
PPTX separately; do not claim the PDF workflow above ran on a native-only deliverable.
Keep `flowchart_spec.json` as
the semantic stage, edge, pictogram, and formula plan and the content ledger as the
claim source. Use `source_data_manifest.json` for any measured image, plot, structure,
or repository object; a pure schematic uses reasoned `not_applicable` coverage. These
records must agree before export.

## 6. Refine the rendered diagram

Read [flowchart refinement](references/refinement-pass.md) after the first complete
render. Improve composition, individual scientific graphics and final-size harmony in
focused passes, preserving the initial draft and comparing actual versions. Select the
better artifact before final handoff; an earlier technical PASS is not visual acceptance.

## 7. Inspect and deliver

Read `references/qa-checklist.md`. Inspect the rendered PDF at its actual aspect ratio
and final physical width. Check scientific fidelity, text size, clipping, collisions,
arrow attachment, grayscale, colour redundancy, font embedding, and vector content.

Preserve the previous accepted version. Deliver a versioned vector PDF and SVG, layout
proof, editable scene source, semantic flowchart specification, content ledger,
audience-safe source data, and a concise QA note. Include the native editable PowerPoint
from the default schematic route and render and inspect it separately. If the required
image model or native presentation capability is unavailable, report the missing stage
as `not_run`; a vector-only export does not complete the default route.
