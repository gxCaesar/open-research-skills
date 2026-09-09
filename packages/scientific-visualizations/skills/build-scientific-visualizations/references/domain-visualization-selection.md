# Domain-aware visualization selection

Choose a display from the scientific question, data shape, comparison, and independent unit. A
familiar chart is not self-justifying. The table entries below are conditional families, not fixed
templates or substitutes for the analysis protocol.

For source-located worked examples in single-cell perturbation, genomics, protein
design and clinical resources, read `cross-domain-figure-cases.md`. Use its observed
figure relationships and explicit transfer limits, not published colours as templates.

## Contents

- [Cross-domain decision rule](#cross-domain-decision-rule)
- [Spatial omics and proteomics](#spatial-omics-and-proteomics)
- [Single-cell and virtual-cell systems](#single-cell-and-virtual-cell-systems)
- [Genomics and regulation](#genomics-and-regulation)
- [Molecular and structural research](#molecular-and-structural-research)
- [Clinical and translational studies](#clinical-and-translational-studies)
- [Machine-learning evaluation](#machine-learning-evaluation)
- [Displays that need a second line of evidence](#displays-that-need-a-second-line-of-evidence)

## Cross-domain decision rule

Before selecting a plot, write:

```text
scientific question + comparison + data shape + independent unit
    -> display family
    -> must-show context
    -> source-data obligation
    -> misleading alternative to avoid
```

Repeated cells, tiles, spectra, frames, time points, prompts, or random seeds do not become new
independent biological samples by being numerous. Show uncertainty over the actual experimental or
sampling unit. When a panel displays a descriptive unit and inference uses another unit, state both.

Pair an overview with the quantitative evidence needed to test it. An embedding, tissue map,
structure view, pathway diagram, or model schematic can orient the reader, but it rarely establishes
an effect alone.

## Spatial omics and proteomics

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| Where is a signal located in tissue? Whole-slide image plus selected fields | Tissue overview with bounded ROI boxes, linked ROI enlargements, channel-resolved or composite image | Tissue-to-ROI relation, physical scale, channel key, orientation, specimen identity, acquisition and crop boundary | Source image or controlled pointer; acquisition, channels, LUT, crop, processing and ROI coordinates | Detached attractive crop with no location or scale |
| Does abundance differ across compartments? Per-cell or per-ROI values nested in specimens | Distribution plus specimen-level paired points or specimen summaries; aligned tissue context when location matters | Compartment definition, specimen as independent unit, cells or ROIs per specimen, normalization, pairing | Tidy values with specimen, compartment, condition, value, unit, inclusion flag and transformation | Bar of all cells treated as independent replicates |
| Is there a spatial gradient or domain boundary? Coordinates with continuous or categorical signal | Tissue map plus distance-to-boundary profile or specimen-level effect; uncertainty outside the map | Coordinate system, segmentation/domain method, distance definition, null or permutation reference | Coordinates or repository object, domain labels, distance calculation, specimen ID, null construction | Smooth colour field without a quantitative validation or scale |
| Are cell types or proteins spatially associated? Neighbour graph or proximity scores | Local spatial view plus per-specimen effect, matched random/null comparator, sensitivity to radius | Neighbour definition, radius, edge direction, abundance control, specimen unit, null model | Node/edge or summarized proximity data, filtering, null draws, per-specimen estimate | Network hairball whose edge count merely follows abundance |
| Is a pathway supported? Protein or gene set scores | Ordered effect plot, compact heat map with raw direction, or enrichment display tied to measured proteins | Measured features, background universe, score direction, multiple-testing scope, specimen unit | Feature values, pathway membership/version, scoring rule, background, adjusted values | Pathway bubble plot with no universe or measured-feature trace |
| Does an intervention change the spatial phenotype? Matched specimens or regions | Paired specimen points, longitudinal profile, effect with interval, aligned pre/post images when registered | Assignment, time, pairing, specimen unit, registration, blinded outcome definition | Individual-unit outcomes, condition/time, exclusions, estimator, interval, registered image metadata | Representative before/after image without unit-level outcome |

Use consistent channel colours only when acquisition and interpretation support comparison. Never add
synthetic cell boundaries, spots, or intensities to a measurement image. Analytical overlays remain
separate layers with their derivation recorded.

## Single-cell and virtual-cell systems

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| What populations are present? High-dimensional cells nested in donors | Embedding for orientation plus marker dot/heat map and donor-aware abundance summary | Donor/sample counts, batch and condition, annotation method, cell versus donor role | Cell annotation table or repository object, donor mapping, markers, embedding coordinates, filters | Embedding alone presented as quantitative separation evidence |
| Does a cell state change by condition? Cells nested in donors or cultures | Donor-level paired distribution, pseudobulk effect, or hierarchical summary; embedding only as context | Independent unit, cell counts per unit, covariates, composition versus state distinction | Cell values and unit map, aggregation rule, model estimate and interval | Violin plot pooling cells across donors with cell-level significance |
| Is a trajectory or transition supported? Ordered or time-resolved observations | Trajectory map plus direction evidence, time/lineage validation and uncertainty | Root choice, direction source, branch support, sampling time, donor unit | Coordinates, ordering scores, branch assignments, time or lineage anchor | Arrow painted on an embedding without directional evidence |
| Does a perturbation model predict response? Cell profiles, perturbations and held-out units | Observed-versus-predicted per unit, effect recovery, calibration and failure slices; qualitative embedding second | Exact split, perturbation and cell-type novelty, donor leakage guard, metric direction, baseline recipe | Predictions and targets per evaluation unit, mask/split, metric inputs, exclusions | Cherry-picked target genes or an embedding with no paired metric |
| Does a virtual-cell model generalize? Multiple tasks and biological contexts | Benchmark matrix plus per-context paired differences, calibration, compute-quality trade-off | Train/development/test roles, context identity, frozen metric, strongest reproducible baseline | Per-unit scores, configuration, split identity, failed runs, uncertainty aggregation | Mean rank without task direction, missing runs, or unit-level differences |

Distinguish a biological independent unit from repeated cells and a computational evaluation unit
from repeated seeds. Seeds quantify algorithmic variability; they do not increase donor count.

## Genomics and regulation

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| What happens at a locus? Genomic tracks across conditions or alleles | Aligned locus tracks, variant annotation and compact effect panel | Genome build, chromosome range, strand, allele, track normalization, sample/replicate unit | Coordinates, build, track values or repository accession, normalization and sample mapping | Cropped track without coordinates, scale, or matched condition |
| Does accessibility or binding change? Peaks/motifs across replicates | Replicate-aware effect plot, aggregate profile with interval, motif logo only when sequence basis is defined | Peak universe, background, motif version, strand, replicate unit, multiple testing | Peak or motif table, counts, background, model/normalization, adjusted values | Volcano plot with no universe or replicate structure |
| Is long-range contact altered? Matrix or loop calls | Contact map with common scale plus loop-level or distance-stratified quantitative comparison | Resolution, normalization, genomic distance, calling rule, replicate unit | Contact matrix/repository, bins, normalization, loop table, sample identity | Two heat maps with independently autoscaled colours |
| Is an allele-specific effect present? Paired allelic counts | Allelic-balance plot with coverage and interval; locus context | Phasing, reference-bias handling, minimum coverage, individual as unit | Ref/alt counts, phase, filters, estimate and interval | Ratio without depth, uncertainty, or bias control |
| Does a regulatory model predict function? Variant or sequence predictions | Calibration, per-locus paired error, effect-direction recovery, assay validation where available | Training overlap, genome split, assay target, metric, measured versus predicted status | Predictions/targets, locus IDs, split, assay data, baseline and uncertainty | Saliency heat map treated as experimental mechanism |

Never infer causality from a motif match, accessibility association, contact map, or attribution alone.
Use direct labels to distinguish measured tracks, computed scores, and proposed regulatory links.

## Molecular and structural research

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| Where is a residue, ligand or interface? Experimental or predicted structure | Source-derived structure overview plus focused contact view and sequence/residue mapping | Structure accession or model status, chain, residue numbering, confidence/resolution, representation | Structure file or repository accession, rendering commands, selections, colours and model status | Generated molecular-looking image with no exact coordinate source |
| Does binding or activity differ? Matched molecules or perturbations | Individual assay values, concentration-response curve, matched-pair effect or property landscape | Assay type, units, replicate hierarchy, censoring/detection limits, fit model | Compound IDs/structures, concentrations, responses, replicate map, fit and uncertainty | Decorative docking pose used as affinity evidence |
| Which contacts support a mechanism? Atom/residue interactions | Contact map plus source-derived local structure; mutational/experimental evidence when claimed | Distance rule, protonation/model assumptions, residue mapping, measured versus predicted contact | Coordinates, contact calculation, mapping, validation data and exclusions | Dense contact cartoon that hides unsupported or uncertain edges |
| How does a generator explore chemical space? Molecules and properties | Property/activity landscape, novelty/diversity distributions, scaffold or matched-pair analysis, failure examples | Reference set, validity rule, duplicate handling, property source, held-out evaluation | Generated structures, canonical identifiers, validity filters, property computations, baseline | Hand-picked attractive molecules without population statistics |
| Is a molecular prediction calibrated? Per-compound predictions and assays | Observed-predicted plot, calibration, ranked retrieval or error slices chosen by the task | Split/scaffold policy, assay unit, censored values, metric direction, baseline | Per-compound predictions/targets, split, metric inputs, uncertainty | Correlation alone when ranking or absolute error drives use |

Chemical structures, protein coordinates, docking poses and residue geometry are scientific data
products. Render them from exact source files or domain software, never from generative illustration.

## Clinical and translational studies

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| How did patients enter analysis? Cohort filtering and split | Participant flow plus explicit cohort/split counts | Eligibility, exclusions with reasons, temporal/site split, final denominators | Count table with reasons and split assignments; no direct identifiers | Flow diagram whose totals do not reconcile |
| How does an endpoint evolve? Longitudinal repeated measures | Patient-level trajectories, paired changes, model-estimated curve with interval | Time origin, visit windows, missingness, intervention, patient as unit | De-identified patient/time/outcome table, inclusion, estimator and interval | Mean curve with no individual variability or missingness |
| Does time-to-event differ? Censored outcomes | Kaplan-Meier with at-risk table or model-based survival estimates | Endpoint, time origin, censoring, numbers at risk, patient unit, interval | Time, event indicator, group, inclusion and analysis specification | Survival curve without at-risk counts or censoring definition |
| Does a diagnostic model discriminate? Scores and binary/multiclass outcome | ROC or precision-recall chosen from use case, threshold table, paired external validation | Prevalence, split/site role, threshold selection, confidence interval, patient unit | Patient-level score/outcome, split, threshold policy, estimator | ROC alone for a low-prevalence use case where precision matters |
| Are predicted probabilities reliable? Risk estimates | Calibration curve, distribution by outcome, decision curve when utility is defined | Calibration sample, time horizon, recalibration, uncertainty, clinical utility assumptions | Patient-level prediction/outcome, bins or smoother, estimator, utility parameters | Accuracy or AUC presented as calibration evidence |
| Is an effect consistent across subgroups? Estimates with intervals | Forest plot with prespecified groups and interaction estimates | Group definitions, counts, reference, multiplicity, interaction rather than within-group P values | Estimates, intervals, group counts, model specification and exclusions | Separate significance stars interpreted as subgroup difference |

Reviewer-safe files use opaque IDs or justified aggregation. A controlled-access pointer states the
request route and conditions without copying protected records or private locations.

## Machine-learning evaluation

| Question and data shape | Preferred display families | Must-show context | Source-data obligation | Misleading alternative |
|---|---|---|---|---|
| Does the method beat a baseline on matched units? Paired task/sample scores | Paired differences, per-task matrix, interval over independent units | Exact split, metric direction, paired unit, baseline recipe, failed/missing runs | Per-unit method and baseline scores, config labels, inclusion, aggregation | Bars of means with no paired units or uncertainty |
| Which component matters? Registered ablations | Ablation matrix or coefficient/effect plot with uncertainty | Full model, one change per ablation, fixed protocol, seeds versus data units | Run-level scores, configs, selection rule, failures, aggregation | Removing several components at once and assigning cause |
| Is confidence meaningful? Probabilities or uncertainty estimates | Reliability diagram, coverage-risk curve, error by confidence | Calibration set, bins/smoother, target coverage, shift context | Predictions, outcomes, uncertainty, split, calibration procedure | Confidence histogram without correctness or coverage |
| Where does the model fail? Prespecified slices | Slice matrix, paired errors, representative examples linked to population counts | Slice definition frozen before result inspection, denominator, baseline, uncertainty | Per-unit slice labels, predictions, outcomes, inclusion, metric | Hand-picked failures with no prevalence or comparison |
| What is the compute-quality trade-off? Runs across resource levels | Pareto plot with resource axis and quality interval | Hardware/precision, train versus inference cost, batch, stopping rule | Quality, runtime/resource measurement, config, repeated-run policy | Parameter count used as a proxy for all compute |
| Does a representation add headroom? Baseline/oracle comparisons | Matched baseline ladder, attainable bound and noise-floor view | Same task and split, strongest representation, recipe parity, independent unit | Per-unit predictions/scores, baseline definitions, oracle construction, noise estimate | Architecture comparison before measuring data/representation headroom |

Use a heat map only when the matrix itself is the evidence and its colour scale, missing cells, metric
direction and labels remain readable. Report failed runs rather than turning them into blank cells
that look like neutral performance.

## Displays that need a second line of evidence

- An embedding needs a non-embedding quantitative validation for separation, change, or prediction.
- A volcano plot needs the tested universe, effect definition, replicate unit, and multiplicity scope.
- A bar chart needs individual units or a justified summary and uncertainty.
- A ROC curve needs prevalence and operating-point context; precision-recall may be more informative.
- A pathway bubble plot needs the measured features, background universe, score direction, and version.
- A heat map needs a shared, interpretable scale and explicit handling of missing values.
- A schematic mechanism needs direct evidence labels and cannot substitute for perturbational support.
- A representative image needs specimen-level context and a quantitative population summary when the
  claim is general.

If the required second line of evidence does not exist, narrow the visual claim. Do not compensate
with denser annotation, stronger colour, or a more elaborate mechanism drawing.
