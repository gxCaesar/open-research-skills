# Research Funding Proposals

This package contains one ready skill, `writing-funding-proposals`. It provides a portable S0--S12
workflow for current-source intake, evidence and applicant-role records, topic comparison,
scientific argument mapping, human-facing section briefs, conditional financial budgets,
artifact-specific commitments, three-pass review, and local final-record completeness checks. It
distinguishes deliverable mainline work, cautious exploration, and boundary confirmation so that
uncertainty is not disguised as a guaranteed result.

It deliberately excludes personal applicant records, proposal history, private writing profiles,
official form copies, hidden workflow state, and third-party examples. Public tests use a synthetic
funder and applicant.

## Policy boundary

The checked 2026 NSFC notice prohibits directly AI-generated applications and unverified generated
content. The bundled NSFC 2026 profile therefore permits evidence organization, source checking,
argument maps, section briefs, and audit of applicant-authored text, but not insertion-ready
application prose. Other programs also default to evidence-and-audit-only until current official
and institutional policy is verified.

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

## Figure handoff

With current funder and institutional permission for the requested AI-assisted visual,
new or redesigned technical-route, architecture, motivation, and mechanism schematics
use the separately installed `build-scientific-visualizations` skill: style-matched
GPT Image 2.5 concept → native editable PPTX → official-template exports and rendered QA.
Proposal width comes from the actual form. Unverified visual policy permits local briefs
and review, not insertion-ready generated figures; private material stays out of external
image services. Result plots remain data-derived. See
[figures, review, and delivery](skills/writing-funding-proposals/references/figures-review-and-delivery.md).

## Install

From the repository root, copy the exact skill directory into a skills directory selected by your
agent runtime:

```bash
cp -R packages/research-funding-proposals/skills/writing-funding-proposals \
  /path/to/skills/writing-funding-proposals
```

The scripts require only Python 3.9 or later. Installation is a copy operation; this repository
does not modify an agent account automatically.

## Synthetic demonstration

The installed skill includes an independently runnable, archived synthetic final-record-completeness
demonstration. See
[`examples/README.md`](skills/writing-funding-proposals/examples/README.md) for its input,
output, fixed historical snapshot, manual-evidence boundary, and publication restriction.

## Invoke

```text
Use $writing-funding-proposals to verify the current NSFC policy, build a source and claim ledger,
compare the candidate topics, and audit my applicant-authored rationale.
```

## Initialize and validate

All runtime commands below use the exact installed skill directory as the current working
directory. Replace the placeholder path with the copied directory:

```bash
cd /path/to/skills/writing-funding-proposals

python3 scripts/init_proposal_workspace.py proposal-workspace \
  --project-id example --program nsfc --year 2026 --project-type general

python3 scripts/validate_proposal_workspace.py proposal-workspace --mode working
python3 scripts/audit_chinese_prose.py proposal-workspace/sections/rationale.md

# Normal final-record completeness check uses today's --as-of value.
python3 scripts/validate_proposal_workspace.py proposal-workspace --mode final

# Archived synthetic example only; it is not real proposal evidence.
python3 examples/run_demo.py /tmp/funding-synthetic-demo
```

Final mode additionally requires current authority, a completed funder-plus-institution authoring
policy refresh, the actual official system template, applicant confirmation, a frozen route,
complete argument links, audited commitments, the conditional budget record when the current
program/project profile requires it, all three review passes, a local build, and visual review.
The JSON and text reports always show `as_of`; JSON declares
`validation_scope: record_completeness` and text prints the same scope as a note. Use
`--as-of YYYY-MM-DD` only when revalidating an archived historical snapshot; that override
cannot support a current-policy claim.

## Test

From this package directory (not the installed skill directory):

```bash
cd packages/research-funding-proposals
python3 -B -m unittest discover -s tests -p 'test_*.py'
find . -type l -print
```

An empty result from `find` is expected. Original instructions, templates, scripts, and tests in
this package are covered by the repository's Apache-2.0 licence.
