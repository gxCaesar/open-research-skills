# Manuscript-core component

This component provides local, deterministic checks for source, PDF, archive, and
review-report artifacts. It does not replace current venue instructions or rendered
inspection.

With `SKILL_DIR` set to the installed skill directory, use the
[TeX auditor](scripts/audit_tex.py), [PDF auditor](scripts/audit_pdf.py),
[archive auditor](scripts/audit_archive.py), and
[review-report validator](scripts/validate_review_report.py) with a current venue or
task-local profile. Start a review report from the
[portable template](assets/review-report-template.json) and read the
[review-report contract](references/review-report-contract.md) before promoting an
automated finding into a scientific or compliance conclusion.
