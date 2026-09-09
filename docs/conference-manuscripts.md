# Conference Manuscripts

[All five skills and repository setup](../README.md)

Prepare an evidence-linked conference paper from draft to local submission package.
This guide covers the independently installable skill
[`prepare-conference-manuscripts`](../skills/prepare-conference-manuscripts/SKILL.md),
for AAAI, ICLR, ACL, CVPR, ICML, NeurIPS and other computing venues.

It covers scientific explanation, abstracts, statistical reporting, manuscript figures,
anonymous review, rebuttals and final files. It preserves the supplied results and
protocol; it does not create missing experiments or submit to a venue on your behalf.

[Try the demo](#five-minute-demo) · [Browse the example](../skills/prepare-conference-manuscripts/examples/showcase/README.md) ·
[Install](#install) · [Skill guide](../skills/prepare-conference-manuscripts/SKILL.md)

![Six synthetic task scores read directly from the supplied CSV.](../skills/prepare-conference-manuscripts/examples/showcase/preview.png)

*Teaching example only, not a benchmark result or accepted paper.
[Source data](../skills/prepare-conference-manuscripts/examples/showcase/scores.csv) ·
[Figure specification](../skills/prepare-conference-manuscripts/examples/showcase/figure.json)*

## What it does

| Mode | Typical task | Deliverable |
|---|---|---|
| `recon` | Resolve current venue/year/track/stage rules | Source-linked requirements and unresolved form questions |
| `draft` | Develop an approved outline and result set | Evidence-linked manuscript sections, abstract and figures |
| `audit` | Check claims, format, anonymity and consistency | Located findings, impact and smallest settling check |
| `polish` | Improve prose without changing the science | Revision copy preserving numbers, qualifiers and citations |
| `rebuttal` | Account for every reviewer concern | Point-by-point response and synchronized changes |
| `camera-ready` | Reconcile accepted text and required changes | Final-source candidate, declarations and rendered review |
| `package` | Check exact submission files | Local candidate inventory and unresolved items |

A combined polish-and-package request follows the
[whole-paper workflow](../skills/prepare-conference-manuscripts/references/full-paper-workflow.md):
intake and audit precede revision. An unsupported load-bearing result, absent scientific
contract or unresolved P0 remains `NOT READY`; polishing cannot repair missing evidence.

## Inputs and outputs

| Provide | Receive, according to the requested mode |
|---|---|
| Exact venue, year, track, stage and requested action | Applicable requirements and a scoped plan |
| Manuscript source/PDF, figures, bibliography and approved outline | Editable revision, figures, legends and inspected rendered candidate |
| Exact results, methods, splits, comparators, independent units, uncertainty and limitations | Claim-to-evidence findings and evidence-preserving prose |
| Reviews and the last approved/submitted version | Complete response and linked change locations |
| Confirmed authorship, declarations and required supplementary files | Reconciled local candidate package and explicit author-only gaps |

The skill can inventory missing inputs, but cannot invent results, declarations or
repository availability. An editable draft is not automatically submission-ready.

## Install

Clone `gxCaesar/open-research-skills` once following the
[repository setup](../README.md#安装与快速开始).
Python 3.9 or later is required. From that checkout root, in your selected environment:

```bash
python3 -m pip install -r skills/prepare-conference-manuscripts/requirements.txt
```

Copy the complete skill directory into the directory used by your runtime, then
register/reload it there. Choose a destination that does not already exist:

```bash
SKILLS_ROOT=/path/to/your/agent/skills
test ! -e "$SKILLS_ROOT/prepare-conference-manuscripts" && \
  cp -R skills/prepare-conference-manuscripts "$SKILLS_ROOT/prepare-conference-manuscripts"
```

No companion repository is required. Keep the intended Python environment available
when the agent invokes helpers. Runtime resources all live below the installed directory.

| Capability | Requirement |
|---|---|
| Source and record checks | Python standard library |
| PDF audit | `pypdf==6.10.2` |
| Source-data figure helper | `matplotlib==3.9.4` |
| Native PPTX authoring | `python-pptx==1.0.2` or an available presentation tool |
| Actual manuscript/PPTX rendering | The project's LaTeX, Word or presentation renderer |
| Concept images | An available image-generation interface and applicable permissions |

Python dependencies are pinned in
[`requirements.txt`](../skills/prepare-conference-manuscripts/requirements.txt).
The demo needs neither TeX nor an image-generation service.

## Five-minute demo

After installing the dependencies, run from this repository root. These commands also
work with `SKILL_DIR` set to an independently installed copy.

```bash
SKILL_DIR="$PWD/skills/prepare-conference-manuscripts"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"

MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

Open `figure.png` in `$DEMO_OUT`, or inspect the committed preview above.
The output contains `figure.svg` (editable text), `figure.pdf` (vector) and
`figure.png` (preview). A new directory on each run preserves earlier outputs.

Audit the deliberately flawed source. This command should exit **1**, reporting
`ANON_SOURCE_IDENTITY` and `ANON_ACKNOWLEDGMENTS`:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/before.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

The corrected excerpt should exit **0**, with `Findings: 0`:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/after.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

The [example walkthrough](../skills/prepare-conference-manuscripts/examples/showcase/README.md)
also shows a manual claim repair:

> Before: “The candidate consistently outperforms the baseline across all tasks.”
>
> After: “In six illustrative tasks, the candidate score is higher on four tasks and
> lower on two. The mean paired difference is 0.005 arbitrary score units.”

The TeX checker catches the source defects, not that scientific overclaim. The profile
is a synthetic teaching contract, not official venue policy. Zero findings do not prove
rendered anonymity or submission readiness. These commands were exercised in an existing
local Python environment; they are not evidence of a fresh installation on every platform.

## Use on your paper

```text
Use $prepare-conference-manuscripts in audit mode on this anonymous paper.
Check the exact venue/year/track requirements and map the central claims to my
supplied result tables. Do not edit files.
```

```text
Use $prepare-conference-manuscripts to polish and package this draft.
Preserve the scientific contract and work in a revision copy. Deliver the revised
source, figures, rendered candidate and the six whole-paper deliverables.
```

```text
Use $prepare-conference-manuscripts in rebuttal mode with these reviews and the
last submitted version. Distinguish completed new evidence from experiments not run.
```

A full-paper pass resolves current rules and evidence, audits, revises within the
approved scope, renders and inspects, then reconciles the local candidate.
Upload, portal changes and submission require separate author authorization.

## Figures and venue support

For permitted schematic work, inspect relevant high-quality examples first. Borrow
composition lessons such as reading order, grouping, hierarchy and label density;
do not transfer their scientific claims, data or proprietary artwork.

New method, architecture, flowchart and motivation schematics default to GPT Image 2.5
concept generation followed by native editable PPTX reconstruction using available tools
directly. A tool without a model selector is still usable; its actual backend is reported
as unknown/unverified. Measured plots remain source-derived. This demo is a data plot,
not a replacement for the schematic workflow. See the
[independent figure route](../skills/prepare-conference-manuscripts/references/standalone-figures.md).

Local adapters cover [AAAI](../skills/prepare-conference-manuscripts/components/venues/aaai/guide.md),
[ICLR](../skills/prepare-conference-manuscripts/components/venues/iclr/guide.md),
[ACL](../skills/prepare-conference-manuscripts/components/venues/acl/guide.md),
[CVPR](../skills/prepare-conference-manuscripts/components/venues/cvpr/guide.md),
[ICML](../skills/prepare-conference-manuscripts/components/venues/icml/guide.md) and
[NeurIPS](../skills/prepare-conference-manuscripts/components/venues/neurips/guide.md).
Select an adapter by exact `venue/year/track` scope. Every profile is a dated engineering
aid, so run `recon` against current first-party sources when its scope is stale or does not
match the intended submission.

Use the generic component only when no current first-class profile matches; create a
task-local profile instead of mutating a bundled one. See the
[generic adapter](../skills/prepare-conference-manuscripts/components/venues/generic/guide.md).

Each formal adapter links to paper observations that are optional empirical drafting
evidence, never venue rules or mandatory section order.
No venue-owned style files or exemplar papers are bundled.

## Limits and troubleshooting

- **Skill not discovered:** copy the whole exact directory and reload/register it in the runtime.
- **Python import fails:** use the environment where requirements were installed. Python
  packages do not install TeX or a PowerPoint renderer.
- **Demo exits 1:** expected for `before.tex`, not `after.tex`. Exit 2 indicates an unusable
  input/profile rather than a manuscript finding. Run intentional-failure commands
  separately if your shell stops on any nonzero exit.
- **Figure output exists:** choose a fresh output stem, preserving approved earlier artifacts.
- **No renderer/image service:** report the precise unrun step and finish independent safe
  work. Source checks are not rendered-PDF review; SVG is not native PPTX.
- **Evidence or current policy is missing:** keep the gap. Validators cannot establish
  novelty, statistical validity, venue-rule currency or acceptance.

## Maintenance

For development, install [test dependencies](../requirements-test.txt) in the intended
environment. Run from the repository root:

```bash
python3 skills/prepare-conference-manuscripts/components/abstract/tests/run_selftest.py
python3 -B -m unittest discover -s tests/conference-manuscripts -p 'test_*.py'
python3 scripts/check_public_content.py .
```

See [contributing](../CONTRIBUTING.md), [maintainers](../MAINTAINERS.md),
[third-party terms](../THIRD_PARTY.md) and the [Apache-2.0 licence](../LICENSE).
Hosted Linux CI is not configured. Examples contain no private reviews or submission material.

## Related work in this repository

For a journal submission, use the [journal guide](journal-manuscripts.md). For advanced
visual design, see [scientific visualizations](scientific-visualizations.md); the conference
skill still completes its own task without that additional installation.
