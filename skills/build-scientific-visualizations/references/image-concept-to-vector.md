# Image concept to editable scientific diagram

This is the default authoring route for new or redesigned scientific flowcharts, model
architectures, motivation diagrams, method schematics and mechanism illustrations,
including schematic panels within conference, journal and compound figures.

The sequence is: lock scientific content and destination policy, select the visual
style, generate a **GPT Image 2.5** concept, inspect it, reconstruct native editable
PPTX objects, then compare the actual render and test editing. The generated image is
an intermediate visual reference; the final schematic is an editable PPTX, with
PDF/SVG exports as required for manuscript insertion. A resolved rough blueprint or
convenient vector starter does not replace the concept-generation step for a new design.

Scope the route to conceptual content. Quantitative plots, exact structures, microscopy
and other measured evidence come from their source data or original images, including
inside a motivation figure. Generate only the schematic portion of a mixed figure.
A disposable layout-only sketch needs no generated image or PPTX. For a small edit to
an approved native design, edit that design directly; do not regenerate its composition.
Follow an explicit user instruction to use another model, supplied concept or direct
vector workflow. If destination policy prohibits the proposed AI-derived design, finish
safe source/style preparation and report the conflict before generating it.

## Establish a visual direction

Read the scientific source and choose a relevant example from the
[design template library](design-template-library.md). Inspect the actual preview or
paper figure. Identify the relationship worth borrowing: an object transformation,
shared parameters across stages, or a matched method comparison. Borrow its hierarchy
and visual reasoning, not its artwork, biological entities, model counts or results.

Lock the required scientific objects, arrow meanings, exact labels and notation in
the current content record. Choose an authoring width and a reading path. A request for
Nature/top-conference style is a design ambition, not an exact publisher specification.
Use [diagram style profiles](diagram-style-profiles.md) to choose an open/object-led
or structured/module-led direction and one palette. Without an established project
style, start with `conference-structured` for top-CS diagrams and `nature-pastel` for
Nature-family diagrams; adapt other journals to their actual visual brief. Inspect its native example and
carry the same semantic colour roles into the concept and editable reconstruction;
do not let generation choose new category meanings or extra branches.

Prefer GPT Image 2.5 for the concept when the interface exposes that model. At the time
of writing that means running the generation step in Codex; the rest of this route --
locking content and style, reconstructing native objects, comparing the render and testing
editability -- has no such dependency and runs in any runtime. Use only
an actual exposed model identifier. A built-in image tool may provide no selector or
backend identity; for an otherwise authorized default-route request, use that tool
and report the model version as unverified. Missing model metadata does not establish
that generation is unavailable and does not require another approval by itself.
If the user explicitly requires a verified exact model, or the interface offers only
a different named model, finish safe content/style preparation and ask once about
access, a supplied concept or an alternative. Mark generation `not_run` only when it
has not run. Never invent a model ID, claim an unreported backend identity, or treat
the model name in a prompt as proof of which model ran.

Start with one complete concept and request another only for an observed design
weakness. Ask for vector-friendly scientific illustration: coherent object shapes,
restrained colour, clear silhouette and meaningful internal detail, sparse labels and
room for exact typesetting. Avoid a visual direction whose appeal depends on texture
or lighting that the requested editable format cannot preserve.

Select the concept by looking at it. Assess composition, scientific object recognition,
hierarchy and reconstruction feasibility separately from scientific correctness. Treat
generated labels, equations, dimensions and graph structure as untrusted. Mark needed
source corrections before reconstruction; beauty does not make those details valid.
Do not require extra variants once a suitable direction is clear.

## Reconstruct objects, not pixels

Use the selected concept as a visual reference and the scientific record as the content
authority. Preserve its useful proportions, alignment, palette roles and graphic detail.
Do not reduce a well-designed pictogram back to a generic labelled rectangle.

Build the default editable PPTX from separate native text, connectors, shapes and grouped
scientific objects using a compatible presentation capability. Recreate formulas from
the source. State whether they are editable text, native equation objects or outlines;
these are different capabilities. A raster picture or an embedded SVG that only moves
as one image is not proof of component editability.

Keep one authoritative object scene or presentation source for geometry. Reuse the
existing scientific ledger rather than duplicating it in prompts or handoff documents.
PPTX reconstruction is a native-format handoff; it does not establish that the shared
PDF renderer or a submission-package validator was run. If those outputs are requested,
produce and validate them through their applicable route.

## Compare the actual native result

Render the exported PPTX and compare it with the selected concept at the same size.
Check object detail and visual hierarchy as well as text, arrow endpoints and notation.
Apply [rendered refinement](visual-refinement.md) to concrete remaining weaknesses.
Report what was intentionally changed to restore source fidelity and what could not be
reproduced in the editable format. A successful export alone is not visual acceptance.

Inspect native object structure and exercise a representative edit in a disposable copy:
change a label, move an object or change a connector, save, reopen and render it. Confirm
that the edits persist and keep the delivered original unchanged. A native-format
library can test this round trip; an independent office renderer adds compatibility
evidence. Neither establishes Microsoft PowerPoint GUI editing unless that application
was actually exercised. Report the application used and any file-access limitation;
do not broaden filesystem permissions to clear an application dialog.

## Reuse and publication

Keep useful original native templates and their rendered previews in the skill's assets;
link them from the template library with their intended use. Leave generation prompts,
rejected concepts and inspection records outside the distributable template assets.
Do not bundle third-party paper figures. Reopen the cited source when its details matter.

A generated or traced conceptual image remains AI-derived design; vector reconstruction
does not remove disclosure or publisher-policy obligations. Check the exact destination
policy before publication. Generated imagery cannot replace measured data, real
specimens, exact structures or quantitative evidence.
