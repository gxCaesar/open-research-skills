# Deciding to stop

The loop has three legal exits. Stopping without naming one is fatigue, and fatigue
produces a method that was abandoned rather than a result that was established.

## Exit 1 — the task is saturated

Measured headroom is at or below the measured noise floor. Both numbers must exist on
the current code and the current split. Three things must already be true before this
exit can be claimed.

An oracle arm has been run. Giving the model an input it will never have at deployment
establishes that a gap exists at all; without it, "no method helped" and "there is
nothing to find" are indistinguishable.

The noise floor was measured rather than asserted, on this code.

The search order was actually walked, from recipe through to architecture, rather than
jumped to the most interesting level.

## Exit 2 — the budget is exhausted

The pre-registered iteration budget has been spent. This exit hands the decision to a
person. It does not authorise freezing the current best configuration on your own
judgement, and the report should state what the next candidate would have been.

## Exit 3 — the working component was published elsewhere

The only component that survived its control has appeared in someone else's work. This
returns to the charter to choose a different contribution, and is not a stop either.

## What is not an exit

"Several candidates were tried and none worked" describes effort, not evidence. It maps
onto exit 1 only when the three preconditions above hold, and otherwise means the search
order has not been walked.

A saturation claim made from an aggregate number is not an exit. Saturation is judged per
slice, and a suite average routinely hides an open task.

## The report

Whatever the exit, the record states the exit number, the measured headroom, the measured
noise floor, the number of iterations, the killed construction shapes with their reasons,
and the single configuration that would be frozen next. A loop that ends without those
fields has to be re-run to be trusted.
