# AAAI venue component

Use this component only after the conference entrypoint has confirmed the exact AAAI
track and year. Read the [official sources](references/official-sources.md),
[AI-policy record](references/ai-policy.md), and [stage matrix](references/stage-matrix.md)
before changing manuscript text. The bundled profile was checked on 2026-09-04;
deadlines, forms, templates, and policies are time-varying and must be refreshed from
official AAAI pages for real submission work.

## Apply the current policy boundary

The checked AAAI-27 pages give conflicting instructions about AI-written manuscript
text. Until AAAI resolves that conflict, apply the narrower dedicated author-policy
boundary: source-check, outline, format, audit, and polish author-written text, but do
not generate new submission-ready prose. Record the conflict and official sources
checked. Do not disguise generation as translation, rewriting, or a template.

This profile covers the AAAI-27 Main Technical Track. Do not apply it silently to a
special track, workshop, journal track, or another year.

## Establish the artifact set

Inventory the main TeX entrypoint, included sources, bibliography, current official
style files, rendered PDF, reproducibility checklist, supplement, code or data package,
and prior response material. Mark each item `observed`, `not_run`, `failed`, or
`inferred`. Do not replace the author's current template with a bundled copy.

Read [manuscript-core scientific review](../../manuscript-core/references/scientific-review.md)
and [AAAI scientific review](references/scientific-review.md). Keep material needed to
assess the central claim in the main paper; a supplement is not guaranteed reviewer
attention.

## Run deterministic checks

With `SKILL_DIR` set to the installed skill directory, run:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/aaai/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/aaai/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_archive.py" /path/to/supplement.zip \
  --identity "author identity pattern"
```

The source audit cannot prove the rendered result. The PDF audit checks geometry, total
pages, and Author metadata, but cannot locate the content-reference boundary. Inspect
the rendered PDF at full page and normal reading size, including fonts, clipping,
equations, floats, content and reference transitions, visible anonymity, and link
targets.

Start from the [review-report template](../../manuscript-core/assets/review-report-template.json)
and validate it with the [review-report validator](../../manuscript-core/scripts/validate_review_report.py).
Separate observed defects from scientific judgment and inference. Saving, uploading, or
submitting is outside this component.
