---
name: prepare-journal-manuscripts
description: Use when preparing, drafting, revising, polishing, auditing, or packaging a journal manuscript, abstract, statistical or evaluation report, cover letter, editor-facing submission pack, data availability statement, peer-review response, revise and resubmit package, clean manuscript, marked manuscript, or final accepted-paper files. This skill owns manuscript-context and journal-package checks; route figure construction or visual QA to build-scientific-visualizations, and establish disputed experiment evidence with research-publication-pipeline before changing manuscript prose.
---

# Prepare Journal Manuscripts

Carry one evidence-linked article through the journal lifecycle. Resolve the exact
journal, article type, stage, and authority; freeze the scientific contract; choose one
mode; and reconcile every editor-facing and reviewer-facing artifact before delivery.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `recon` | Refresh journal, article-type, policy, format, reporting, data, code, image, and disclosure requirements | `references/journal-lifecycle.md` |
| `draft` | Draft sections from an author-approved outline and locked scientific contract | `references/drafting-and-polish.md` |
| `audit` | Challenge claims, reporting, novelty, policy compliance, and cross-artifact consistency without editing | `references/adversarial-audit.md` |
| `polish` | Make targeted evidence-preserving edits and repair narrative structure | `references/drafting-and-polish.md` |
| `editor-pack` | Assemble title page, manuscript, figures, declarations, checklists, and editor-facing metadata | `references/editor-pack-and-cover-letter.md` |
| `cover-letter` | Draft or audit a factual journal-specific cover letter | `references/editor-pack-and-cover-letter.md` |
| `revision-response` | Build a complete point-by-point response and synchronized clean and marked manuscripts | `references/revision-response.md` |
| `final-package` | Verify accepted-paper source, rendering, declarations, availability statements, and files under current production instructions | `references/journal-lifecycle.md` |

Use one primary mode per pass. Run `recon` when the exact journal, article type, stage,
or official authority is uncertain. A publisher-wide page or remembered convention
cannot replace the target journal's current first-party instructions.

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime component
is below that directory; never resolve through the package parent. Read only the component
needed for the current task:

| Need | Component |
|---|---|
| abstract drafting, compression, or audit | `components/abstract/guide.md` |
| statistical and evaluation reporting | `components/statistics-reporting/guide.md` |
| data inventory, access routes, and statement | `components/data-availability/guide.md` |

The bundled validators check local completeness and consistency. They do not establish
scientific truth, repository access, consent, licence rights, or journal acceptance.

## Lock the scientific contract before prose

Obtain the article's question, contribution, methods, data, split, comparators,
independent units, endpoints, statistical design, results, uncertainty, limitations,
and exact source artifacts. This is the locked scientific contract. Manuscript work may
explain or narrow it, but cannot invent a result, redesign an analysis, choose a
favorable subset, strengthen causality, or convert future work into completed evidence.

Map title, abstract, main claims, figures, tables, discussion, and conclusion to exact
support. Distinguish observed result, author interpretation, and broader implication.
Keep critical definitions, controls, denominators, exclusions, and limitations visible
in the main article when the journal expects the paper to stand on its own.

For `draft` and `polish`, use the paragraph and reverse-outline workflow in
`references/drafting-and-polish.md`. Preserve every number, unit, direction, interval,
qualifier, and citation scope. Use the abstract component only after the central claim
and evidence boundary are stable. Statistical design belongs upstream in
`research-publication-pipeline`; the reporting component checks and expresses the
frozen analysis.

For Nature-family full-paper or section work, read the relevant sections of
[section-specific writing](references/nature-section-style.md): title, abstract,
Introduction, Results, Methods, Discussion, legends and supplementary text. A full-paper
request requires coverage of every supplied section; report missing sections explicitly.

When the task explicitly asks to calibrate an Article against published Nature-family
examples, also read `references/nature-family-article-shapes.md`. Its DOI and PDF-page
locators document a bounded exemplar corpus. They are empirical precedents, not current
journal policy or a fixed manuscript template.

For Nature-family `draft` or `polish` tasks involving paragraph flow, comparison prose,
or legends, read [paragraph and legend lessons](references/nature-paragraphs-and-legends.md).
Use the located examples to preserve comparison regimes, meaningful transitions and
panel-specific sampling; adapt the writing to the current evidence.

## Build editor and review packages as linked artifacts

For `editor-pack` and `cover-letter`, inventory every required item before writing.
Describe fit, contribution, related submissions, prior dissemination, authorship,
ethics, competing interests, data and code status, and suggested or opposed reviewers
only from confirmed facts. Do not claim novelty, exclusivity, repository availability,
or author agreement without evidence.

For `revision-response`, read `references/revision-response.md`. Account for every
editor and reviewer comment. Link each answer to evidence and an exact change location.
The response letter, clean manuscript, marked manuscript, figures, supplement, and
availability statements must describe the same revision. A promised analysis remains
future work until its outputs have been inspected.

## Resolve data, code, figures, and policy

For a data availability task, inventory every dataset supporting main and supplementary
claims before drafting the statement. Never invent an accession, DOI, licence,
restriction, controller, access procedure, embargo, or deposit state. Actual public
release and repository mutation belong to `research-publication-pipeline`; this skill
owns statement accuracy and manuscript-package consistency.

Route claim-bearing figure construction and visual QA to
`build-scientific-visualizations`. Verify the target journal's current policies for
image manipulation, generated images, source data, code, reporting checklists, AI use,
ethics, and disclosure. Do not treat a publisher-family convention as universal.

For new or redesigned flowchart, architecture, motivation, method or mechanism schematics,
including panels in main, Extended Data and Supplementary figures, use that skill's
default **GPT Image 2.5 concept, then native editable PPTX** workflow. Carry the
journal-appropriate style and locked scientific content into the handoff; no separate
image-first or PowerPoint request is needed. Measured plots and real images remain
source-derived. Follow its model-availability and policy handling, and retain the
journal-required vector exports for manuscript insertion. If the visualization skill
is not installed, prepare the figure brief and report the missing dependency. Read-only
audits do not authorize new drawing or modification of an approved figure.

## Audit and deliver

Apply `references/adversarial-audit.md` to the exact candidate files. Inspect rendered
pages at normal reading scale, not only source. Reconcile the title page, anonymous or
identified manuscript, figures, tables, legends, supplement, declarations, cover
letter, response, marked copy, data statement, and code statement as applicable.

Report observed findings separately from inference, `not_run`, and failed checks. Give
each defect the smallest valid action and a settling check. Preserve the last accepted
or author-approved baseline before revision. Uploading, changing repository records,
contacting an editor, or submitting is an external action requiring explicit author
authorization.

## Boundary with the other public skills

This skill owns journal prose, editor-facing materials, peer-review revision, current
journal compliance, and final packaging. `research-publication-pipeline` owns research
design, experiments, frozen evaluation, claim lock, paper reading, and actual public
release. `build-scientific-visualizations` owns figure construction and visual QA.
