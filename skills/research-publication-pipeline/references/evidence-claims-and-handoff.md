# Evidence, claims, and handoff

Use this reference when converting experimental records into claims, manuscript work, a negative
result, or a public artifact.

## Observation is not inference

Keep four evidence states separate in iteration and claim records:

- `observed`: an actual output, value, command result, or inspected artifact with a locator;
- `failed`: an attempted check or run that did not produce valid evidence;
- `not_run`: work that remains unperformed;
- `inferred`: scientific or editorial interpretation derived from stated observations.

An agent narrative or validator pass is not experimental evidence. A missing value, placeholder,
illustrative bar, inaccessible link, planned repository, or neighboring result cannot support a
positive claim.

## Build the claim register from results

Give each scientific statement a stable ID and classify it as `RESULT`, `METHOD`, `PRIOR_WORK`, or
`LIMITATION`. Record its status:

- `PROSPECTIVE` before the result exists;
- `SUPPORTED` when the exact scoped evidence supports it;
- `NARROWED` when only a smaller population, task, metric, context, or mechanism survives;
- `REFUTED` when the frozen test contradicts it;
- `UNVERIFIED` when load-bearing evidence is inaccessible or incomplete.

An included result claim needs exact scope, verified source IDs, result locators, uncertainty,
observations, and limitations. Keep comparator, metric, dataset, split, population, direction, and
validation qualifiers attached to the sentence. A supported narrow result does not license a broad
mechanism, biological discovery, clinical, or prospective claim.

Refuted results are either excluded from a positive narrative or recorded with
`REPORT_NEGATIVE`. Do not hide them by changing the endpoint, selecting a favorable slice, or
switching contribution lane after seeing the outcome.

## Choose a terminal outcome

### `MANUSCRIPT`

Use only after the final evaluation matches the frozen protocol, the strongest comparator is
included, locked-test usage remains within budget, included claims are locked to evidence, and the
selected route has its required validation. Top-CS usually needs transfer across data, tasks,
contexts, or shifts plus ablations and failure bounds. Nature-family usually needs orthogonal,
external, prospective, functional, or real-use biological validation. Another learned evaluator
is not independent biological validation.

### `NEGATIVE_RESULT`

Preserve at least one refuted or narrowed claim, its exact protocol, and the negative evidence.
State whether the result closes one mechanism, one task, or practical headroom. A negative outcome
can inform a paper or report, but it does not automatically become a benchmark contribution.

### `RETURN_TO_INTAKE`

Use for a framing repair, unresolved data gap, material route change, or lane-identical scoop.
Preserve prior work. Start a new versioned hypothesis rather than editing the failed one into a
different claim.

### `STOPPED`

Use only when practical headroom is measured closed or the frozen budget is exhausted. Report the
strongest falsifier, what was actually tried, and which conclusion is no longer supported.

## Independent manuscript completion and optional handoff

Before marking a manuscript handoff ready, identify the exact downstream tasks:

- paper reading and claim extraction;
- statistical and evaluation reporting;
- data and code availability;
- figure content and visual QA;
- venue-specific manuscript rules;
- abstract compression after the results and claim boundary are fixed.

For a full research-to-paper request, use [standalone manuscript](standalone-manuscript.md)
to produce the complete working draft, figures and local package. A handoff record alone
does not complete that request. Open current official venue instructions. Installed
specialists are optional enhancements; neither the local route nor a specialist may
change the split, metric, baseline, result or claim scope to improve the story.

When figure production is within an authorized manuscript handoff or working-draft
scope, or the user requests it directly, construct source-bound schematics without a
duplicate figure confirmation. Use [standalone figures](standalone-figures.md) for the
default destination-style GPT Image 2.5 concept → inspection → native editable PPTX →
rendered comparison and representative edit test, using available tools directly.
Preserve objects, arrow meanings, exact labels, claim limits and destination policy.
Optional `build-scientific-visualizations` adds specialist layouts and design helpers;
its absence does not gate the default route.

Generate only conceptual content. Quantitative panels, exact structures, microscopy,
and other measured evidence keep their original data or image route, including within
mixed motivation or method figures. Preserve negative findings, uncertainty, and the
planned-versus-observed distinction. An explicitly requested early planning schematic
may describe a prospective design; it cannot establish a completed experiment or a
`MANUSCRIPT` outcome. Routine `pilot` and `monitor` work does not trigger figure production.

Verify actual model identity before claiming it was the engine used. A built-in image
tool without a selector is usable; report its backend as unverified/unknown. Only
actual unavailable or prohibited steps use the standalone guide's fallback path.
The handoff grants no new compute, locked-test, canonical-artifact or
external-publication authority.

Mutation of an existing canonical or frozen manuscript requires explicit authorization. A new
working draft may be prepared only within the user's stated scope and must preserve the original.

## Curate the public release

Build public artifacts from `public-release/`, not from the publication workspace or experiment
parent. A useful release may contain:

- source code and small tests;
- pinned dependency versions and runnable commands;
- public configurations and split or preprocessing instructions;
- small synthetic examples and expected outputs;
- data access, licence, citation, and honest limitation notes.

Do not include credentials, private data, personal project material, raw experiment directories,
internal decision records, execution or authorization records, hidden prompts, agent instructions,
automation traces, or submission-portal state. Inspect filenames and readable text before any
external action. Service-managed integrity information stays on the service rather than being
reproduced in the repository.

`public-release` validation checks only the local curated tree. It does not publish, upload, create
a repository, submit a benchmark result, or submit a manuscript. Those actions need explicit
authorization and must be verified from the destination afterward.

## Readiness fields stay separate

Report these independently:

- scientific route outcome;
- module or analysis completion;
- manuscript handoff readiness;
- local public-release readiness;
- external release status;
- submission status.

A complete local module is not evidence that a paper is ready, released, submitted, or accepted.
