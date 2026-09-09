# Proposal workspace

This directory separates official authority, evidence, topic choice, scientific argument,
human-authored sections, figures, review findings, and final-format evidence.

1. Read `project.json` and confirm the current authoring-policy mode. A bundled profile
   is working-mode routing only; final mode needs a completed current refresh.
2. Register every opened official or scientific source in `authority/source-register.csv`.
   For each final policy source, bind its source ID to one `authority_kind` (`funder` or
   `institution`), program, year, scope, checked date, and the completed live-refresh ID
   in `project.json`. The two authority kinds need different source IDs and distinct
   `(issuer, url_or_path, clause_locator)` identities; one joint document needs distinct
   clause locators.
3. Register final-role sources separately: `official_authority` / `official authority`,
   `official_template` / `official template`, and
   `financial_budget_requirement` / `financial budget requirement`. Each must match the
   project program/year and final `as_of`; a local template source path must equal
   `official_template.artifact_path`.
4. Link every load-bearing claim in `evidence/claim-ledger.csv` to a registered source.
5. Compare candidates before freezing a route.
6. Complete the Q/C/V/O/CL/F argument graph before expanding section briefs.
7. In `budget/financial-budget.json`, record the current program/project decision on
   whether a financial budget is required; complete it only when required.
8. In `commitments/commitment-records.json`, record each research content, annual task,
   and output with its own primary class, finite bound, stop rule, dependencies, and sequence.
9. Use the current official system template for final formatting; it is not bundled here.
10. Run the validator in working mode during development and final mode only on the exact
   applicant-reviewed local candidate. Final validation defaults `--as-of` to today;
   use an explicit historical override only for an archived snapshot.

Validation does not submit anything and does not establish funding, acceptance, or policy
compliance by itself.
