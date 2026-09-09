# Abstract argument patterns

Choose one pattern from the paper's actual contribution. These are reasoning guides,
not fixed sentence templates and not venue rules.

## Theory or formal result

Use for optimality, decidability, complexity, identifiability, or guarantee-driven work.

`formal task → unresolved boundary → condition or formulation → theorem or algorithm → tightness and scope`

Preserve qualifiers that define the result, such as `almost surely`, a named logic
class, or `optimal up to a constant factor`. A guarantee is evidence; do not pad the
abstract with invented empirical detail.

## Method or algorithm

Use when the contribution is a learning method, architecture, objective, or training
procedure.

`capability → concrete failure → mechanism → why it addresses the failure → matched evaluation → bounded comparative result`

The common failure is naming modules without explaining the mechanism. A comparative
result needs the metric, direction, comparator, and evaluation regime.

## Empirical analysis

Use for behavioral, probing, alignment, audit, or measurement studies.

`consequential unknown → missing coverage or confound → measurement design → varied dimensions → principal finding → caution or implication`

Foreground what was learned, not a tool built to run the analysis. Distinguish
association from causation.

## Dataset or benchmark

Use when the dataset or benchmark itself fills a named measurement gap.

`missing coverage or invalid comparison → sampling and annotation design → scale and independent units → evaluation dimensions → finding → use boundary`

State why the artifact changes what can be measured. Dataset size alone is not a
scientific result.

## Scientific or application system

Use for deployed systems, biological or clinical applications, human studies, and
social-impact work.

`real decision or scientific need → technical bottleneck → scoped mechanism → realistic or independent validation → measurable result → tested population or setting`

Do not generalize beyond the population, site, geography, time period, or operating
condition actually evaluated.

## Selection checks

1. Can the scientific question be stated without the method name?
2. Does the mechanism directly address the diagnosed failure?
3. Does the evidence test the dominant question on the correct independent unit?
4. Does the main result answer that question rather than list benchmark wins?
5. Does the final sentence state a supported answer and boundary?
6. Would removing a sentence preserve the argument? If yes, merge or cut it.
