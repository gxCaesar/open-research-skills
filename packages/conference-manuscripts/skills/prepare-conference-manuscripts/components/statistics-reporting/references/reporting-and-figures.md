# Statistical reporting and figures

## Methods record

For each major analysis report endpoint, independent unit, hierarchy, inclusion and
exclusion, missing-data handling, transformation, model or test, paired/repeated status,
assumptions or diagnostics, comparison family, multiplicity strategy, effect and
uncertainty convention, p-value policy, software, and version when known.

Do not write “data were normally distributed” without a basis. Do not fill a generic
test-name skeleton before the design is known.

## Results wording

Prefer the factual order:

```text
comparison -> effect estimate and unit -> uncertainty -> exact test/model result
-> bounded interpretation
```

Avoid `proved`, `confirmed the mechanism`, `highly significant`, or `no effect` when the
design supports only association, an imprecise estimate, or failure to reject a null.
Equivalence or non-inferiority requires its own design and margin.

## Quantitative figures

For each panel or panel group define:

- what every point, line, bar, box, violin, band, or error bar represents;
- the exact independent `n` and any technical subsamples;
- mean/median and SD, SEM, interval, IQR, range, or model-estimate convention;
- model or test, pairing/repeated status, comparison family, and correction;
- exact p values or fully defined thresholds;
- source data containing independent values, skip counts, and exclusions where allowed.

Box plots need median, quartiles, whisker, and outlier rules. Heat maps need scaling,
normalization, clustering, feature selection, and multiplicity. Regression plots need
the coefficient or estimand, uncertainty, point independence, and whether the fit is
descriptive or inferential.

Visual overlap of error bars is not itself a test, and star annotations must not carry
the whole conclusion.
