# ICLR venue component

Use this component only after the conference entrypoint has confirmed the ICLR
Conference year and stage. Read the [official sources](references/official-sources.md),
[stage matrix](references/stage-matrix.md), [AI-use record](references/ai-use.md), and
[discussion and revision guidance](references/discussion-and-revision.md). The bundled
profile was checked on 2026-09-04. Reopen the official author guide, AI policy, style
package, and any stage-specific instructions before real submission work.

This profile covers the ICLR 2027 Conference. Do not reuse it silently for a workshop,
blog post, another track, or another year.

## Establish the artifact and claim map

Inventory the registered abstract, author list and freeze state, main TeX file,
included sources, bibliography, official style files, rendered PDF, appendix,
supplement, code or data package, current AI-use record, and discussion history. Mark
each item `observed`, `not_run`, `failed`, or `inferred`.

Read [manuscript-core scientific review](../../manuscript-core/references/scientific-review.md).
Preserve all numbers, comparison directions, and qualifiers. Keep the main paper
independently assessable because reviewers are not required to read appendices or
supplementary material.

For anonymous submission, inspect source and rendered output. An `author` command may
remain in source while the official style suppresses it; do not flag that command alone.
Active `iclrfinalcopy`, visible identity, identifying acknowledgments, identity-bearing
PDF metadata, or identity in a supplement is a critical defect.

## Record AI use truthfully

Create the factual activity record described in [AI-use guidance](references/ai-use.md).
State the actual task, relevant tool, human verification, and author responsibility.
Do not infer non-use from missing notes or copy boilerplate that contradicts the real
workflow.

The in-paper disclosure is mandatory, but the checked policy says its example format
need not be followed exactly. The static audit therefore does not accept or reject a
paper by one disclosure heading. Inspect the actual in-paper section and its truthfulness
manually before submission or camera-ready delivery.

## Run deterministic checks

With `SKILL_DIR` set to the installed skill directory, run:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/iclr/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/iclr/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_archive.py" /path/to/supplement.zip \
  --identity "author identity pattern"
```

The TeX audit follows only static includes and cannot prove rendering. The PDF audit
checks geometry and anonymous metadata, but not main-text boundaries, font quality,
clipping, or visible identity. Inspect the rendered author block, headers, equations,
figures, tables, references, appendix transition, links, and disclosure placement.

For a discussion revision, preserve the original candidate and map each change to one
reviewer concern and valid evidence. A response cannot silently replace the central
paper, tune on a locked test, or hide a negative result.

Start from the [review-report template](../../manuscript-core/assets/review-report-template.json)
and validate it with the [review-report validator](../../manuscript-core/scripts/validate_review_report.py).
Saving, uploading, commenting, or submitting is outside this component.
