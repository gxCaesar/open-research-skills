# Figure specification

`figure_spec.json` is the single source for visible copy, colours, dimensions, element
coordinates, and composite placement. It does not own venue authority, scientific
hierarchy, source-data coverage, or flowchart meaning.

## Top level

```json
{
  "schema_version": "1.2",
  "figure_id": "fig1",
  "delivery_mode": "composite",
  "mode": "compound-figure",
  "editable_pptx": false,
  "layout_profile": "nature-figure-guide-2026-09-double",
  "annotation_profile": "minimal",
  "journal_profile": {
    "page_width_mm": 183,
    "dpi": 500,
    "font_family": "Arial",
    "min_font_pt": 5.0
  },
  "style": {"colors": {"paper": "#FFFFFF", "ink": "#2E3540"}},
  "assets": {},
  "panels": [],
  "composite": {"size_mm": [183, 120], "placements": []}
}
```

The layout profile resolves through `assets/venue-profiles.json`. Dated names identify
one journal, article type, submission stage, authority URL, checked date, and width.
Legacy aliases remain readable but are marked `unverified_legacy_alias`. A custom
profile requires an explicit positive `page_width_mm` and never claims to be a journal
requirement.

`delivery_mode: composite` requires one complete vector PDF/SVG and summary render.
`panel_set` additionally requires PNG/PDF/SVG for every panel. Set `editable_pptx: true`
only when the workflow will create and verify a PowerPoint deliverable.

## Coordinates

Panel size uses millimetres. Elements use normalized top-left coordinates in `0..1`.
Every visible string belongs in this specification, not separately in renderers.

When editing a data-derived figure, keep source keys separate from display labels.
A longer descriptor label should change text, not the key used to retrieve its values.
Likewise, preserve a panel's source/claim identity when moving it; update its printed
letter and figure/legend cross-references according to the new reading order. Use the
existing scene representation for visible letters rather than renaming data identities.

For a custom native renderer, verify that the edited scene property reaches the export.
An accepted JSON field may be ignored or used as a lookup key. After changing labels
or page width, re-budget the actual text and plotting area at the required physical
font size; changing only the outer rectangle does not prove the contents still fit.

## Schema 1.2 companion records

All records share the same `figure_id`:

- `venue_contract.json` owns target context, authority, and selected physical geometry;
- `layout_blueprint.json` owns page question, groups, anchor, reading path, hierarchy,
  shared encodings, and source-data obligations;
- `source_data_manifest.json` owns datasets, access classes, plotting entrypoints,
  per-panel coverage, and audience-authorized rendered outputs;
- `flowchart_spec.json` owns semantic stages, edges, pictograms, and formulas when a
  panel is `flowchart`, `method`, or `model_architecture`;
- `qa/layout_review.json` records final-width review of one blueprint revision.
- `qa/layout_proof.json` records the exact composite and resolved placement geometry
  shown in that proof.

Do not duplicate coordinates, visible labels, or colours into these records. Schema
1.0 and 1.1 projects remain readable and are not rewritten by validation.

## Assets

Each asset record contains:

```json
{
  "path": "assets/processed/example.png",
  "kind": "data_render",
  "evidence_role": "claim_supporting",
  "alt": "Description of the visible scientific object"
}
```

Allowed kinds are `conceptual_ai`, `data_render`, `structure_render`, and
`reference_image`. Allowed evidence roles are `schematic`, `claim_supporting`, and
`decorative`. A conceptual AI asset cannot be claim supporting. A claim-supporting
asset's `asset_manifest.json` record must bind non-empty `source_dataset_ids`; external
eligibility is limited by those dataset access records. Set `requires_transparency:
true` only for a cutout that must have a clean alpha border. Opaque microscopy and data
images do not need that flag.

## Panels and elements

Every panel has a unique ID, `size_mm`, `panel_kind`, and element list. Panel kinds are
`concept`, `data`, `result`, `negative_result`, `flowchart`, `method`, and
`model_architecture`.

Supported elements are text, rounded rectangle, image, line, arrow, and status mark.
Element IDs are unique across the complete figure. For line or arrow elements use
`x1`, `y1`, `x2`, and `y2`. Other positioned elements use `x`, `y`, `w`, and `h`.

Flowchart-like arrows also declare:

```json
{
  "type": "arrow",
  "id": "conditioning-arrow",
  "x1": 0.2,
  "y1": 0.5,
  "x2": 0.8,
  "y2": 0.5,
  "role": "conditioning",
  "line_style": "dashed",
  "redundancy": ["line_style", "label"]
}
```

`predicted`, `prospective`, `conditioning`, `control`, `parallel`, `optional`, and
`training_only` are dashed. `primary`, `sequence`, `inference`, `measured`, and a
source-established `causal` route are solid.

For schema 1.2 method-like panels, the same visible arrow ID appears in exactly one
semantic edge inside `flowchart_spec.json`. The semantic record resolves its endpoints,
claim anchor, optional formulas, line style, and non-colour redundancy. Coordinates do
not determine scientific direction.

## Composite placement

Composite placement uses millimetres from the top-left corner. Every panel appears
exactly once. The vector compositor scales a panel inside an optional placement box
without rasterizing it. Resolved placement boxes must remain inside the composite page;
final validation compares them with the layout-proof geometry receipt.

The placement geometry must fit the selected venue width and provide enough area for
the blueprint's intended panel job. Before detailed drawing, render the placeholder
layout proof and review it at final physical width. Fixed-height profiles constrain the
composite directly. Caption-dependent final-artwork profiles require a project-relative
`caption_file` in `venue_contract.json` before final validation.
