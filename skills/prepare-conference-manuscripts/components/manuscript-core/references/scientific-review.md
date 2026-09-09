# Scientific review

Review the paper as a scientific argument before line editing it.

## Claim map

For every contribution claim, record:

- the question and comparison actually being answered;
- the method, theorem, dataset, or analysis that supplies the answer;
- the independent evaluation unit and split or proof assumptions;
- the strongest relevant comparator and any recipe differences;
- the result, uncertainty, negative result, and scope boundary;
- the exact table, figure, theorem, appendix item, or external artifact supporting it.

A contribution list is not a claim map. Reject a claim when its evidence tests a
different task, the split permits leakage, the metric does not represent the stated
outcome, or the conclusion generalizes beyond the evaluated unit.

## Falsification pass

Try the cheapest decisive challenge first:

1. Can a train-only simple baseline, representation change, or fair recipe close the
   claimed gain?
2. Does the result survive the actual independent unit rather than repeated seeds or
   correlated samples?
3. Are exclusions, missing values, stopping rules, and model selection defined before
   the test result?
4. Do the abstract, main text, figures, tables, appendix, code, and supplement state the
   same quantity and boundary?
5. Is the strongest alternative explanation measured or merely discussed?

Label unrun checks `not_run` and unresolved evidence `UNVERIFIED`. Never repair a weak
claim by strengthening its prose.

## Readability pass

After the claim map survives, remove repeated setup, unused acronyms, promotional
adjectives, generic importance statements, and module inventories. Each paragraph
should advance one question, mechanism, result, limitation, or consequence. Preserve
numbers, comparison direction, uncertainty, and scientific qualifiers exactly.
