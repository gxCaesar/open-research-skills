# Page-first blueprint contract

A publication figure is one visual argument, not a folder of panels. Plan the complete page before
drawing detailed marks. The blueprint assigns scientific jobs, reading order, relative area, shared
encodings, and source-data obligations. `figure_spec.json` remains the only authority for visible
copy and geometry.

## Contents

- [Freeze content before layout](#freeze-content-before-layout)
- [Define the page argument](#define-the-page-argument)
- [Group evidence and allocate area](#group-evidence-and-allocate-area)
- [Write layout_blueprint.json](#write-layout_blueprintjson)
- [Render the layout proof](#render-the-layout-proof)
- [Review at final physical width](#review-at-final-physical-width)
- [Proceed to detailed drawing](#proceed-to-detailed-drawing)
- [Stop conditions](#stop-conditions)

## Freeze content before layout

Before choosing panel sizes, reconcile the manuscript passage, caption, analysis outputs, plotting
code, and source images. For each proposed panel, lock:

- the question and claim;
- the exact source anchor;
- measured, inferred, predicted, prospective, schematic, or decorative status;
- the comparison, direction, unit, denominator, and decisive control;
- the independent unit and any repeated observations nested within it;
- the source-data record that supports every visible mark or image;
- the implication the panel must not create.

Do not use a layout decision to resolve a scientific disagreement. If two interpretations change a
claim, arrow direction, comparison, independent unit, or evidential status, keep that element out of
the claim-bearing page until the source resolves it.

## Define the page argument

Write one answer for each field before arranging panels:

| Field | Test |
|---|---|
| `question` | Can a reader state the complete-page scientific question in one sentence? |
| `narrative_job` | What work does this figure do that no preceding figure already does? |
| `decision_unlocked` | What inference, experiment, or limitation becomes justified after reading it? |
| `visual_anchor` | Which evidence must be seen first or largest for the argument to remain honest? |
| `reading_path` | In what semantic order should the evidence be decoded? |

The visual anchor follows evidential importance and legibility. A whole-slide image, structural
overview, longitudinal trajectory, or decisive outcome may need more area than a compact control.
The most colourful panel is not automatically the anchor.

## Group evidence and allocate area

Group panels by scientific transition, not by file origin or chart family. Useful transitions
include measurement to mechanism, cohort to endpoint, global tissue to ROI, prediction to
independent validation, and headline result to falsification. Give every group one role and every
panel exactly one owning group.

Allocate area in this order:

1. protect the anchor's minimum legible image or plotting area;
2. protect scales, channel keys, axes, labels, and uncertainty needed to decode evidence;
3. align comparisons that share conditions, scales, or independent units;
4. reserve whitespace or a thin divider between different inferential jobs;
5. compress secondary controls only after they remain readable at final width;
6. remove repeated legends, repeated axes, and decorative framing;
7. if necessary evidence still cannot fit, identify the exact constraint and propose a
   scientific figure split rather than shrinking type below the venue minimum or
   silently removing requested panels.

Unequal panel area is often useful, but asymmetry is not a style requirement. Four or more equal
panels are acceptable when equality expresses a scientifically matched comparison. Record that
reason in `uniform_size_rationale`. Without it, validation emits a mechanical-grid warning rather
than silently treating a default grid as deliberate design.

Shared scales and legends require scientific compatibility. Do not share an axis across different
units, transformations, denominators, or estimands. Do not share a colour scale across images with
different acquisition or processing unless the values are genuinely comparable.

## Write layout_blueprint.json

The blueprint contains hierarchy and meaning, never visible coordinates. A minimal record is:

```json
{
  "schema_version": "1.2",
  "figure_id": "fig1",
  "blueprint_revision": 1,
  "mode": "compound-figure",
  "question": "Does the spatial signal survive specimen-level validation?",
  "narrative_job": "connect the tissue measurement to the held-out validation",
  "decision_unlocked": "whether the proposed spatial association is credible",
  "reading_path": ["measurement", "validation"],
  "visual_anchor": {
    "panel_id": "a",
    "reason": "the tissue overview defines every downstream ROI comparison"
  },
  "groups": [
    {
      "id": "measurement",
      "panels": ["a", "b"],
      "role": "measurement",
      "emphasis": "primary"
    },
    {
      "id": "validation",
      "panels": ["c"],
      "role": "outcome",
      "emphasis": "supporting"
    }
  ],
  "panels": [
    {
      "id": "a",
      "group_id": "measurement",
      "evidence_role": "measurement",
      "priority": "anchor",
      "preferred_aspect": "wide",
      "shared_scale_group": null,
      "legend_owner": "a",
      "source_data_required": true
    }
  ],
  "shared_scale_groups": [],
  "layout_rationale": "The tissue overview is wide; validation shares condition order but not image scale."
}
```

Panel IDs must match `figure_spec.json`, `content_ledger.json`,
`source_data_manifest.json`, and composite placements. `reading_path` names groups rather than
panels so the page can contain local comparisons without turning into one long row. Increment
`blueprint_revision` after changing the panel set, group ownership, anchor, reading path, shared
encoding, or intended relative area.

## Render the layout proof

Initialize the project with the intended mode and a dated venue profile:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <project> \
  --figure-id <id> --mode compound-figure \
  --layout-profile nature-figure-guide-2026-09-double
```

After editing the content records, blueprint, panel sizes, and composite placements, run only the
layout phase:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
```

This validates the schema and writes `outputs/layout/<id>_layout-proof.svg` plus a PNG preview. It
also writes `qa/layout_proof.json`, a plain geometry receipt containing the blueprint revision,
composite size, and resolved placement boxes. The proof draws boundaries, panel IDs, short evidence
roles, legend ownership, reading-path order, and the anchor marker. It deliberately does not load
microscopy, structures, quantitative plots, or other claim-supporting assets.

Schema 1.0 and 1.1 projects remain validation-only in the layout phase. They are not silently
rewritten and do not receive a schema-1.2 proof or receipt.

## Review at final physical width

Inspect the proof at its actual aspect ratio and selected width. Record all seven checks in
`qa/layout_review.json`:

| Check | PASS means |
|---|---|
| `question_and_reading_path` | The eye encounters evidence in the order needed to answer the page question. |
| `anchor_and_hierarchy` | The anchor is dominant enough, while supporting evidence remains legible. |
| `grouping_and_whitespace` | Boundaries reveal scientific transitions without decorative containers. |
| `final_width_allowance` | Text, axes, scale bars, images, and dense labels have realistic space. |
| `shared_encodings` | Shared axes, scales, legends, and condition order are scientifically valid. |
| `mechanical_grid_risk` | Equal sizing is justified or the page has been redesigned. |
| `semantic_coverage` | Flowchart semantics and source-data obligations are resolved. |

Set `status` to `PASS` only when every check passes. The record must echo the current
`blueprint_revision`, ordered panel IDs, and selected venue width. A mismatch makes the review
stale. Final validation also compares `qa/layout_proof.json` with the current composite and
placement geometry, so changing a page box after review invalidates the proof even if the revision
number was not updated. These checks are intentionally plain and inspectable.

## Proceed to detailed drawing

After layout review passes:

1. populate source-data files and image metadata;
2. replace placeholders with source-derived plots and registered assets;
3. write all visible copy and geometry in `figure_spec.json`;
4. cross-link method-like panels through `flowchart_spec.json`;
5. run `run_workflow.py --phase final`;
6. inspect the complete figure before inspecting isolated panels;
7. package only after final QA passes.

For a journal figure set, repeat the blueprint and proof for each main, Extended Data, and
Supplementary display item. Share notation and encodings across the set, but do not force all
figures into the same geometry.

## Stop conditions

Stop claim-bearing drawing when any of these remains unresolved:

- the source does not determine a claim, direction, comparison, or independent unit;
- panel IDs disagree across the project records;
- a method-like panel has an uncovered or multiply covered visible arrow;
- a data-bearing panel lacks source-data coverage;
- the requested figure width is tied to an ambiguous legacy alias;
- the page exceeds the fixed or caption-dependent venue height;
- the proof cannot keep required evidence legible at final physical width;
- the layout review or geometry receipt is `REVISE`, stale, missing, or incomplete.

A stopped detailed render is a useful result: revise the page argument or obtain the missing
evidence without manufacturing a polished but unsupported figure.
