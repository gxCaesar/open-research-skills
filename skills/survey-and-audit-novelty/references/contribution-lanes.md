# Declaring the contribution lane

The lane is written down before the search starts. It determines what a collision means,
so deciding it afterwards lets the verdict follow whatever the search happened to return.

## The three lanes

| Lane | What is claimed | How a collision behaves |
|---|---|---|
| `discovery` | A specific fact about the world was found | Binary and brittle. The same finding published first reduces the contribution to zero |
| `sota-method` | A method performs better on a stated task | Graded and robust. Another method on the same task is a comparator; only a comparable margin is fatal |
| `benchmark` | A named evaluation gap is now covered | Depends on coverage. A collision matters only where the gap it fills is the same gap |

`discovery` and `benchmark` are lanes in their own right, not consolation prizes for a
method that did not win. Each carries its own required fields: a discovery states the
falsifier, a benchmark states the named gap and why an existing suite does not cover it.

## Why the lane must precede the search

"This whole area has been published" is a statement about a lane. The same territory can
be closed for `discovery` and wide open for `sota-method`, or the reverse. Before
declaring a space exhausted, state which lane the search ran in, and whether the same
territory is still open in the others.

## Margins

Set the bar from what the target venue actually published, not from a remembered
multiple. Sample recent accepted papers of the same type, measure the improvement each
reported on its headline metric, and use that distribution.

Bounded metrics such as accuracy, area under a curve, or correlation cannot move far
near their ceiling, so a multiplicative bar imported from an unbounded axis will
disqualify most of the papers you intend to sit beside. Compute the arithmetic ceiling of
the metric before choosing the bar.

Accepted work almost always carries a second axis alongside the headline number:
parameters, training cost, data efficiency, robustness, or a regime the incumbent cannot
enter. Design that axis during the charter. Looking for it while writing the discussion
means it was not part of the contribution.
