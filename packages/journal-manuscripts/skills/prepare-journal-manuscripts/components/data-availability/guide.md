# Data-availability component

Connect each paper claim to the data needed to inspect, verify, and reuse it. A polished
statement cannot repair an absent deposit, undefined restriction, or unsupported promise.
In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`.

## Establish current authority

Identify the journal, article type, target stage, current journal instructions,
repository mandates, funder or institutional rules, and whether human, sensitive,
commercial, endangered-location, or third-party data are involved. Read
`references/authority-and-policy.md` for a Nature-family task.

The bundled source map was checked on 2026-09-04. Reopen the target journal and
repository pages before final advice. Do not apply a generic Nature-family rule when the
specific journal or data type imposes a different requirement.

## Inventory before drafting

Start from `examples/data-inventory.example.json`. Inventory every dataset family needed
for main and supplementary claims:

- generated raw and processed data;
- figure and table source data;
- analysis inputs and model or simulation outputs;
- reused public datasets with version or access date when relevant;
- licensed, sensitive, controlled, or otherwise restricted data;
- exact article-hosted or supplementary files.

For each record, map `claim/figure/table -> dataset -> exact file -> origin and processing
route`. Separate data from custom code, materials, and protocols unless the journal asks
for a combined statement. Do not treat a repository name, planned upload, lab website,
or temporary sharing link as a verified durable deposit.

## Choose one access route per dataset family

Read `references/routes-and-statements.md`. Use one route:

- `public_repository`;
- `controlled_access`;
- `within_paper_or_supplement`;
- `reused_public`;
- `third_party_restricted`;
- `justified_request`;
- `not_applicable` only when no data were generated or analysed.

Prefer a mandated or community repository, then a suitable durable generalist or
institutional repository. For restricted data, state the reason, discoverable metadata,
controller, eligible users, request procedure, conditions, and any shareable aggregate,
derived, or synthetic data. “Available on reasonable request” without this route is not
an access plan.

Never invent a DOI, accession, repository, version, licence, embargo, consent scope,
ethics approval, data owner, access committee, review period, or permission. Use
`AUTHOR_INPUT_NEEDED` in working mode.

## Validate the record

```bash
python3 "$SKILL_DIR/components/data-availability/scripts/validate_data_inventory.py" data-inventory.json \
  --mode working
```

The validator enforces route-specific fields and claim-to-file mappings. It does not
open links or establish sharing rights. Before final mode, manually confirm that each
identifier resolves to the intended version, reviewer access works outside the author
account when relevant, the licence is valid, restrictions match consent and law, files
open, and the manuscript, repository, and supplement agree.

Read `references/repositories-and-metadata.md` for repository, citation, README, and FAIR
checks. Prefer repository-managed version and integrity metadata over author-created
side records in a public deposit.

## Draft only from verified records

Write an explicit dataset-to-location statement. Cover both new and reused data. Cite
public datasets supporting conclusions in the reference list when required, with
creator, title, repository/publisher, year, and persistent identifier under the target
style.

For Chinese input, read `references/chinese-author-alignment.md`. Accept Chinese notes,
but return submission-ready English unless the user requests Chinese-only text. Translate
the access logic, not a vague phrase literally.

Use this default output:

```text
Data Availability
[evidence-grounded statement]

Repository and citation actions
- [exact outstanding action or None]

Claim-to-artifact mapping
- [claim/figure/table -> dataset -> file -> access route]

Missing information and risk
- [AUTHOR_INPUT_NEEDED fields or None]

中文核对
- [author confirmations in Chinese or 无]
```

Run `--mode final` only after all fields are resolved. A pass means the local inventory
contract is complete; it does not prove journal compliance, public access, consent,
licence rights, or successful submission. Uploading or changing repository records is an
external action outside this skill.
