# Full-project workflow

Use this reference for a complete proposal or to resume an existing workspace. Each stage
has one scientific or delivery decision. The files are human-facing records and remain
subordinate to actual official sources, applicant evidence, and rendered artifacts.

## S0--S4: establish authority, evidence, and route

### S0 — authority and intake

Record the target program and year, project type, current official and institutional
sources, confidentiality, authoring-policy mode, and whether the actual system template
has been opened. Final mode needs a completed live authoring-policy refresh covering both
the funder and institution, not only a bundled profile. Bind each refresh source to its
single authority kind, selected program/year/scope, checked date, and refresh ID, then
reconcile the binding with its source-register row. Use different source IDs for funder
and institution, with distinct `(issuer, url_or_path, clause_locator)` evidence identities.
Final authority, template, and budget-requirement sources must use their controlled
source-register context, match the selected program/year, and have current access dates.
Final validation defaults the refresh date to today; an explicit historical `--as-of` is
only for archived-snapshot revalidation. A missing future template limits final-format
work; it does not stop evidence collection, topic comparison, or structural review.

### S1 — evidence and applicant foundation

Populate `authority/source-register.csv` and `evidence/claim-ledger.csv`. Applicant-role
claims need direct evidence of what the applicant did, owns, can access, or can transfer.
Publication metadata alone cannot establish contribution or proposal readiness.

### S2 — candidate portfolio

Compare a small set of credible scientific candidates. For each candidate record the
question, contribution lane, data feasibility, linkable variables, independent unit,
nearest work, strongest cheap baseline, discriminating validation, failure criterion,
applicant fit, program fit, and cheapest next check. Retain held or excluded candidates
and their reasons rather than inventing weak alternatives to hit a fixed count.

### S3 — novelty and feasibility disposition

Open the load-bearing papers and current data sources. Record dated searches and classify
the nearest work as `IDENTICAL`, `ADJACENT`, or `UNCERTAIN` within the declared
contribution lane. Record `FRAMING`, `DATA`, or `TASK` separately. A strong adjacent paper
does not kill a testable delta, and a data failure is not a task failure.

### S4 — freeze one route

Select one central contribution and the most natural current reviewer community. Compare
plausible program codes using the project question, output, validation endpoint, and
strongest mismatch. Freeze only after the applicant confirms the resulting scope.

## S5--S9: build the argument and human-authored artifact

### S5 — scientific argument graph

Complete `argument/argument-map.json`. Every Q* has content and discriminating validation.
Every C* has data or object, mechanism or method, V*, O*, supporting CL*, and any F* that
carries the argument. Every V* names a comparison, independent unit, evaluation boundary,
failure criterion, and action on failure.

### S6 — section and resource handoff

Give each planned paragraph one rhetorical job and explicit controlled IDs. Allocate page
space after the argument graph is complete, then name annual outputs, acceptance evidence,
technical risks, triggers, and fallbacks. Record separate commitments for research
contents, annual tasks, and outputs, including a finite bound, stop rule, dependencies,
and sequence. Determine from the current program/project profile whether a financial
budget is required; if so, link its balanced annual and category allocations to tasks and
resources. Counts follow scientific dependencies, not a three-part writing formula.

### S7 — applicant-authored sections

Keep `rationale`, `contents`, and `foundation` independently reviewable. Under
`EVIDENCE_AND_AUDIT_ONLY`, the applicant writes the application prose and the skill
checks structure, scope, traceability, omissions, and contradictions. Do not transform a
brief into generated submission prose.

### S8 — figure and table portfolio

Keep only visuals that make one evidence-linked judgment easier to inspect. Each retained
item has a rhetorical job, body anchor, claim and source IDs, editable master, render, and
QA result. Merge duplicate jobs before production. For new or redesigned schematics,
follow the policy-scoped independent construction route and optional specialist enhancement in
[figures, review, and delivery](figures-review-and-delivery.md); quantitative plots
retain their source-data route.

### S9 — official-template integration

Integrate applicant-authored sections into the actual current form. Template headings,
page rules, fields, and attachments come from the target-year system artifact, not a
bundled imitation. Recheck cross-references, terminology, figures, citations, and scope
after integration.

## S10--S12: review and local delivery

### S10 — three review passes

- `R1_FATAL`: authority, eligibility, integrity, confidentiality, access, ethics, and
  contradiction risks.
- `R2_SCIENCE`: question, novelty, alternative explanations, validation, feasibility,
  applicant foundation, annual outputs, and fallback logic.
- `R3_READABILITY`: cross-area comprehension, direct Chinese prose, terminology,
  citations, and independent copyedit of the revised artifact.

Keep one finding per row in `reviews/review-findings.csv`. A resolved or not-applicable
finding needs concrete evidence. An open fatal finding prevents final readiness.

### S11 — build and visual review

Build the exact integrated artifact using the official form or institution-approved
workflow. Record the command or tool used, actual outcome, rendered artifact, and visual
review. Inspect every page for clipping, overlap, headings, references, figures, tables,
fonts, and final-size readability. A word count is not a page-layout check.

### S12 — local candidate record-completeness check and external boundary

Run the validator in final mode on the exact applicant-reviewed candidate. It checks the
recorded live policy refresh, conditional budget record, and commitment dependencies in
addition to the other local artifacts. A pass means only that the public workspace
contract is internally complete. The report declares
`validation_scope: record_completeness`: it does not parse the candidate file, run rendering,
or judge visual quality. It does not prove eligibility, correctness, policy compliance,
submission, review success, or funding.
External upload or submission remains a separate applicant-authorized action.

## Invalidation and resume

When a source, claim, dataset, route, or policy changes, reopen only its dependents. For
example, a changed source may reopen claims, linked contents, figures, sections, and review
findings while leaving an independent chapter intact. Record what changed and why in the
affected human-facing file; do not preserve a false completed status.
