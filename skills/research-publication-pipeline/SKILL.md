---
name: research-publication-pipeline
description: Use when selecting, starting, or resuming an evidence-gated research route for a top computer-science venue or Nature-family journal; source-grounded paper reading, AI-for-biology data feasibility, scoop checks, venue fit, baseline headroom, frozen protocols, controlled iterations, claim locking, negative-result handling, preparing a full working manuscript with figures, or curating a reproducible public code release. The workflow completes its local research-to-manuscript scope without another skill; compute, locked-test access, canonical mutation and external writes require their own authorization.
---

# Research Publication Pipeline

Turn a research idea into a sequence of falsifiable decisions. Keep feasibility, novelty,
contribution lane, venue fit, empirical headroom, and final claim support separate. A polished
story cannot substitute for a failed gate.

This public edition is a human-facing scientific workflow. It does not contain a remote launcher,
private infrastructure, opaque control state, or publication automation.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `survey` | Map papers, data, task definitions, current incumbents, failure modes, credible contribution routes, or publication patterns under a bounded search or supplied corpus | `references/survey-and-planning.md`; add the paper-card component for one source or `references/exemplar-corpus-calibration.md` for a multi-paper exemplar corpus |
| `plan` | Freeze the project charter, lane, hypothesis, decision-relevant checks, resources, and stop rules | `references/survey-and-planning.md` |
| `pilot` | Run the smallest real-data test that can invalidate feasibility or the load-bearing premise | `references/pilot-and-monitoring.md` |
| `develop` | Measure headroom and test one registered mechanism at a time under the frozen protocol | `references/protocol-headroom-and-development.md` |
| `monitor` | Observe an authorized run from its outputs, detect anomalies, and separate progress from completion | `references/pilot-and-monitoring.md` |
| `freeze` | Lock protocol and candidate, verify evaluation readiness, then protect the final test boundary | `references/frozen-evaluation.md` |
| `claim-lock` | Convert the frozen result into supported, narrowed, refuted, and not-run claims | `references/frozen-evaluation.md` and `references/evidence-claims-and-handoff.md` |
| `handoff` | Select a terminal scientific outcome and transfer a locked contract to manuscript or figure work | `references/evidence-claims-and-handoff.md` |
| `manuscript` | Write, illustrate, render and inspect a complete evidence-linked working manuscript and local candidate package | `references/standalone-manuscript.md` |
| `public-release` | Curate and rehearse a clean, runnable public code artifact without publishing it | `references/public-code-release.md` |

Use one primary mode per pass and return to an earlier mode when its underlying decision
is invalidated. A mode name records the scientific boundary being resolved; it does not
claim that an experiment ran or an external action occurred.

## Start or resume

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every bundled script,
reference, template, and component is below that directory; never resolve through the
package parent. Run scripts by their resolved skill-local paths rather than assuming the
user's working directory.

For a new project, create an empty workspace:

```bash
python3 "$SKILL_DIR/scripts/init_publication_project.py" /path/to/project \
  --project-id example-study \
  --title "A falsifiable research question" \
  --domain single-cell \
  --contribution-lane sota-method
```

Choose one contribution lane at intake:

- `sota-method`: a mechanism is expected to beat the strongest matched comparator on a frozen
  task and representation.
- `discovery`: the central output is a scientific finding with an independent validation path.
- `benchmark`: the central output is a consequential missing resource or corrected evaluation
  contract with a credible venue precedent.

Do not change lanes because the original route became difficult. Record a new route decision and
return to intake.

When resuming, read `project.json`, all eight records named in `START_HERE.md`, current project
authority, and the newest actual result before trusting a narrative status. Modification time is
not authority.

Run the smallest relevant check:

```bash
python3 "$SKILL_DIR/scripts/validate_publication_project.py" /path/to/project \
  --target working --format text
```

The targets are cumulative scientific boundaries:

| Target | What it checks |
|---|---|
| `working` | Portable structure and explicit unresolved work |
| `pilot` | Authority, data feasibility, lane-specific scoop verdict, venue fit, and hypothesis |
| `development` | Frozen protocol, baseline parity, open measured headroom, candidate order, and locked-test isolation |
| `handoff` | Terminal outcome, result comparison, claim locking, limitations, and specialist readiness |
| `public-release` | Handoff plus a curated, inspected `public-release/` tree |

A pass means the records satisfy this contract. It does not prove scientific truth, novelty,
venue acceptance, or permission to act externally.

## Synthetic demonstration

To inspect a complete local record contract without using real research material, run the
bundled demonstration from this installed skill directory:

```bash
python3 examples/run_demo.py OUTPUT_DIRECTORY
```

`OUTPUT_DIRECTORY` must be a new directory outside this skill. The command prints the
observed `PASS` status for `pilot`, `development`, and `handoff`. It does not run a real
experiment, access a locked test, authorize an action, publish anything, or demonstrate
scientific effectiveness. Read [examples/README.md](examples/README.md) for expected output
and the generated-workspace boundary; the workspace is a runtime output, not release content.

Add `--with-public-release` to rehearse the bundled synthetic code release: package,
fresh unpack, run its fixed example and tests, compare the result, then validate the
curated tree. This optional path records actual local command observations, not a real
research experiment or external publication. It uses the existing Python environment.

## Reference router

Read only what the current boundary needs:

| Task | Read |
|---|---|
| authority, data feasibility, novelty, contribution lane, or venue route | `references/intake-and-routing.md` |
| bounded field survey, paper reading, charter, or execution plan | `references/survey-and-planning.md` |
| multi-paper exemplar corpus, publication-pattern calibration, or cross-paper figure/section precedent | `references/exemplar-corpus-calibration.md` |
| pilot design, retrainability probe, authorized-run observation, or anomaly handling | `references/pilot-and-monitoring.md` |
| benchmark freeze, baselines, headroom, candidate design, iteration, or recovery | `references/protocol-headroom-and-development.md` |
| evaluation lock, baseline parity, known-answer guard, lockbox exposure, or frozen decision | `references/frozen-evaluation.md` |
| source status, claims, negative results, manuscript handoff, or public release | `references/evidence-claims-and-handoff.md` |
| complete manuscript, figures, declarations, response or local submission candidate | `references/standalone-manuscript.md` and `references/standalone-figures.md` |
| curated code tree, clean-room rehearsal, documentation, or release readiness | `references/public-code-release.md` |

Open current primary sources for literature claims and current official instructions for venue
rules. A cached reference explains the method but cannot establish a current deadline, policy, or
format rule.

## Stage 1: resolve authority and evidence

Record the source that defines the active project before ideating. Current explicit user scope and
structured project status outrank an old README or plan. A withdrawn, superseded, frozen, or
provenance-only artifact may be audited but must not silently become the active submission base.

In `evidence/source-register.json`, use only:

- `VERIFIED` when the source was opened and the cited location was inspected;
- `UNVERIFIED` when it has not been checked;
- `COULD_NOT_OPEN` when access failed;
- `NOT_FOUND` when a dated search found no candidate source.

Only `VERIFIED` sources support a passing gate. Keep locators and inspected sections precise. Do
not infer facts from a title, search result, neighboring project, or remembered citation.

## Stage 2: make three independent intake judgments

Complete `intake/intake.json` in this order:

1. `data_feasibility`: prove the required variables coexist in linkable samples, count the true
   independent units, name the strongest cheap baseline, and define a leakage-safe split.
2. `scoop`: search the exact contribution lane and return `IDENTICAL`, `ADJACENT`, or `UNCERTAIN`.
   Adjacent work constrains the delta but does not kill the topic.
3. `venue_fit`: match the contribution shape and necessary evidence to a current venue and article
   type. Weak venue fit is not an identical-work verdict.

Then freeze one hypothesis with endpoint, direction, minimum relevant effect, uncertainty method,
validation path, and kill criterion. A pilot tests feasibility; it does not prove novelty or
submission readiness.

Refresh the current incumbent at intake and immediately before protocol freeze. A later
method or corrected implementation can change the comparator set and practical
headroom without making the original survey dishonest.

## Stage 3: measure headroom before method complexity

Freeze `protocol/protocol.json` before controlled iteration. It must name the exact data versions,
preprocessing boundary, independent-unit split, leakage guard and known-bad guard test, primary
metric implementation, baselines and tuning parity, uncertainty unit, selection and checkpoint
rules, finite budgets, locked-test policy, allowed changes, and four-way stop rules.

Before aggregate scoring, run the known-answer and leakage guard cases described in
`references/frozen-evaluation.md`. Abort evaluation if a guard fails. Record every
lockbox exposure, including structural inspection that reveals labels, ordering, or
other outcome-bearing information.

Reproduce the strongest cheap and field comparator before proposing a new architecture. Record
`development/headroom.json` for the exact task and strongest available representation. `OPEN`
requires a measured gap above both the noise floor and the minimum claim-worthy margin. If that
gap is closed, change the question or stop; tuning cannot manufacture headroom.

## Stage 4: run controlled, failure-directed iteration

Register causal candidates in `development/iteration-ledger.json`. Each candidate names a
diagnosed failure node, one minimal mechanism, its predicted slice, a matched control, and a
falsifier. For a SOTA-method lane, register at least two mechanism-level alternatives, but do not
register a second architecture while lower construction rungs remain unresolved.

Use the fixed order:

```text
recipe_parity -> objective_alignment -> data_or_representation
-> ensemble -> test_time_compute -> architecture
```

One cycle tests one registered load-bearing change. Record actual observations with locators,
failed work, work not run, and scientific inference in separate fields. Do not tune on the locked
test, promote a secondary metric, hide failed trials, shop seeds, weaken baselines, or remove an
unfavorable dataset after seeing results.

Two misses on the frozen predicted slice kill that mechanism, not the whole route. If headroom,
budget, and a registered alternative remain, pivot. Route-level stopping is limited to measured
closed headroom, exhausted frozen budget surfaced for human review, or a newly verified
lane-identical scoop. An integrity anomaly requires a new protocol; it is not evidence that the
scientific question failed.

## Stage 5: evaluate once and lock claims

Freeze the selected candidate before opening the locked test. Locked-test access, remote compute,
and benchmark submission always require separate explicit authorization outside this local record.
Evaluate with the frozen data, split, metric, comparator, seed aggregation, and uncertainty unit.
Keep a failed final evaluation visible.

Apply frozen criteria as the exact logical conjunction registered in the protocol; do
not replace all-required conditions with a convenient subset after seeing results.
Distinguish an underpowered check from a measured miss using the preregistered
resolution and uncertainty rule, not post-hoc optimism.

In `claims/claim-register.json`, every included result claim must have:

- `SUPPORTED` or `NARROWED` status;
- exact scope and verified evidence sources;
- result locators and uncertainty;
- separate observed facts, inference, limitations, and work not run.

A refuted claim is excluded or reported as a negative result. It is never rewritten as a positive
claim through framing.

## Stage 6: route the handoff

Choose one terminal outcome in `handoff/handoff.json`:

- `MANUSCRIPT`: the frozen evaluation and route-specific validation support scoped claims;
- `NEGATIVE_RESULT`: preserve a refuted or narrowed claim and its evidence;
- `RETURN_TO_INTAKE`: reframe a framing failure, hold a data gap, or respond to an identical scoop;
- `STOPPED`: measured headroom is closed or the frozen budget is exhausted.

For a full research-to-paper request, continue from the locked outcome to
[standalone manuscript production](references/standalone-manuscript.md). The internal
paper-reading component and the following optional specialists can enhance this work:

| Need | Capability |
|---|---|
| paper understanding | internal `components/paper-card/guide.md` |
| handing a running project to another person | internal `components/project-handover/guide.md` |
| conference manuscript, abstract, statistics reporting, or rebuttal | `prepare-conference-manuscripts` |
| journal manuscript, abstract, statistics reporting, data availability, or revision | `prepare-journal-manuscripts` |
| scientific figures and flowcharts | `build-scientific-visualizations` |
| Chinese funding proposal | `writing-funding-proposals` |

Read each selected skill or component before using it. No specialist is required for
this skill's own research-to-manuscript scope. Their absence is not permission to invent
venue rules or scientific evidence, and is not a reason to stop at a handoff record.

When an authorized manuscript handoff or working-draft scope includes figure production,
or the user requests figures directly, new or redesigned flowchart, architecture,
motivation, method and mechanism figures default to destination-style GPT Image 2.5
concepts followed by native editable PPTX using available tools directly via
[standalone figures](references/standalone-figures.md). The optional visualization skill
adds specialist compound layouts and design helpers to that same route.
Keep locked scientific content and destination policy;
measured panels retain their source-data plotting route. Follow the scoped boundaries in
[evidence, claims, and handoff](references/evidence-claims-and-handoff.md).
A pilot or status-only task does not itself request figure production.

## Public release boundary

Follow `references/public-code-release.md`. Build public material only inside the
project's relative `public-release/` directory from an explicit allowlist. Include useful
code, configuration, small examples, dependency versions, data-access instructions,
expected outputs, tests, licence, citation, and honest limitations. Do not copy the
publication workspace, internal decision records, credentials, hidden prompts,
execution records, private project evidence, or automation traces into that tree.

The `public-release` validator inspects the curated tree. Publishing a repository, creating a
release, uploading files, mutating a canonical manuscript, submitting a benchmark result, or
submitting a paper remains a separate external action requiring explicit authorization and direct
service evidence.

## Report status precisely

Lead with the current decision, then report:

- observed commands, results, paths, and source locators;
- failed and not-run work;
- inference and its uncertainty;
- the next scientific gate;
- any exact authorization boundary.

Keep module completion, manuscript readiness, public-release readiness, and actual publication as
different states.
