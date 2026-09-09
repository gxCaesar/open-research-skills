# Protocol, headroom, and controlled development

Use this reference after intake supports a specific hypothesis and route.

## Freeze the benchmark contract

Before controlled iteration, record:

- exact data and label versions, licences, preprocessing, and missing-data policy;
- independent unit and every group, entity, time, cohort, scaffold, or out-of-distribution split;
- all train-derived normalization, feature, retrieval, prior, and cache boundaries;
- primary metric direction and exact implementation;
- baseline versions, configurations, information access, and tuning budgets;
- seed aggregation, uncertainty unit and method, early stopping, checkpoint selection, and
  exclusion rules;
- finite development-cycle and locked-test-access budgets;
- locked-test custodian and permitted access time;
- allowed development changes and exact `advance`, `revise`, `pivot`, and `stop` rules.

Run one known-bad leakage mutation and show that the guard rejects it. A guard that has only passed
clean data has not demonstrated its failure sensitivity.

The frozen protocol does not authorize compute. A changed claim, endpoint, split, metric,
comparator set, selection rule, or test policy requires a named pivot and a new versioned protocol.

## Reproduce before inventing

Run comparators in this order when applicable:

1. constant, mean, label-shuffle, and tiny-subset sanity controls;
2. linear or ridge, nearest neighbor, additive response, fixed workflow, retrieval-only, or
   another strongest cheap comparator;
3. accepted domain practice;
4. a recent strong method using its official implementation and matched recipe;
5. parameter-, information-, and compute-matched controls for the proposed mechanism.

Resolve an unexplained reproduction mismatch before designing a new model. Record observed and
reference values, tolerance, split, metric, configuration, environment, predictions, and log
locator. Apply comparable tuning effort to baselines and candidates.

## Measure practical headroom

Bind headroom to one task, the strongest available representation, the strongest frozen baseline,
primary metric, independent unit, and empirical noise floor.

For a higher-is-better metric:

```text
measured_headroom = credible_upper_bound - strongest_baseline
```

For a lower-is-better metric:

```text
measured_headroom = strongest_baseline - credible_lower_bound
```

Use an oracle, assay ceiling, cross-replicate ceiling, privileged-information model, or another
defensible practical bound. Do not call headroom open merely because the theoretical metric range
extends farther. `OPEN` requires the measured gap to exceed both implementation or sampling noise
and the minimum margin that would support the intended claim.

If the strongest cheap baseline closes the gap, change the scientific question or stop. A more
fashionable architecture cannot create decision-relevant headroom.

## Diagnose before choosing a mechanism

Slice development errors by the true independent unit, scientific context, novelty or distance,
quality, prevalence, and consequential subgroups. Distinguish data or label ceiling, numerical or
optimization failure, shortcut or leakage, representation mismatch, missing biological context,
calibration or uncertainty, out-of-distribution shift, and retrieval or orchestration failure.

For each candidate, record:

| Diagnosed failure | Minimal mechanism | Predicted slice | Matched control | Falsifier |
|---|---|---|---|---|

Candidates must differ by failure node or design axis, not only by module name. Compare an LLM,
agent, graph, diffusion model, foundation model, or additional scale against a null and an
equal-information control. Reject the specialized component when those controls explain the gain.

## Fixed construction order

Use this order and document why every lower rung was tried, ruled out, or does not apply:

1. `recipe_parity`
2. `objective_alignment`
3. `data_or_representation`
4. `ensemble`
5. `test_time_compute`
6. `architecture`

Architecture is last. Do not register a second architecture while a lower rung remains untried.
For a SOTA-method lane, retain at least two causal mechanism candidates so that one falsified
mechanism does not collapse the project into unregistered trial-and-error.

## One controlled cycle

One cycle tests one registered load-bearing change under the unchanged protocol. Record:

- the candidate and construction rung;
- predicted-slice result;
- matched-control and ablation status;
- complete seed aggregation and paired independent-unit uncertainty;
- observed facts with output or log locators;
- failed, invalidated, pruned, and planned-but-not-run work;
- scientific inference separately from observation;
- exactly one decision: `ADVANCE`, `REVISE`, `PIVOT`, `STOP`, or `NEW_PROTOCOL`.

Do not inspect the locked test during development. Do not select a favorable seed subset, promote a
secondary metric, change exclusions after outcomes, weaken a comparator, conceal a failed trial,
or use case studies to choose the winning model.

`ADVANCE` requires the mechanism to be supported on its frozen predicted slice, matched control,
load-bearing ablation, aggregate floor, uncertainty unit, and efficiency evidence. A good aggregate
with a failed predicted slice does not establish the proposed mechanism.

## Failure-directed recovery

Diagnose in this order:

1. protocol and official-recipe parity;
2. data, labels, and independent-unit count;
3. numerical stability and optimization;
4. leakage or split mismatch;
5. slice-specific representation or inductive-bias failure;
6. uncertainty and whether the effect is below the noise floor;
7. mismatch between the task and intended claim.

`REVISE` permits one registered change to the same mechanism. `PIVOT` selects a different
registered candidate and requires a renewed protocol when it changes a frozen field. Two misses on
the candidate's predicted slice forbid another revision of that mechanism. They do not kill a
different registered candidate.

While measured headroom is open, budget remains, and an eligible registered alternative exists,
the route must pivot rather than stop. Legitimate route exits are measured closed headroom,
exhausted frozen budget surfaced as a human decision, or a newly verified lane-identical scoop.
Integrity anomalies and baseline mismatches require protocol repair, not optimization or a claim
that the research route is exhausted.

## Locked evaluation

Freeze the selected candidate before final evaluation. Use the same data, split, metric,
preprocessing, comparator versions, information access, seed aggregation, uncertainty unit, and
exclusion rules. Open the locked test no more than the frozen budget permits and only after explicit
authorization outside this workflow.

Report the strongest comparator, paired effect, interval, robustness, calibration, failure slices,
negative results, ablations, and training and inference cost. Use “SOTA candidate” until this exact
comparison supports a scoped claim. A failed final evaluation remains a failed final evaluation;
it is not development feedback for the same locked test.

## Resource lane

A benchmark or dataset contribution needs a consequential gap: missing measurement or context,
unpaired modalities or outcomes, unreliable or circular labels, leakage-prone evaluation, missing
independent validation, or unavailable actionability. Scale or aggregation alone is insufficient.
Compare against existing resources on coverage, reliability, licence, pairing, evaluation, and
field usefulness. Do not adopt a resource lane merely because a method missed its target.
