# Nature-family exemplar calibration

Use this reference only when an author asks to calibrate a draft against published
Nature-family examples. It is a source-located sample of article shapes, not a style
template and not a substitute for the target journal's current instructions.

## Read the evidence labels literally

- **Observed in the sampled papers** means that the stated sequence was inspected in
  the supplied publisher PDF at the locator shown.
- **Editorial heuristic** means a drafting choice inferred from those observations. It
  is conditional on the manuscript's own evidence and may be rejected.
- **Official requirement** means a current rule from the exact journal and article
  type. No observation in this reference establishes one; verify it in `recon` mode.

The calibration corpus contained 51 publisher PDFs: 42 Articles, one Brief
Communication, five Comments, one News feature, one Editorial, and one source-limited
page. It was concentrated in Nature Methods (23 PDFs) and Nature Communications (16),
with three Nature papers and nine papers from other Nature-family titles. Treat every
frequency as sample-specific. Supplementary items cited by an article but absent from
the supplied PDF were not assessed.

Use the locator form `DOI | PDF page | display or section | observed role`. PDF page is
the one-based page index in the inspected file, not the printed folio. Re-open the
source before relying on a locator in a new project.

## Source-located precedent index

Every empirical example used below has one canonical record here. Page ranges are
one-based indices in the inspected PDF.

| ID | Shape | DOI | PDF pages | Locator | Observed role |
|---|---|---|---|---|---|
| `form-deepprep` | publication-form | [10.1038/s41592-025-02599-1](https://doi.org/10.1038/s41592-025-02599-1) | 1-3 | section structure; Figs. 1-2 | Brief Communication compresses workflow and performance into two main figures |
| `method-cylinter` | computational-method | [10.1038/s41592-024-02328-0](https://doi.org/10.1038/s41592-024-02328-0) | 2-10; 17-24 | Figs. 1-6; ED Figs. 1-6 | artifacts, pre-QC distortion, removal, two post-QC datasets, and expanded diagnostics |
| `method-diatracer` | computational-method | [10.1038/s41467-024-55448-8](https://doi.org/10.1038/s41467-024-55448-8) | 1-14 | section structure; Figs. 1-7 | workflow followed by task and sample-regime tests; no ED caption block visible |
| `discovery-aging` | discovery-mechanism | [10.1038/s43587-025-00823-3](https://doi.org/10.1038/s43587-025-00823-3) | 3-13; 25-38 | Figs. 1-8; ED Figs. 1-10 | localization, proteome, pathway, perturbation, in-vivo evidence, and molecular model |
| `discovery-contact` | discovery-mechanism | [10.1038/s41467-025-57405-5](https://doi.org/10.1038/s41467-025-57405-5) | 1-23 | section structure; Figs. 1-8 | screen, complex, localization, metabolic dependency, in-vivo test, and proposed model; no ED caption block visible |
| `translational-ten` | translational | [10.1038/s41586-024-08061-0](https://doi.org/10.1038/s41586-024-08061-0) | 1-10; 15-30 | section headings; Figs. 1-6; ED Figs. 1-10 | cohort, pathway, preclinical inhibition, patient observation, and no standalone Results heading |
| `translational-hcc` | translational | [10.1038/s41586-025-08668-x](https://doi.org/10.1038/s41586-025-08668-x) | 1-14; 21-39 | section headings; Figs. 1-5; ED Figs. 1-10 | spatial association, score, interpretation, mouse perturbation, and no standalone Results heading |
| `sections-cell-discovery` | section-counterexample | [10.1038/s41421-024-00764-y](https://doi.org/10.1038/s41421-024-00764-y) | 1-15 | section headings; Figs. 1-7 | explicit Introduction, Results, Discussion, and Materials and Methods headings |

## Separate publication form from contribution shape

Classify `publication_form` before choosing a narrative pattern: `Article`, `Brief
Communication`, `Comment`, `News/Editorial`, or `source-limited`. Classify the scientific
contribution separately. An Article may be a method, discovery, or translational study;
a Comment about a method is not a method Article.

Only a complete research Article should default to a question-to-evidence Results arc.
The `form-deepprep` Brief Communication used two main figures for a compressed workflow
and performance argument. Do not use non-research forms such as Comments, News
features, or Editorials to infer the evidence structure of a research Article.

If a file identifier conflicts with its PDF metadata or the source does not contain a
complete article, classify it as `source-limited`; do not count its sections, displays,
or apparent absence of evidence.

## Conditional Article shapes

The sequences below describe argumentative jobs, not mandatory section names or figure
counts.

### Computational method or analysis system

**Observed in the sampled papers:** in `method-cylinter` and `method-diatracer`, the arc
made the failure or workflow interface visible, tested the system on task-matched
comparisons, and then moved to distinct datasets, conditions, or downstream uses.

- `method-cylinter`: recurring imaging artifacts -> pre-QC distortion -> removal
  procedure -> post-QC results in two datasets, with expanded diagnostics in ED.
- `method-diatracer`: workflow -> performance under several proteomics tasks and sample
  regimes.

**Editorial heuristic:** organize Results by the scientific or analytical question that
each comparison resolves. Do not write a module inventory. Put the simplest decisive
comparison before broader applications, and let each new setting test a named limit or
capability rather than merely add another dataset.

### Biological discovery or mechanism

**Observed in the sampled papers:** in `discovery-aging` and `discovery-contact`, the arc
moved from measurement and localization to a candidate mechanism, then to perturbational
or orthogonal validation and a closing mechanistic model.

- `discovery-aging`: proximity labelling -> subcellular proteome -> pathway and lipid
  evidence -> mTOR evidence -> human iPSC and in-vivo perturbation -> molecular model.
- `discovery-contact`: discovery screen -> protein complex and localization -> altered
  metabolism -> transfer requirement -> sensitization -> in-vivo test -> proposed model.

**Editorial heuristic:** keep localization, association, necessity, sufficiency, and
mechanism distinct. A proposed model may synthesize the chain but cannot supply a missing
perturbation or convert association into mechanism.

### Translational prediction or intervention

**Observed in the sampled papers:** in `translational-ten` and `translational-hcc`, the
arc began with a cohort and measurement contract, identified a clinically relevant state
or score, and then added functional, animal, or patient-level evidence commensurate with
the title claim.

- `translational-ten`: cohort and cell-resolved proteomics -> disease-state comparison
  -> JAK/STAT activation -> in-vitro and in-vivo inhibition -> patient observations.
- `translational-hcc`: spatial immune mapping -> score construction and validation ->
  biological interpretation and perturbational support.

**Editorial heuristic:** calibrate the title and abstract verb to the strongest completed
evidence. Prediction, association, mechanism, and treatment are different promises. A
model name is secondary when the load-bearing result is a disease state, endpoint, or
intervention.

## Build a figure-argument map before drafting Results

For complete worked examples, read [whole-paper argument cases](whole-paper-argument-cases.md).
They trace a method, a discovery/translation Article and a publisher-labelled Resource
from abstract promises through figures to Discussion, including why adjacent Results
blocks cannot always be exchanged.

For every main Results block, record:

| Field | Question to answer |
|---|---|
| Section question | What uncertainty is resolved here? |
| Display locator | Which main, Extended Data, Supplementary, table, or source-data item carries the evidence? |
| Comparison or observation | What was actually measured, against what, and at which independent unit? |
| Justified claim | What is supported without strengthening causality or scope? |
| Next dependency | What remains unresolved and motivates the next block? |
| Placement reason | Why must this evidence be main, or why is support outside main safe? |

Use the map to order evidence, not to force one paragraph per figure. A headline claim,
its decisive control, and any qualifier that changes its meaning stay in the main
argument. Robustness, calibration, additional cases, and diagnostics may sit in Extended
Data or Supplementary material when the article form permits and the main claim remains
honest without them.

## Counterexamples and stopping rules

- `translational-ten` and `translational-hcc` did not expose a standalone `Results`
  heading, while `sections-cell-discovery` did. These located counterexamples are enough
  to reject a publisher-family heading rule; they do not estimate either format's
  frequency.
- `method-cylinter` and `discovery-aging` visibly include ED, while the complete supplied
  PDFs for `method-diatracer` and `discovery-contact` do not expose an ED caption block.
  This bounded contrast rejects a universal packaging rule; it is not proof that other
  supplementary material does not exist.
- A Fig. 1 workflow is useful only when understanding the system or acquisition is the
  first unresolved question. A discovery paper may open with the biological landscape.
- A Discussion should name a source-anchored applicability boundary, alternative
  explanation, or missing validation. Generic future-work language does not repair an
  unsupported claim.

If the manuscript's article form, evidence type, or claim strength does not match these
examples, stop using the pattern. Return to the locked scientific contract and the exact
journal's current Official requirement.
