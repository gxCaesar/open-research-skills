# Abstract revision blueprint

Fill this in during `review-diagnose` mode. It plans an abstract by rhetorical
function **without writing final prose**, so the author keeps authorship of the
words. One blueprint per abstract. Delete the `> …` instruction lines in the output.

---

## Target

- **Venue / track:** {{venue}}  ·  **Type:** {{conference | journal}}
- **Length target:** {{min}}–{{max}} words  ·  **Structured?** {{no | Background/Methods/Results/Conclusions}}
- **References allowed in abstract?** {{no | yes}}  ·  **Anonymous?** {{yes | no}}
> Copy these from `references/venue-conventions.md`, then confirm against the live CFP.

## Dominant scientific question

> One sentence. Must stay meaningful after the method's name is removed.
{{question}}

## Archetype

> One of: theory-formal / method-algorithm / empirical-ML-LLM / dataset-benchmark / system-application-human.
{{archetype}}

## Rhetorical-function plan

For each function: the **current** state, the **target**, and the **evidence
location** it must trace to. Leave a function blank only if the archetype genuinely
omits it.

| Function | Current (quote/paraphrase) | Target | Evidence location |
| --- | --- | --- | --- |
| Problem & scope | {{...}} | {{...}} | {{...}} |
| Gap | {{...}} | {{...}} | {{...}} |
| Approach | {{...}} | {{...}} | {{...}} |
| Mechanism (why it works) | {{...}} | {{...}} | {{...}} |
| Evidence (data/theorems) | {{...}} | {{...}} | {{...}} |
| Result (locked numbers) | {{...}} | {{...}} | {{table/fig/source}} |
| Meaning & boundary | {{...}} | {{...}} | {{...}} |

## Locked results

> Every headline number, verbatim, with unit, direction, comparator, and uncertainty.
> These must match a committed table/figure/fact source; the prose may not exceed them.
- {{metric = value ± uncertainty, vs comparator, on dataset/regime, source}}

## Move-sequence issues

> Coded sequence of the current abstract and the specific reordering/insertions needed.
- Current: {{CONTEXT_OR_IMPORTANCE → ...}}
- Fixes: {{e.g. insert CORE_MECHANISM after METHOD_OVERVIEW; move QUANTITATIVE_RESULT before SIGNIFICANCE}}

## Claims to remove or qualify

> Superlatives, "first", causal or hedge words (robust/general/efficient) lacking a
> defined test, comparators without a named baseline/regime, references/URLs if banned.
- {{claim}} → {{cut | downgrade to bounded comparative | add condition}}

## Smallest-edit list

> Ordered, minimal edits — exact phrase → revision objective. Not a full rewrite.
1. {{phrase}} → {{objective}}
