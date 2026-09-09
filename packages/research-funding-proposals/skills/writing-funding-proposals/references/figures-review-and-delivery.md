# Figures, review, and delivery

## Figure and table contract

Every visual has one rhetorical job, a body anchor, linked CL* and source IDs, an editable
master, a rendered output, and a QA decision. Choose a process diagram, comparison table,
timeline, result plot, or foundation map only when the available evidence supports that
form.

First verify that current funder and institutional rules permit the requested
AI-assisted visual. Permission for prose assistance alone does not establish permission
for AI-derived figures. If visual permission is unverified or prohibits the requested
work, prepare a local figure brief or audit the applicant's existing master; do not
produce an insertion-ready generated figure. Keep `APPLICANT_PRIVATE` and
`RESTRICTED_CONFIDENTIAL` material, including derived figure briefs, out of external
image services. Only approved `PUBLIC` content may enter that concept-generation step.

Once policy, evidence links, and rhetorical job are settled, hand new or redesigned
technical-route, method, architecture, motivation, and mechanism schematics to
`build-scientific-visualizations`: use `flowchart` for standalone schematics and
`compound-figure` when one figure combines schematic and data panels. Follow its
`references/image-concept-to-vector.md` default for the schematic portion: select a
style from the proposal brief, generate and inspect a GPT Image 2.5 concept, reconstruct
native editable PPTX objects,
then render and test a representative edit. Deliver the editable master and the exports
needed by the official form; no separate PPTX request is needed. Use the actual current
template width, not a journal column profile. Keep source labels, semantic arrows, and
the distinction between completed and planned work fixed. Generate only schematic
content; result plots still come from analysis outputs.

The visualization skill owns exact-model selection, explicit user overrides, small
native-edit exceptions, and native editability checks. If that skill or a verifiable
GPT Image 2.5 interface is unavailable, report the unrun step and finish safe local
content/style preparation; a default route is not evidence that generation succeeded.

Author figures at final size. Avoid document-level scaling that shrinks already-small
labels, and avoid automatic tight cropping that changes the declared canvas. Use colour
with marker, line style, hatch, shape, or direct labels. A bar chart starts at zero unless
a different non-bar encoding is used. Quantitative values come from analysis outputs, not
manual transcription.

Before retaining a portfolio, merge or drop visuals with duplicate rhetorical jobs. A
planned visual does not substitute for a delivered master, render, source record, or QA
result.

## Three review passes

Record one issue per row in `reviews/review-findings.csv`:

1. `R1_FATAL` checks current authority, eligibility evidence, citation integrity,
   confidential material, data access, applicant roles, ethics and security, policy, and
   contradictions.
2. `R2_SCIENCE` challenges the question, novelty, route, data, strongest alternative,
   discriminating validation, failure criteria, feasibility, applicant foundation,
   annual outputs, and technical fallbacks.
3. `R3_READABILITY` asks whether an adjacent-area reviewer can recover the problem,
   precise gap, route, validation, and bounded significance. It also checks direct prose,
   terminology, citations, cross-references, and the revised artifact.

Give each finding its strongest falsifier, exact location, required evidence, cheapest
valid revision, resolution status, and resolution evidence. A score change or favorable
impression is not resolution evidence. An open fatal issue blocks final mode.

## Build and visual review

Use the current official template and the institution-approved build path. Inspect the
actual build log and rendered artifact. Record `NOT_RUN` or `FAILED` when accurate. Check
every page for:

- required headings, fields, attachments, page limits, and references;
- missing characters, compile errors, clipping, overlap, and stale figure copies;
- font consistency, line and table legibility, image resolution, and final-size labels;
- agreement between figure captions, panel labels, body references, and the claim ledger;
- unresolved placeholders, hidden comments, tracked changes, or applicant-private source
  material outside its intended location.

A PDF existing on disk does not prove a successful build or visual review. The proposal
validator reports `validation_scope: record_completeness`; it checks the recorded status and
local path, not the file format, rendering, or visual quality.

## Local package and external action

Build any local candidate package from an explicit allowlist. Include only the official
form output and required attachments. Exclude research notes, source papers, confidential
evidence, drafting records, tool traces, and internal QA material unless the funder
explicitly requires a named item.

Final-mode validation establishes only local record completeness. It does not determine
scientific truth, eligibility, policy compliance, authorship, funding, external submission,
file format, rendering, or visual quality. Uploading or submitting requires applicant
authorization and direct evidence from the intended platform.
