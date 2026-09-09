# ICML venue component

This component covers ICML 2026 Main Track, checked on 2026-09-04. Checked 2027
author-instruction and CFP endpoints were 404, so complete 2027 rules are `NOT_FOUND`.
Run `recon` before any later-cycle submission. Read the [official sources](references/official-sources.md),
[stage matrix](references/stage-matrix.md), and [proceedings observations](references/published-paper-observations.md).

The profile checks the US-Letter `article` shell, anonymous `\usepackage{icml2026}`
without `[accepted]`, and camera-ready `\usepackage[accepted]{icml2026}`. It requires
the Main Track `Impact Statement` heading and uses the current 50 MB anonymous and
20 MB final limits. It does not revive stale 10 MB, Type-1, or Word wording from an
example PDF.

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/icml/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/icml/references/venue-profile.json" \
  --stage anonymous_submission
```

Manually assess the 8/9 content-page boundaries, Impact Statement substance and
placement, anonymous links/artifacts, conflicts, reciprocal review, portal forms, and
receipt. A review supplement is allowed, but camera-ready has no independent
proceedings supplement.
