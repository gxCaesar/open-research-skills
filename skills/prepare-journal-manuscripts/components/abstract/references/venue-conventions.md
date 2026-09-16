# Venue conventions and editorial presets

Venue requirements change. Establish them in this order:

1. the current submission form for the exact venue and track;
2. the current official call, author guide, or journal instructions;
3. an explicitly dated local profile;
4. the checker's editorial preset as a drafting fallback.

Record whether each constraint is an `official_rule`, `editorial_default`, or
`unverified`. Never convert a convention into a hard rule.

## AAAI profile

The bundled AAAI preset is **150–200 words, one paragraph, and no citations**. This is
an editorial target inherited from the focused AAAI abstract workflow, not an official
AAAI-27 word-limit claim.

Checked on 2026-09-04, the official AAAI-27 submission instructions required a complete
title and abstract by the abstract deadline, rejected placeholder abstracts, and warned
against substantial abstract changes before the paper deadline. The public instructions
did not state a 150–200-word limit or an abstract-specific citation ban. Confirm the live
OpenReview form before submission:

- https://aaai.org/conference/aaai/aaai-27/submission-instructions/

Use `--venue aaai` when the author chooses this editorial target. Otherwise pass the
live form's explicit limits.

## Bioinformatics profile

Checked on 2026-09-15 against the current Oxford Academic Bioinformatics
Author Guidelines.

For Original Papers, Bioinformatics uses a structured abstract with five
headings:

- Motivation
- Results
- Availability and Implementation
- Contact
- Supplementary Information

The journal recommends a maximum of 150 words. The current guidance also
explicitly permits internet hyperlinks in the abstract where applicable.

Application Notes use a different four-heading structure:

- Summary
- Availability and Implementation
- Contact
- Supplementary Information

The bundled `bioinformatics` preset therefore targets the Original Paper
editing shape. Its 100-word lower bound remains an editorial drafting
guardrail inherited from the existing preset; it is not presented as an
official Bioinformatics minimum. The upper bound is updated to the current
150-word recommendation.

The preset preserves the existing citation/DOI guard while allowing ordinary
URLs, because the first-party guidance explicitly permits hyperlinks. Passing
`--forbid-citations` explicitly disables this URL exception and restores the
strict citation/URL check.

Application Notes are documented here but are not assigned a separate numeric
preset because the current guidance describes them as much shorter without
giving a numeric abstract word limit in that section.

As with every bundled venue preset, this remains an editorial drafting aid
rather than a substitute for checking the current instructions for the exact
article type and submission stage.

First-party source:

- https://academic.oup.com/bioinformatics/pages/author-guidelines

## Other bundled presets

`scripts/check_abstract.py --venue list` prints all available editing presets. They are
convenience defaults for drafting and local QA; they are not a substitute for current
official rules. In particular, presets for venues without a public hard word cap use a
broad editing range rather than claiming a submission limit.

Explicit `--min-words`, `--max-words`, and `--max-paragraphs` values override a preset.
`--forbid-citations` can tighten a preset when the current instructions prohibit
references or URLs.

## Structured abstracts

When a journal requires headings, map the shared argument into its exact schema. For a
common Background/Methods/Results/Conclusions form:

- Background: problem and gap;
- Methods: approach, mechanism, and evidence setup;
- Results: locked results with units, comparator, and uncertainty;
- Conclusions: answer and boundary.

Set `--max-paragraphs` to the number of required blocks. Do not invent a generic IMRaD
format when the journal names different headings.

## Anonymity and references

Check the exact track. If review is anonymous, remove author-identifying material from
the abstract. If references, URLs, or repository links are forbidden, run the checker
with `--forbid-citations`. A citation policy for the paper body does not automatically
establish a citation policy for the abstract field.
