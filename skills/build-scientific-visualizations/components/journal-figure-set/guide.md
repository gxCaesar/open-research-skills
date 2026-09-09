# Journal-Figure-Set Mode Reference

Coordinate a complete journal figure set without turning every display item into the same
template. Each figure keeps its own scientific question while sharing notation, colour
semantics, typography, geometry, and evidence rules across the manuscript.

## Ownership boundary

- Select this mode for a manuscript-wide main, Extended Data, and Supplementary set.
- Select `compound-figure` to author or redesign one complete figure.
- Select `flowchart` for one standalone workflow, mechanism, or architecture diagram.

Resolve `../../shared/figure-core/` relative to this guide. Use that shared core for
each figure project; do not copy or fork its scripts. Read
`references/nature-geometry.md`, `references/palette-and-accessibility.md`, and the
shared `references/qa-contract.md` before fixing the set-wide contract.
When the author asks to calibrate the figure sequence against published Nature-family
Articles, or requests DOI/PDF-page-supported empirical precedents for the sequence,
also read `references/nature-family-evidence-arcs.md`. Its examples are bounded
precedents, not a fixed template or current journal policy.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## 1. Build a figure inventory

Create one inventory row for every main, Extended Data, and Supplementary display item:

| Field | Required content |
|---|---|
| ID and class | Figure number plus main, Extended Data, or Supplementary |
| Scientific question | One question the figure resolves |
| Narrative job and decision | Its role in the article and the next inference or experiment it unlocks |
| Claim and source | Claim, exact artifact or manuscript anchor, and evidence state |
| Panels | Panel IDs, roles, required comparisons, and decisive controls |
| Geometry | Exact journal, article type, stage, dated authority, target width, estimated height, caption words |
| Blueprint | Page question, anchor, semantic groups, reading path, relative area, shared encodings, revision |
| Dependencies | Source-data IDs, analysis files, source images, plotting modules, and upstream figures |
| Source visibility | Main, Extended Data, and Supplementary coverage; verified caption, page, and panel count or explicit `UNVERIFIED` |
| Status | planned, draft, validated, visually reviewed, or accepted |

Use main figures for the central causal or empirical argument. Move robustness,
diagnostics, and scope extension to Extended Data only when doing so does not hide a
load-bearing qualifier. Supplementary figures remain interpretable and source anchored;
they are not a dumping ground for unexplained outputs.

Do not impose a panel-count ceiling or uniform density. Use whitespace to separate
semantic groups and protect the visual anchor. Dense displays are valid when every panel
advances a necessary comparison and the reading order remains legible at final size.

For any dense member of the set, use
[dense compound design](../../references/dense-compound-design.md) to allocate evidence
groups and internal views before rendering. Keep visual consistency across the set
without copying the same grid or panel density into every figure.

## 2. Freeze the shared visual contract

Define one set-wide registry for notation, abbreviations, category-to-colour mappings,
markers, line styles, hatches, typography, line weights, panel letters, and legend
language. A semantic role keeps the same encoding across all figures. Colour never
carries category identity alone.

Use Arial or the target journal's required sans-serif at final size. Nature-family
sources differ by journal and stage, including 88, 89, 90, 135, 180, and 183 mm width
records in the bundled snapshot. Select the record that matches the actual destination
and stage. These are dated engineering profiles, not universal journal rules; current
target-journal instructions take precedence.

## 3. Author each figure from its own canonical scene

Create one project per display item:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <project> \
  --figure-id <id> --mode journal-figure-set --layout-profile <dated-profile> \
  --annotation-profile minimal --delivery-mode composite
```

Complete the content ledger, source-data manifest, venue contract, and asset registry
before rendering. Give every main, Extended Data, and Supplementary display item its
own `layout_blueprint.json`; do not reuse one geometry merely for set-wide consistency.
Render and review each whole-page proof before detailed panels. Keep visible text,
coordinates, page dimensions, colours, and placements in `figure_spec.json`. Apply the
flowchart semantic contract to any method or architecture panel. For new or redesigned
method, architecture, motivation or mechanism schematics, follow the default
[image concept to editable PPTX route](../../references/image-concept-to-vector.md)
using the journal-appropriate style. Keep only those conceptual panels on that route;
measured plots and source images retain their data-derived content and rendering.

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
# Inspect at final width and complete the matching layout review.
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase final
```

Keep manuscript figure includes pointed at the canonical build outputs. Avoid an
untracked second copy that can become stale. When an output depends on analysis files,
rebuild it after those inputs change and record that dependency in the inventory.

## 4. Validate geometry against the actual caption

Export one vector PDF page per display item. Count caption words from the manuscript or
the exact legend being delivered, then validate the PDF page:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/validate_journal_pdf.py" <figure.pdf> \
  --venue-contract <project>/venue_contract.json --caption-file <caption.txt>
```

The validator reads actual PDF dimensions. It enforces the selected dated profile and a
0.2 mm engineering tolerance; it does not prove acceptance by a journal. A target
journal's current instructions, production request, or supplied template overrides the
bundled table. Do not resize a finished PDF inside the manuscript to make it appear
compliant.

## 5. Verify scientific and set-wide consistency

Refine each schematic using
[rendered schematic refinement](../../references/visual-refinement.md), then compare
the retained figures together for consistent visual language. Keep measured evidence
unchanged and avoid polishing each panel into an unrelated style.

For every figure, run the shared schema validator, renderer, compositor, and QA script.
Then inspect the whole set in manuscript order. Check:

- every displayed value, label, crop, and arrow against its source;
- consistent notation, semantic colours, units, baselines, scales, and condition order;
- independent legibility of main, Extended Data, and Supplementary legends;
- exact PDF width and caption-dependent height;
- embedded fonts, vector content, clipping, collisions, and minimum type size;
- grayscale and colour-vision-deficiency decoding;
- figure references and panel letters in the manuscript.

At first reading, each figure should reveal its question, compared conditions, direction,
and principal readout without depending on the caption. The caption supplies independent
units, sample counts, uncertainty and statistical tests, treatment details, scale,
channel definitions, exclusions, and evidence boundaries; it does not rescue an
undecodable composition.

A geometry check cannot see a line crossing text, an ambiguous crop, or a misleading
visual comparison. Render every delivered PDF to an image and review it at final size.
Write a short disposition for every QA warning and keep unresolved high-severity defects
out of the release set.

## 6. Handle generated assets and policy safely

Prefer native vector or licensed source assets. Before using any generated or modified
asset, check the current policy of the exact target journal and record the applicable
decision in the author workspace. Never treat a general publisher policy as permanent
permission for every journal, article type, or image role. Generated content cannot
stand in for scientific evidence.

## 7. Deliver the set

Deliver:

- canonical vector PDFs and SVGs for main, Extended Data, and Supplementary figures;
- one legend per display item, matching manuscript panel labels and terminology;
- editable scene specifications, page blueprints, layout proofs, palettes, source-data
  manifests, and plotting modules;
- a set-wide inventory and concise visual QA report;
- native editable PowerPoint for schematics authored through the default route,
  separately rendered and checked; a PowerPoint copy of the entire set is optional.

Reviewer-facing material excludes controlled raw objects, private locators, drafting
prompts, agent instructions, internal workflow state, approval records, and internal
integrity metadata. Include only declared reviewer-eligible source files plus safe
repository or controlled-access pointers. A mixed-access figure may need a separately
labelled quantitative-only reviewer view rather than the full image-bearing composite.
