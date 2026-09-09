# Scientific argument and section contracts

## Q/C/V/O/CL/F graph

Build this dependency chain before expanding section prose:

```text
project goal -> question -> research content -> data or object
             -> method or mechanism -> discriminating validation
             -> output -> prior evidence -> figure -> annual output
```

Controlled IDs make each dependency inspectable:

| ID | Role |
|---|---|
| Q* | Core scientific question or testable central proposition |
| C* | Research content that resolves part of a question |
| V* | Discriminating validation and its failure consequence |
| O* | Verifiable output with acceptance evidence |
| CL* | Bounded prior or applicant evidence from the claim ledger |
| F* | Figure or table with a rhetorical job and body anchor |

Every Q* needs at least one C* and V*. Every C* names its data or object, method or
mechanism, V*, O*, supporting CL*, and any F*. Every V* names the comparator or
alternative explanation, independent unit, evaluation boundary, failure criterion, and
the resulting revise, reframe, or stop action.

Add content only when it resolves a dependency needed by the goal, another content,
validation, or output. Merge content that creates no separate scientific judgment.
Remove platform-building, model-brand, or performance-only items that have no linked
question and falsifiable output.

## Root section jobs

Current official headings control final structure. For the common three-root arrangement,
the scientific jobs are:

- `rationale`: establish value, the precise unresolved condition, Q*, and why the chosen
  route can resolve it;
- `contents`: state the goal and dependency graph, then give every C* its object, mechanism
  or method, V*, output, risk, and fallback;
- `foundation`: connect completed work and transferable capability to specific C* items,
  while keeping planned work and unavailable evidence separate.

Title and abstract compress a settled argument; they do not introduce a new claim or
broaden the scope. Declarations and other system fields follow current official sources
and applicant confirmation.

## Section briefs under a restricted authoring policy

When the mode is `EVIDENCE_AND_AUDIT_ONLY`, each section file remains a structured brief
for the applicant. Record:

- rhetorical job and controlled argument IDs;
- source and claim IDs;
- paragraph dependencies and transition logic;
- figure slots and body anchors;
- strongest falsifier and unresolved evidence;
- an explicit applicant drafting or confirmation task.

Do not turn these records into application prose. Review applicant-authored text against
the brief, report exact locations and evidence gaps, and preserve numerical and citation
scope. Mark an unresolved brief with its explicit `status`; substantive Chinese text is
checked by visible non-whitespace characters rather than English-style word splitting.

## Page and annual-output handoff

Allocate pages after the argument is stable. A page budget records rhetorical job, target
and upper bound, figure or table slots, actual rendered pages, and revision action.
Rendered pages, not word count, decide whether the integrated artifact fits.

For each annual task, name its linked C*, V*, output, acceptance evidence, timing, and
dependency. Then create separate commitment records for each research content, annual
task, and output, each with a primary class, finite bound, stop rule, dependencies, and
sequence. For each technical risk, name its source, trigger, impact, mitigation,
fallback, and decision point. A generic promise to optimize more is not a fallback.
