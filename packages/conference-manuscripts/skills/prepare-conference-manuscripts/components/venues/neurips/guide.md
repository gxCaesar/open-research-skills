# NeurIPS venue component

This component covers NeurIPS 2026 Main Track, checked on 2026-09-04. Checked 2027
handbook and CFP endpoints were 404, so complete 2027 rules are `NOT_FOUND`. Run
`recon` before any later cycle. Read [official sources](references/official-sources.md),
[stage matrix](references/stage-matrix.md), and [proceedings observations](references/published-paper-observations.md).

The profile checks the US-Letter `article` shell and `neurips_2026` package. Anonymous
submission accepts the default or `[main]` and rejects `[final]` and `[preprint]`.
Camera-ready requires `[main,final]` and rejects `[preprint]`. Both paper stages
require the `NeurIPS Paper Checklist`; the submission PDF limit is 50 MB.

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/neurips/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/neurips/references/venue-profile.json" \
  --stage anonymous_submission
```

Manually check the 9/10 content-page boundaries, checklist completeness and truth,
contribution type, profile and conflict state, disclosures, lay summary, and portal
receipt. Rebuttal is OpenReview discussion: it does not authorize a revised paper or
supplement upload.
