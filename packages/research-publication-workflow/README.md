# Research Publication Workflow

This package contains `research-publication-pipeline`, a portable evidence-gated workflow for
research intake, contribution routing, headroom measurement, frozen protocols, controlled
iteration, claim locking, source-grounded paper reading, and manuscript or public-release
handoff. Paper reading is an internal component rather than an additional public entrypoint.

The reusable scientific decision system and validators are public. Private infrastructure,
remote launch adapters, historical run state, actual authorization records, and project-specific
evidence are excluded. The package is self-contained and uses no absolute local dependency or
external symlink.

## Install

Copy the independently installable skill into the skills directory selected by your agent runtime:

```bash
cp -R packages/research-publication-workflow/skills/research-publication-pipeline \
  /path/to/skills/research-publication-pipeline
```

Python 3.9 or later is required. The initializer and project validator use only the Python
standard library. The internal paper-card component needs pypdf for PDF input and Poppler's
`pdftoppm` only when rendered pages are requested. From the copied skill directory, install the
tested Python dependency with `python3 -m pip install -r requirements.txt`. Installation is a copy
operation; this repository does not alter an agent account.

## Invoke

```text
Use $research-publication-pipeline to assess this AI-for-biology topic. Keep data feasibility,
lane-specific scoop, and venue fit separate, measure cheap-baseline headroom before proposing a
model, and identify the next evidence-backed gate.
```

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

The public entrypoint routes nine working modes: `survey`, `plan`, `pilot`, `develop`,
`monitor`, `freeze`, `claim-lock`, `handoff`, and `public-release`. These modes separate
field reconnaissance, scientific planning, execution evidence, final-test discipline,
claim formation, manuscript transfer, and clean code release.

## Figure handoff

For figure production included in an authorized manuscript handoff or working-draft
scope, or requested directly, new or redesigned flowchart, architecture, motivation,
method, and mechanism schematics use the separately installed
`build-scientific-visualizations` skill: destination-style GPT Image 2.5 concept →
native editable PPTX → required manuscript exports and rendered QA. The pipeline passes
locked scientific content and preserves destination policy; quantitative panels remain
data-derived. A pilot or status check does not trigger drawing. See
[evidence, claims, and handoff](skills/research-publication-pipeline/references/evidence-claims-and-handoff.md).

## Synthetic demonstration

The installed skill includes a complete, local synthetic demonstration. From its directory,
run `python3 examples/run_demo.py OUTPUT_DIRECTORY`; the output must be a new directory
outside the skill. It prints the observed passing `pilot`, `development`, and `handoff`
validator statuses. See [examples/README.md](skills/research-publication-pipeline/examples/README.md)
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
python3 -B -m unittest discover \
  -s packages/research-publication-workflow/tests -p 'test_*.py'
python3 scripts/check_public_content.py .
find packages/research-publication-workflow -type l -print
```

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

Original instructions, tests, templates, and scripts in this package are covered by the
repository's Apache-2.0 licence.
