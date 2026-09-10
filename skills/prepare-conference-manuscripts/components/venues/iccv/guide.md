# ICCV venue component

This component covers ICCV 2025 Main Conference, checked on 2026-09-10. ICCV is
biennial, so this is the most recent completed cycle rather than an upcoming one: the
ICCV 2027 author-guideline page returned HTTP 404 on the same date and the conference
site presented 2025 only, so 2027 rules are `NOT_FOUND` and are not inherited from here.
Read the [official sources](references/official-sources.md), [stage matrix](references/stage-matrix.md),
and [proceedings observations](references/published-paper-observations.md) first.

The profile checks the US-Letter `article` shell with `10pt`, `twocolumn`, and
`letterpaper`; `\usepackage[review]{iccv}` for anonymous submission;
`\usepackage[rebuttal]{iccv}` for rebuttal; and no review or rebuttal option at
camera-ready. Those come from the official author kit, which is the shared
CVPR/ICCV/3DV template. ICCV's own pages supply the page limit, the anonymity rule and
the supplement boundary, so nothing about policy is inherited from CVPR.

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/iccv/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/iccv/references/venue-profile.json" \
  --stage anonymous_submission
```

Manually inspect the eight-content-page boundary excluding references, visual and link
anonymity, and the camera-ready package. Two limits that CVPR states and ICCV does not
are deliberately absent from the profile rather than copied across: the rebuttal has no
stated page count and the supplement has no stated size cap. Verify both against the
portal for the cycle you are actually submitting to.

An appendix inside the main PDF is unsupported rather than forbidden by a quoted
sentence: the guidelines permit additional pages containing only cited references and
say nothing that admits an appendix.
