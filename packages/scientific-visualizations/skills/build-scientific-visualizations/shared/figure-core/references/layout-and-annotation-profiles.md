# Layout and annotation profiles

## Dated physical profiles

| Profile family | Widths | Scope |
|---|---:|---|
| `nature-figure-guide-2026-09-*` | 89 or 183 mm | Nature Research Figure Guide preparation snapshot |
| `nature-initial-submission-2026-09-*` | 90 or 180 mm | Nature initial-submission snapshot |
| `nature-research-final-artwork-2026-09-*` | 88 or 180 mm | Nature Research final artwork with caption-dependent heights |
| `nature-protocols-final-artwork-2026-09-*` | 135 or 180 mm | Nature Protocols final artwork with caption-dependent heights |
| `a4-width` | 210 mm | Author-selected general canvas, not a publisher requirement |
| `custom` | explicit | Another venue, presentation, preprint, or supplied target |

The exact records, sources, checked dates, and technical fields live in
`assets/venue-profiles.json`. Profiles are engineering snapshots, not substitutes for
current author instructions. Source and stage differences explain why there is no
single universal Nature width.

The legacy aliases `nature-single`, `nature-protocols`, and `nature-double` preserve old
projects but emit an unverified warning. They are unsuitable for a final journal package
until replaced by the exact target and stage. `venue_contract.json` records the profile
actually used; `figure_spec.json` retains the derived width needed by renderers.

## Annotation profiles

Use `minimal` for concept, data, result, and negative-result panels. Keep the panel
letter and title, decoding labels, and only the decisive values.

Use `method-readable` only for flowchart, method, and model-architecture panels. Each
stage may have a short label, one method phrase, and one necessary threshold or output.
Move explanation to the caption.

Review thresholds:

| Panel kind | Text objects | Visible characters |
|---|---:|---:|
| concept or result | 10 | 220 |
| data or negative result | 12 | 240 |
| flowchart, method, or architecture | 24 | 420 |

These thresholds produce warnings, not automatic scientific edits. Inspect any long
label or dense panel at final size.

## Open-layout rules

- Default to paper white without a full-panel frame.
- Use filled regions only for a real grouping or state.
- Prefer fewer simultaneous columns before reducing type size.
- Choose the page anchor and semantic groups before detailed panel styling.
- Let microscopy, structures, spectra, timelines, or dense axes occupy the area they
  need; do not normalize every panel to a card.
- Share axes, legends, colour scales, and condition order only when units and
  transformations are compatible.
- For four or more equal panels, state why equal area follows the scientific comparison.
- Remove unused height after the reading path is stable.
- Review a placeholder-only proof at final physical width before drawing scientific
  assets.
- Preserve the last accepted version and compare revisions at identical width.
