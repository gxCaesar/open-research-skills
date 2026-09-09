# Open Research Skills

Five public agent skills cover the research-to-publication workflow without exposing a
large set of overlapping triggers.

| Package | Sole public skill | Main capabilities |
|---|---|---|
| [scientific-visualizations](packages/scientific-visualizations/README.md) | `build-scientific-visualizations` | Page-first layouts, semantic flowcharts, compound figures, source data, and conference or journal figure sets |
| [conference-manuscripts](packages/conference-manuscripts/README.md) | `prepare-conference-manuscripts` | Venue recon, drafting, audit, polish, rebuttal, camera-ready work, and packaging |
| [journal-manuscripts](packages/journal-manuscripts/README.md) | `prepare-journal-manuscripts` | Drafting, audit, editor packs, cover letters, revision responses, data availability, and final packages |
| [research-funding-proposals](packages/research-funding-proposals/README.md) | `writing-funding-proposals` | Chinese funding authority, evidence, topic selection, scientific argument, figures, review, and delivery |
| [research-publication-workflow](packages/research-publication-workflow/README.md) | `research-publication-pipeline` | Survey, planning, pilot, headroom, controlled development, frozen evaluation, claim lock, handoff, and public code release |

Each package has one `SKILL.md`. Focused capabilities live below that exact skill directory in
`components/`, `shared/`, or `references/` and do not create additional trigger surfaces. Copy the
selected directory under `packages/<package>/skills/<skill>/`; it is the independent installation
unit and does not depend on the rest of this checkout.

The repository excludes private reviews, applicant records, personal writing profiles,
credentials, machine-specific state, authorization records, submission automation, and
third-party material without confirmed redistribution rights. Dated venue or policy
profiles are starting points; current first-party instructions remain authoritative.

## Start with one skill

Choose the package above that owns your requested deliverable. Copy its complete
`packages/<package>/skills/<skill>/` directory to your agent runtime's skills location
and follow that package's dependency and invocation instructions. Do not copy only
`SKILL.md`, nest it inside a second directory of the same name, or overwrite an existing
installation without reviewing your local changes. No global installer is required.

For a local software demonstration, use the
[funding example](packages/research-funding-proposals/skills/writing-funding-proposals/examples/README.md)
or [publication-workflow example](packages/research-publication-workflow/skills/research-publication-pipeline/examples/README.md).
Both use synthetic records; a passing validator is not evidence that a real scientific
result, grant application or manuscript is correct. The
[editable visual library](packages/scientific-visualizations/skills/build-scientific-visualizations/references/design-template-library.md)
provides original diagram examples and previews for adaptation.

## Test

From the repository root:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B -m unittest discover -s packages/conference-manuscripts/tests -p 'test_*.py'
python3 -B -m unittest discover -s packages/journal-manuscripts/tests -p 'test_*.py'
python3 -B -m unittest discover -s packages/research-funding-proposals/tests -p 'test_*.py'
python3 -B -m unittest discover -s packages/research-publication-workflow/tests -p 'test_*.py'
python3 -B -m unittest discover -s packages/scientific-visualizations/tests -p 'test_*.py'
python3 scripts/check_public_content.py .
find packages -type l -print
```

An empty `find` result is expected. Package READMEs list runtime dependencies and
focused validation commands. `requirements-test.txt` pins the development test dependencies.
The optional Ubuntu/Python 3.9 and 3.12 workflow is manual-only; pushes and pull requests
do not start it. Local checks remain available without hosted CI.

## Maintenance

See [maintainers](MAINTAINERS.md) and [contributing](CONTRIBUTING.md). Report a problem
with the skill name, a minimal non-sensitive example, expected behavior and observed
behavior. Do not attach private manuscripts, applicant records or credentials to an issue.

## Status and licence

Repository hosting state and release tags are the authority for whether a version is public; this
README does not claim that a remote, tag, or release exists. Original repository code and
instructions are licensed under Apache-2.0. See `THIRD_PARTY.md` for the redistribution boundary.
