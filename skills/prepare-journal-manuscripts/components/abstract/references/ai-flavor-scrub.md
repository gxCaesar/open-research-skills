# AI-flavor scrub for abstracts

LLM-drafted abstracts share a recognizable register — intensifiers, vogue verbs,
throat-clearing openings, and hollow contribution phrasing — that reads as generated and
weakens the claim. Run this pass in `polish-compress` and before returning any `draft`.
The fix is almost always the same: **replace the empty word with the specific noun,
verb, or number it is standing in for.** This operationalizes the skill's "mechanism
verbs over adjectives" and "don't end on *effective*" rules.

## Cut or replace on sight

**Empty intensifiers** (delete, or replace with the number): `significantly`,
`remarkably`, `notably`, `substantially`, `dramatically`, `crucially`, `importantly`,
`greatly`, `highly`. "Improves significantly" → "improves by 4.2 points".

**Vogue verbs / hype**: `delve into`, `leverage` (overused), `harness`, `unlock`,
`showcase`, `underscore`, `boast`, `foster`, `pave the way`, `shed light on`, `usher
in`. Use a plain verb: `use`, `exploit`, `show`, `enable`.

**Throat-clearing openings** (delete; start from the object or problem): `In recent
years,`, `With the rapid development of …`, `As … has become increasingly …`, `plays a
pivotal/crucial/vital role`, `has garnered significant attention`, `in the era/realm of
…`, `Artificial intelligence has achieved remarkable success`.

**Hollow contribution phrasing** (replace with the mechanism / the number):
- `we propose a novel framework that …` → name what it does: "we condition X on Y by …".
- `extensive/comprehensive experiments demonstrate the effectiveness/superiority of …`
  → state the result: "on COCO and BDD100K, it improves mask AP by N over B".
- `achieves promising/competitive/state-of-the-art results` → give the number and the
  comparator, or drop the claim.

**Connective chaining**: `Furthermore, / Moreover, / Additionally, / In addition,`
strung across sentences. Keep at most one; prefer a causal link.

**Vague closers** (replace with the answer to the question): `provides valuable
insights`, `opens new avenues`, `holds great promise`, `has broad implications`,
`paves the way for future work`.

**Triadic filler**: parallel adjective triples (`efficient, robust, and scalable`) where
only one is tested. Keep the tested property; cut the rest.

## Before → after

| AI-flavored | Scrubbed |
| --- | --- |
| In recent years, large language models have garnered significant attention. | (delete — open on the problem) |
| We propose a novel and effective framework to leverage graph structure. | We exploit graph structure to <mechanism>. |
| Extensive experiments demonstrate the superiority of our method. | On <datasets>, it improves <metric> by <N> over <baseline>. |
| Our approach achieves promising results and provides valuable insights. | It answers <question>: <the finding>, within <boundary>. |

## Keep (these are not AI-tells)

- **Real numbers, comparators, units, uncertainty** — concreteness is the antidote.
- **Exact formal qualifiers** (`almost surely`, `optimal up to a constant`, named
  complexity/logic class) — precision, not flourish.
- **Deployment qualifiers** (unseen regions, weak supervision, no target labels).
- Field-standard terms of art — do not "de-jargon" a precise technical term into vague
  prose.

## Rule

If deleting a word or sentence does not remove any information a reviewer needs, delete
it. Every surviving sentence should carry a fact, a mechanism, or the answer — never
mood.
