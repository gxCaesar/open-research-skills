# Abstract component

Produce an abstract in which one scientific question connects the problem, mechanism,
evidence, result, and bounded conclusion. Preserve the value and scope of every retained
number and qualifier; select the details needed for the central claim. Never manufacture
evidence to make the paragraph sound complete.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## Choose the mode

- **Draft:** build an abstract from a manuscript, outline, results, or notes.
- **Polish or compress:** improve an existing abstract while preserving its claims.
- **Review:** diagnose the smallest changes needed; do not rewrite unless asked.

Use this component for the abstract itself. The journal entrypoint owns the complete
manuscript, revision response, cover letter, and final package.

## Load only the needed resources

- Read `references/rhetorical-audit.md` for every task.
- Read `references/venue-conventions.md` when a venue, track, length, anonymity rule,
  citation rule, or structured format matters.
- Read `references/abstract-patterns.md` when drafting or changing the argument shape.
- Apply `references/ai-flavor-scrub.md` before returning drafted prose.
- Read `references/title-audit.md` only when the title is also in scope.
- Consult `references/worked-examples.md` only when the mode or archetype is unclear.
- For Nature-family abstracts, read the Abstract section of
  [section-specific writing](../../references/nature-section-style.md) for capability,
  discovery and translational examples and their limits.
- Use `assets/abstract-blueprint-template.md` for review output.

## 1. Establish the target

Record the venue and track, length window, paragraph or heading requirement, citation
policy, and anonymity status. Current official instructions and the submission form
override every bundled preset.

`scripts/check_abstract.py --venue aaai` uses a 150–200-word, one-paragraph,
no-citation **editorial default** inherited from the focused AAAI workflow. It is not a
claim about the current official AAAI form. Supply explicit limits when the live form
differs or does not state that window.

## 2. Ground the abstract

Extract a fact sheet from the supplied material:

- research object, setting, and desired capability or knowledge;
- the closest concrete failure, assumption, or unresolved question;
- the proposed mechanism, analysis, theorem, or measurement design;
- datasets, independent units, baselines, evaluation regimes, or proof conditions;
- strongest result with unit, direction, comparator, and uncertainty;
- conclusion boundary and material negative result.

If a load-bearing fact is missing, mark it as unknown or ask for it when the answer
would change the claim. Normalize terminology before drafting.

## 3. Distill one scientific question

Build this problem spine:

`object X → desired outcome Y → obstacle or unknown Z → condition C → answer Q`

The question must remain meaningful after removing the method name. Choose one dominant
question; modules, datasets, proofs, and applications support it rather than becoming
unrelated contribution lists.

Reject a spine when the mechanism does not address the stated obstacle, the evaluation
does not test the question, or the conclusion exceeds the evidence.

## 4. Shape the argument

Choose the closest archetype in `references/abstract-patterns.md`: theory/formal,
method/algorithm, empirical analysis, dataset/benchmark, or scientific/application
system. Draft the smallest causal chain that contains:

1. exact problem and scope;
2. specific gap or boundary;
3. answer-oriented objective;
4. approach and why its mechanism addresses the gap;
5. evidence or proof setup;
6. strongest supported result;
7. meaning and justified boundary.

These are rhetorical functions, not seven required sentences or a fixed order. A
descriptive or discovery study needs an intelligible measurement strategy, not an
invented biological mechanism. A capability abstract need not contain a numerical
margin; a comparative performance claim must retain the evidence that makes it precise.

Theory may end on a guarantee rather than a benchmark number. Empirical work should
name the comparator and regime for comparative claims. Application claims stay inside
the independently tested population or operating setting.

## 5. Draft, compress, or diagnose

For drafting, aim below the upper limit so revision has room. Give each sentence one
main rhetorical job. Prefer mechanism verbs and concrete evidence over adjectives,
module inventories, or generic statements of importance.

For compression, remove repetition, setup detail, unused acronyms, implementation
trivia, and generic openings before deleting the scientific question, mechanism,
headline evidence, or validity boundary.

For review, quote the exact problematic phrase and report its rhetorical function,
evidence mismatch, and smallest revision objective. Use the blueprint; return a revised
abstract only when requested.

Never strengthen a claim merely to improve style. Unsupported `first`, `state of the
art`, causal, robust, general, scalable, or human-level claims must be removed or tied to
the exact evidence that earns them.

## 6. Validate

Count only the abstract body. Prefer explicit live limits:

```bash
printf '%s' "$ABSTRACT" | python3 "$SKILL_DIR/components/abstract/scripts/check_abstract.py" \
  --min-words <MIN> --max-words <MAX> \
  [--max-paragraphs <N>] [--forbid-citations]
```

`--venue <name>` is a convenient editorial preset; `--venue list` prints the roster.
Explicit length and paragraph flags override a preset. Revise until the checker reports
`PASS`, then manually confirm that the question, mechanism, evidence, and conclusion
form one chain and every number traces to the supplied material.

## Return format

Unless the user requests abstract-only output:

```text
Scientific question: <one sentence>

Abstract (<N> words):
<one paragraph, or the required headed sections>
```

For abstract-only output, return the abstract and verified word count. For review mode,
return the completed blueprint and only the edits requested.

## Verify changes to this component

```bash
python3 "$SKILL_DIR/components/abstract/tests/test_check_abstract.py"
python3 "$SKILL_DIR/components/abstract/tests/run_selftest.py"
```
