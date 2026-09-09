# Intake and routing

Use this reference before a pilot, method design, venue recommendation, or claim of absent data or
prior work.

## Resolve the active scientific object

Read current project authority before broad literature or file discovery. Apply this order:

1. the user's current explicit scope and requested operation;
2. a structured project decision or publication status file;
3. active claim, quarantine, withdrawal, supersession, or frozen-source records;
4. current start and run instructions;
5. dated reports and registered protocols;
6. repository overview and manuscript prose;
7. plans and conversational memory.

A lower source cannot revive a claim rejected by a higher one. Same-level conflicts remain an
authority conflict. A source selected for historical audit is not thereby selected for active
publication.

## Evidence status

Open every source that supports a gate. Record its locator, access date, inspected location, scope,
and status. Search results and citation metadata may locate evidence but do not verify it. Preserve
`UNVERIFIED`, `COULD_NOT_OPEN`, and `NOT_FOUND` instead of filling gaps from memory.

For current venue rules, deadlines, data licences, repository versions, or live project status,
refresh the first-party source. A static skill reference cannot make a time-sensitive fact current.

## Data feasibility comes before model design

Ask whether all variables required by the claim coexist in the same linkable units. Separate
datasets satisfy this only when a defensible linking key and measurement contract exist. Record:

- data accession or source and version;
- required inputs, outcomes, covariates, and validation labels;
- evidence that those fields coexist;
- independent unit after the proposed split;
- number of independent units, not rows, cells, patches, reads, or repeated runs;
- missingness, replicate reliability, assay ceiling, and label direction;
- strongest cheap baseline and positive control;
- group-, entity-, scaffold-, cohort-, or time-disjoint split appropriate to the claim;
- an orthogonal, external, prospective, or real-use validation path;
- the cheapest test that can falsify feasibility.

If the exact entities do not overlap, examine broader sources, a defensible pathway- or
mechanism-level link, and a genuine resource contribution before concluding the data are absent.
An absence claim needs a dated search ledger.

## Separate three judgments

### Data feasibility

Use `PASS` only when the joint variables, access, independent units, readout, split, and validation
path are supported. Use `HOLD` for a specific closable evidence gap and `FAIL` for a demonstrated
incompatibility. This judgment says nothing by itself about novelty or venue fit.

### Scoop verdict

Interpret novelty inside the chosen contribution lane:

| Lane | `IDENTICAL` means |
|---|---|
| `sota-method` | the same method and claimed margin already exist under a matched task, representation, split, metric, and comparator protocol |
| `discovery` | the same scientific finding is already supported by comparable evidence |
| `benchmark` | the same consequential gap-filling resource or evaluation correction already exists |

Use `ADJACENT` when nearby work constrains framing, becomes a comparator, supplies data, or leaves a
specific delta. Use `UNCERTAIN` when the strongest relevant source could not be opened or search
coverage remains incomplete. Weak venue fit is never relabelled as an identical scoop.

Search independently by claim and endpoint, mechanism and alternate terminology, data and split,
simple-baseline or negative-result findings, neighboring venue vocabulary, and recent primary
papers, preprints, code, datasets, or patents. State the nearest work and one-sentence difference.

### Venue fit

Match the contribution and evidence package before naming a prestigious venue:

| Property | Top-CS route | Nature-family route |
|---|---|---|
| Central claim | algorithm, evaluation method, generalization law, efficiency, or reliable system behavior | biological method, resource, benchmark, mechanism, or discovery |
| Breadth | multiple datasets, tasks, contexts, or shifts | deep biological validation in the target system |
| Comparators | current methods plus strong cheap and compute-matched controls | accepted biological practice plus computational controls |
| Validation | ablation, robustness, calibration, efficiency, and reproducibility | orthogonal and preferably prospective biological validation |

Use `dual-track` only when one predeclared scientific core supports two independently sufficient
evidence packages. Do not hide a failed Nature validation in a conference fallback.

## Disposition is not one generic kill switch

Name the failure layer:

- `FRAMING`: reframe the question; preserve usable data and evidence.
- `DATA`: hold while a dated search or access gap remains; do not declare the task dead.
- `TASK`: kill only after the strongest available representation and cheap comparator close
  headroom at the correct independent unit.

A lane-identical scoop returns the project to intake. Adjacent work remains alive for delta design.
Changing contribution lane is a new decision, not a quiet fallback.

## Domain-specific minimum checks

For single-cell or perturbation tasks, distinguish donors, cell lines, perturbations, guides,
compounds, doses, times, and cells; a random cell split rarely tests unseen biology. For genomics,
check donor, locus, chromosome, gene-family, homology, time, and cohort leakage. For molecular
design, keep docking, affinity, reward, selectivity, exposure, and functional activity as separate
claims and use scaffold- or time-disjoint evaluation when novelty is claimed. For biological LLM
or agent systems, compare with a fixed workflow, retrieval-only system, non-agent model, and an
equal-information control; orchestration success is not scientific correctness.

## Pilot boundary

Freeze one falsifiable claim, endpoint and direction, minimum relevant effect, uncertainty method,
independent unit, generalization split, strongest cheap baseline, validation path, and kill
criterion. The pilot is the smallest real-data test of the load-bearing premise. Its GO result
supports feasibility only. It does not authorize compute, establish novelty, or make the project
submission-ready.
