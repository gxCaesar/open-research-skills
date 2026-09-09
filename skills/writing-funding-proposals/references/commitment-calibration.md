# Commitment calibration

Classify proposed work by what the applicant can honestly commit to, not by how
important the section sounds. Record research content, annual task, and output as
separate auditable artifacts. Give each artifact one primary class; it does not replace
its hypothesis, evidence, dependencies, validation, or failure criterion.

## Deliverable mainline

Use `deliverable mainline` when the work is essential to the central argument and its
execution is supported by the applicant's verified foundation, available data or
materials, resources, dependency chain, and a credible fallback that preserves the
scientific question.

Record:

- the exact result or artifact to be delivered;
- why it is necessary for the central contribution;
- prerequisite evidence and applicant capability;
- validation and acceptance evidence;
- main technical risk and a scientifically meaningful fallback;
- downstream tasks that depend on it.

Commit to executing the work and reporting the valid outcome. Do not guarantee a
favorable biological finding, metric improvement, mechanism, or proof that remains the
object of research.

## Cautious exploration

Use `cautious exploration` for a plausible but nonessential extension whose uncertainty
is itself worth resolving. It must have a bounded resource envelope and must not be
quietly required for the mainline claim.

Record:

- the hypothesis and why it is plausible;
- the cheapest discriminating experiment or analysis;
- its strongest falsifier and decision date;
- what is learned from a positive, negative, or inconclusive result;
- the finite resource bound and stop rule;
- whether a later proposal stage may promote it and what evidence that requires.

Do not list open-ended optimization, broad data collection, or a rescue for a weak
mainline as exploration. A negative result remains an informative outcome rather than a
reason to change the metric, population, or claim after observation.

## Boundary confirmation

Use `boundary confirmation` when an early check determines whether a downstream scope,
dataset, mechanism, or validation route is defensible. It is a dependency gate, not the
proposal's final contribution.

Record:

- the exact uncertain boundary;
- the source of uncertainty;
- the minimal check and independent unit;
- the go and no-go criteria;
- the downstream branch selected by each outcome;
- the last point at which the check can occur without wasting dependent work.

A boundary check must resolve a real fork. Do not add ceremonial feasibility tests whose
outcomes cannot change the plan.

## Record contract

Use `commitments/commitment-records.json` to record each artifact with its type
(`research_content`, `annual_task`, or `output`), controlled ID, primary class, finite
bound, stop rule, dependencies, and sequence. An annual task additionally links to the
research-content IDs it serves. Dependencies name earlier commitment records; a later
record cannot depend on one at the same or a later sequence.

Do not impose one class on all artifacts in a work package. For example, a research
content can be deliverable mainline, its first annual task can be boundary confirmation,
and a contingent output can be cautious exploration. State that relationship directly
instead of silently promoting the contingent artifact to a guaranteed result.

## Cross-artifact audit

For each work package, compare the stated dependency and consequence across the
scientific argument, section brief, timeline, annual output, risk table, figure, and
prose. Different artifact classes are permitted; flag only contradictions such as:

- a cautious exploration described elsewhere as guaranteed output;
- a boundary check scheduled after dependent mainline work;
- a mainline dependency without evidence, acceptance criteria, or fallback;
- the same favorable outcome counted as both validation and deliverable;
- a negative or no-go outcome with no stated scientific disposition.

Use direct language. Ambition comes from a consequential question and discriminating
validation, not from describing uncertain work as certain.
