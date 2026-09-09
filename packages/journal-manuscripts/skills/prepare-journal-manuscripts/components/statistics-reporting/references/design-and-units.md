# Design and analysis units

## Independent unit

Define the smallest unit independently assigned, sampled, or capable of carrying the
comparison. Cells, fields, images, wells, reads, spectra, repeated observations, and
technical replicates usually describe subsampling within a biological or experimental
unit. They may show within-unit variation but do not automatically increase independent
`n`.

Record the whole hierarchy, for example:

```text
participant -> visit -> tissue -> section -> field -> cell
training dataset -> split -> example; optimization run -> checkpoint -> evaluation
```

Then state which level supports uncertainty and generalization. Use aggregation,
hierarchical models, cluster-robust methods, paired analysis, or another justified
treatment only after the design is known.

## Paired, repeated, nested, and blocked designs

- Preserve pairing when the same unit appears under both conditions.
- Treat repeated measurements from one unit as dependent.
- Represent site, batch, donor, plate, run, or study effects when they can carry
  systematic variation.
- Do not call a fold valid merely because train and test are disjoint. Confirm each fold
  contains the label or outcome variation needed for the selected metric.
- If a grouping factor is nested inside the label, ordinary group holdout may produce
  single-class folds. Redesign the evaluation at the independent unit before interpreting
  the metric.

## Denominators and exclusions

For every mean, rate, ratio, metric, subgroup, panel, and evaluation slice, record units
included and skipped. Give the reason and timing for every exclusion. A plausible
aggregate over survivors can hide a nearly empty or selectively filtered comparison.

An operational failure is not automatically a statistical outlier. Link the raw
observation, protocol rule, scientific impact, disposition, and sensitivity analysis
when exclusion can affect a conclusion.

## Stochastic computational studies

Seeds describe optimization or sampling variation; they are not new biological samples.
Compare methods on the same seeds when possible and analyze paired differences. Freeze
checkpoint selection, early stopping, model choice, thresholding, and comparison budget
before locked-test evaluation. Report all registered runs, failures, and selection rules.
