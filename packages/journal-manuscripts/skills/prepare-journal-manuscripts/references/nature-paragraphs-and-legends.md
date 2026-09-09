# Paragraphs and legends from inspected Nature-family examples

Use for Nature-family drafting or polish when paragraph logic, Results transitions,
figure legends, or evidence qualifications need work. These are conditional editorial
lessons from selected pages, not a publisher rule or proof that every supplied paper
was read equally deeply. PDF pages below are one-based file pages. Reopen the cited
page before reusing a paper-specific detail. Supplementary files not supplied were not
assessed. All descriptions below are paraphrases; do not transplant the papers' prose.

## Contents

- [Located observations](#located-observations)
- [From introduction to the first result](#from-introduction-to-the-first-result)
- [Build a comparison paragraph](#build-a-comparison-paragraph)
- [Make transitions resolve a dependency](#make-transitions-resolve-a-dependency)
- [Write legends from panel facts](#write-legends-from-panel-facts)
- [Polish without changing the scientific promise](#polish-without-changing-the-scientific-promise)

## Located observations

| Source | PDF location | Observed writing choice | Conditional lesson |
|---|---|---|---|
| [diaTracer](https://doi.org/10.1038/s41467-024-55448-8) | pp. 2–3; introduction end, workflow, first performance subsection | The introduction names the additional ion-mobility dimension as the compatibility problem. Results first explain the input-to-spectrum interface, then define data/library regimes before comparing outputs. | Make the gap an operational limitation; supply only the method interface needed to interpret the first comparison. |
| [diaTracer](https://doi.org/10.1038/s41467-024-55448-8) | p. 3; deep-proteome comparison and CSF subsection | The direct-DIA comparison reports DIA-NN identifying more proteins than FragPipe; hybrid-library and missingness results are described separately. The CSF comparison distinguishes per-file yield from total yield. | Keep favorable and unfavorable results under their actual information budgets and denominators. |
| [HCC / TIMES](https://doi.org/10.1038/s41586-025-08668-x) | p. 6; clinical-utility paragraph and SPON2 subsections | A 25-patient treatment-response observation is immediately qualified as preliminary. The subsequent text moves from predictive features to cell identity, spatial position, then perturbation and contact tests. | State what the current result leaves unresolved before introducing the next analysis; keep the validation limit beside the result it limits. |
| [HCC / TIMES](https://doi.org/10.1038/s41586-025-08668-x) | p. 6; NK–T-cell interaction subsection | The paragraph distinguishes computationally predicted signalling, spatial proximity, co-culture tests and a short-duration experiment without significant enhancement. | Preserve evidence verbs and the local negative result when compressing a mechanism narrative. |
| [TEN / JAK inhibition](https://doi.org/10.1038/s41586-024-08061-0) | p. 7, Fig. 5 legend; p. 8, Fig. 6 and Discussion | Fig. 5 assigns assay, animal-model, timing and statistical information to panel groups. Fig. 6 shows one patient's course; the Discussion separately discusses seven treated patients and the need for larger trials. | A displayed example, the treated series and confirmatory evidence have different scopes. |
| [CyLinter](https://doi.org/10.1038/s41592-024-02328-0) | p. 4, Fig. 2 legend | Cluster summaries are tied to raw tissue examples and cell galleries; the legend identifies normalization, channels and per-channel/per-image contrast adjustment in panel o. | Explain how to decode a display and disclose processing that affects its interpretation. |

## From introduction to the first result

Explain why the unresolved limitation changes the scientific analysis. Name the input,
measurement constraint, missing capability, or comparison that existing approaches
cannot resolve under the stated conditions. Then describe how the proposed approach
addresses that limitation and what evidence the manuscript will actually supply.

In diaTracer, the extra measurement dimension motivates an input-processing capability.
This is a useful pattern for a method with an interface limitation; it does not establish
a novelty claim for another method. Recheck the current project's competitors.

Decide whether the first Results block needs a short workflow explanation or can begin
with the decisive observation. Define unfamiliar objects before using them. Move
implementation detail to Methods when removing it does not alter interpretation of the
comparison. Avoid making every introduction end with the same enumerated contribution
list or announcing an unperformed experiment.

## Build a comparison paragraph

Use the existing scientific contract to recover the comparison regime, outcome and
qualification before rewriting. A useful order is the comparison being tested, the
evidence needed to judge it, and its bounded implication. Vary sentence order when the
reader already knows the setup; do not enforce a fixed number of sentences.

The diaTracer p. 3 direct-DIA example reports an average of 9,296 proteins per run for
FragPipe, 8,997 for Spectronaut and 9,520 for DIA-NN. Those are published example values,
not defaults or results to use in a new manuscript. It would be false to compress this
into a claim that FragPipe identified the most proteins among all three tools. Hybrid
library results answer a different comparison because extra DDA data are available.

For the current paper:

- Keep per-sample, pooled-total, precursor and protein outcomes distinct.
- Attach the figure/table reference to the claim it supports, not indiscriminately to
  a paragraph containing several different claims.
- Retain the strongest comparator and any exception that changes the conclusion.
- Describe a numerical difference without adding significance when uncertainty or the
  corresponding test was not supplied.
- State one useful inference rather than repeating all plotted values. Refer readers
  to the figure for secondary values that do not change the argument.

## Make transitions resolve a dependency

Before adding a transition, identify what the preceding evidence established and what
the next analysis can establish that it could not. For example, the HCC passage changes
the question from predictive association to cellular identity, then to spatial context
and functional dependence. Feature importance alone does not establish mechanism.

Choose the relation: motivation, contrast, alternative explanation, generalization or
boundary. Express that relation directly. A chronological connector does not explain
why the next experiment matters. Do not add the same purpose clause to every paragraph.

An original illustrative repair, not text from a published paper:

> The spatial association did not establish contact dependence. We therefore compared
> direct and separated co-cultures.

Use this only if the stated association and both culture conditions actually exist.
If the analysis is absent, describe the unanswered question rather than inventing the
transition. Preserve short-duration or context-specific null findings even when later
evidence supports a broader, qualified interpretation.

## Write legends from panel facts

Work from the figure, source-data record and analysis description together. The figure
shows the comparison; the legend lets the reader identify what was measured and how
the displayed quantity was obtained. Reuse existing records rather than creating a
parallel reporting manifest.

For each relevant panel or group, recover the specimen/cohort, condition and timing,
readout and units, what a point or line represents, independent n and nested sampling,
summary and interval, test/comparison/tails/correction if performed, and source location.
For images, recover channel identities, scale, ROI location, processing and how the
representative field was selected. A schematic legend instead defines objects and
arrows and identifies optional or proposed paths; statistical fields may not apply.

Group panel letters only when their statements really share scope. In TEN Fig. 5,
six biological replicates per condition and four fields per well are not 24 biological
replicates. Fifteen thickness measurements per mouse are not fifteen independent mice.
Preserve the actual experimental unit; do not infer its identity from the word
"biological" alone when the study records leave it unclear.

Keep shared definitions together and state panel-specific exceptions locally. Do not
copy a one-tailed test, summary convention or caption phrase merely because a published
paper uses it. Describe the frozen analysis actually run. If n, normalization, adjustment
or field-selection details are missing, identify the missing fact for the author.

Read the legend once against the figure with Results hidden, then read Results against
both. Repair contradictory labels, denominators or claims. A unit that appears wrong in
an exemplar should be checked against the actual assay and scale calibration, not copied.

## Polish without changing the scientific promise

Preserve the observation–interpretation–implication distinction through title, abstract,
Results and Discussion. A patient course illustrates timing; an uncontrolled series
cannot supply a randomized treatment effect. A useful Discussion connects the supported
finding to its implications and names the evidence still needed for a stronger claim.

Improve cadence after repairing logical order: remove repeated setup, vary overloaded
purpose clauses, use concrete subjects and keep qualifiers close to the claims they
limit. Do not imitate promotional wording from accepted papers. Check the revised
paragraph against its supporting result and strongest exception; fluency does not
justify changing numbers, causal verbs or citation scope.
