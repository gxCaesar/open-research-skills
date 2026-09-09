# Exemplar-corpus calibration

Use this reference in `survey` mode when a directory or collection of papers is being
studied to improve manuscript or figure decisions. The output is a reproducible map of
sampled publication practice. It is not a literature review, a popularity count, a
publisher policy, or permission to copy source material.

## 1. Freeze the calibration question and denominator

State what the corpus is meant to calibrate: article shape, Results logic, figure
sequence, panel composition, caption burden, main-versus-supplement placement, or
another named decision. Define inclusion and exclusion criteria before interpreting
the papers.

Build a corpus census covering every supplied input. Record:

| Field | Required content |
|---|---|
| Source identity | DOI or other stable identifier, title, journal, year, and local source ID |
| `publication_form` | Article, Brief Communication, Review, Comment, News/Editorial, or unresolved |
| Contribution shape | method, discovery, resource, clinical/translational, review, or another justified class |
| Source completeness | complete, partial, supplement unavailable, metadata-only, internally inconsistent, or unreadable |
| Coverage | readable pages, main displays, Extended Data, Supplementary, tables, and source-data visibility |
| Validation | parse status, visual-render status, locator mode, and exact anomaly |
| Disposition | eligible for pattern inference, framing-only, counterexample, duplicate/version, or excluded |

Keep the source path in the author workspace; use a portable source ID in any transferable
matrix. A filename is not bibliographic authority. If filename, embedded metadata,
visible title, DOI, page continuity, or article completeness conflict, classify the
source as `source-limited` and exclude it from pattern counts until resolved.

Report the full input denominator, the eligible denominator, exclusions by reason, and
missing supplementary coverage. `Not visible in the supplied PDF` is not evidence that
an item does not exist.

## 2. Stratify on independent axes

Do not let journal, publication form, and scientific contribution collapse into one
label. Stratify at least by:

- journal and article type or publication form;
- contribution shape and evidence strength;
- date range and scientific domain when they could alter practice;
- source coverage, especially whether Extended Data or Supplementary files are visible.

A methods-heavy special issue cannot estimate all Nature-family practice. An Article
about a computational method and a Comment about methods serve different jobs. Record
small or empty strata rather than pooling them into a convenient generalization.

## 3. Combine full-corpus census with stratified deep reading

Run a shallow structural pass over every eligible source: metadata, headings, display
captions, page locators, visible supplementary classes, and parse anomalies. Treat
automatic panel-letter counts and layout extraction as triage until the rendered page is
inspected.

Choose deep-reading cases from a rule fixed before judging their aesthetics:

- at least one representative from each decision-relevant stratum;
- competing evidence shapes, not only the most attractive examples;
- sparse and dense displays when visual density is being studied;
- at least one counterexample to every proposed general rule;
- every source anomaly that could change the denominator or locator reliability.

Record why each paper was selected. Stop when the preregistered strata and
counterexample checks are covered, the source budget is exhausted, or new papers add no
new role relevant to the calibration question. Do not keep sampling until a preferred
pattern appears dominant.

Use the single-paper component for load-bearing reconstruction. Text extraction can
locate candidates; rendered-page inspection establishes layout, panel hierarchy,
caption continuation, and image-versus-schematic boundaries.

## 4. Build a cross-paper evidence matrix

Each row supports one narrowly phrased observation:

| Field | Required content |
|---|---|
| Source | DOI and portable source ID |
| Stratum | journal, `publication_form`, contribution shape, and coverage state |
| Locator | one-based PDF page plus Figure, Extended Data, table, or section |
| Observed role | what the section or display actually does in the argument |
| Proposed pattern | the cross-paper claim this row supports or challenges |
| Quality basis | legibility, claim fit, comparison completeness, or another explicit criterion |
| Counterevidence | counterexample, divergent implementation, or unavailable evidence |
| Confidence | verified, partial, or not assessable, with reason |

Use `PDF page` only for a page-grounded source. For HTML or incomplete sources, use the
reliable structural locator and mark absent page indices `not assessable`.

## 5. Separate observation, judgement, and policy

Every synthesis statement receives exactly one evidence class:

- **Observed pattern:** what occurred in the eligible sampled papers, with denominator
  and source locators.
- **Editorial judgement:** why a pattern is useful or harmful for a particular claim and
  evidence shape. State the quality criterion and the counterexample.
- **Official requirement:** a current rule verified from the exact journal and article
  type's first-party instructions. Published examples do not establish it.

Frequency is not quality. Acceptance does not make every design choice exemplary. A
single striking paper may demonstrate that an alternative is possible, but it cannot
establish a dominant pattern. Keep `not assessed`, `UNVERIFIED`, and source-coverage
limitations visible.

## 6. Transfer only bounded decisions

Create one transfer card per pattern that could change another skill's output:

| Field | Required content |
|---|---|
| Target | manuscript drafting, title/abstract, figure set, compound figure, or another named capability |
| Pattern and use condition | the narrow action and the article/evidence shapes for which it applies |
| Evidence | at least two independent source locators when claiming a recurring pattern |
| Counterexample | a source or condition that defeats universal use |
| Stronger rejected rule | the tempting but unsupported generalization |
| Policy boundary | what still needs a current Official requirement check |
| Source boundary | corpus composition, exclusions, and unavailable material |

Transfer a conditional heuristic or reference, not a mechanical checker, unless a
specific observed failure proves that deterministic validation is possible and useful.
The receiving skill keeps its own scientific and venue authority. If a pattern changes
the claim, data interpretation, or experiment rather than presentation, return it to
the publication pipeline instead of silently editing prose or figures.

## 7. Keep public outputs clean and lawful

Public skill material may contain paraphrased patterns, bibliographic identifiers,
short factual metadata, source locators, corpus boundaries, and honest limitations. Do
not copy publisher PDFs, page images, screenshots, extracted full text, long passages,
supplementary files, or third-party figures. Do not expose private paths, personal
library structure, prompts, agent traces, or internal execution records.

Keep the full census, access notes, and local source map in the author workspace. Before
public transfer, inspect every included locator and remove any claim that depends on an
unavailable page or unverified supplement.

## Deliverables

Return:

1. corpus census and exclusion ledger;
2. stratum counts with explicit denominators;
3. deep-read selection and stopping rationale;
4. cross-paper evidence matrix;
5. observed patterns, editorial judgements, counterexamples, and official-policy gaps;
6. bounded transfer cards for the target skills;
7. source and copyright limitations.

Do not call the calibration complete when only the attractive exemplars were read or
when source anomalies, missing supplements, and counterexamples remain unaccounted for.
