# ACL venue component

This component covers the ACL 2026 Main Conference through ACL Rolling Review (ARR),
checked on 2026-09-04. ACL 2027 author rules were `NOT_FOUND`; run `recon` against
current first-party pages before any later-cycle submission. Read the [official sources](references/official-sources.md),
[stage matrix](references/stage-matrix.md), and [proceedings observations](references/published-paper-observations.md)
before relying on this dated profile.

For an ARR manuscript, use A4 `article` at `11pt` with `\usepackage[review]{acl}`.
The profile requires a `Limitations` heading and checks source anonymity, acknowledgments,
PDF geometry, and metadata. For camera-ready work, use `\usepackage{acl}` without
`review` or `final`. It does not infer that arbitrary unrecognized options are valid.

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/acl/references/venue-profile.json" \
  --stage anonymous_submission

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" /path/to/paper.pdf \
  --profile "$SKILL_DIR/components/venues/acl/references/venue-profile.json" \
  --stage anonymous_submission
```

Treat long/short content limits (8/4 at review and 9/5 at final), reference and
appendix boundaries, responsible-NLP checklist truth, visible or linked identity,
deadlines, and portal receipts as manual checks. ARR Author Response is discussion
text, not a replacement-paper upload. A supplement is optional reviewer attention and
cannot hold the core contribution.
