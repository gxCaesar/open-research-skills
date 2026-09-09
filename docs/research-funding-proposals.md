# Research Funding Proposals

[All five skills and repository setup](../README.md)

An independently installable agent skill for turning a Chinese research-funding idea into
an evidence-linked proposal workflow. It helps organize sources, compare topics, build
arguments, prepare section briefs, audit applicant-authored text, produce permitted
figures and inspect local delivery records. It is not an automatic grant writer or a
prediction of funding success.

**Start here:** [five-minute demo](#five-minute-demo) ·
[read the sample](../skills/writing-funding-proposals/examples/section-brief-walkthrough.md) ·
[skill instructions](../skills/writing-funding-proposals/SKILL.md) ·
[full workflow](../skills/writing-funding-proposals/references/full-project-workflow.md)

`writing-funding-proposals` is one of five skills in Open Research Skills. It remains
independently usable; no second research skill is required. Python scripts provide local tools; your agent runtime reads
the skill and carries out the evidence and writing work within the requested scope.

It deliberately excludes personal applicant records, proposal history, private writing profiles,
official form copies, hidden workflow state, and third-party examples. Public tests use a synthetic
funder and applicant.

## What you can do

| Your situation | What you provide | Useful output |
|---|---|---|
| Starting an NSFC, Guangdong or other Chinese proposal | Program/year/type, official sources and institutional instructions | Source register, current-policy questions and permitted assistance scope |
| Choosing between ideas | Candidate questions, data-access evidence and applicant experience | Topic comparison, nearest-work delta and cheapest feasibility check |
| Turning an idea into research contents | Verified premises and one selected route | Question–content–validation–output map and section briefs |
| Avoiding unrealistic promises | Work packages, dependencies and resources | Bounded commitments, annual outputs, risks and a conditional financial budget |
| Reviewing a draft | Applicant-authored text, sources and actual form | Located fatal, scientific and readability findings with revision tasks |
| Preparing local delivery | Reviewed text, permitted figures and current official template | Integrated candidate, real build/visual review work and local record check |

The argument follows the evidence, not a fixed three-aim template. Commitments distinguish
deliverable mainline work, cautious exploration and early boundary confirmation.

## Five-minute demo

Clone `gxCaesar/open-research-skills` once using the [repository setup](../README.md).
Python 3.9+ and its standard library are sufficient. This demo needs no
network, API key, agent account or third-party Python packages. Run from the repository
root and use a new output directory:

```bash
demo_root=$(mktemp -d)
python3 -B skills/writing-funding-proposals/examples/run_demo.py "$demo_root/funding-demo"
```

Expected status lines:

```text
Observed validator status: PASS
Observed validator scope: record_completeness (record-only)
```

The command also prints the output location and synthetic-use warning. The workspace
stays outside the checkout; only the curated teaching sample belongs in the public repo.
These commands use macOS/Linux-style shell syntax; on another shell supply an equivalent
new temporary output path. The [demo guide](../skills/writing-funding-proposals/examples/README.md)
explains the generated files and their limits. The fixture uses a fixed `2024-02-29`
snapshot with a 2026 program label for software testing, not real historical policy
evidence. Files named `.pdf` are test placeholders, **not rendered PDFs**.

Read the [annotated section brief](../skills/writing-funding-proposals/examples/section-brief-walkthrough.md)
without running anything. Its human-facing preview:

| Argument element | Synthetic example |
|---|---|
| Question | Does mechanism M distinguish outcome Y? |
| Comparison | M versus a simple baseline on held-out synthetic subjects |
| Intended output | A paired estimate with uncertainty, not a guaranteed positive result |
| Failure response | Reframe the mechanism claim when the comparison fails |

No real proposal, applicant review, policy check or scientific experiment occurred. Do
not publish the generated workspace, submit it, or present it as research evidence.

## Policy boundary

The bundled [NSFC 2026 profile](../skills/writing-funding-proposals/references/profiles/nsfc-2026.md)
records a prohibition on directly AI-generated applications and unverified generated content.
It therefore permits evidence organization, source checking,
argument maps, section briefs, and audit of applicant-authored text, but not insertion-ready
application prose. Other programs also default to evidence-and-audit-only until current official
and institutional policy is verified. The bundled profile is a routing reference, not a
live confirmation of the current rules for your application.

Final mode requires a live authoring-policy refresh covering both the funder and institution. Each
registered policy source has one controlled authority kind, plus project program/year/scope,
checked date, and refresh ID; the two authority kinds require different source IDs. Aggregate
coverage cannot substitute for source-level authority, and duplicate `(issuer, url_or_path,
clause_locator)` evidence cannot cover both roles. Final official-authority, official-template,
and financial-budget requirement records also bind dedicated `VERIFIED` sources to the selected
program/year, role-specific source-register scope/type, and the final `as_of` date. A local
template source path must match its registered artifact path. A bundled `VERIFIED_PROFILE`
supports working mode only. The public tools validate a local record contract. They cannot
establish eligibility, scientific truth, authorship, policy compliance, submission, review
success, or funding.

Every validator report sets `validation_scope: record_completeness`. A final pass checks
recorded statuses and local file paths; it does not parse the final file, run a renderer, or
judge rendered visual quality. The applicant still performs and records the real build and
page-by-page review.

## Independent completion and figures

For permitted schematic work, inspect relevant high-quality examples first. Borrow
composition lessons such as reading order, grouping, hierarchy and label density;
do not transfer their scientific claims, data or proprietary artwork.

With current funder and institutional permission for the requested AI-assisted visual,
new or redesigned schematics use the bundled [local figure route](../skills/writing-funding-proposals/references/standalone-figures.md):
style-matched GPT Image 2.5 concepts followed by native editable PPTX using available
tools directly, then official-template exports and rendered QA. A source-plotting and
native-vector fallback helper is bundled. Optional `build-scientific-visualizations`
adds design helpers. The policy-permitted S0–S12 workflow requires no second skill.
Proposal width comes from the actual form. Unverified visual policy permits local briefs
and review, not insertion-ready generated figures; private material stays out of external
image services. Result plots remain data-derived. See
[figures, review, and delivery](../skills/writing-funding-proposals/references/figures-review-and-delivery.md).

## Install

From the repository root, copy the exact skill directory into a skills directory selected by your
agent runtime:

```bash
cp -R skills/writing-funding-proposals \
  /path/to/skills/writing-funding-proposals
```

Replace the destination with your runtime's skills directory. Use a destination that
does not already contain this skill; preserve or deliberately update an existing copy.
Every reference, template, example and script is inside this one install unit. Select
`writing-funding-proposals` in your runtime, or invoke `$writing-funding-proposals`
where named skill invocation is supported.

The record tools require only Python 3.9 or later. The optional local figure helper uses
`matplotlib==3.9.4`, and local PPTX authoring can use `python-pptx==1.0.2`, both declared
in the installed skill's `requirements.txt`. Install dependencies in the intended
environment when needed. Installation is a copy operation; this repository
does not modify an agent account automatically.

For the optional local graphics capabilities, install the declared dependencies in
your intended environment:

```bash
python3 -m pip install -r skills/writing-funding-proposals/requirements.txt
```

Live source checking needs a browser or source-access tool supplied by your runtime.
Image concepts need an available, permitted image service; document/PPTX rendering
needs the corresponding local tool. None is invoked or installed by the record demo.

## Synthetic demonstration

The installed skill includes an independently runnable, archived synthetic final-record-completeness
demonstration. See
[`examples/README.md`](../skills/writing-funding-proposals/examples/README.md) for its input,
output, fixed historical snapshot, manual-evidence boundary, and publication restriction.

## Invoke

```text
Use $writing-funding-proposals to verify the current NSFC policy, build a source and claim ledger,
compare the candidate topics, and audit my applicant-authored rationale.
```

## Initialize and validate

For a real project, provide the target program/year/type, requested scope,
confidentiality, actual official form, source links and applicant-authored material.
Keep personal or restricted evidence in that project, not the public skill checkout.
These commands run from the repository root; after installation, resolve the script
paths inside your copied skill instead:

```bash
python3 skills/writing-funding-proposals/scripts/init_proposal_workspace.py ../proposal-workspace \
  --project-id example --program nsfc --year 2026 --project-type general

python3 skills/writing-funding-proposals/scripts/validate_proposal_workspace.py ../proposal-workspace --mode working
python3 skills/writing-funding-proposals/scripts/audit_chinese_prose.py ../proposal-workspace/sections/rationale.md

# Normal final-record completeness check uses today's --as-of value.
python3 skills/writing-funding-proposals/scripts/validate_proposal_workspace.py ../proposal-workspace --mode final
```

Change program/year/type to the actual target. Initialization creates unresolved records,
not a completed application, and refuses to overwrite a non-empty directory. Work proceeds
through these dependencies rather than running final mode immediately:

1. Establish current authority and allowed assistance; open the actual sources.
2. Assemble applicant-role and claim evidence, compare topics and settle one route.
3. Map questions to methods, comparisons, outputs and figures; prepare section briefs,
   bounded commitments and any required financial budget.
4. The applicant writes prose when policy requires it. Review the text, produce only
   permitted figures and integrate into the official template.
5. Perform fatal, scientific and readability review, build the real candidate, inspect
   every rendered page and then check the final records.

Final mode additionally requires current authority, a completed funder-plus-institution authoring
policy refresh, the actual official system template, applicant confirmation, a frozen route,
complete argument links, audited commitments, the conditional budget record when the current
program/project profile requires it, all three review passes, a local build, and visual review.
The JSON and text reports always show `as_of`; JSON declares
`validation_scope: record_completeness` and text prints the same scope as a note. Use
`--as-of YYYY-MM-DD` only when revalidating an archived historical snapshot; that override
cannot support a current-policy claim.

## Questions and limitations

**Will this write my whole NSFC application?** Not under the bundled evidence-and-audit-only
profile. Completing the workflow respects policy; it does not imply generated prose.

**Does `PASS` mean ready to submit?** No. The validator checks recorded statuses and local
paths, not source truth, authorship, file format, visual quality, eligibility or funding.
Real build and review remain required; portal writes and submission need explicit
applicant authorization.

**Why did a repeat demo refuse its output?** Its destination must be new. Use
the temporary-directory command again; do not overwrite a real project to make it pass.

**Can I use another funder or a future year?** Yes, with `--program other` or the relevant
supported program and your year. Current sources and the actual form are still required;
a bundled profile does not transfer automatically to another call.

**What if an image tool has no model selector?** Follow the bundled figure route: use
the available tool and report its backend as unknown unless verified. Genuinely
unavailable or prohibited steps remain unrun. SVG is not native PPTX, and another skill
is not required to complete permitted local work.

## Test

From the Open Research Skills checkout root (not `docs/` or the installed skill directory):

```bash
# Run from this repository root.
python3 -m pip install -r requirements-test.txt
python3 -B -m unittest discover -s tests/research-funding-proposals -p 'test_*.py'
python3 scripts/check_public_content.py .
find . -type l -print
```

The repository suite includes optional figure tests; install its declared environment only
when needed. The quick record demo above remains standard-library-only.

An empty result from `find` is expected. Original instructions, templates, scripts, and tests in
this package are covered by the repository's Apache-2.0 licence.

## Repository maintenance

Open Research Skills contains five complete entrypoints in one repository. This skill
can still be installed on its own; the other four are optional enhancements. Runtime
dependencies and actual source material remain necessary for the selected task.

See [maintainers](../MAINTAINERS.md), [contributing](../CONTRIBUTING.md), and [third-party terms](../THIRD_PARTY.md). Hosted Linux CI is not configured.

## Related work in this repository

For research planning before the proposal, see [research workflow](research-publication-workflow.md).
For visual-design examples, see [scientific visualizations](scientific-visualizations.md).
These are optional adjacent tasks, not required installations.
