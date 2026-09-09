# CVPR venue component

This component covers CVPR 2026 Main Conference, checked on 2026-09-04. The CVPR 2027
Call for Papers said its document was not yet available, so complete 2027 author rules
are `NOT_FOUND`. Run `recon` before applying this profile to any later cycle. Read the
[official sources](references/official-sources.md), [stage matrix](references/stage-matrix.md),
and [proceedings observations](references/published-paper-observations.md) first.

The profile checks the US-Letter `article` shell with `10pt`, `twocolumn`, and
`letterpaper`; `\usepackage[review]{cvpr}` for anonymous submission;
`\usepackage[rebuttal]{cvpr}` for rebuttal; and no review/rebuttal option at
camera-ready. It also enforces the one-page rebuttal PDF limit.

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/cvpr/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/rebuttal.pdf \
  --profile "$SKILL_DIR/components/venues/cvpr/references/venue-profile.json" \
  --stage rebuttal
```

Manually inspect the eight-content-page/reference boundary, visual and link anonymity,
ethics/AI/IRB claims, Compute Reporting Form truth and portal state, and the current
camera-ready package. External links cannot expand the submission, supplement, or
rebuttal. Supplementary material is optional reviewer attention.
