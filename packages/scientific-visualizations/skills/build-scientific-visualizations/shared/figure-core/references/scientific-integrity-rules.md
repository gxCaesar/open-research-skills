# Scientific integrity rules

## Separate conceptual illustration from evidence

In delivered figures, restrict AI-generated assets to conceptual illustration:

- animals, cells, organs and generic laboratory apparatus;
- schematic assay concepts;
- non-quantitative mechanism illustrations;
- decorative biological context.

The default [schematic authoring route](../../../references/image-concept-to-vector.md)
uses a complete image concept to guide native editable reconstruction.
Keep this visual-design intermediate separate from evidence, and verify every label,
symbol and relationship against the scientific source before it enters the final figure.
Reconstruction does not remove AI-derived-artwork disclosure or publisher restrictions.

Use real source data or structure-derived rendering for claim-supporting elements:

- protein structures and residue locations;
- docking poses and molecular contacts;
- chemical structures;
- quantitative charts and statistical annotations;
- microscopy, pathology and experimental images.

Never let an AI-generated object resemble a measured or computed result without a visible `schematic` label.

## Build a content ledger before drawing

For every panel, record:

- the core claim;
- source file and exact anchor or line span;
- required objects and labels;
- evidence status (`observed`, `prospective`, `hypothesis`, `schematic`);
- whether wet data exist;
- prohibited implications;
- the decisive control.

Do not promote a prospective assay, predicted pose or planned validation into an observed result.

## Validate every visible statement

- Match panel text to the ledger before export.
- Keep wet-data status explicit when the figure is prospective.
- Keep target attribution separate from drug pharmacology.
- Use knockout, mutation or control logic only when supported by the manuscript.
- Do not invent affinity, direction, selectivity or significance values.

## Bind evidence to source data

- Give every data-bearing panel a complete `source_data_manifest.json` record.
- Preserve the independent unit and the mapping from nested cells, ROIs, tiles,
  technical replicates, time points, or seeds.
- Record transformations, normalization, exclusions, missingness, estimates, and
  uncertainty used by the display.
- Keep scientific images tied to acquisition, channels, LUT, crop, registration,
  segmentation, processing, and an exact source or controlled-access pointer.
- Treat a repository identifier as a pointer, not evidence that access or redistribution
  is unrestricted.
- Never package a restricted raw object merely because it is present in a processed or
  output directory.

## Preserve page-level scientific hierarchy

Choose the whole-page question, anchor, groups, reading path, and relative area before
detailed drawing. Panel area communicates importance and protects legibility. Equal
sizes are valid for a scientifically matched comparison, not as an automatic grid.
Review the complete page at final physical width; do not accept a visually coherent
panel set whose page order changes the intended inference.

## Caption contract

Open with the scientific takeaway the reader should learn from the figure, then define panels,
conditions, encodings, statistics and provenance needed to interpret it without hunting through the
main text. Keep extended interpretation and argument in the manuscript. A caption must not strengthen
the claim beyond the content ledger or turn a schematic into evidence.

## Treat exact structures as data products

Export exact structural elements from PyMOL, ChimeraX, RDKit, Mol*, plotting code or the original analysis artifacts. AI may supply a pale membrane, cell or contextual background, but not the residue geometry or quantitative relationship.
