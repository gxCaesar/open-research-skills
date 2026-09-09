# One component per iteration

An iteration is a single change with a stated mechanism, a stated slice, and a control
that could have voided it. Two changes in one iteration produce a result that cannot be
attributed to either.

## Before the run

Write four lines and keep them with the run.

1. **Order.** Which of the six search levels this candidate sits at. Recipe, objective,
   data, ensembling, test-time computation, architecture.
2. **Construction shape.** What the candidate operates on and what it does to it, in one
   sentence, with no product names. This is how duplicates are detected.
3. **Mechanism.** Which failure the component removes.
4. **Predicted slice.** Where the improvement must appear if the mechanism is real.

A candidate whose construction shape matches an already-killed candidate inherits that
kill. Overriding the inheritance requires one sentence naming which computation differs.
Renaming is not a difference.

The bundled checker compares shapes after removing case, punctuation and spacing, so it
catches a rename and nothing more. Two descriptions of the same construction in different
words read as different shapes to it. Deduplication is your judgement; what the checker
enforces is that a repeat you did notice was acknowledged rather than left implicit.

## Designing the control

The control destroys the mechanism and preserves everything else. Both halves are
required and the second is the one that fails in practice.

A control that removes the component but substitutes another genuine intervention —
a different initialisation, an extra normalisation, a changed batch composition —
recovers much of the gain and makes a working component look inert. When that happens
the component is not disproved; the control is.

Never issue a void verdict from one seed. Killing is the irreversible direction, so it
carries the heavier evidential burden. Run the control at the same seed count as the
treatment arm and compare the paired differences.

## Reading the outcome

| Outcome | Reading |
|---|---|
| Aggregate improves and the predicted slice improves | The mechanism is supported |
| Aggregate improves, predicted slice does not | Something else is responsible; restate the mechanism or drop the claim |
| Neither improves, control also inert | The candidate is dead; record the shape so its siblings inherit it |
| Control recovers most of the gain | The control is broken; rebuild it before judging the component |

A tie is reported as "not distinguishable at this sample size", never as "no difference".
The remedy for a tie is more resolution, not a looser threshold.

## Keeping the ledger

Every iteration appends one row: date, order, construction shape, mechanism, predicted
slice, seeds, treatment result, control result, verdict. Negative rows stay. They are
what stops a later iteration from re-running a shape that has already been killed, and
they are what a supplementary section needs when the work is written up.
