# Research Publication Workflow

[All five skills and repository setup](../README.md)

An independently installable agent skill for taking a research question through data
feasibility, literature comparison, fair baselines, controlled experiments, claim
formation, an evidence-linked working manuscript and local code-release preparation.
It is designed for top computer-science and Nature-family research, with substantial
AI-for-biology guidance. It does not turn incomplete experiments into a finished paper.

**Start here:** [five-minute demo](#five-minute-demo) ·
[read a result-to-paragraph example](../skills/research-publication-pipeline/examples/result-to-paragraph.md) ·
[skill instructions](../skills/research-publication-pipeline/SKILL.md) ·
[independent manuscript route](../skills/research-publication-pipeline/references/standalone-manuscript.md)

`research-publication-pipeline` is one of five skills in Open Research Skills. Paper
reading, manuscript guidance and local figure tools are included. Other research skills
are optional enhancements. Scripts initialize and check records; the agent and researcher
still perform source inspection, experiments, interpretation, writing and visual review
using appropriate tools and authority. A full research-to-paper request continues through
the inspected local candidate, not just a handoff record.

The reusable scientific decision system and validators are public. Private infrastructure,
remote launch adapters, historical run state, actual authorization records, and project-specific
evidence are excluded. The package is self-contained and uses no absolute local dependency or
external symlink.

## Choose the work you need

| Mode | Typical input | Output or decision |
|---|---|---|
| `survey` | Research question, papers, data sources or a bounded paper corpus | Source-grounded field map, paper cards and candidate gaps |
| `plan` | Selected route, project authority and constraints | Charter, hypothesis, decisive checks, resources and stop rules |
| `pilot` | Accessible data and one uncertain premise | Small feasibility test and observed limits |
| `develop` | Frozen protocol and matched baseline results | Measured headroom and controlled mechanism comparisons |
| `monitor` | Outputs from an already authorized run | Observed progress, completion or anomaly |
| `freeze` | Candidate, selection rule and evaluation contract | Evaluation readiness with the locked-test boundary preserved |
| `claim-lock` | Actual results and uncertainty | Supported, narrowed, refuted and not-run claims |
| `handoff` | Locked evidence and terminal scientific outcome | Scoped transfer, a negative report, renewed intake or stop decision |
| `manuscript` | Sufficient evidence, working-draft authority and current venue rules | Complete sections, figures, legends, rendered candidate and local package |
| `public-release` | Ready local research code tree | Curated artifact and observed rehearsal, without publication |

Use it to assess a new single-cell method, compare exemplar papers, resume a study,
preserve a negative result or complete an authorized research-to-paper task. A
survey-only or status-only request does not implicitly request experiments or a paper.

## Five-minute demo

This is a local software demonstration, not a biological experiment. Python 3.9+ and
its standard library are sufficient. Clone `gxCaesar/open-research-skills` once using
[repository setup](../README.md); the demo then needs no network, API key,
agent account or package installation. Run from the repository root:

```bash
demo_root=$(mktemp -d)
python3 -B skills/research-publication-pipeline/examples/run_demo.py "$demo_root/publication-demo" --with-public-release
```

Expected status lines:

```text
pilot: PASS
development: PASS
handoff: PASS
public-release: PASS
```

The script also prints a synthetic-use warning and output location. The workspace stays
outside the checkout; the curated teaching sample is the public demonstration.
These commands use macOS/Linux-style shell syntax; on another shell supply an equivalent
new temporary output path. It creates a synthetic project, packages a ten-file arithmetic example,
unpacks it into a fresh temporary directory, runs its example and two tests, and checks
the output using the existing interpreter. It does not install a fresh environment.

| What actually ran | Observed result | What this does not prove |
|---|---|---|
| Arithmetic example on `[1, 2, 3]` | `count = 3`, `total = 6` | Scientific effectiveness |
| Two packaged tests | Both pass | General correctness on all inputs |
| Local record and release checks | Four targets pass | Independent research reproduction or permission to publish |

Read the [annotated result and manuscript-style excerpt](../skills/research-publication-pipeline/examples/result-to-paragraph.md)
without running anything, or inspect the outputs using the
[demo guide](../skills/research-publication-pipeline/examples/README.md). Scientific
comparison values in the fixture are injected, not estimated by this demo. It does
not write or render a full manuscript or figure. Do not publish the generated workspace
as research evidence.

## Install

Copy the independently installable skill into the skills directory selected by your agent runtime:

```bash
cp -R skills/research-publication-pipeline \
  /path/to/skills/research-publication-pipeline
```

Replace the destination with your runtime's skills directory. Use a destination that
does not already contain this skill; preserve or deliberately update an existing copy.
Everything needed by the skill is below that one directory. Select
`research-publication-pipeline`, or invoke `$research-publication-pipeline` where your
runtime supports named skills. Copying does not configure an account or install another
research skill.

Python 3.9 or later is required. The initializer and project validator use only the Python
standard library. The internal paper-card component needs pypdf for PDF input and Poppler's
`pdftoppm` only when rendered pages are requested. From the copied skill directory, install the
tested Python dependencies with `python3 -m pip install -r requirements.txt`; the local
figure helper uses `matplotlib==3.9.4`, and native PPTX authoring can use
`python-pptx==1.0.2`, both declared locally. Installation is a copy
operation; this repository does not alter an agent account.

From the checkout, the equivalent optional dependency command is:

```bash
python3 -m pip install -r skills/research-publication-pipeline/requirements.txt
```

Live sources require browser/source access. Image concepts require an available,
permitted image service. Actual manuscript and PPTX rendering require their respective
project tools. The standard-library demo needs none of these; it does not install or
invoke them.

## Invoke

```text
Use $research-publication-pipeline to assess this AI-for-biology topic. Keep data feasibility,
lane-specific scoop, and venue fit separate, measure cheap-baseline headroom before proposing a
model, and identify the next evidence-backed gate.
```

For a real task, provide the research question, current project authority, target
contribution/venue, papers, data-access evidence, existing protocol/results and resource
constraints. Keep private data and project records outside the public checkout.

Create and check a standalone workspace by resolving the copied skill directory explicitly:

```bash
SKILL_DIR=/path/to/skills/research-publication-pipeline
python3 "$SKILL_DIR/scripts/init_publication_project.py" /path/to/project \
  --project-id example-study \
  --title "A falsifiable research question" \
  --domain genomics \
  --contribution-lane sota-method

python3 "$SKILL_DIR/scripts/validate_publication_project.py" /path/to/project \
  --target working --format text
```

The initializer refuses to overwrite a non-empty directory. Validation targets progress through
`working`, `pilot`, `development`, `handoff`, and `public-release`.

An initialized workspace contains unresolved records, not a completed experiment. On
resume, inspect its actual authority and newest results before trusting narrative status.
The ordinary full workflow is:

1. Judge data feasibility, lane-specific scoop and venue fit separately. Choose
   `sota-method`, `discovery` or `benchmark` explicitly; difficulty does not authorize
   changing the contribution type.
2. Freeze the hypothesis and fair evaluation protocol. Measure cheap-baseline headroom
   before adding complexity, against the strongest relevant matched comparator.
3. Run authorized experiments one registered mechanism at a time, retain negative
   outcomes and protect the final-test boundary.
4. Lock claims against actual results and uncertainty over independent units. Select
   a manuscript, scoped negative report, renewed intake or stop outcome.
5. For a full research-to-paper request, continue through working sections,
   source-derived figures, legends, declarations and the real rendered candidate.
6. When requested, curate and rehearse public code locally. Publication or submission
   remains a separate authorized action.

The public entrypoint routes ten working modes: `survey`, `plan`, `pilot`, `develop`,
`monitor`, `freeze`, `claim-lock`, `handoff`, `manuscript`, and `public-release`. These modes separate
field reconnaissance, scientific planning, execution evidence, final-test discipline,
claim formation, manuscript transfer, and clean code release.

Working modes are not validator targets. In particular, a `handoff` validator pass does
not inspect a finished manuscript. Use the bundled manuscript route for that work and
the [public-release guide](../skills/research-publication-pipeline/references/public-code-release.md)
for clean packaging and actual command rehearsal.

## Independent manuscript and figure completion

For permitted schematic work, inspect relevant high-quality examples first. Borrow
composition lessons such as reading order, grouping, hierarchy and label density;
do not transfer their scientific claims, data or proprietary artwork.

For figure production included in an authorized manuscript handoff or working-draft
scope, or requested directly, use the bundled [figure route](../skills/research-publication-pipeline/references/standalone-figures.md)
for default destination-style GPT Image 2.5 concepts followed by native editable PPTX
using available tools directly. It bundles source-plotting and vector-fallback helpers.
Optional `build-scientific-visualizations` adds specialist compound layouts, without
gating concept or PPTX production. The [manuscript route](../skills/research-publication-pipeline/references/standalone-manuscript.md)
covers complete sections, figures, legends, declarations, rendering and local packaging
without a writing skill dependency. Locked content and destination policy still apply.
A pilot or status check does not trigger drawing. See
[evidence, claims, and handoff](../skills/research-publication-pipeline/references/evidence-claims-and-handoff.md).

## Synthetic demonstration

The installed skill includes a complete, local synthetic demonstration. From its directory,
run `python3 examples/run_demo.py OUTPUT_DIRECTORY`; the output must be a new directory
outside the skill. It prints the observed passing `pilot`, `development`, and `handoff`
validator statuses. See [examples/README.md](../skills/research-publication-pipeline/examples/README.md)
for invocation and the strict human-evidence boundary. Generated workspaces are runtime
outputs, not package or release contents.

For an actual local packaging rehearsal, add `--with-public-release`. It creates a
small synthetic code tree, packages and unpacks it in a fresh temporary directory,
runs its arithmetic example and two tests, checks the output, and reports the observed
`public-release` validator status. No dependencies are installed and nothing is
published. Command records and generated results stay outside the curated tree.

## Test

From the repository root:

```bash
python3 -m pip install -r requirements-test.txt
python3 -B -m unittest discover \
  -s tests/research-publication-workflow -p 'test_*.py'
python3 scripts/check_public_content.py .
find . -type l -print
```

The repository suite includes PDF and figure checks; install its documented environment only
when needed. The quick demonstration above remains standard-library-only.

An empty result from `find` is expected. The skill can also be checked with the
`quick_validate.py` utility supplied by Codex's `skill-creator` package.

## Boundaries and limitations

The validator checks whether the local records satisfy a transparent contract. It does not prove
scientific truth, novelty, causal mechanism, SOTA, repository safety, venue acceptance, or
publication readiness beyond the declared fields. Remote compute, locked-test access, mutation of
a canonical manuscript, repository publication, uploads, and submission remain separate actions
requiring explicit authorization.

JSON and text reports declare `validation_scope: records_and_local_artifact_checks`.
The public-release target also inspects local files for named content risks; findings identify
the file and risk class without echoing matched text. These bounded checks do not establish
independent reproduction, universal privacy protection, or policy truth. Inspect the actual
release and observed rehearsal results before authorizing publication.

## Questions

**Is this an automatic experiment runner?** No. It provides instructions and local tools,
not a remote launcher or credentials. Experiments need real data, execution tools and
the appropriate authority.

**Can it complete a paper without another writing skill?** Yes, within an authorized
full task and sufficient evidence. The standalone route covers writing, figures and
local delivery. Missing evidence, official instructions or rendering tools must be
reported, not replaced by invented results or false completion claims.

**Why did a second demo run refuse its path?** The destination must be new and outside
the installed skill. Run the temporary-directory command again rather than overwriting prior work.

**What if the hypothesis fails?** Preserve the tested conditions and negative result.
Narrow or refute the claim, return to intake, or stop under the registered criteria;
do not silently promote another metric or contribution type.

**What if the image tool has no model selector?** Use the available tool and report the
backend identity as unknown unless verified. A genuinely unavailable or prohibited step
stays unrun while safe local work continues. A local SVG is not evidence of native PPTX
delivery, and another skill is not required to follow the permitted default route.

Original instructions, tests, templates, and scripts in this package are covered by the
repository's Apache-2.0 licence.

## Repository maintenance

Open Research Skills contains five complete entrypoints in one repository. This skill
can still be installed on its own; the other four are optional enhancements. Runtime
dependencies and actual source material remain necessary for the selected task.

See [maintainers](../MAINTAINERS.md), [contributing](../CONTRIBUTING.md), and [third-party terms](../THIRD_PARTY.md). Hosted Linux CI is not configured.

## Related work in this repository

Detailed [conference](conference-manuscripts.md), [journal](journal-manuscripts.md) and
[visualization](scientific-visualizations.md) guides are available in this same repository.
They enhance specialization without becoming prerequisites for the complete workflow.
