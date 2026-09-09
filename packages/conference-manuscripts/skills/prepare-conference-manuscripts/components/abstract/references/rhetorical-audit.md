# Rhetorical audit for abstracts

The venue-agnostic backbone for both drafting and reviewing. It answers "what job
does each sentence do?" and "is each claim earned?" independent of word limit or
venue.

## The seven rhetorical functions

Locate all seven **without** forcing one sentence per function — one sentence may
carry two, and a mature abstract rarely spends more than one sentence on any of the
first two. In review mode, name which function each sentence serves and flag any
that is missing, buried, or doing a second function's job.

1. **Problem & scope** — What exact problem, for whom, under what setting?
2. **Gap** — What fails or remains unknown in the *closest* prior work? (Not a broad
   "little attention has been paid" — a specific mechanism that breaks.)
3. **Approach** — What is introduced, changed, measured, or proved?
4. **Mechanism** — Why should the approach work, *beyond a method name*? A reader
   should understand the causal idea even after deleting the method's name.
5. **Evidence** — Which datasets, environments, analyses, or theorems test the claim?
6. **Result** — What exact outcome supports the main claim? Preserve **units,
   direction, comparator, and uncertainty**.
7. **Meaning & boundary** — What is learned, and what is *not* established?

An abstract passes the audit when problem → gap → mechanism → evidence → result →
meaning form **one causal chain**, and the dominant scientific question survives the
removal of the method's name.

## The ten-move sequence (sentence-level coding)

Tag each sentence's dominant move in reading order; repeated moves are allowed. Use
this to diagnose order problems (e.g. results before the question, or a method
inventory with no mechanism).

`CONTEXT_OR_IMPORTANCE` · `PROBLEM_OR_GAP` · `OBJECTIVE_OR_CLAIM` ·
`METHOD_OVERVIEW` · `CORE_MECHANISM` · `EVALUATION_SETUP` · `QUALITATIVE_RESULT` ·
`QUANTITATIVE_RESULT` · `SIGNIFICANCE` · `LIMITATION_OR_SCOPE`

Diagnostics on the coded sequence:
- **Missing `CORE_MECHANISM`** after `METHOD_OVERVIEW` → the abstract names a method
  but never says why it works. Highest-frequency defect.
- **No `PROBLEM_OR_GAP`** → the reader cannot recover the question without the title.
- **`QUANTITATIVE_RESULT` absent** when the paper is empirical and has headline
  numbers → the result is under-claimed. (`has_quantitative_result` is true only when
  a number reports a *result magnitude*, not dataset size alone.)
- **`SIGNIFICANCE`/`LIMITATION_OR_SCOPE` absent** → the abstract ends on a benchmark
  win rather than an answer. Generic future work does not count as scope.

## Claim-strength scale

Rate the abstract's dominant claim; **never equate force with quality**. A precise,
bounded claim is usually more defensible than a broad one.

`DESCRIPTIVE` → `BOUNDED_COMPARATIVE` → `BROAD_COMPARATIVE` → `SUPERLATIVE_OR_BREAKTHROUGH`

- Push a claim **down** the scale until the supplied evidence supports it. A bounded
  comparative ("improves X over baseline B on benchmark C under regime R") is almost
  always the right register.
- `SUPERLATIVE_OR_BREAKTHROUGH` ("first", "state-of-the-art", "human-level",
  "solves") requires the source materials to establish it *and* the claim to be
  essential. Otherwise reject it.

## Integrity checks

- **Trace every number** to a table, figure, or committed fact source. Preserve
  units, direction (↑/↓, better/worse), the **named comparator**, and uncertainty.
- **Comparison language** must name the comparator *and* the evaluation regime. "Ours
  is better" without "than what, measured how" is not a claim.
- **Causal language** ("causes", "because", "leads to") needs identification or
  intervention, not association alone.
- **Test every hedge-word**: `robust`, `general`, `scalable`, `efficient`,
  `zero-shot`, `human-level` each require a defined test in the paper. If undefined,
  cut the word or add the condition.
- **No implementation trivia** that displaces the contribution (framework names,
  library versions, hyperparameters).
- **Honest scope over mechanical limitations** — add a boundary when it keeps the
  claim honest; do not bolt on a limitation that obscures the result.

## Evidence typing (so guidance never masquerades as a rule)

Every prescription this skill emits carries one **basis**:

- `official_hard_rule` — a current venue rule (e.g. "no references in the abstract",
  a hard word limit). Overrides everything. Cite the live source.
- `manuscript_fact` — something true of the supplied materials.
- `general_guidance` — accepted writing convention, unverified for this venue.
- `inference` — your own reasoning; flag it as such.

Only a current official rule can force a formatting change independent of the
manuscript. When remembered guidance and a live source conflict, the live source wins.
When general guidance conflicts with a manuscript fact, the manuscript fact wins.

## Using this in each mode

- **draft** — walk functions 1→7 in order; code the draft's move sequence and repair
  gaps before compressing.
- **polish-compress** — keep the move sequence; give each sentence one job; delete any
  sentence whose removal does not break the chain.
- **review-diagnose** — for each issue report the **exact phrase, its function, the
  evidence location, the mismatch, and the smallest revision objective** (never a
  full rewrite unless asked). Fill `assets/abstract-blueprint-template.md`.
