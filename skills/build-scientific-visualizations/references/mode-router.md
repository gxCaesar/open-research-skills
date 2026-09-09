# Visualization mode router

Choose the smallest mode that produces the requested deliverable.

All final modes use the same page-first contract: freeze claims and source coverage,
write the whole-page blueprint, render and review its proof, then draw details. A mode
changes the scientific semantics and delivery scale; it does not bypass that order.

Across final modes, new or redesigned conceptual flowchart, architecture, motivation
and method panels use the default
[image concept to editable PPTX route](image-concept-to-vector.md). Include their
native PPTX alongside required manuscript exports. Measured panels retain the data
plotting route; layout-only sketches and small edits to approved native designs do not
trigger concept regeneration.

| Mode | Minimum inputs | Required outputs | Must not be mistaken for |
|---|---|---|---|
| `layout-sketch` | panel jobs, rough hierarchy, target aspect ratio | disposable layout preview plus unresolved-content list | evidence, final artwork, or a submission figure |
| `flowchart` | stage and arrow semantics, claims, notation, venue contract | page blueprint, vector scene, cross-linked semantic graph, final-size QA | a compound result figure |
| `compound-figure` | panel claims, source data or images, caption draft, venue contract | page blueprint, source-data map, canonical scene, vector PDF or SVG, QA note | a manuscript-wide figure plan |
| `conference-figure-set` | locked paper claims, venue profile, figure jobs, insertion widths | coordinated compact set, consistent registry, rendered manuscript previews | a universal fixed three-figure template |
| `journal-figure-set` | full display-item inventory, current journal profile, exact legends | main, Extended Data, and Supplementary set plus inventory and set-wide QA | repeated copies of one layout |

## Layout sketch

Use simple boxes, panel letters, short role labels, and approximate proportions. Mark
missing evidence and unresolved comparisons directly. Do not spend time on final icons,
fonts, colours, or polish. Delete or clearly quarantine the sketch when the canonical
scene is created so it cannot be shipped accidentally.

## Conference figure set

Read [conference figure design](conference-figure-design.md). It covers selecting
distinct figure jobs, method semantics, inspected paper examples and checking the
actual compiled insertion. Refresh current venue authority for format and geometry;
the examples do not establish submission rules.

## Routing edge cases

- A schematic panel inside a compound figure uses `flowchart_spec.json` semantics and
  compound-page composition; every visible arrow is covered exactly once.
- A graphical abstract is normally `compound-figure`; use `flowchart` only when the
  whole artifact is genuinely a process diagram.
- A redesign request keeps the original evidence and claim boundary unless the user
  explicitly authorizes a scientific change.
- A figure-set request starts with an inventory. Do not polish individual panels until
  the set has no duplicated job or missing load-bearing claim.
