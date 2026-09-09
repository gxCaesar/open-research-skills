# Paper-card component

Turn one paper into a reproducible map of its reasoning and evidential limits. The output
is not a translated abstract, formal referee report, literature review, or publicity
article.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## Establish the source boundary

Record the supplied source, declared and verified format, access state, coverage,
figures/tables available, supplement access, extraction confidence, and locator mode.
A `.pdf` filename does not prove that the file is a PDF. Readable HTML can support
full-text structural analysis but cannot support invented PDF page numbers.

For a local PDF or structured source-map JSON, run the bundled preparer:

```bash
python3 "$SKILL_DIR/components/paper-card/scripts/prepare_paper.py" INPUT \
  --output WORKDIR/source_bundle.json
```

Add `--render-dir WORKDIR/rendered-pages` when figures, tables, equations, or layout must
be inspected visually. PDF parsing requires `pypdf`; rendering also requires Poppler's
`pdftoppm`. Inspect the validation status before analysis.

For a paper URL, DOI, or publisher page, open the actual source. A search result or
metadata page cannot establish detailed methods or results. If access is partial, mark
the card partial and do not infer unseen content.

## Select one locator mode

- `page-grounded`: a local PDF was successfully parsed and PDF page indices are
  reliable. Cite `PDF p. N` plus figure, table, equation, or section when available.
- `structure-grounded`: sections or display identifiers are reliable but page indices
  are not. Use section, figure, table, equation, or source-block IDs only.
- `source-limited`: only an abstract, metadata, or supplied excerpt is reliable. Cite
  only that scope and mark unseen sections `Not assessable`.

Never turn a missing or invalid page locator into page 1. Printed page labels are
optional metadata and must not be confused with the file's PDF page index.

## Choose the analytical lens

Read `references/paper-type-lenses.md`. Select one primary lens and at most one
substantial secondary lens: methods, discovery, resource, clinical, materials, or
review. Classify by the paper's evidence logic rather than its field label.

## Build evidence before prose

Before drafting, inventory:

- bibliographic metadata and access status;
- the research question and claimed contribution;
- method components, assumptions, inputs, outputs, data flow, and cost;
- every main figure, table, and essential equation with its argumentative role;
- datasets or populations, splits, baselines, metrics, ablations, uncertainty, and
  reported results;
- author-stated limitations and unavailable supplementary evidence;
- stable source pointers for every load-bearing statement.

Then build a claim-evidence matrix containing the exact claim, evidence type, source
pointer, supported strength, stronger unsupported reading, conflict or gap, and
confidence. Read `references/evidence-and-provenance.md` before making analytical or
external claims.

## Reconstruct and challenge the argument

Write the causal chain:

```text
problem -> prior limitation -> core insight -> design choice
-> evidence required -> evidence supplied -> bounded conclusion
```

For each component, ask why it exists and which controlled comparison isolates it. For
each experiment, state the claim tested, conditions, independent unit, comparator,
metric, result, uncertainty, justified conclusion, and unsupported stronger conclusion.

Separate association, necessity, sufficiency, prediction, and mechanism. Check task and
split identity, leakage, baseline fairness, model selection, oracle inputs, end-to-end
status, missingness, exclusions, and population or domain boundary when applicable.

## Write fixed Sections 01--16

Use `assets/paper-card-template.md` and `references/card-schema.md`. Keep all sixteen
headings once and in order. Match the user's language while retaining canonical method,
dataset, symbol, and formula names. Use `Not applicable` or `Not assessable from supplied
material` rather than filling a section speculatively.

Section 12 contains only limitations the authors explicitly acknowledge. Section 13
contains `[Analysis]` concerns and falsifying tests. In Sections 14--16, distinguish
paper-derived knowledge, verified external connections, user-supplied ideas, and agent-
derived candidates.

External search is optional for bibliographic verification, Section 04, Section 15, or
an explicit novelty check. Mark context as `paper-only`, `targeted external check`, or
`externally verified`. The paper's related-work account does not independently verify
field history.

Before Section 16, read `references/research-idea-gates.md`. Every idea needs a source
observation, falsifiable hypothesis, exact delta, matched validation, go/no-go rule,
budget when relevant, and plausible failure modes. Call novelty `unverified` until a
dedicated current prior-art search supports a narrower statement.

## Audit before delivery

```bash
python3 "$SKILL_DIR/components/paper-card/scripts/audit_paper_card.py" \
  --card WORKDIR/paper-card.md \
  --bundle WORKDIR/source_bundle.json \
  --locator-mode page-grounded \
  --report WORKDIR/audit-report.json
```

Use the actual locator mode. Supply the bundle whenever preparation produced one; omit
it only when none exists. Fix audit errors and review warnings. The auditor checks
structure and traceability, not scientific truth. Manually verify every central number,
display, equation, limitation, contradiction, and conclusion boundary.

Return `paper-card.md`, the locator mode and source coverage, the audit result, and exact
limitations. Do not add Sections 17 or 18.
