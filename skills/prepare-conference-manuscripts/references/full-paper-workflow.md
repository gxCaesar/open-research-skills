# Whole-paper workflow

Use this recipe when one whole-paper request combines polishing and a package, whether
or not it names audit.
It composes the existing modes; it does not create an eighth mode. Keep one primary
mode per pass and use the existing [venue routing](../SKILL.md),
[adversarial audit](adversarial-audit.md), and
[manuscript lifecycle](manuscript-lifecycle.md) guidance for their respective checks.

## Pass order

1. **Intake.** Identify the venue, year, track, stage, canonical source, PDF,
   bibliography, supplement, figures and tables, checklist or disclosure, reviewer
   material, locked scientific contract, and evidence anchors. Mark missing artifacts
   explicitly.
2. **Conditional recon.** If the requested scope does not exactly match a dated
   adapter, or current first-party authority is unresolved, run `recon` before the
   next pass. Do not make a local profile impersonate the requested venue.
3. **Audit gate.** Run `audit` before editing. Build the claim-evidence map and
   P0/P1/P2 report. An unresolved P0, absent scientific contract, or unsupported
   load-bearing result is `NOT READY`; stop polish and package progression.
4. **Revision-copy polish.** Only after the audit gate passes, use `polish` on a
   revision copy. Keep the locked scientific contract immutable: do not change a
   number, comparison direction, qualifier, split, metric, or result, and do not
   choose a favorable result or slice. Default to a revision copy. Explicit author
   permission covering canonical edits after a passing audit remains valid; do not
   ask for it again merely because the audit finished. Seek new permission only if
   the audit reveals a material scope change or a mutation outside that authorization.
5. **Re-audit and package.** Audit the revision copy, then use `package` on the
   exact candidate source, rendered PDF, supplement, figures, checklist, disclosure,
   and archive. Reconcile their claims before marking local readiness.

Automated checks do not settle rendered-PDF identity or layout, semantic adequacy,
content/reference boundaries, live portal state, or acceptance. List these as manual
checks and keep them `not_run` until they are actually inspected or confirmed.

## Ordered outputs

Return these outputs in this order, using the reusable
[whole-paper deliverable skeleton](../assets/full-paper-deliverables.md):

1. intake and missing-artifact summary;
2. claim-evidence map;
3. P0/P1/P2 review report;
4. ordered revision plan;
5. revision-copy diff or a clear `not_run` explanation;
6. final verification summary with `READY` or `NOT READY` and manual checks.
