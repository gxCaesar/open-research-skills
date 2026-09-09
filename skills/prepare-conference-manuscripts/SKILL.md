---
name: prepare-conference-manuscripts
description: Use when preparing, drafting, revising, polishing, rebutting, auditing, anonymizing, packaging, or checking a conference manuscript, abstract, appendix, supplement, rebuttal, author response, camera-ready paper, or conference statistical or evaluation report for AAAI, ICLR, ACL, CVPR, ICML, NeurIPS, or another peer-reviewed computing venue. Includes manuscript-context figures and venue-package checks without requiring another skill; disputed experiment evidence must be resolved before changing manuscript prose.
---

# Prepare Conference Manuscripts

Carry one evidence-linked paper through the conference lifecycle. First identify the
venue, track, year, stage, and permitted action. Then lock the scientific contract,
select one mode, apply current official rules, and verify the exact rendered artifact.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `recon` | Resolve current official venue rules, template, stages, policy conflicts, and live-form unknowns | [manuscript lifecycle](references/manuscript-lifecycle.md) |
| `draft` | Turn an author-approved outline and locked scientific contract into manuscript sections when venue policy permits | [manuscript lifecycle](references/manuscript-lifecycle.md), [abstract and statistics](references/abstract-and-statistics.md) |
| `audit` | Falsify the claim-to-evidence map, venue compliance, anonymity, and artifact consistency without editing | [adversarial audit](references/adversarial-audit.md) |
| `polish` | Make local evidence-preserving edits to author text without changing the scientific contract | [manuscript lifecycle](references/manuscript-lifecycle.md) |
| `rebuttal` | Build a complete concern-to-evidence matrix and response or discussion revision | [rebuttal and revision](references/rebuttal-and-revision.md) |
| `camera-ready` | Reconcile accepted claims, required changes, authorship, disclosure, source, and final PDF under current instructions | [manuscript lifecycle](references/manuscript-lifecycle.md) |
| `package` | Audit the exact main PDF, supplement, code/data materials, checklist, and archive intended for submission | [adversarial audit](references/adversarial-audit.md) |

Use one primary mode per pass. Run `recon` whenever the venue, year, track, stage, or
official authority is uncertain. A venue profile is a dated engineering aid, not a
substitute for current first-party instructions.

For a compound whole-paper request that combines polishing and packaging, whether or
not it names audit, follow the [whole-paper workflow](references/full-paper-workflow.md)
and return the ordered [whole-paper deliverables](assets/full-paper-deliverables.md).
It composes existing modes as separate passes, starting with intake and audit before
editing, and defaults to a revision copy after the audit boundary.

## Resolve the package and venue component

The directory containing this `SKILL.md` is the installed skill root; call it
`$SKILL_DIR`. Every bundled component, guide, profile, and command below resolves from
that directory. Do not resolve a tool through a sibling package or a repository parent.

Select a local adapter by exact `venue/year/track` scope. Read its official-source
record before its profile or proceedings observations.

| Local adapter | Dated scope | Guide | Optional paper observations |
|---|---|---|---|
| AAAI | AAAI-27 Main Technical Track | [guide](components/venues/aaai/guide.md) | [observations](components/venues/aaai/references/published-paper-observations.md) |
| ICLR | ICLR 2027 Conference | [guide](components/venues/iclr/guide.md) | [observations](components/venues/iclr/references/published-paper-observations.md) |
| ACL | ACL 2026 Main Conference through ARR | [guide](components/venues/acl/guide.md) | [observations](components/venues/acl/references/published-paper-observations.md) |
| CVPR | CVPR 2026 Main Conference | [guide](components/venues/cvpr/guide.md) | [observations](components/venues/cvpr/references/published-paper-observations.md) |
| ICML | ICML 2026 Main Track | [guide](components/venues/icml/guide.md) | [observations](components/venues/icml/references/published-paper-observations.md) |
| NeurIPS | NeurIPS 2026 Main Track | [guide](components/venues/neurips/guide.md) | [observations](components/venues/neurips/references/published-paper-observations.md) |

If the requested venue/year/track differs from the dated scope, if a profile is stale,
or if its current authority is uncertain, run `recon` before drafting, auditing, or
packaging. Use [generic venue-profile](components/venues/generic/guide.md) only when
no current first-class profile matches; create a dated task-local profile from current
official sources and do not mutate a bundled profile to impersonate another venue.

The linked paper observations are optional empirical drafting evidence. They can inform
writing choices after official authority is resolved, but they never define venue rules,
mandatory section order, or a replacement for current first-party instructions.

Record official sources as `VERIFIED`, `UNVERIFIED`, `COULD_NOT_OPEN`, or `NOT_FOUND`.
Search snippets, prior-year instructions, and remembered limits are not authority.
Preserve conflicts instead of choosing the convenient rule. Do not bundle or modify
venue-owned style files unless redistribution and modification are explicitly allowed.

## Freeze the scientific boundary before writing

Obtain the question, contribution, method or argument, data, split, comparison,
independent unit, metric, uncertainty, results, limitations, and supporting artifacts.
Treat them as the locked scientific contract. Manuscript work may explain or narrow
that contract, but it must not create a result, change a protocol, select a favorable
slice, strengthen a causal claim, or convert `not_run` into completed evidence.

Build a claim map for the title, abstract, contributions, main findings, and conclusion.
Each claim needs its exact table, figure, theorem, analysis, or external artifact. Keep
load-bearing definitions, protocol choices, and decisive evidence in the main paper.
An appendix or supplement is not guaranteed reviewer attention.

For `draft`, work from paragraph jobs: question, evidence, interpretation, and boundary.
For `polish`, use targeted edits and a reverse outline. Preserve every number,
comparison direction, uncertainty statement, citation scope, and qualifier. Follow any
narrower venue rule on AI-assisted writing.

When drafting or repairing a method paper's contribution, Method or Experiments
explanation, read [method argument cases](references/method-argument-cases.md). Use its
inspected paragraph and figure anchors to connect the scientific question, method
operation and comparison; do not impose a universal paper template.

## Handle abstracts, statistics, and responses

Read [abstract and statistics](references/abstract-and-statistics.md) before drafting or
auditing an abstract or statistical statement. Use the local
[abstract component](components/abstract/guide.md) for an abstract checker and the
[statistics-reporting component](components/statistics-reporting/guide.md) for the
analysis-register validator. The abstract is a compressed claim map, not an importance
pitch. Statistical and evaluation reporting must name the independent unit, estimand,
uncertainty, exclusions, and multiplicity treatment actually used. Experimental design,
split construction, and frozen evaluation remain upstream in the publication pipeline;
this skill reports and audits them without redesigning the protocol.

For `rebuttal`, read [rebuttal and revision](references/rebuttal-and-revision.md). Account for every material
comment. Distinguish correction, clarification, valid new evidence, principled
disagreement, partial resolution, and accepted limitation. Never describe a promised or
requested experiment as completed. Keep the response, revised manuscript, and change
locations synchronized.

## Audit source, rendering, and package

Use the local [manuscript-core component](components/manuscript-core/guide.md) with a
current venue profile. Its TeX, PDF, archive, and review-report commands live under
`$SKILL_DIR/components/manuscript-core/`.
Automated checks are necessary but incomplete. Inspect the rendered PDF at the actual
page size and normal reading scale for visible identity, page transitions, fonts,
clipping, equations, tables, figures, captions, links, references, disclosure, and
main-supplement consistency.

Run the adversarial lenses in [adversarial audit](references/adversarial-audit.md). A passing format check
does not establish scientific soundness, and a strong scientific argument does not
waive venue rules. Report observed defects separately from inference. Give each finding
the smallest valid action and a verification step.

Preserve the last accepted manuscript before a rebuttal or final revision. For
`camera-ready` and `package`, compare the candidate against that baseline and reconcile
all promised changes. Uploading, saving to a submission portal, posting a response, or
submitting is an external action and requires explicit author authorization.

## Independent completion and optional specialists

This skill completes conference prose, manuscript-context figures, current venue
compliance, responses and the local submission package without another installed skill.
For authorized plotting or diagram construction, read
[standalone figures](references/standalone-figures.md). New or redesigned schematics
default to **GPT Image 2.5 concept, then native editable PPTX** using available image
and presentation tools directly. Produce the master, manuscript exports and inspected
render, not merely a brief. Measured plots stay
source-derived. Read-only audits do not authorize drawing or changing an approved figure.

When available, `build-scientific-visualizations` adds specialist layouts and design
helpers to that same default. Its absence does not stop concept generation or local
PPTX construction. Scientific design, new
experiments, protocol changes and disputed result resolution remain separate research
scope, whether handled directly or with optional `research-publication-pipeline`.
