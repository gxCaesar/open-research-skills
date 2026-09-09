---
name: develop-method-to-sota
description: Use when a method is not yet beating its baseline and the next change has to be chosen, including improving a model, reaching state of the art, deciding which component to add next, measuring headroom before building, designing an ablation control that can void a component, reading error by slice instead of one aggregate, or deciding whether to keep iterating or stop. Use during exploratory development on a development split, before any confirmatory run is frozen.
---

# Develop a Method to State of the Art

Turn a validated pilot into a method worth freezing. The loop is: measure what is
available to win before building anything, read the error where it actually lives,
add one component at a time with a mechanism hypothesis and a control that could void
it, and stop for a stated reason rather than from fatigue.

This skill governs the exploratory phase only. Iterating after a confirmatory run is
frozen is an unblinding event, not development.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `headroom-measure` | Establish the ceiling and the measured noise floor before designing anything | `references/headroom-and-noise-floor.md` |
| `error-slices` | Locate the loss by stratum rather than in one aggregate number | `references/error-slices.md` |
| `single-component` | Design, implement and test one component with a control that can void it | `references/component-iteration.md` |
| `exit-decision` | Decide freeze, continue, or return to the charter, and name which exit applies | `references/exit-decisions.md` |

Run `headroom-measure` first on any task the loop has not yet measured. A component
designed before the ceiling is known is a guess about where the loss is.

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through a package parent.

## Measure before building

Two numbers precede design work, and both are measured rather than claimed.

**Headroom** is how much of the metric is still available on this task with this
representation. It is a property of the task and the representation together, not of
the task alone, so it is measured per task and never extrapolated from a neighbour.
Ask first whether the current representation is the strongest one obtainable, because a
weak representation manufactures headroom that a better one would remove.

**The noise floor** is the spread of the same code, on the same split, across seeds,
library versions and environments. A reported margin smaller than the measured noise
floor carries no information. A bootstrap standard error is not a noise floor: it
describes resampling of one run, not re-execution of the pipeline. Pair the runs when
pairing is possible instead of differencing two point estimates.

When headroom is at or below the measured noise floor, the task is saturated for this
representation, and that is one of the three exits below.

## Order the search

Cheap and general changes come before expensive and specific ones. Architecture is last
because it is the most expensive place to be wrong.

1. Recipe: optimiser, schedule, regularisation, batch composition
2. Objective alignment: what the loss actually rewards versus what the metric scores
3. Data: quantity, cleaning, augmentation, weighting, label quality
4. Ensembling and aggregation
5. Test-time computation
6. Architecture

Record the order number of every candidate. A candidate at order 6 does not get a second
attempt while lower orders remain unexplored.

## One component, one mechanism, one control

Each iteration states a mechanism hypothesis before the run: which failure the component
is supposed to remove, and on which slice the improvement should therefore appear. A
component that improves the aggregate but not its stated slice has not been shown to
work by the mechanism claimed.

The control arm destroys the mechanism and preserves everything else. The second half of
that sentence is the half that gets violated: a control that still applies some other
real intervention will recover most of the gain and will make a working component look
dead. Never issue a void verdict from a single seed.

Deduplicate candidates by construction shape rather than by name. Write one line saying
what the candidate operates on and what it does to it; a candidate with the same shape
as a killed one inherits that kill unless you can say in one sentence which computation
differs.

## Three legal exits

Stopping requires naming which exit applies. If none applies, the loop continues.

1. Measured headroom is at or below the measured noise floor.
2. The pre-registered budget is exhausted. This returns the decision to a person; it is
   not a licence to freeze on your own.
3. The only component that worked has been published by someone else. This returns to
   the charter, which is also not a stop.

"Several things were tried and none worked" is not an exit. Before claiming saturation,
an oracle arm must have been run — a model given an input that is unavailable at
deployment — so that the remaining gap is known to exist.

## Boundaries

This skill does not decide whether an idea is novel, does not run the confirmatory
campaign, and does not write the paper. It reports what a development split shows.
A development-split result is not a finding until a frozen run reproduces it.
