# Section-by-section polish and continuation

Use within `polish` for one named section, section-by-section revision, or
"continue the next section" / "逐节打磨" / "继续下一节". This is not a new mode.
Revise the actual manuscript; a checklist or proposed rewrite alone is not execution.

## Bind the task to one manuscript

Read the current project instructions and existing checkpoint before editing.
Identify the authoritative manuscript version, its evidence sources, the writable
revision copy, and the user's section scope and existing edit authorization.
Use paths plus the actual version/date or relevant diff; do not select by filename
alone. If competing versions cannot be resolved, ask only for that remaining choice.

Preserve canonical/frozen sources unless their editing is already authorized.
Do not request the same authorization again at every section. A read-only request
allows diagnosis, not manuscript or checkpoint writes; report the proposed next step.

## Build and resume the section queue

Derive the queue from the manuscript's actual headings and the user's requested range,
including legends, appendices or supplementary sections only when in scope.
Respect the requested order; otherwise use the existing manuscript order rather than
imposing a fixed paper template. Record stable heading/file locators, not positions
alone that become ambiguous after a section is moved.

Default to one section per invocation. If the user explicitly authorizes the whole
queue or automatic continuation through that scope, proceed section by section
without asking for repeated approval. A request for the next section authorizes that
next item, not unrelated sections, new research or external actions.

On continuation, read the checkpoint and current candidate, then compare the recorded
version, section and evidence with what is now present. Reopen only affected completed
items when their text, source results, citations or linked figures changed, or their
acceptance check failed. Old `done` is not evidence that a changed section is accepted.
Do not restart unaffected completed work or skip an unresolved item as though done.
If continuation has no reliable progress record, recover what is established from the
current revision and evidence. If the next item still cannot be identified, ask that
specific scope question rather than guessing a completed section or restarting all.

## Work on the selected section

1. State its thesis in one sentence: what does this section establish or explain?
   Read enough adjacent text to identify its role and transition, without silently
   expanding the editing scope.
2. Map each paragraph's job to the actual definition, method, result or source it uses.
   Find repeated setup, unsupported steps and missing definitions before line editing.
3. Make local, evidence-supported edits to the authorized copy. Preserve numbers,
   units, comparison direction, negation, uncertainty, qualifiers and citation scope.
   Keep observed results, interpretation and proposed work distinct. Do not invent
   statistics, parameters, studies or successful examples to repair a transition.
4. Check the revised sentences against the actual supporting tables, figures,
   source data, methods and cited passages needed for the changes. Preserve negative
   results and material limits. Inspect the real diff or before/after content.

If a critical evidence conflict, suspected leakage, inconsistent result or unresolved
scientific decision affects this section, stop its affected edits and acceptance.
Preserve the finding and original evidence; do not smooth it away, invent a resolution
or mark the item `done`. Continue independent authorized work only when it does not
depend on that conflict, leaving the outstanding item and its impact visible.

## Verify the section in its actual format

Use the project's existing build/render path and the smallest relevant source checks.
For LaTeX, compile the real candidate when needed and inspect affected pages; for
Word or other formats, use their actual export/render workflow. For a text-only
deliverable, inspect the revised text and links rather than inventing a TeX build.
Check changed equations, references, labels, page breaks, figures and captions that
the edit can affect, including a neighbouring page if layout moved.

Record the exact command or inspection and its observed result. A successful compile
does not replace reading the output. Required but unavailable rendering remains
`not_run` and the section awaits verification; a failed check remains failed.
Mark `done` only when the requested section work and its applicable acceptance checks
are complete on the current candidate. Reuse still-valid checks rather than rerunning
unaffected builds merely to produce another receipt.

## Keep lightweight author-side progress

Update the project's existing checkpoint/status record; do not create a parallel log.
Only if no suitable record exists, create a small local author work note within the
authorized workspace. Keep it out of manuscript text, supplement and submission
packages. No fixed log filename, per-section commit, model or extra agent
is required. Record only what continuation needs:

- manuscript/candidate identity and the authorized queue/range;
- current section locator, thesis, paragraph/evidence anchors and concrete changes;
- status such as `pending`, `in_progress`, `needs_evidence`, `needs_verification`, `done`;
- actual source/build/render checks and outcomes, with failures or `not_run` explicit;
- remaining questions, affected dependencies and the next eligible section.

At a stopping point, return the section changed, evidence checked, observed validation
and next item. Do not report a planned edit, an old status or a checker summary as
proof that the manuscript was actually revised.

## Close the requested scope once

For a single-section assignment, close with that section's acceptance and necessary
adjacent-text or reference consistency checks; do not expand into a whole-paper audit.
For an authorized multi-section queue or whole manuscript, once every in-scope item
is accepted, perform one closing cross-section and finished-artifact pass on the same
candidate. Within that scope and its dependencies, reconcile title/abstract promises,
definitions, notation, numbers, units, citations, figures/tables, legends and main/
supplement links. Inspect the finished deliverable in its actual format without
claiming comprehensive review of unscoped sections. If a specific defect is revealed,
reopen the affected item and recheck its consequences, not the whole queue.

Report section completion separately from scope completion and manuscript readiness.
Completing one requested section does not certify untouched sections or a submission
package. Unresolved material evidence or required unrun checks prevent an unqualified
whole-manuscript completion claim; uploads and submissions remain separate actions.

For conference work, retain exact venue/year/track/stage and current policy boundaries.
Use [manuscript lifecycle](manuscript-lifecycle.md) for ordinary polish. When the task
also includes packaging, this section loop sits inside the revision pass of the
[whole-paper workflow](full-paper-workflow.md), after its audit boundary. Its final
re-audit can serve the closing pass above; do not duplicate valid checks or bypass P0.
