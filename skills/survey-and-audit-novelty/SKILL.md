---
name: survey-and-audit-novelty
description: Use when deciding whether a research direction is still open, including a literature survey that has to end in a decision, a novelty audit, a prior art check, a scoop check against recent work, asking whether anyone has already done this, or checking that the variables an idea needs actually co-exist in one obtainable dataset. Use before an experimental plan is written, and again whenever a near-identical paper appears.
---

# Survey and Audit Novelty

Turn a direction into a decision. The survey ends with a verdict rather than a reading
list, the novelty audit tries to destroy the idea rather than confirm it, and the
feasibility check asks whether the data the idea needs exists in one place.

Three verdicts come out and they are recorded separately, because merging them hides
which one actually fired.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `contribution-lane` | Name the lane before searching, because the lane decides what counts as a collision | `references/contribution-lanes.md` |
| `joint-variable-audit` | Check that the variables the hypothesis needs co-exist in one obtainable cohort | `references/joint-variable-audit.md` |
| `search-angles` | Run the survey across several independent framings and record what each returned | `references/search-angles.md` |
| `kill-layer` | Adjudicate collisions and name which layer a kill lands on | `references/kill-layers.md` |

Run `contribution-lane` first. A search launched without a declared lane produces
"this space is taken", which is a statement about the lane, not about the space.

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through a package parent.

## Record three verdicts, not one

| Field | Values | Meaning |
|---|---|---|
| `scoop_verdict` | `IDENTICAL`, `ADJACENT`, `UNCERTAIN` | Whether existing work is the same work |
| `feasibility` | supported by measured headroom and a measured noise floor | Whether the task has room left |
| `venue_fit` | a judgement, with reasons | Whether the result would be publishable where you intend |

`venue_fit` may recommend stopping, but it must be reported under its own name. A
venue-fit doubt presented as a collision is a silent rejection, and it is unappealable
because the reader cannot see what was actually decided.

Only `IDENTICAL` kills. Adjacent work is a baseline to build on and to compare against,
not a verdict.

## Audit the data before auditing the idea

Before any novelty judgement, establish that the variables the hypothesis needs are
observed together in samples you can actually obtain. Conditions satisfied separately
with an empty intersection is the most common way a direction dies, and it is invisible
until counted.

The evidence is a measured co-occurrence table, produced before any analysis code is
written. "The data all exists" is not that table.

An empty intersection does not close the direction. Three moves come next, and skipping
them turns a data question into an unsupported claim that the data does not exist:
widen or substitute the source, relax the matching level to a coarser but still
meaningful unit, or assemble the pairing yourself and say so.

## Say what you searched

"No such data exists" and "no one has done this" are strong assertions. Both require an
enumerated list of what was checked. Not having looked is not evidence of absence, and
the list is what a reader uses to find the resource you missed.

When quoting another paper's ablation, limitation or conclusion in support of a kill,
read the whole passage first. A verbatim half-sentence used against its own context is
more dangerous than no citation, because it is checkable and wrong.

## Name the layer before reporting a kill

A collision report is not automatically a kill. State which of three layers died.

1. **Framing.** The way the question is phrased is taken. Change the framing; the
   underlying asset is untouched. This layer is routinely misreported as a dead asset.
2. **Data.** The required observations are unavailable. This claim must pass the
   enumeration rule above; the first place you looked coming up empty is not this layer.
3. **Task.** Measured headroom is at or below the measured noise floor. This is the
   only layer that kills the asset.

A kill that cannot name its layer has not been established.

Read per-item verdicts before the summary verdict. A summary verdict is written at the
widest scope in the report, and the widest scope is the one most likely to be occupied
already, so a narrow claim can survive a report whose headline says otherwise.

## Audit your own kills before reporting them

List every kill, then ask for each one what single correction to the search or the
framing would reverse it. If most of them would be reversed by an available correction,
the audit was measuring your fatigue rather than the literature. Report the count.

## Boundaries

This skill does not design experiments, does not measure headroom itself, and does not
write the plan that consumes its output. It produces the charter, the survey and the
audit that a planning step reads.
