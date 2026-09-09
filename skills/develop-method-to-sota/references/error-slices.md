# Reading the error by slice

One aggregate number cannot say where a method loses, and a method designed against an
aggregate is a guess. Before any component is designed, partition the evaluation set and
read the error inside each part.

## Choosing the partition

Partition by the variables that plausibly change the difficulty of the prediction, not by
whatever the metadata makes convenient. Typical axes are the size or length of the unit,
the frequency of the label, the acquisition batch or site, the distance from the training
distribution, and the presence of the phenomenon the method targets.

Report, for every slice, the count that entered it and the count that was excluded. A
slice whose denominator is not stated cannot be compared with anything.

## Reading the table

Look for three shapes.

A slice that carries most of the total loss identifies where a component can pay for
itself. Compute each slice's contribution to the overall error, not only its own rate:
a bad rate on a rare slice moves nothing.

A slice where the method already performs near the oracle arm is closed. Effort there
returns nothing regardless of how bad the absolute number looks.

A slice that is worse than a trivial predictor indicates a defect rather than a research
opportunity. Investigate before designing anything.

## Connecting slices to components

The slice table is what makes a mechanism hypothesis testable. A component introduced to
fix a stated failure should improve the slice where that failure concentrates. If the
aggregate improves while the target slice does not, the component works for some other
reason, and the stated mechanism has not been demonstrated.

Keep the slice table under version control alongside the run that produced it. It is
re-read at every iteration and is the main defence against optimising an average.
