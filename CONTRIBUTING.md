# Contributing

Keep each exact skill directory self-contained and expose only one public `SKILL.md` per package.
Put focused guidance or implementation below it under non-triggering `components/`, `shared/`, or
`references/` directories. Document runtime dependencies and preserve the package's
ownership boundary with the other four skills.

Use a topic branch and a pull request for shared changes. Summarize the affected skill,
the demonstrated problem, the focused verification and any unrun checks. Ask another
maintainer to review changes to validators, scientific boundaries or public packaging;
small prose corrections do not need a new workflow or additional gate. The hosted
test workflow is optional and manual-only; do not describe unrun CI as passing.

For a validator or contract change, include one clean fixture that passes and one
known-bad fixture that fails for the intended reason. Run the smallest package test
first, then the root suite and public-content scanner. Inspect generated or rendered
artifacts when a structural test cannot establish their quality.

Do not contribute credentials, private correspondence, applicant or reviewer records,
personal writing profiles, machine-specific paths, hidden prompts, internal workflow
state, authorization records, execution traces, public-facing integrity sidecars, or
third-party assets without confirmed redistribution rights. Use current first-party
sources for time-varying venue, funder, publisher, repository, and policy claims.

Before opening a change, run:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_public_content.py .
find packages -type l -print
```

For a real release candidate, keep project-specific names and host identifiers in a private
newline-delimited file outside the checkout and run
`python3 scripts/check_public_content.py . --deny-term-file /path/to/private-deny-terms.txt`.
Do not commit that file or its terms.

The scanner reads UTF-8 text and the XML parts inside PPTX files, including document properties,
speaker notes and relationships. Its scan count includes those XML parts. It rejects Finder
metadata and unreadable PPTX files, and redacts private deny terms from reported filenames.
Other binary assets still need metadata inspection and human review before publication.

Also run the affected package's tests and validate its sole skill with the runtime's
skill validator.
