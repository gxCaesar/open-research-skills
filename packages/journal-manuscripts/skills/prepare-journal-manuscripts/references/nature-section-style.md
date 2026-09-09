# Nature-family writing by section

Use for Nature-family full-paper drafting, stylistic revision, abstracts or section
rewrites. Read the relevant sections below. Preserve article form and evidence; these
are editorial lessons, not a journal rule or a claim that every corpus paper received
the same depth of reading.

## Contents

- [Source basis](#source-basis)
- [Voice and sentence craft](#voice-and-sentence-craft)
- [Title](#title)
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Results and headings](#results-and-headings)
- [Methods](#methods)
- [Discussion and conclusion](#discussion-and-conclusion)
- [Legends and supplementary text](#legends-and-supplementary-text)
- [Full-paper editing pass](#full-paper-editing-pass)

## Source basis

Observations are paraphrased from supplied publisher PDFs. Pages are one-based file
pages; reopen the source before relying on a particular published detail.

| Source | Pages and section | Observed writing choice |
|---|---|---|
| [diaTracer](https://doi.org/10.1038/s41467-024-55448-8) | pp. 1–3; title, abstract, Introduction, first Results | Capability-and-data-type title; transformation and uses in the abstract without a numerical performance margin; a measurement advance narrowed to a computational compatibility problem |
| [TEN / JAK inhibition](https://doi.org/10.1038/s41586-024-08061-0) | p. 1, abstract; pp. 7–8, Discussion | Spatial measurement followed by pathway evidence, intervention and patient observation; Discussion reconnects findings to disease biology and future clinical testing |
| [HCC / TIMES](https://doi.org/10.1038/s41586-025-08668-x) | p. 6, Results; p. 12, Methods | Prediction leads to questions about biological interpretation and function; Methods separates cohort collection, preparation, processing, imaging and gene-set definitions |
| [CyLinter](https://doi.org/10.1038/s41592-024-02328-0) | pp. 4 and 10, Figs. 2 and 6 and adjacent Results | Cluster summaries are interpreted alongside marker profiles and images; an underclustered population remains explicit in the post-QC results |

These examples support different writing shapes, not copying claims, adjectives,
settings, protocols or citation policies. Published descriptions may contain errors or
ambiguities; the current project's underlying artifacts decide what is correct.

## Voice and sentence craft

Prefer concrete subjects: a measurement changes, a model estimates, a control
distinguishes, a cohort supports an inference. Use active voice for analytical choices
and interpretation; passive voice can emphasize a material or procedure. Do not
mechanically convert every Methods sentence.

Use past tense for completed procedures and observations, present tense for definitions
and what figures depict, and conditional language for proposed implications. Preserve
time and evidence status rather than imposing one tense on an entire section.

Introduce familiar information before a new term, then keep its referent stable.
Replace ambiguous pronouns with the measured object. Put contrasts and qualifications
close to the result they modify. Alternate short conclusions with the longer sentence
needed to explain a comparison; split stacked conditions when scope becomes unclear.

Remove ceremonial transitions, unused abbreviations, promotional adjectives and
repeated announcements of analysis. Retain a purpose clause when it explains a real
change of question. Do not impose banned-word lists or synonym quotas; precision may
require repeating the same term.

Original illustrative edits, only usable when the facts support them:

- Replace "Our innovative framework comprehensively captures spatial patterns" with
  "The model estimates how protein abundance changes across tissue compartments."
- Replace "We next performed another analysis" with the actual dependency, such as
  "The association did not establish whether the signal persisted across specimens."
- Replace "These results prove broad clinical utility" with the supported endpoint
  and population. Do not invent external validation to complete the sentence.

## Title

Use a capability title for a method, a bounded finding title for discovery, or a resource
title for a dataset. Identify the object and what the paper establishes. A method name
may help recognition but should not displace the contribution. A causal verb requires
evidence for that causal relationship.

Do not inherit a treatment or mechanism title from a paper with richer evidence.
Shorten background and unused acronyms, not the condition that makes the title true.
Title, abstract and main Results must refer to the same claim.

## Abstract

Use the abstract component for drafting and length checks. Choose the paper's answer
before arranging sentences. These emphases are prompts, not fixed sentence slots:

| Contribution | Foreground | Compress |
|---|---|---|
| Method/system | Capability gap, intelligible transformation, evaluation regime, supported capability or comparative result | Software inventory, peripheral datasets, low-level implementation |
| Discovery/mechanism | Biological unknown, discriminating measurement, finding, intervention or orthogonal support when available | Exploratory chronology and every pathway hit |
| Translational | Clinical question, cohort/measurement, outcome and actual validation/intervention design | Generic disease burden and claims beyond the evaluated population |
| Dataset/resource | Named coverage gap, newly enabled measurement, independent units and demonstrated use | Size alone and a catalogue of every field |

Open at the useful scale of the scientific problem. Give enough context for a reader
outside the immediate subfield, then reach the unknown promptly. Explain what the
approach does to the data or uncertainty. Select evidence that answers the question
and close on the implication it earns.

A capability description is not evidence that existing tools lack that capability.
For example, compatible output does not establish that other tools cannot consume the
input. Ground any prior-art limitation separately; otherwise describe the supported
task without inventing a universal gap.

The diaTracer abstract is an observed counterexample to a mandatory numeric-margin
sentence. Capability claims can be specific without that number. If the current claim
is comparative performance and magnitude matters, retain the effect, comparator and
regime. Sample counts alone are not performance evidence. Never manufacture a margin,
CI or significance to satisfy a pattern.

The TEN abstract illustrates an evidence progression, not a requirement that every
discovery include animals and patients. Keep predictions, associations, perturbations
and patient observations distinguishable. Scope can be conveyed by the named population
or design rather than a ritual final disclaimer. Retain any limit needed for truth.
Missing items in supplied notes are author-side questions, not an automatic list for
the final abstract. Include only boundaries material to the central claim; a
nonclinical capability abstract does not need an unrelated clinical or mechanistic
disclaimer.

After the facts are correct, make a separate compression pass. A sentence listing
resource coverage, controls, filtering, failures, profiles and software installation
may be entirely true but still unreadable. Separate the study design from the few
release features that explain its use; move the software check out unless usability
is the central claim. Close on the supported use, with its limiting condition where
needed. "Supports candidate follow-up" can delimit a localization result without
ending a nonclinical resource abstract with "not a mechanistic or clinical claim."

Define only abbreviations used again. Select numerical details; every retained value
must remain exact with its unit and scope. Omit secondary results during compression
only when their omission does not change the headline. Do not force every manuscript
number into the abstract or assign a fixed word budget per rhetorical function. Use
the exact target's current length, structure and citation rules.

## Introduction

Connect the scientific need to the precise unknown. Explain the closest approach's
relevant capability before its limitation. Place citations at the claims they support;
a bibliography list is not an explanation of the gap.

Narrow the question through what matters, what is understood, what remains unresolved
and why the proposed approach can address it. These jobs may share paragraphs. Avoid a
history of the whole field or claiming that no method performs a task when the real
limitation is a particular input, regime or assumption.

End with the answer-oriented objective, approach and brief evidence preview. Keep
detail that establishes the central idea; defer procedural settings to Methods. Do not
turn the ending into a second abstract or a mandatory three-item contribution list.

## Results and headings

Order blocks by inferential dependency. Supply the setup needed for interpretation,
report the observation, then draw the bounded inference. Use the detailed comparison
and transition guidance in `nature-paragraphs-and-legends.md` when needed.

A heading may state a finding if supported; otherwise name the precise question or
analytical task. Keep headings at comparable logical levels. Name the generalization
question a new dataset tests instead of merely numbering datasets, but do not disguise
an ordinary replication as a new mechanism.

Keep negative results and strongest baselines where they change interpretation. The
text identifies the inference, the graphic exposes the pattern, and the legend defines
the measurements. Do not recite every panel or plotted value, or add causal language to
make a descriptive result sound stronger.

## Methods

Organize by reconstructable operations and dependencies. State the material/input,
operation, choices affecting the quantity, and output. Match names to Results, figures
and code. Define objects and units before parameters; package/version lists alone do
not describe an analysis.

Where relevant, explain cohort provenance and eligibility, sampling hierarchy,
split/selection, acquisition, preprocessing, model/measurement, comparators, endpoint
and uncertainty. Give actual versions and parameters that affect reproduction; do not
import them from an exemplar or infer missing settings from library defaults.

Explain nonstandard choices when they affect interpretation. Reference standard
methods accurately and spell out modifications. Distinguish training-derived
preprocessing from its application to held-out samples, and fixed from tuned choices,
using the actual configuration. Describe randomization, blinding, exclusions,
sample-size reasoning and ethics when applicable and known; do not assume they occurred.

An unresolved field remains a specific author query. Methods states what was done
without promoting the method or concealing a deviation. The structure of the HCC
Methods is a useful example; its numerical settings are not recommended defaults.

## Discussion and conclusion

Interpret the central answer at a higher level than the last Results paragraph. Explain
what changes relative to prior understanding, what mechanism is supported and which
alternative remains possible. Do not repeat the abstract's dataset catalogue.

Make implications follow evidence. Distinguish demonstrated from proposed use and name
the condition under which extrapolation is reasonable. Discuss a limitation through its
consequence for interpretation and the evidence needed to resolve it. Avoid generic
lists asking for more data, models and future work.

Keep the positive contribution clear without unsupported superlatives or generic
caution. Finish on the strongest bounded scientific implication. Add a separate
Conclusion only when requested or appropriate to the article form.

## Legends and supplementary text

Use `nature-paragraphs-and-legends.md` for panel groups, nested n, processing and
statistical scope. Prefer a precise legend title, locally scoped panel descriptions
and shared definitions that genuinely apply. Main and supplementary material use the
same terminology, units and evidence verbs.

Supplementary Methods explain extensions without redefining the main protocol.
Supplementary Results state their question and relation to a main claim. Move material
by argumentative role, not because it is unfavorable or hard to explain. Keep the
control or limitation that changes a headline's meaning in the main argument.

## Full-paper editing pass

Check claim consistency from title through conclusion, then repair section and
paragraph order, then edit sentences, headings, captions and terminology. A requested
complete revision covers every supplied section; editing only the abstract and first
Results block does not complete the manuscript.

Use a compact working checklist of sections present and unresolved issues; no new
metadata contract is needed. Mark absent sections as absent. Report actual coverage
and remaining evidence needs. Writing quality checks do not certify scientific validity
or publisher acceptance.
