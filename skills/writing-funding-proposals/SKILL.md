---
name: writing-funding-proposals
description: Use when establishing current policy or authority, organizing evidence, mapping arguments, planning proposal-specific technical routes and figures, preparing section briefs, reviewing, or validating Chinese research-funding proposals, including NSFC information science and Guangdong natural science funds. Includes permitted local figure construction without another skill. Check current funder and institutional authoring policy before producing prose; when direct generation is prohibited or unverified, limit work to source verification, evidence maps, section briefs, structural critique, and audit.
---

# Research Funding Proposals

Build a current, evidence-linked scientific argument around applicant-authored material.
Historical applications and templates may inform non-expressive structure, but they are
never current format authority and must not be copied into a public or applicant package.

## Start with policy and authority

Before substantive work, identify the target year, funder, program, project type,
institutional instructions, current official sources, actual system template,
confidentiality class, and requested scope. Read `references/authority-and-policy.md`
and the matching profile.

The authoring-policy mode controls what this skill may produce:

- `EVIDENCE_AND_AUDIT_ONLY`: organize sources and claims, compare topics, build an
  argument map, prepare section briefs, audit applicant-authored text, and return exact
  revision tasks. Do not produce insertion-ready application prose.
- `ASSISTED_DRAFTING_ALLOWED`: use only after a directly checked current funder and
  institutional source permits the requested assistance. Preserve the applicant's
  authorship, factual responsibility, required declarations, and review.
- `UNVERIFIED`: apply `EVIDENCE_AND_AUDIT_ONLY` until resolved.

The checked 2026 NSFC profile is `EVIDENCE_AND_AUDIT_ONLY`: the official notice says
applications must not be directly generated with generative AI and generated research or
reference information must be verified. Do not bypass that rule by calling generated
prose a template, rewrite, translation, or polished final draft.

A bundled `VERIFIED_PROFILE` supports working-mode routing only. Final mode requires a
new `VERIFIED` authoring-policy record with non-empty registered source IDs, a parseable
checked date, `authoring_policy` scope, coverage for both `funder` and `institution`, and
an explicit completed live refresh. Bind each policy source to one controlled
`authority_kind` (`funder` or `institution`), project program and year, scope, checked
date, and live-refresh ID; the binding must agree with the registered source row. Final
validation rejects funder/institution bindings that reuse the same `(issuer, url_or_path,
clause_locator)` identity; a joint document needs distinct clause locators. It defaults
`--as-of` to today and requires every refresh date to equal it. Final authority, template,
and financial-budget requirement sources must separately match the selected program/year,
their controlled source-register scope/type, and `as_of`; a local template source path
must equal the registered artifact path. Use an explicit historical `--as-of` only to
revalidate an archived snapshot, never to claim that old evidence is current. Read
`references/authority-and-policy.md` before recording this contract; it records local
evidence, not an inferred official permission.

## Create or resume a workspace

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every bundled script,
reference, profile, and template is below that directory; never resolve through the
package parent or assume the user's current working directory.

For a new project:

```bash
python3 "$SKILL_DIR/scripts/init_proposal_workspace.py" <project> \
  --project-id <id> --program <nsfc|guangdong|other> \
  --year <year> --project-type <type>
```

The initializer creates human-facing records for authority, evidence, topic selection,
the scientific argument, section briefs, figures, conditional financial budget,
commitments, reviews, and final-format evidence. It does not bundle an official form and
refuses to overwrite a non-empty directory.

For an independently runnable archived fixture, see
[`examples/README.md`](examples/README.md). It creates a synthetic workspace outside the
installed skill, uses a fixed historical snapshot, and demonstrates only the local
record-completeness check;
it is never real policy, applicant, scientific, eligibility, or funding evidence.

On resume, read `project.json`, actual artifacts, the newest source entries and review
findings, then run:

```bash
python3 "$SKILL_DIR/scripts/validate_proposal_workspace.py" <project> --mode working
```

Use observed files and validator output over stale status prose. Do not mark a stage
complete because a neighboring artifact exists.

## Full-project workflow

Read `references/full-project-workflow.md`. The stages are scientific dependencies, not a
quota of forms:

| Stage | Decision or artifact |
|---|---|
| S0 | Current authority, funder-plus-institution authoring policy, material classification, and official-source register |
| S1 | Claim ledger and applicant-role evidence |
| S2 | Candidate portfolio with data and program feasibility |
| S3 | Dated novelty search, scoop verdict, and strongest falsifier |
| S4 | One frozen contribution lane and route or code fit |
| S5 | Q/C/V/O/CL/F scientific argument graph |
| S6 | Section briefs, artifact-specific commitments, conditional financial budget, paragraph jobs, page budget, risks, and annual outputs |
| S7 | Applicant-authored root sections and evidence-preserving review |
| S8 | Minimal sufficient editable figure and table portfolio |
| S9 | Integration into the current official template without changing scientific scope |
| S10 | Fatal, science, and readability review passes |
| S11 | Actual build, PDF inspection, and final-size visual review |
| S12 | Local candidate record-completeness check and explicit external-submission boundary |

Continue through every safe dependent stage. Pause only for a genuine claim or route fork,
missing load-bearing evidence, prohibited authoring action, confidential-data transfer,
destructive change, or external submission.

## Reference router

| Task | Read |
|---|---|
| intake, annual refresh, policy, or format | `references/authority-and-policy.md` and the matching profile |
| evidence, topic, novelty, route, or application code | `references/evidence-topic-and-route.md` |
| argument map, outline, section brief, or prose review | `references/argument-and-sections.md` and `references/plain-chinese-prose.md` |
| work-package commitment, annual output, risk, or fallback | `references/commitment-calibration.md` |
| technical-route figure, table, reviewer audit, PDF, or handoff | `references/figures-review-and-delivery.md` |

For an AI-for-biology or computational-biology proposal, do not select an information-
science code merely because AI or omics appears in the title. Compare the central new
knowledge, natural reviewer community, claimed output, validation endpoint, and strongest
mismatch for plausible alternative codes using current official labels.

## Calibrate scientific commitments

Read `references/commitment-calibration.md` before turning the scientific graph into
research contents, annual tasks, outputs, or risk statements. Classify each work package
as exactly one of:

- `deliverable mainline`: a dependency-backed result the proposal commits to deliver
  and can assess with named acceptance evidence;
- `cautious exploration`: a potentially valuable hypothesis with a cheap falsifier,
  finite decision point, and useful negative outcome, not a guaranteed primary result;
- `boundary confirmation`: an early scope or feasibility check with an explicit go or
  no-go rule before downstream work depends on it.

Do not promote every idea to deliverable mainline merely to sound ambitious. Do not hide
a required feasibility gate as cautious exploration, and do not present boundary
confirmation as the final scientific contribution. Keep the class consistent across the
argument map, section briefs, timeline, annual outputs, risks, and figures.

## Scientific integrity rules

- Register every opened authority or scientific source with its scope and verification
  state. A search result, filename, remembered citation, or unopened PDF is not evidence.
- Give every load-bearing scientific, feasibility, applicant-foundation, and compliance
  claim a stable `CL*` record. Preserve numerical values, uncertainty, population scope,
  citation scope, and applicant role.
- Never infer a grant number, applicant contribution, data licence, access right,
  preliminary result, eligibility fact, or ethics status from a neighboring proposal,
  author position, publication count, or generic platform description.
- Compare topic candidates before prose expansion. Record `data_feasibility`, linkable
  variables, independent unit, strongest cheap baseline, discriminating validation,
  failure criterion, `IDENTICAL`/`ADJACENT`/`UNCERTAIN`, and `FRAMING`/`DATA`/`TASK`.
- Let the smallest dependency-complete Q/C/V/O/CL/F graph determine research-content and
  figure count. A funder heading does not require three symmetric aims.
- Separate completed work, transferable capability, planned work, and unavailable
  evidence. A polished sentence cannot repair an evidential gap.
- Keep restricted material local and out of fixtures, shared skills, examples, and public
  packages.

## Figures and prose

This skill independently completes the proposal workflow within the verified
authoring-policy mode; a prohibition on generated prose is not a missing skill.
It first locks policy, evidence and the scientific argument. When current funder and
institutional rules permit the requested AI-assisted figure, use the bundled
[standalone figures](references/standalone-figures.md) route: default to style-matched
GPT Image 2.5 concepts followed by native editable PPTX using available tools directly,
then proposal exports and visual QA. `build-scientific-visualizations`, when installed,
adds optional design helpers; its absence does not stop that permitted default. Read
[figures, review, and delivery](references/figures-review-and-delivery.md) before production
for policy, confidentiality, source-data, and capability boundaries. Its source ledger,
semantic arrows, editability, and rendered QA apply; journal column widths do not.
Derive the proposal width from the actual official template. A schematic is not proof
of feasibility, and a decorative icon is not scientific evidence.

Run the prose audit on applicant-authored text:

```bash
python3 "$SKILL_DIR/scripts/audit_chinese_prose.py" <files>
```

The audit flags reviewable surface cues. It does not establish scientific accuracy,
policy compliance, quality, or authorship. Inspect every finding in context and retain
necessary official names, direct quotations, qualifiers, and citations.

## Final-record completeness and external boundary

An official guide that mentions a form does not verify the actual form. Final mode
requires the target-year system template, a completed funder-plus-institution authoring
policy refresh, opened official sources, applicant review, frozen route, complete
scientific graph, required conditional budget evidence, auditable commitments, three
review passes, a successful local build, and visual inspection of the rendered artifact:

```bash
python3 "$SKILL_DIR/scripts/validate_proposal_workspace.py" <project> --mode final
```

The report declares `validation_scope: record_completeness`. It checks recorded statuses and
local paths, not file format, rendering, or visual quality; the applicant still performs and
records the real build and page-by-page inspection. It cannot determine eligibility,
scientific truth, authorship, policy compliance, funding, or submission. Uploading, saving in
a portal, or submitting is an external action that requires the applicant's explicit
authorization and direct platform evidence.
