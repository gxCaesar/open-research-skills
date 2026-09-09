# Conference Manuscripts

This package exposes one public skill:
[`prepare-conference-manuscripts`](skills/prepare-conference-manuscripts/SKILL.md).
Its seven modes cover recon, drafting, audit, polishing, rebuttal, camera-ready work,
and final package checks without changing the locked scientific protocol.

For new or redesigned method, architecture, flowchart and motivation schematics, the
skill delegates to `build-scientific-visualizations`: GPT Image 2.5 concept generation
in the corresponding style, followed by native editable PPTX reconstruction and
manuscript-ready exports. Install that separate skill when figure construction is
needed; prose and audit tools remain independently usable. Data plots stay source-derived.

The registered skill is self-contained. A fresh installation needs only the exact
`skills/prepare-conference-manuscripts/` directory, which includes:

- local [AAAI](skills/prepare-conference-manuscripts/components/venues/aaai/guide.md),
  [ICLR](skills/prepare-conference-manuscripts/components/venues/iclr/guide.md),
  [ACL](skills/prepare-conference-manuscripts/components/venues/acl/guide.md),
  [CVPR](skills/prepare-conference-manuscripts/components/venues/cvpr/guide.md),
  [ICML](skills/prepare-conference-manuscripts/components/venues/icml/guide.md), and
  [NeurIPS](skills/prepare-conference-manuscripts/components/venues/neurips/guide.md)
  adapters, plus the [generic venue-profile](skills/prepare-conference-manuscripts/components/venues/generic/guide.md)
  fallback;
- local [manuscript-core](skills/prepare-conference-manuscripts/components/manuscript-core/guide.md)
  source, PDF, archive, and review-report tools;
- a complete [abstract workflow](skills/prepare-conference-manuscripts/components/abstract/guide.md)
  and [statistics-reporting workflow](skills/prepare-conference-manuscripts/components/statistics-reporting/guide.md).

Select an adapter by exact `venue/year/track` scope. Every profile is a dated engineering
aid, so run `recon` against current first-party sources when its scope is stale or does
not match the intended submission. Use the generic component only when no current
first-class profile matches; create a task-local profile instead of mutating a bundled
one. Each formal adapter links to paper observations that are optional empirical drafting
evidence, never venue rules or mandatory section order. The package contains no venue
style files, exemplar papers, private reviews, submission records, or portal automation.
For a compound whole-paper request that combines polish and package work, whether or
not it names audit, use the linked [whole-paper workflow](skills/prepare-conference-manuscripts/references/full-paper-workflow.md):
an unresolved P0, absent scientific contract, or unsupported load-bearing result is
`NOT READY` and stops polish and package progression.

## Install and invoke

Set `SKILL_DIR` to the installed skill directory. Python 3.9 or later is required; the
bundled PDF auditor uses the declared `pypdf==6.10.2` dependency.

```bash
SKILL_DIR=/path/to/prepare-conference-manuscripts
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
```

Every bundled command resolves from that directory, never from a sibling package:

```bash
# Expected failure: this deliberately short input is below the abstract word limit.
printf '%s' 'This deliberately short synthetic abstract demonstrates the word-count failure.' | \
  python3 "$SKILL_DIR/components/abstract/scripts/check_abstract.py" --venue aaai

python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$SKILL_DIR/components/statistics-reporting/examples/analysis-register.example.json" \
  --mode final

python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile "$SKILL_DIR/components/venues/aaai/references/venue-profile.json" \
  --stage anonymous_submission
```

```text
Use $prepare-conference-manuscripts in audit mode to review this anonymous ICLR paper against its
locked scientific contract and the current official venue profile.
```

```text
Use $prepare-conference-manuscripts in audit mode to review this ICML 2026 Main Track
anonymous manuscript; reject a camera-ready-only style option, then mark the Impact
Statement's substance and placement as manual checks.
```

```text
Use $prepare-conference-manuscripts to polish and package this ICML 2026 anonymous
manuscript. Follow the whole-paper workflow, retain a revision copy after the audit
boundary, return its six ordered deliverables, and stop at NOT READY if a P0,
scientific-contract, or load-bearing-evidence gate is unresolved.
```

```text
Use $prepare-conference-manuscripts in recon mode before preparing an ACL 2027 paper:
the local ACL 2026 profile is not an exact venue/year/track match.
```

```text
Use $prepare-conference-manuscripts in rebuttal mode to build a complete concern-to-evidence matrix
for these AAAI reviews without inventing results or promises.
```

## Test

For a package-maintainer checkout, define both bases explicitly:

```bash
PACKAGE_DIR=/path/to/conference-manuscripts
SKILL_DIR="$PACKAGE_DIR/skills/prepare-conference-manuscripts"
python3 "$SKILL_DIR/components/abstract/tests/run_selftest.py"
python3 -B -m unittest discover -s "$PACKAGE_DIR/tests" -p 'test_*.py'
```

The local tools do not upload, comment, save, or submit anything to a venue. Validator
success checks local record completeness; it does not establish scientific truth,
statistical validity, venue-rule currency, manual content/reference boundaries, visible
anonymity, portal state, or submission acceptance. Original instructions and code are
covered by the repository's Apache-2.0 licence.
