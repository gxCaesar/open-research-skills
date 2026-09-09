---
name: run-cold-review-panel
description: Use when a manuscript you wrote is nearly finished and needs a hostile read before it is submitted, including a mock review, a simulated reviewer panel, a pre-submission review, red-team the paper, asking whether this would get rejected, or checking which reviewer objection the paper cannot survive. Use for your own unsubmitted manuscript; reviewing someone else's submission as an invited referee is a different task.
---

# Run a Cold Review Panel

Read your own manuscript with reviewers that have never seen the project. The value comes
entirely from what they do not know: an author's summary of the work repairs, in the
reading, exactly the gaps a reviewer would have fallen into.

The panel is inbound. The manuscript is yours and has not been submitted.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `isolation-manifest` | Construct and prove the reviewers' context, from the filesystem rather than from assertion | `references/isolation.md` |
| `lens-assignment` | Assign the reading lenses and the model families that carry them | `references/lenses.md` |
| `artifact-execution` | Have one reviewer actually run the released artifact and report what happened | `references/artifact-execution.md` |
| `meta-review` | Adjudicate the reports into one decision with prioritised repairs | `references/meta-review.md` |

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through a package parent.

## Prove the isolation, do not assert it

A reviewer that has absorbed the project's own framing will reproduce it. The panel is
worthless unless each reviewer's inputs are known, and knowing them means constructing
them.

Build a review directory containing exactly what a reviewer would receive: the
manuscript, the figures, the supplementary material, and the artifact as released. Record
the listing of that directory, byte sizes included, as the isolation manifest.

A statement from the reviewer that it has no other context is not evidence. A model's
report about its own inputs is a description it generates, not an observation it makes.
The directory listing is the observation. Where the runtime permits it, start each
reviewer in that directory and nowhere else.

## Give the lenses different jobs

Five reviewers reading for the same thing produce one review five times. Assign distinct
lenses and keep them separate until adjudication.

| Lens | Reads for |
|---|---|
| Claim support | Whether each stated claim is carried by the evidence offered for it |
| Method correctness | Whether the procedure could produce the reported number at all |
| Comparison fairness | Whether the comparators were given a real chance |
| Reproducibility | Whether the released material lets someone else reach the result |
| Significance | Whether the result, if entirely true, matters to the stated audience |

Carry the lenses across more than one model family where that is available. Two families
disagree in different places, and the disagreements are where the manuscript is soft.

## One reviewer runs the artifact

At least one lens executes the released material rather than reading about it. Reports
that a package installs, that a command exists, or that a script "should" reproduce a
figure are not findings. What happened when it was run is a finding.

Record the commands and their output verbatim, including the failures. A panel that
never touched the artifact cannot speak to reproducibility, and should say so instead of
implying otherwise.

## Adjudicate, then prioritise

The meta review is not an average. Adjudicate each finding: confirmed, unsupported, or
needing evidence the panel did not have. A finding raised by one lens and missed by four
is not thereby weak; a finding raised by all five may still be wrong about the paper.

Order the surviving findings by what a real rejection would rest on, and state for each
what change would remove it and what that change costs.

## Boundaries

This skill produces a rehearsal, not an acceptance prediction. It cannot see the venue's
actual reviewer pool, the committee's calibration, or the competing submissions. It also
does not edit the manuscript: repairs are handed back to whoever owns the prose.
