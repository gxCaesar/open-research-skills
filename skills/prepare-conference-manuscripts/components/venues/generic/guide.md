# Generic peer-reviewed computing venue profile

Use this component only after reconciling the exact venue, track, year, and stage from
current first-party instructions. It supplies a task-local profile shape; it does not
state rules for any particular conference.

Copy the [profile template](references/venue-profile.template.json) into the manuscript
workspace and replace every `REPLACE_WITH_*` field, the zero-valued year, and every
zero-valued PDF dimension with facts from the current official author guide. Record source
IDs in `rule_sources`.
Do not modify the bundled AAAI or ICLR profiles to impersonate another venue.

The [profile field schema](references/venue-profile.schema.md) identifies the contract
used by the bundled source and PDF auditors. Choose a neutral `style_rule_id`, such as
`VENUE_STYLE_CURRENT`, or a venue-specific ID such as `SYNTHETIC_STYLE_CURRENT`; the
TeX audit emits that configured ID rather than applying an ICLR label.

With `SKILL_DIR` set to the installed `prepare-conference-manuscripts` directory, run
the auditor against the task-local profile:

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" /path/to/paper.tex \
  --profile /path/to/task-local-venue-profile.json \
  --stage anonymous_submission
```

The profile is an engineering aid. It cannot establish that a rule is current, that a
template renders correctly, or that a submission portal accepts an artifact.
