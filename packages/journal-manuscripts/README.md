# Journal Manuscripts

This package exposes one public skill: `prepare-journal-manuscripts`.

For new or redesigned method, architecture, flowchart and motivation schematics, the
skill delegates to `build-scientific-visualizations`: GPT Image 2.5 concept generation
in the corresponding journal style, followed by native editable PPTX reconstruction
and journal-required vector exports. This includes schematic panels within mixed
figures; measured plots and images remain source-derived. Install the visualization
skill when construction is needed; prose and audit tools remain independently usable.

Its eight modes cover the journal lifecycle:

| Mode | Responsibility |
|---|---|
| `recon` | Refresh journal, article-type, stage, policy, format, and reporting authority |
| `draft` | Draft from an author-approved outline and locked scientific contract |
| `audit` | Challenge claims, statistics, novelty, policy, and exact artifacts |
| `polish` | Make targeted evidence-preserving edits |
| `editor-pack` | Reconcile all initial-submission and editor-facing materials |
| `cover-letter` | Write or audit a factual journal-specific letter |
| `revision-response` | Synchronize point-by-point response, clean manuscript, and marked manuscript |
| `final-package` | Verify accepted-paper files and production-stage requirements |

Abstract, statistical reporting, and data availability are retained as non-triggering
components inside the exact skill directory under `components/`. They include focused validators and examples. Paper
reading now belongs to the publication pipeline and is not an extra public entrypoint.

Copy and register `skills/prepare-journal-manuscripts/` with the agent runtime. That exact
directory is independently installable and includes no journal templates, exemplar papers, private reviews,
submission records, or portal automation.

```bash
cp -R packages/journal-manuscripts/skills/prepare-journal-manuscripts \
  /path/to/skills/prepare-journal-manuscripts
```

## Invoke

```text
Use $prepare-journal-manuscripts in editor-pack mode to reconcile this Nature-family manuscript,
figures, declarations, cover letter, data availability, and source-data inventory.
```

```text
Use $prepare-journal-manuscripts in revision-response mode to account for every editor and reviewer
comment and synchronize the response, clean manuscript, and marked manuscript.
```

Python 3.9 or later is required for the bundled validators. Current official
journal-specific instructions override any editorial preset or dated source map.

## Test

From the repository root:

```bash
python3 packages/journal-manuscripts/skills/prepare-journal-manuscripts/components/abstract/tests/run_selftest.py
python3 -B -m unittest discover -s packages/journal-manuscripts/tests -p 'test_*.py'
python3 scripts/check_public_content.py .
find packages/journal-manuscripts -type l -print
```

An empty `find` result is expected. Validator success checks local record completeness;
it does not establish scientific truth, statistical validity, repository access, or
journal acceptance. The tools do not upload, contact editors, or submit. Original
instructions, tests, and scripts are covered by the repository's Apache-2.0 licence.
