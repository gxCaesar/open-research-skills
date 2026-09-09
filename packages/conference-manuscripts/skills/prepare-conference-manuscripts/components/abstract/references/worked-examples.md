# Worked examples

Two end-to-end runs of the skill. Both papers are **synthetic illustrations** — invented
to show the process, not real work. Do not reuse their wording; abstract the *moves*, as
`abstract-patterns.md` requires. Every word count shown was produced by
`scripts/check_abstract.py`.

---

## Example 1 — `draft` mode (method-algorithm archetype)

### Input materials (what the user supplies)

- Setting: retrieval-augmented question answering (a reader model conditioned on
  retrieved passages), deployed where wrong answers are costly.
- Observation: the system answers even when retrieved passages do not support any
  answer, producing confident errors.
- Idea: judge whether the retrieved evidence is sufficient before answering.
- Mechanism: measure agreement among passages — do they entail a common answer or only
  share topic words — and abstain below a threshold calibrated on held-out questions.
- Evidence: three open-domain QA benchmarks; compared against confidence-based and
  entropy-based abstention; reports selective accuracy at a fixed answer rate; measures
  unsupported-answer rate and answerable-question accuracy.
- Boundary: gains hold under retrieval distribution shift; shrink when passages are
  highly redundant.

### Step 1 — working fact sheet

object = RAG reader + retrieved passages · desired = answer only when evidence suffices,
else abstain · gap = current RAG answers regardless of support → confident errors ·
mechanism = inter-passage agreement (entailment vs topical overlap), calibrated abstention
threshold, independent of generator confidence · evidence = 3 benchmarks, vs confidence/
entropy baselines, selective accuracy @ fixed answer rate, unsupported-answer rate ·
boundary = holds under shift, narrows under redundancy.

### Step 2 — scientific question

> How can a retrieval-augmented reader decide when its retrieved evidence is sufficient
> to answer, instead of always answering?

It survives deleting the method name (there is no "AbstainQA" in it) — a valid spine.

### Step 3 — archetype and move sequence

**method-algorithm** → `CONTEXT` → `PROBLEM_OR_GAP` → `OBJECTIVE` → `METHOD_OVERVIEW`
→ `CORE_MECHANISM` → `EVALUATION_SETUP` → `QUANTITATIVE_RESULT` → `LIMITATION_OR_SCOPE`.
Note the mechanism sentence is explicit (the most-skipped move).

### Step 4–7 — final abstract (167 words, one paragraph, PASS at 150–200)

> Retrieval-augmented question answering is deployed where wrong answers are costly, yet
> current systems answer even when the retrieved passages do not actually support any
> answer, producing confident errors that are hard to detect downstream. We ask how a
> reader model can decide when its retrieved evidence is sufficient to answer, rather
> than always answering. We introduce AbstainQA, which estimates answerability from the
> agreement structure among retrieved passages: it measures whether passages entail a
> common answer or merely share topic words, and abstains when cross-passage support
> falls below a threshold calibrated on held-out questions. Because the signal comes from
> inter-passage agreement rather than the generator's own confidence, it remains
> informative when the generator is miscalibrated. On three open-domain benchmarks,
> AbstainQA raises selective accuracy at a fixed answer rate over confidence- and
> entropy-based abstention, and cuts unsupported answers by a clear margin while leaving
> answerable-question accuracy unchanged. The gains hold under retrieval distribution
> shift but narrow when passages are highly redundant, indicating that agreement, not
> volume, drives the estimate.

Validation: `printf '%s' "$ABSTRACT" | python3 "$SKILL_DIR/components/abstract/scripts/check_abstract.py"` → `PASS`
(167 words). Note the result is bounded ("a clear margin", "at a fixed answer rate") —
no fabricated percentage, because the materials supplied none. If the user provides the
numbers, drop them in verbatim with unit and comparator.

---

## Example 2 — `review-diagnose` mode (empirical-ML-LLM archetype)

### The submitted abstract (76 words — fails the gate)

> In recent years, large language models have garnered significant attention and play a
> crucial role in many applications. However, their alignment across cultures remains an
> important problem. In this paper, we propose a novel and comprehensive framework to
> leverage prompting for studying this crucial issue [12]. Extensive experiments
> demonstrate the effectiveness and superiority of our approach, achieving promising
> results. Furthermore, our work provides valuable insights and opens new avenues for
> future research in this exciting direction.

`check_abstract.py --forbid-citations` → **FAIL**: contains `[12]`; and at 76 words it is
far too thin — because five of seven functions are missing or hollow, not because it
needs padding.

### Rhetorical-function audit

| Function | State in the draft |
| --- | --- |
| Problem & scope | Vague ("alignment across cultures … important problem") — no setting |
| Gap | **Missing** — no specific failure of prior work |
| Approach | "a novel and comprehensive framework" — names nothing |
| Mechanism | **Missing** — "leverage prompting" is not a mechanism |
| Evidence | **Missing** — no data, no dimensions varied, no comparator |
| Result | **Hollow** — "effectiveness and superiority", "promising results" |
| Meaning & boundary | **Missing** — "valuable insights / new avenues" is filler |

Coded move sequence: `CONTEXT`(throat-clearing) → `PROBLEM`(vague) → `METHOD_OVERVIEW`(no
mechanism) → `QUALITATIVE_RESULT`(empty) → `SIGNIFICANCE`(vague). Claim strength =
`BROAD_COMPARATIVE` ("superiority") with zero support → must downgrade.

### AI-flavor hits (from `ai-flavor-scrub.md`)

`In recent years` · `garnered significant attention` · `play a crucial role` · `novel and
comprehensive framework` · `leverage` · `Extensive experiments demonstrate the
effectiveness and superiority` · `achieving promising results` · `Furthermore` ·
`provides valuable insights and opens new avenues` · `exciting direction`. Plus the banned
`[12]`.

### Smallest-edit list (exact phrase → objective)

1. "In recent years … applications." → **delete**; open on the specific problem.
2. "alignment across cultures remains an important problem" → state the real gap:
   *alignment is usually tested in English on a few countries.*
3. "propose a novel and comprehensive framework to leverage prompting … [12]" → name the
   measurement design (countries, languages, ground-truth survey); **remove [12]**.
4. "Extensive experiments demonstrate the effectiveness and superiority … promising
   results" → report the principal finding with the dimensions varied and its direction.
5. "Furthermore … exciting direction." → replace with the bounded implication.

### Revised abstract (166 words — PASS at 150–250, no citations)

> Whether large language models express consistent opinions across cultures is usually
> tested in English on a handful of countries, leaving open how far apparent alignment is
> an artifact of that narrow setting. We measure opinion alignment across forty countries
> and six languages, and ask whether prompting in a country's own language shifts a
> model's responses toward that country's survey distribution. Reusing an established
> cross-national opinion survey as ground truth, we compare model answers to human
> response distributions under matched prompts, varying only the language and the named
> country. Alignment is uneven: models track high-income, English-speaking populations
> far more closely than others, and prompting in the local language moves responses
> toward the local distribution for some countries while leaving others unchanged. The
> direction of the shift is not always toward better alignment, so language steering
> cannot be treated as a reliable correction. These results bound claims of global
> alignment to the countries and languages actually evaluated, and show that measured
> alignment depends on the prompt language used.

`check_abstract.py --min-words 150 --max-words 250 --forbid-citations` → `PASS` (166
words). The claim is now `BOUNDED_COMPARATIVE`, every function is present, and the closer
answers the question instead of gesturing at "future research".

---

## Example 3 — `draft` mode (theory-formal archetype): short is correct

Theory abstracts can be short and claim-light — a guarantee, not a benchmark number,
is the result. Do **not** pad one to hit a generic editorial window.

### Input materials

- Object: testing whether a hidden binary relation is a partial order, via comparison
  queries.
- Boundary: in the worst case this needs almost all pairs queried.
- Idea: a promise that the order has bounded *width* should make it cheap.
- Result: with width ≤ w, adaptive queries recover the order in `O(n w log n)`
  comparisons; a matching lower bound up to the log factor; without the width promise, a
  pairs-linear lower bound returns.

### Scientific question

> Does bounding a hidden partial order's width make it efficiently testable by comparison
> queries, and how tight is that dependence?

Claim-light and name-free — a valid theory spine.

### Archetype and moves

**theory-formal** → `PROBLEM_OR_GAP` → `OBJECTIVE_OR_CLAIM` → `CORE_MECHANISM`
(width-parameterized adaptive querying) → `QUALITATIVE_RESULT` (upper + matching lower
bound) → `SIGNIFICANCE` (what quantity governs the problem). No `EVALUATION_SETUP`,
no `QUANTITATIVE_RESULT` — theory does not need them.

### Final abstract (109 words — short on purpose)

> Testing whether a hidden binary relation is a partial order can, in the worst case,
> force a learner to query almost every pair. We ask whether a promise on the order's
> width makes the problem cheap. We show that when the width is at most w, adaptive
> comparison queries recover the order using O(nw log n) comparisons, and that no
> algorithm does better up to the logarithmic factor. The bound is tight in the width:
> without a width promise, a lower bound linear in the number of pairs returns. The
> result isolates width, not sparsity, as the quantity that governs how efficiently such
> an order can be tested.

Validation: `check_abstract.py --min-words 60 --max-words 150 --forbid-citations` →
`PASS` (109 words). The **same** text FAILs the AAAI editorial default 150–200 ("Add at least 41
words") — the right response is to pick the venue's real window, **not** to inflate the
abstract. The 150–200 default is an editorial target, not a universal or official rule.
Note the exact qualifier "up to the logarithmic factor" is preserved (it
defines the contribution) and no percentage is invented.
