# Review report contract

Use one report for compliance, scientific review, and revision planning. Automated
findings are candidates; inspect the cited artifact before promoting them into the
report.

## Basis

- `official_hard_rule`: a current, opened venue source states the requirement.
- `official_guidance`: a current, opened venue source recommends the practice.
- `manuscript_fact`: the source, rendered PDF, archive, or build log directly shows it.
- `scientific_judgment`: an evidence-grounded assessment of the paper's argument.
- `inference`: a plausible concern that still requires a settling check.

## Priority

- `P0`: a directly observed desk-reject risk, invalid scientific claim, anonymity
  breach, missing mandatory element, or artifact failure. Never assign P0 from an
  inference or an unverified rule.
- `P1`: likely review-impacting weakness, reproducibility gap, important inconsistency,
  or non-fatal format problem.
- `P2`: local clarity, economy, or polish improvement.

Every finding states one location, what was observed, what was expected, the impact,
the smallest valid action, and a verification step. Do not convert disagreement with a
reviewer into P0 unless an artifact or current rule establishes the defect.

Use the [review-report template](../assets/review-report-template.json) as the starting
record. With `SKILL_DIR` set to the installed skill directory, then run:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/validate_review_report.py" review-report.json
```

`PASS` means the report follows this data contract. It does not establish that a venue
rule is current, a claim is true, a paper is acceptable, or a portal upload succeeded.
