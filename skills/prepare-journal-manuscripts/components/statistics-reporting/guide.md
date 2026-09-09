# Statistical-reporting component

Make the design, analysis unit, comparison, estimate, uncertainty, and limitation visible.
This is a reporting and bounded audit component. Do not claim that an analysis is correct
without the protocol and required data.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## Select the mode and authority

Choose `audit`, `draft`, `revise`, `figure alignment`, `reviewer response`, or explicitly
requested `data-backed reanalysis`. Record the supplied Methods, Results, legends,
tables, protocol, analysis plan, reviewer comments, and data boundary.

Read `references/source-basis.md` when a venue or reporting guideline matters. Current
target-journal and study-type instructions override generic guidance. If essential
design facts are missing, use `AUTHOR_INPUT_NEEDED`; never invent a test, sample size,
p value, interval, correction, exclusion, randomization, blinding, software, or version.

## Build the design before choosing wording

Read `references/design-and-units.md`. For every claim-bearing analysis, record:

- endpoint, groups, treatments, time points, and comparison;
- independent experimental unit and full sampling hierarchy;
- biological versus technical replicates, repeated measures, pairs, blocks, batches,
  sites, donors, patients, animals, cultures, simulations, or model runs;
- independent-unit counts for every compared group, total units included, units skipped,
  and the reason for every skip;
- inclusion/exclusion timing, missing-data handling, randomization, and blinding when
  applicable;
- transformation, normalization, model or test, assumptions, and diagnostics;
- comparison family, multiplicity strategy, effect estimate, uncertainty, and p-value
  policy;
- for stochastic computation, seed role, paired aggregation, checkpoint and early-
  stopping rules, comparison budget, and selection rule.

Start from `examples/analysis-register.example.json`. Replace every synthetic field with
observed manuscript or protocol facts and run:

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" analysis-register.json \
  --mode working
```

The validator checks completeness and cross-field logic. It does not select a method,
read raw data, or establish that the recorded analysis is valid.

## Audit the inferential chain

Map each claim to the exact comparison and analysis. Check:

1. whether `n` counts independent units rather than cells, fields, technical readings,
   spectra, repeated measurements, or seeds;
2. whether paired, repeated, clustered, longitudinal, blocked, or nested dependence is
   modeled or aggregated appropriately;
3. whether every fold or evaluation slice is not only disjoint but scorable for the
   claimed metric;
4. whether the comparison family and correction or prespecified limited-comparison
   rationale are explicit;
5. whether an interaction is tested directly rather than inferred from “significant”
   versus “not significant”;
6. whether effect size and uncertainty carry the conclusion instead of a threshold or
   star alone;
7. whether exclusions, missing units, and model-selection decisions could change the
   claim;
8. whether computational methods are compared on paired runs and equal budgets where
   pairing is possible.

Read `references/failure-modes.md` for specific risk patterns. If a potential issue
cannot be settled from supplied material, state the concern and cheapest required check;
do not accuse the authors or silently choose an analysis.

## Align Methods, Results, and figures

Read `references/reporting-and-figures.md`. Each reported aggregate gives its own
denominator and skipped count. Define what points and error bars represent, panel-
specific `n`, plot conventions, tests/models, pairing, correction, and exact p-value
policy. Ensure the same number, unit, interval type, and analysis name appear in Methods,
Results, legends, tables, and source-data notes.

Revise prose only inside the evidence boundary. Statistical association is not mechanism
or causality; absence of statistical significance is not evidence of equivalence. Keep
negative, imprecise, or unstable results visible.

## Prioritize and return

Use:

- `P0`: observed unit/design/analysis defect that can invalidate a central claim;
- `P1`: likely review-impacting reporting or interpretation gap;
- `P2`: local clarity or consistency issue.

Do not assign P0 from a guess. Unless the user asks for another format, return:

```text
Statistics review scope
- Materials observed:
- Not assessed:
- Independent unit and hierarchy:

Findings
- [P0/P1/P2] Location; observed issue; impact; smallest fix; verification.

Ready-to-paste revision
[Only evidence-supported text, or “Not requested”]

AUTHOR_INPUT_NEEDED
- [short factual fields only]

Validator result and residual risk
- [command/result; what it cannot establish]
```

Before final delivery, run the register in `--mode final`. A pass establishes only that
the record is complete under this local contract. Medical, regulatory, confirmatory
trial, or high-stakes causal decisions require the applicable protocol and qualified
statistical leadership.
