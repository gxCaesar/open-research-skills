# Figure source-data contract

`source_data_manifest.json` binds every data-bearing panel to the exact portable file, repository
record, or controlled-access pointer that supports its visible marks. The manifest is safe to copy
to a reviewer-facing delivery: it contains no absolute local paths, credentials, restricted raw
objects, drafting records, or machine-specific state.

## Contents

- [Project structure](#project-structure)
- [Dataset records](#dataset-records)
- [Numeric data](#numeric-data)
- [Image data](#image-data)
- [Structures and repository objects](#structures-and-repository-objects)
- [Panel coverage](#panel-coverage)
- [Safe paths and access classes](#safe-paths-and-access-classes)
- [Reviewer delivery](#reviewer-delivery)
- [Validation commands](#validation-commands)

## Project structure

Keep portable files below `source-data/files/` and plotting entrypoints below `scripts/`:

```text
source_data_manifest.json
source-data/
  README.md
  files/
    panel-a.csv
    panel-b.tsv
scripts/
  plot_panel_a.py
```

Every file under `source-data/files/` must be declared exactly once by a dataset record. Large or
domain-native objects that should remain in a repository are represented by an accession and stable
access route instead of being copied into this directory.

The optional author-local resolution map belongs at `qa/private/source_data_local_map.json`. It may
map a dataset ID to a local working file, but delivery packaging never copies it.

## Dataset records

Each dataset has a stable ID, title, description, kind, availability, and audience. Allowed kinds
are:

- `numeric` for values used in points, lines, bars, distributions, heat maps, matrices, and summary
  statistics;
- `image` for microscopy, pathology, spatial assays, gels, or other image evidence;
- `structure` for exact molecular or macromolecular representations;
- `repository_object` for a larger or domain-specific object maintained elsewhere.

Allowed availability values are:

- `file`: a portable project-relative file is delivered;
- `repository`: an accession or stable repository record is delivered;
- `controlled_access`: a pointer, conditions, and request route are delivered, not the object;
- `not_applicable`: used only with a reason when a dataset record itself is intentionally a
  non-data placeholder. Purely schematic panels usually express this at panel coverage instead.

`audiences` contains one or more of `author`, `reviewer`, and `public`. A reviewer delivery copies
only file records eligible for `reviewer`, while retaining eligible repository and controlled-access
pointers in the delivered manifest.

The same allowlist rule applies to rendered outputs. The initializer predeclares the expected
layout-proof and complete-figure paths for the `author` audience so final pre-render validation can
run before those files exist. Add `reviewer` or `public` only after the rendered file exists and its
access boundary has been reviewed:

```json
{
  "path": "outputs/summary/fig1_reviewer-quantitative.pdf",
  "audiences": ["reviewer"],
  "content_scope": "quantitative_only",
  "contains_controlled_visual_content": false,
  "dataset_ids": ["panel-a-data"]
}
```

Every record uses a safe project-relative path below `outputs/`, declares its intended audiences,
names the content scope, and explicitly states whether it contains controlled visual content. A
reviewer or public record with controlled visual content is invalid. Final validation requires an
output declaration. The workflow's internal pre-render check accepts those declared future paths;
its post-render final check and packaging prove that every selected file exists and is a regular
non-symlink file. Reviewer packaging requires at least one substantive output.

When any declared source or asset is controlled access, every external output must use
`content_scope: quantitative_only`, bind only audience-eligible numeric `dataset_ids`, and be PDF
or SVG. Quantitative-only SVG must contain no image element, and quantitative-only PDF must contain
no image XObject. This intentionally rejects unverifiable raster substitutes; the author workspace
may still retain the full image-bearing composite and its layout proof. Mixed-access reviewer and
public packages omit layout proofs because a placeholder SVG or PNG can still embed a restricted
image.

## Numeric data

A file-backed numeric record includes:

```json
{
  "id": "panel-a-data",
  "title": "Per-specimen response values",
  "description": "Values used for every point and interval in panel a.",
  "kind": "numeric",
  "availability": "file",
  "path": "source-data/files/panel-a.csv",
  "portable_format": "CSV",
  "data_dictionary": [
    {"name": "specimen_id", "description": "Opaque specimen identifier", "unit": "identifier"},
    {"name": "response", "description": "Measured response", "unit": "normalized_unit"}
  ],
  "variables": ["specimen_id", "condition", "response", "included"],
  "conditions": ["control", "intervention"],
  "independent_unit": "specimen",
  "sample_identifiers": "reviewer-safe opaque specimen_id",
  "transformations": ["predeclared normalization"],
  "normalizations": ["state the exact denominator or reference"],
  "exclusions": ["record each material exclusion and final count"],
  "missing_values": "state whether missing values are retained, excluded, or imputed",
  "estimates": ["individual values", "prespecified group contrast"],
  "uncertainty": "interval over independent specimens",
  "render_entrypoint": "scripts/plot_panel_a.py",
  "audiences": ["author", "reviewer"]
}
```

CSV, TSV, XLSX, JSON, and plain text are the default portable formats. Preserve full precision in
the source file even when display labels are rounded. Include rows needed to reconstruct error bars,
intervals, missingness, and exclusions. Do not publish only the plotted group means when individual
values are needed to reproduce the panel.

The data dictionary defines every identifier, variable, unit, condition, and flag. `independent_unit`
names the level used for uncertainty or inference. If cells, tiles, time points, or technical
replicates are nested in that unit, keep their IDs and parent mapping rather than describing them as
independent samples.

`render_entrypoint` must read the declared file and reproduce the data marks. It must not download
an undeclared private object or silently replace data with embedded example values.

## Image data

An image record includes enough metadata to locate and interpret the displayed field:

- acquisition modality, instrument or acquisition setting needed for interpretation;
- channel identities and compositing order;
- LUT or pseudocolour mapping and whether scaling is global or per image;
- crop coordinates or an explicit `full field; no crop` statement;
- registration method or `not_applied`;
- segmentation method or `not_applied`;
- processing steps, including any global linear adjustment;
- a rendering entrypoint, or a reason that rendering is performed by a registered external imaging
  workflow.

For repository or controlled-access images, provide `repository_or_accession`. Controlled access
also requires `access_conditions` and a syntactically public HTTPS `access_route`, normally the
repository or data-access request page. A local directory, mounted share, `file:`, `smb:`, `afp:`,
or other machine-local locator is invalid; separately verify that the HTTPS route is live and
authoritative.

Source data for an image are the unprocessed or minimally processed image and its metadata, not a
pixel export of the final panel. Record crops, nonlinear transforms, pseudocolour, compositing,
registration, segmentation, and exclusions. Apply global adjustments consistently across images
being compared. Never use generative filling, object removal, or synthetic measurement marks on
scientific images.

## Structures and repository objects

A molecular or macromolecular `structure` record identifies the exact coordinate source, chain,
residue or atom mapping, model status, and rendering entrypoint. Experimental coordinates keep the
accession and resolution context. Predicted coordinates remain labelled as predicted and retain the
model/version or confidence fields required to interpret them.

A `repository_object` is appropriate for large matrices, domain-native images, genomic tracks, or
other objects that should not be flattened into a lossy table. Record the accession, version,
applicable subset, variables or layers used, and transformation performed by the plotting code.
Repository availability is not proof that the object is openly downloadable; use
`controlled_access` when access is restricted.

## Panel coverage

Every panel has one coverage record:

```json
{
  "panel_id": "a",
  "coverage": "complete",
  "dataset_ids": ["panel-a-data"],
  "supports": ["all individual points", "group contrast", "uncertainty interval"],
  "reason": null
}
```

`complete` means every quantitative mark or claim-supporting image is bound to a declared dataset.
`partial` is useful during drafting but cannot satisfy a panel whose kind is `data`, `result`, or
`negative_result`. `not_applicable` is valid only for a purely schematic or decorative panel and
requires a concrete reason. A `complete` or `partial` record cannot cite a `not_applicable` dataset,
and `not_applicable` cannot waive coverage for a claim-supporting image.

Every claim-supporting processed asset also declares non-empty `source_dataset_ids` in
`asset_manifest.json`. External eligibility is derived from both the asset record and those source
records. An asset cannot make a controlled source public by labelling itself `shareable`; the
canonical asset may remain author-only or controlled, while any distributable quantitative view is
declared separately in `delivery_outputs`.

The layout blueprint may set `source_data_required: true` for additional panels. This flag can
strengthen the obligation but cannot weaken requirements derived from panel kind or asset role.

When a panel combines microscopy and a quantitative plot, declare both image and numeric datasets
and state which visible objects each supports. When several panels share one table, all panel records
may reference the same stable dataset ID; do not duplicate the file.

## Safe paths and access classes

A file path must be relative, contain no `..`, remain below `source-data/files/`, and resolve to a
regular non-symlink file inside the project. A rendering entrypoint follows the same rule below
`scripts/`; declared outputs follow it below `outputs/`. Absolute macOS, Linux, network-share, and
Windows paths and symlink escapes are invalid in the canonical manifest.

Do not place a controlled raw object in `source-data/files/` and mark it restricted. Store only its
pointer and request conditions. Processed assets use an explicit distribution field in
`asset_manifest.json`; `controlled_access` assets are excluded from both reviewer and author
delivery trees.

The canonical manifest excludes credentials, direct subject linkage, private tile or field
locators, and machine-specific commands. Use opaque reviewer-safe identifiers when row-level data
can be shared. If de-identification or aggregation would destroy the scientific relationship, keep
the object controlled and provide an access route.

## Reviewer delivery

The reviewer packager includes:

- `venue_contract.json`, `layout_blueprint.json`, and the audience-filtered
  `source_data_manifest.json`;
- the public content ledger and asset inventory;
- `source-data/README.md`;
- only declared portable files eligible for the reviewer audience;
- eligible plotting entrypoints;
- only validated outputs explicitly authorized for the reviewer audience in `delivery_outputs`;
- a plain delivery index.

It excludes undeclared source files, author-only data files, controlled raw objects,
`qa/private/`, and internal drafting material. It fails when a required panel has no
reviewer-eligible dataset rather than creating a misleadingly complete package.

External packaging scans copied text tables, JSON, SVG, office XML, image metadata, and PDF
metadata/actions for private locators and internal workflow residue. It rejects PDF attachments.
The scan is a fail-closed hygiene check, not proof of consent, de-identification, or licence.

For a mixed-access figure, keep the full image-bearing composite and layout proof `author` only,
build an explicitly labelled quantitative-only reviewer view, and declare that separate output for
`reviewer`. Undeclared and author-only outputs are not recursively copied. Do not describe the
reduced view as visually equivalent to the full figure.

## Validation commands

Validate structure and coverage during drafting:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/validate_figure_project.py" <project> --stage draft
```

Render and review the placeholder page before detailed plots:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
```

After the review record and scientific outputs are complete, run final validation and package:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/validate_figure_project.py" <project> --stage final
python3 "$SKILL_DIR/shared/figure-core/scripts/package_deliverables.py" <project> \
  --audience reviewer
```

The packager independently reruns strict final validation and fresh QA before creating the
delivery directory. A saved PASS report is not reusable after the figure, layout, or contract
changes.

Use `--audience public` only after datasets, assets, and rendered outputs explicitly include the
`public` audience; it follows the same external-package checks with the stricter public allowlist.

Validation establishes internal consistency and safe inclusion. It does not establish scientific
correctness, consent, licence permission, de-identification, or acceptance by a publisher; those
remain tied to the actual source and destination policy.
