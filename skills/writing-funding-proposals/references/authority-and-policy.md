# Authority and authoring policy

## Source order

For format and compliance, use the current target-year announcement, program guide,
management rules, system template, institutional instructions, and live form fields. User
requirements and historical examples come after those sources.

For scientific and applicant claims, use inspected primary results, data and code,
applicant contribution records, papers and supplements, then bounded secondary evidence.
A search snippet, folder name, inherited statement, or unopened document cannot support a
load-bearing claim.

## Verification vocabulary

| State | Meaning |
|---|---|
| `VERIFIED` | An opened source supports the current wording and scope. |
| `UNVERIFIED` | Direct evidence has not yet been checked. |
| `NOT_FOUND` | A dated, bounded search did not find the required evidence. |
| `COULD_NOT_OPEN` | A candidate source was found but could not be inspected. |
| `INFERRED` | A conclusion follows from named verified facts but is not directly stated. |
| `NOT_RUN` / `FAILED` | A relevant check was not run / ran and failed. |
| `DECISION_REQUIRED` | Two supported options materially change the scientific claim or route. |

Do not use `VERIFIED` for a remembered fact or plausible inference. Keep an unavailable
source unavailable rather than completing a row with invented detail.

## Authoring-policy modes

Record the current funder and institutional rule before writing:

| Mode | Permitted work |
|---|---|
| `EVIDENCE_AND_AUDIT_ONLY` | Source organization, literature verification, claim ledger, topic comparison, scientific graph, section briefs, questions, diagnostics, and audit of applicant-authored text. |
| `ASSISTED_DRAFTING_ALLOWED` | The above plus bounded drafting assistance explicitly permitted by the checked current rule and applicant instruction. |

`UNVERIFIED` policy defaults to `EVIDENCE_AND_AUDIT_ONLY`. A later permissive rule must
be recorded with issuer, date, source, clause locator, scope, and any declaration duties.
No label or local preference overrides a funder's prohibition.

## Local final-mode authoring-policy record

The workspace records a local evidence contract; it does not infer an official rule. In
final mode, `project.json` must record an authoring-policy `status` of `VERIFIED`,
non-empty source IDs that resolve to `VERIFIED` source-register rows, a parseable ISO
`checked_on` date, `scope: authoring_policy`, and `coverage` containing both `funder`
and `institution`. Set `live_refresh_completed: true` only after those current sources
have been opened and checked for the requested assistance.

Do not let an aggregate coverage list stand in for source evidence. For every policy
source, add one `source_bindings` record containing its `source_id`, one controlled
`authority_kind` (`funder` or `institution`), the selected project `program` and `year`,
`scope`, `checked_on`, and `live_refresh_id`. The referenced source-register row must be
`VERIFIED` and agree on program, year, scope, and `accessed_on`; policy source IDs must
exactly equal the bound source IDs. The aggregate coverage is recomputed from these
kinds. Final mode therefore needs distinct source IDs for funder and institution rather
than accepting two self-reported roles for one source. It also treats
`(issuer, url_or_path, clause_locator)` as the underlying evidence identity: funder and
institution bindings may not reuse the same identity under different source IDs. One
joint document is allowed only when its two bindings point to distinct clause locators.

Record a non-empty `live_refresh_id` and parseable `live_refresh_completed_on`; both the
policy `checked_on` date and every binding must match that refresh. In final mode,
`validate_proposal_workspace.py` defaults `--as-of` to the local current date and
requires policy, refresh, binding, and source-access dates to equal it. For a historical
snapshot, pass its explicit `--as-of YYYY-MM-DD`; the report records that override. This
is an auditable local completion record, not a claim that the validator fetched a live
website or can infer an official expiry period. An archived override must not be described
as current policy evidence.

A bundled profile may be marked `VERIFIED_PROFILE` because it is a dated routing aid. It
can support working-mode evidence organization, but it cannot satisfy final mode by
itself. Do not substitute a copied profile, remembered policy, or a synthetic source for
the current funder and institutional check.

## Final authority and template source contexts

Final mode uses controlled source-register contexts so an unrelated `VERIFIED` row cannot
stand in for the current project record. Each source must match the selected project
`program` and `target_year`, and its `accessed_on` must equal final validation's `as_of`.
Use these local record labels:

| Project record | Required source `scope` | Required source `source_type` | Additional final binding |
|---|---|---|---|
| `official_authority` | `official_authority` | `official authority` | `last_checked` equals `as_of` |
| `official_template` | `official_template` | `official template` | Local `url_or_path` equals `artifact_path`; remote HTTP(S) paths remain source URLs |
| `financial-budget.json` `requirement` | `financial_budget_requirement` | `financial budget requirement` | `requirement.checked_on` equals `as_of` |

The local template artifact must still exist. Do not relabel an authoring-policy source as
one of these roles; register the actual applicable authority, template, or budget-rule
source. These labels are a validator contract, not claims about an official document's
title or live availability.

## Conditional financial budget

The current program and project-type profile must explicitly state whether a financial
budget is required. Record that decision in `budget/financial-budget.json` with its
current `financial_budget_requirement` source IDs, checked date, and scope. In final mode
the requirement source must use the matching controlled source type and current project
context above. If it is required, also record the budget method and source IDs, total,
annual allocations, program-appropriate category allocations, and task/resource linkages.
Categories are not standardized by this skill: use only those established by the
applicable current program or institution.

## Official template

A web guide, historic Word or PDF file, LaTeX facsimile, or funded example does not prove
the current system template. Final-format status requires the actual target-year artifact
and applicable institutional overlay, registered under the controlled template context
above. Never redistribute that artifact unless its terms permit it; this public skill
deliberately does not bundle one.

## Confidentiality and applicant truth

Classify sources as `PUBLIC`, `APPLICANT_PRIVATE`, or `RESTRICTED_CONFIDENTIAL`. Process
private in-scope material locally, but do not move it into a public skill, fixture, or
external service. Do not infer grant numbers, identity fields, contribution, facility
access, ethics clearance, or data rights. The applicant confirms them against direct
records.
