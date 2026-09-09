# Journal Manuscripts

[All five skills and repository setup](../README.md)

Prepare a journal article and its editor-facing materials as one consistent package.
This guide covers the independently installable skill
[`prepare-journal-manuscripts`](../skills/prepare-journal-manuscripts/SKILL.md),
covering drafting, revision, figures, statistical reporting, data availability and
final local delivery.

Nature-family writing guides are included, while the exact journal, article type and
current instructions control the task. The skill improves a supplied scientific argument;
it cannot create missing findings, author declarations or journal acceptance.

[Try the demo](#five-minute-demo) · [Browse the example](../skills/prepare-journal-manuscripts/examples/showcase/README.md) ·
[Install](#install) · [Skill guide](../skills/prepare-journal-manuscripts/SKILL.md)

![Six synthetic paired observations read directly from the supplied CSV.](../skills/prepare-journal-manuscripts/examples/showcase/preview.png)

*Teaching example only: six constructed specimens with two measurements each, not a
biological study or accepted paper.
[Source data](../skills/prepare-journal-manuscripts/examples/showcase/observations.csv) ·
[Revised excerpt](../skills/prepare-journal-manuscripts/examples/showcase/after.md) ·
[Figure specification](../skills/prepare-journal-manuscripts/examples/showcase/figure.json)*

## What it does

| Mode | Typical task | Deliverable |
|---|---|---|
| `recon` | Resolve journal, article type, stage and current policy | Source-linked requirements and unresolved authority |
| `draft` | Develop an approved outline and evidence | Complete sections within the supplied scientific contract |
| `audit` | Challenge claims, reporting and consistency | Located findings and the cheapest valid settling checks |
| `polish` | Improve structure, transitions and prose | Revision copy preserving numbers and qualifications |
| `editor-pack` | Reconcile initial-submission files | Manuscript, figures, declarations and required metadata |
| `cover-letter` | Explain journal fit without overselling | Factual journal-specific editor letter |
| `revision-response` | Address all editor and reviewer comments | Response, clean/marked copies and change locations |
| `final-package` | Prepare accepted-paper files | Inspected candidate and required production materials |

Abstracts, [statistical reporting](../skills/prepare-journal-manuscripts/components/statistics-reporting/guide.md)
and [data availability](../skills/prepare-journal-manuscripts/components/data-availability/guide.md)
are bundled components, not separate skills to install.

## Inputs and outputs

| Provide | Receive, according to the requested mode |
|---|---|
| Journal, article type, stage and requested action | Current requirements and a scoped plan |
| Manuscript source/PDF, approved outline, bibliography and evidence | Editable revision and claim-to-evidence findings |
| Figures, source data, units, uncertainty and exclusions already used | Consistent figures, full legends and reporting |
| Confirmed author, ethics, funding and repository facts | Factual declarations, availability statements and editor materials |
| Reviews and the last submitted version | Complete response and synchronized clean/marked copies |

Delivery can include the inspected rendered candidate, audit/change report, cover letter,
supplementary material and local package. Missing author-only facts remain unresolved.
An editable working draft is not automatically submission-ready.

## Install

Clone `gxCaesar/open-research-skills` once following the [repository setup](../README.md).
Python 3.9 or later is required. From that checkout root, in your selected environment:

```bash
python3 -m pip install -r skills/prepare-journal-manuscripts/requirements.txt
```

Copy the complete skill directory into the directory used by your runtime. Choose a
destination that does not already exist, then register/reload the skill:

```bash
SKILLS_ROOT=/path/to/your/agent/skills
test ! -e "$SKILLS_ROOT/prepare-journal-manuscripts" && \
  cp -R skills/prepare-journal-manuscripts "$SKILLS_ROOT/prepare-journal-manuscripts"
```

No companion repository is required. Keep the intended Python environment available
when the agent invokes helpers. Runtime resources all live below the installed directory.

| Capability | Requirement |
|---|---|
| Abstract, analysis-register and data-inventory checks | Python standard library |
| Source-data figure helper | `matplotlib==3.9.4` |
| Native PPTX authoring | `python-pptx==1.0.2` or an available presentation tool |
| Manuscript/PPTX rendering | The project's Word, LaTeX or presentation renderer |
| Concept images | An available interface and applicable permissions |

Python dependencies are pinned in
[`requirements.txt`](../skills/prepare-journal-manuscripts/requirements.txt).
The demo needs neither an image-generation service nor a document renderer.

## Five-minute demo

After installing Python dependencies, run from this repository root. These commands
also work with `SKILL_DIR` set to an independently installed copy.

```bash
SKILL_DIR="$PWD/skills/prepare-journal-manuscripts"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"

MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

Open `figure.png` in `$DEMO_OUT`, or inspect the committed preview above. The same command
creates editable-text `figure.svg` and vector `figure.pdf`. Each run gets a new output
directory to preserve earlier exports.

The incomplete analysis record should exit **1** with one `INDEPENDENT_UNIT` error:

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-missing-unit.json" --mode final --format markdown
```

The complete record should exit **0**, with `PASS`, zero errors and zero warnings:

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-complete.json" --mode final --format markdown
```

The data inventory should also exit **0** with `PASS`. It names the supplied CSV, not
an invented external repository or accession:

```bash
python3 "$SKILL_DIR/components/data-availability/scripts/validate_data_inventory.py" \
  "$DEMO/data-inventory.json" --mode final --format markdown
```

Compare the [before](../skills/prepare-journal-manuscripts/examples/showcase/before.md)
and [after](../skills/prepare-journal-manuscripts/examples/showcase/after.md):

> Before: “Twelve independent samples prove that the treatment improves response and
> generalizes to the wider population.”
>
> After: “Six constructed specimens each contribute one baseline and one follow-up
> value. Follow-up exceeds baseline for four specimens and is lower for two.”

That correction requires inspecting the source and study design. The validator catches
a missing field; it does not itself detect causal overclaiming, verify raw-data counts
or establish statistical validity. The demo performs no hypothesis test or population
inference. Its commands were exercised in an existing local Python environment, not
a fresh installation of all requirements on every platform.

## Use on your article

```text
Use $prepare-journal-manuscripts to polish this Nature-family Results section.
Keep population, effect estimates, uncertainty and citations unchanged.
Align each paragraph with its figure and flag unsupported interpretations.
```

```text
Use $prepare-journal-manuscripts in editor-pack mode to reconcile my manuscript,
figures, legends, declarations, cover letter and source-data inventory.
Do not invent author facts, repository identifiers or submission status.
```

```text
Use $prepare-journal-manuscripts in revision-response mode. Account for every
editor and reviewer comment and synchronize the response, clean manuscript and
marked version. Distinguish completed analyses from work not run.
```

A full-manuscript pass resolves authority and the scientific contract, drafts or revises
a working copy, constructs figures, renders and inspects actual pages, then reconciles
the local candidate. Editor contact, deposits, portal writes and submission remain
separate authorized actions.

## Nature-family writing and figures

The local guides address [section-level writing](../skills/prepare-journal-manuscripts/references/nature-section-style.md),
[paragraph flow and legends](../skills/prepare-journal-manuscripts/references/nature-paragraphs-and-legends.md)
and [article-shape examples](../skills/prepare-journal-manuscripts/references/nature-family-article-shapes.md).
Examples inform editorial choices; they are not universal journal rules.

For permitted schematic work, inspect relevant high-quality examples first. Borrow
composition lessons such as reading order, grouping, hierarchy and label density;
do not transfer their scientific claims, data or proprietary artwork.

New method, architecture, flowchart, motivation and mechanism schematics default to
GPT Image 2.5 concept generation followed by native editable PPTX reconstruction using
available tools directly. If the interface hides model selection, its actual backend
is reported as unknown/unverified. Measured panels remain source-derived. The bundled
[independent figure route](../skills/prepare-journal-manuscripts/references/standalone-figures.md)
covers production and actual-tool-unavailability fallbacks without another skill.

The small demo renderer is a starter for observation plots, not a turnkey dense
Nature-family figure designer. Complex figures need a project-local layout and actual
final-size review. An optional visualization skill can add specialist modality and
compound-layout guidance, but its absence does not stop this skill's work.

## Limits and troubleshooting

- **Skill not discovered:** copy the entire exact directory and reload/register it in the runtime.
- **Python import fails:** use the environment where requirements were installed.
  Document and presentation renderers are separate capabilities.
- **Demo exits 1:** expected only for `analysis-missing-unit.json`. Inspect unexpected
  failures; run intentional-failure commands separately in shells that stop on nonzero exits.
- **Figure output exists:** choose a new stem, preserving an accepted earlier artifact.
- **No renderer/image service:** complete independent work and report the exact unrun
  capability. Do not call an unrendered manuscript or raster slide fully editable.
- **A declaration, accession or analysis fact is missing:** request the specific fact
  rather than converting unknowns into polished assertions.
- **A validator passes:** this establishes bounded local record checks, not current
  policy, repository accessibility, scientific truth or acceptance.

## Maintenance

For development, install [test dependencies](../requirements-test.txt) in the intended
environment. Run from the repository root:

```bash
python3 skills/prepare-journal-manuscripts/components/abstract/tests/run_selftest.py
python3 -B -m unittest discover -s tests/journal-manuscripts -p 'test_*.py'
python3 scripts/check_public_content.py .
```

See [contributing](../CONTRIBUTING.md), [maintainers](../MAINTAINERS.md),
[third-party terms](../THIRD_PARTY.md) and the [Apache-2.0 licence](../LICENSE).
Hosted Linux CI is not configured. The repository contains no private reviews,
participant records, journal-owned templates or portal automation.

## Related work in this repository

For conference-specific stages, use the [conference guide](conference-manuscripts.md).
The [visualization guide](scientific-visualizations.md) adds advanced layouts and examples;
it is not a prerequisite for this skill.
