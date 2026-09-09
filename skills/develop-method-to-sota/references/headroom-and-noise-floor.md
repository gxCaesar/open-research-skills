# Headroom and the noise floor

Both numbers are measured on the current code and the current split. Neither is quoted
from a paper, inherited from a neighbouring task, or estimated from experience.

## Measuring the noise floor

Run the identical configuration several times while varying only what you do not control
at deployment time: the seed, the library build, the machine. Report the spread, not a
single number, and state how many runs entered it.

Three failure modes appear here repeatedly.

A bootstrap standard error is not a noise floor. Resampling one run's predictions
describes sampling variability inside that run; it says nothing about what changes when
the pipeline is executed again.

A threshold written as `mean ± k × range` should be converted to standard deviations
before it is used, because the two scales diverge fast at small sample sizes. With four
runs, twice the range is roughly five standard deviations, which is a far weaker claim
than it appears.

Two point estimates plus an assumed margin is not a comparison. When the same instances
can be scored under both conditions, pair them and test the paired differences.

## Measuring headroom

Headroom is the distance between the current score and the best score reachable on this
task with this representation. Estimate the upper end with an arm that is allowed
something the deployed model never gets: the true label for a nuisance variable, a
retrieval oracle, a held-out covariate. The gap that arm leaves is the headroom that
method work can address.

Two rules keep this honest.

Headroom belongs to the pair (task, representation). Changing the representation changes
the headroom, so ask whether the current representation is the strongest available
before concluding that a task is saturated.

Headroom is measured per task. A saturated task in a benchmark suite says nothing about
its neighbour, and a suite-level average hides exactly the tasks worth working on.

## What the numbers decide

| Observation | Consequence |
|---|---|
| Headroom greatly exceeds the noise floor | The task is open; proceed to error slices |
| Headroom is comparable to the noise floor | Improve the representation or the measurement before designing components |
| Headroom is at or below the noise floor | Exit 1 applies; record it and stop |

Record both numbers with the command that produced them. A number without its
measurement procedure cannot be re-used and will be re-derived at full cost.
