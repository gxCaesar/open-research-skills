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
