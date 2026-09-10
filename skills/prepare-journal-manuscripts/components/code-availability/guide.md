# Code-availability component

Answer the question a reader actually has: what do I install, and at which exact version,
to re-run the analysis behind this claim. A statement that names a repository without a
version, a licence, or an environment answers none of it.

In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`. This component is the sibling of `components/data-availability`; keep code
and data separate unless the target journal asks for one combined statement.

## Establish current authority

Identify the journal, the article type, the stage, and what the journal's current
instructions require for custom code. Requirements differ by journal and by article
type, and several publishers now distinguish code that is central to the conclusions
from convenience scripts. Read `references/routes-and-statements.md` before drafting.

The bundled guidance was checked on 2026-09-10. Reopen the target journal's page before
final advice rather than applying a remembered family-wide rule.

## Inventory before drafting

Start from `examples/code-inventory.example.json` and record every component a
conclusion depends on:

- custom analysis, training, and figure-generating code;
- reused public implementations, with the version actually run;
- third-party or vendor code that the pipeline requires;
- anything a reader must install to reach the reported numbers.

For each, map `claim/figure/table -> component -> exact version -> route`. A component
that no claim depends on does not belong in the statement.

## Choose one route per component

| Route | Use when |
|---|---|
| `archived_with_identifier` | the exact version is deposited and has a persistent identifier |
| `public_repository` | the code is public but not yet deposited; pair it with an archive before final |
| `within_paper_or_supplement` | the code is small enough to ship with the article |
| `reused_public` | someone else's implementation, cited at the version you ran |
| `third_party_restricted` | a vendor or licensed component you cannot redistribute |
| `justified_request` | nothing better is available and the journal accepts it |
| `not_applicable` | no code underlies this claim, with the reason stated |

A repository URL is a moving target: it can change, move, or disappear, and it does not
identify the state the paper describes. Deposit the exact version and record its
persistent identifier. The validator reports this as a warning while drafting and as an
error at final.

Custom code that a conclusion depends on cannot take `not_applicable`.

## Validate

```bash
python3 "$SKILL_DIR/components/code-availability/scripts/validate_code_inventory.py" \
  /path/to/code-inventory.json --mode working --format markdown

python3 "$SKILL_DIR/components/code-availability/scripts/validate_code_inventory.py" \
  /path/to/code-inventory.json --mode final --format markdown
```

`working` reports what is still missing. `final` treats an unarchived repository, an
unresolved placeholder, and a statement that promises rather than provides as errors.

## What the statement may not do

It may not promise. "Code will be made available upon reasonable request" and its
variants give a reader nothing to act on, and the validator rejects them at final. If a
request route is genuinely the only option, say who to contact, who qualifies, and how
long a reply takes, and confirm the journal accepts that for code central to the
conclusions.

It may not imply reuse the licence does not permit. Released code without a licence is
readable and not runnable in any project that takes licensing seriously.

## Boundaries

The validator checks the record, not the world. It cannot confirm that an identifier
resolves, that a repository is public, that the licence is yours to grant, or that the
code reproduces anything. Running it from a fresh install is the only way to learn that,
and that verification belongs with the release itself.
