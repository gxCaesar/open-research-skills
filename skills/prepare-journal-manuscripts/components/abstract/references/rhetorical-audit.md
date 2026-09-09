# Rhetorical audit for abstracts

The venue-agnostic backbone for both drafting and reviewing. It answers "what job
does each sentence do?" and "is each claim earned?" independent of word limit or
venue.

## The seven rhetorical functions

Use the seven functions to diagnose the argument, without forcing one sentence per
function or a fixed order. One sentence may carry two functions. Adapt their emphasis
to the contribution and exact article form; identify a missing function only when its
absence obscures the question, evidence or conclusion.

1. **Problem & scope** — What exact problem, for whom, under what setting?
2. **Gap** — What fails or remains unknown in the *closest* prior work? (Not a broad
   "little attention has been paid" — a specific mechanism that breaks.)
3. **Approach** — What is introduced, changed, measured, or proved?
4. **Mechanism or measurement logic** — Why does the approach address the question,
   beyond its name? Discovery or descriptive work needs a measurement strategy that
   resolves the unknown, not an invented causal mechanism.
5. **Evidence** — Which datasets, environments, analyses, or theorems test the claim?
6. **Result** — What exact outcome supports the main claim? Preserve **units,
   direction, comparator, and uncertainty**.
7. **Meaning & boundary** — What is learned, and what is *not* established?

An abstract passes the audit when problem → gap → mechanism → evidence → result →
meaning form **one coherent argument**, and the dominant scientific question survives the
removal of the method's name.

## The ten-move sequence (sentence-level coding)

Tag each sentence's dominant move in reading order; repeated moves are allowed. Use
this to diagnose order problems (e.g. results before the question, or a method
inventory with no mechanism).

`CONTEXT_OR_IMPORTANCE` · `PROBLEM_OR_GAP` · `OBJECTIVE_OR_CLAIM` ·
`METHOD_OVERVIEW` · `CORE_MECHANISM` · `EVALUATION_SETUP` · `QUALITATIVE_RESULT` ·
`QUANTITATIVE_RESULT` · `SIGNIFICANCE` · `LIMITATION_OR_SCOPE`

Diagnostics on the coded sequence:
- **Missing `CORE_MECHANISM`** in a method abstract → check whether the text explains
  how the approach addresses the gap. Discovery or descriptive work may instead need
  measurement logic; absence of an identified biological mechanism is not a stylistic defect.
- **No `PROBLEM_OR_GAP`** → the reader cannot recover the question without the title.
- **`QUANTITATIVE_RESULT` absent** → check whether the central claim needs a magnitude.
  A numerical performance comparison should state its relevant evidence; a demonstrated
  capability need not have an invented margin. Dataset size alone is not an effect.
- **`SIGNIFICANCE`/`LIMITATION_OR_SCOPE` absent** → check whether the answer and scope
  are already clear from the finding, named population or design. Do not append a
  formulaic limitation sentence when it adds no interpretive information.

## Claim-strength scale

Rate the abstract's dominant claim; **never equate force with quality**. A precise,
bounded claim is usually more defensible than a broad one.

`DESCRIPTIVE` → `BOUNDED_COMPARATIVE` → `BROAD_COMPARATIVE` → `SUPERLATIVE_OR_BREAKTHROUGH`

- Narrow unsupported claims to the evidence. Use the appropriate descriptive,
  comparative or causal register; do not turn a discovery into a benchmark claim or
  weaken a supported finding into generic caution.
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

- **draft** — use the relevant functions to shape the contribution's argument; repair
  missing logic before compressing without requiring a fixed sentence sequence.
- **polish-compress** — keep the move sequence; give each sentence one job; delete any
  sentence whose removal does not break the chain.
- **review-diagnose** — for each issue report the **exact phrase, its function, the
  evidence location, the mismatch, and the smallest revision objective** (never a
  full rewrite unless asked). Fill `assets/abstract-blueprint-template.md`.
