# Frozen evaluation

## Freeze only after parity and guard readiness

Record the exact candidate, code and configuration version, data and label versions,
preprocessing, split, independent unit, primary metric implementation, comparator set,
uncertainty, seed aggregation, checkpoint selection, exclusions, and decision rules.

Baseline parity covers information access, preprocessing, tuning opportunity, model
selection, compute or capacity where relevant, version, and evaluation implementation.
An official name alone does not establish parity. Resolve reproduction mismatches before
the final test.

Run known-answer cases before any aggregate score. Include at least one clean case with
an expected direction and one mutated or leakage-bearing case the guard must reject.
Abort before aggregate evaluation when a known-answer or leakage guard fails; do not
interpret the resulting metric.

## Treat the lockbox as exposed by information

Record every lockbox exposure. Exposure includes labels or outcomes, case ordering that
reveals them, per-example feedback, hidden-stratum membership, repeated leaderboard
feedback, or structural inspection that can guide selection. It is not limited to
copying a test file.

Keep the allowed exposure count, custodian, reason, observer, information revealed, and
resulting action. Any unregistered exposure invalidates the frozen decision and requires
a new untouched evaluation source or a scoped non-confirmatory report.

## Apply criteria exactly

Translate the frozen decision rule into a logical conjunction of all required
conditions. If the protocol requires primary-metric margin, predicted-slice support,
matched control, uncertainty, and efficiency, all must pass. Do not convert the rule to
"most conditions" or choose a subset after seeing results.

Distinguish a true miss from an underpowered check using the preregistered resolution,
minimum relevant effect, uncertainty method, and independent unit. `INCONCLUSIVE` is
valid only when those rules define it; it is not a rescue label for an unfavorable
point estimate.

## Keep the final test terminal

Report the frozen result against the strongest comparator with the paired effect,
interval, robustness, failure slices, calibration, costs, ablations, and negative
results required by the protocol. A failed criterion remains failed. Do not rescue the
route by changing metric, slice, exclusion, seed subset, comparator, or claim after the
lockbox is opened.

Lock claims only after evaluation. Mark each as `SUPPORTED`, `NARROWED`, `REFUTED`, or
`UNVERIFIED` with exact scope and locators. Preserve frozen negative results and work not
run. Development may begin again only under a new versioned hypothesis and untouched
evaluation boundary.
