# Data and model cards

A card lets someone decide whether the artifact fits their question without asking you.
Its value is in the limits it states, not in the description it gives.

## The data card

**Provenance.** Where each part came from, with the accession, release or version and the
date obtained. A source named without a version is not reproducible.

**Composition.** How many units, of what kind, and the unit of independence. State the
counts per stratum that matter for the analysis, not only the total.

**Collection.** How the data was produced, by whom, and under what protocol. For human
subjects, the approval and the consent scope, including whether the consent covers
redistribution.

**Processing.** Every transformation between the source and the released files, with the
code that performed it. Filtering steps get their before and after counts.

**Splits.** How the partition was made, on what unit, and what prevents information from
crossing it.

**Known limitations.** Populations under-represented, measurement artefacts, label noise,
and the questions the data cannot answer. This section is the one readers use.

## The model card

**What it does.** The task, the input, the output and the intended use.

**Training.** Data, objective, hyperparameters, hardware, duration and seeds.

**Evaluation.** Metrics with their definitions, per-stratum results, uncertainty, and the
comparators with the budget each received.

**Failure modes.** Where it performs worst, which inputs it should not receive, and what
happens when it is given data outside its training distribution.

**Out-of-scope use.** Uses the evidence does not support. Write these as specifics; a
generic disclaimer transfers no information.

## Keep the cards honest

Negative results, abandoned variants and the strata where the method loses stay in. They
are what make the reported successes credible, and their absence is noticed.

Every number on a card traces to something in the package that shows how it was obtained.
