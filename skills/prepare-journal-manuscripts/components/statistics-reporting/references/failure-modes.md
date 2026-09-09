# Common statistical failure modes

## P0 candidates

- **Pseudoreplication:** subsamples are treated as independent units, overstating
  precision.
- **Dependence ignored:** paired, repeated, clustered, longitudinal, blocked, or nested
  observations are analyzed as independent.
- **Multiplicity hidden:** many comparisons are performed without defining the family,
  correction, or prespecified primary set.
- **Interaction inferred incorrectly:** two effects are said to differ because one
  comparison crosses a significance threshold and the other does not.
- **Outcome-dependent exclusion or selection:** units, seeds, checkpoints, metrics, or
  thresholds are selected after observing the result.
- **Unscorable evaluation:** a fold or slice lacks the classes/events needed by the
  metric, then disappears from an aggregate.

Treat these as P0 only when the supplied artifact establishes the defect and it affects a
central claim. Otherwise record an unresolved risk and settling check.

## P1 candidates

- effect estimate or uncertainty missing for a central comparison;
- small independent sample with strong, precise, or general claims;
- assumptions unsupported for the model and data scale;
- outlier, missing-data, or exclusion handling unclear;
- correlation or predictive association rewritten as causality or mechanism;
- model-selection, seed aggregation, or comparison budget missing;
- denominator and skipped count absent for a reported aggregate.

## P2 candidates

- error bars, box/violin conventions, stars, or `ns` undefined;
- panel-specific `n` missing;
- software or version omitted when relevant and available;
- inconsistent terms for units, replicates, intervals, or tests across artifacts.

The smallest fix is often a definition, exact count, corrected claim, or direct test. Do
not recommend a more complicated model merely because it sounds rigorous.
