---
name: review-others-manuscripts
description: Use when acting as an invited referee on someone else's submission, including writing a referee report, drafting reviewer comments, assessing a revision round against the authors' response letter, running an editorial prescreen for scope and policy, or judging whether a stated claim is carried by the evidence in a manuscript under review. Use for a manuscript that is not yours and is confidential; rehearsing objections against your own unsubmitted paper is a different task.
---

# Review Someone Else's Manuscript

A referee report answers one question for the editor: is each claim carried by the
evidence offered for it, and if not, what would carry it. Everything else in the report
serves that question.

The manuscript is confidential and belongs to its authors. That constraint shapes what
you may do with it before it shapes what you write.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `initial-review` | First-round report on a new submission | `references/claim-evidence-review.md` |
| `revision-round` | Check the response letter against the actual changes | `references/revision-round.md` |
| `editorial-prescreen` | Scope, fit and policy compliance before peer review | `references/prescreen.md` |
| `confidentiality` | Establish what may be done with the manuscript at all | `references/confidentiality.md` |

Read `confidentiality` before opening the manuscript in any tool. It constrains the other
three modes rather than following them.

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through a package parent.

## The confidentiality boundary

A manuscript under review is unpublished, non-public work shared with you for one
purpose. Do not redistribute it, do not quote it outside the report, do not use its
results in your own work before publication, and do not paste it into a service that
retains submissions unless the journal's own policy permits that service by name.

Declare a competing interest and decline where one exists. Reviewing a direct competitor's
submission while working on the same problem is a conflict even when you intend to be
fair, and the intention is not the test.

If you delegate any part of the reading, the confidentiality obligation travels with the
text. Whoever reads it is bound by the same terms, and the journal's policy decides
whether that delegation is permitted at all.

## Structure a report the editor can act on

Separate three things and never merge them.

**Claims and their support.** Take each claim the authors make and find the evidence
offered. Report the ones where the claim is broader than the support, naming the location
of both. This section is the report.

**Defects.** Problems that make a reported result unsafe: a leaked split, an undefined
metric, a comparator that was not given a fair budget, an independence assumption the
design violates, a statistical test whose assumptions the data breaks. State the
consequence, not only the deviation.

**Requests.** What would resolve each point. A request must be executable by the authors
with material they plausibly have. "Run a larger study" is not a request; "report the
per-site breakdown that the aggregate in Table 2 was computed from" is.

## Calibrate the severity

| Severity | Test |
|---|---|
| Fatal | The result would not survive the correction |
| Major | The result probably survives, but the paper cannot be judged until it is shown |
| Minor | The claim is unaffected; the presentation misleads |
| Taste | You would have done it differently and the paper is not worse for it |

Taste-level points belong in a short final paragraph or nowhere. Presenting them at major
severity is the most common way a report becomes unusable to an editor.

## Write for two readers

The editor needs a recommendation and the two or three points it rests on, near the top.
The authors need every point located and actionable. Write the report so that both are
served without a private section that contradicts the public one.

## Boundaries

This skill drafts a report; it does not decide acceptance and does not audit an author's
raw data. It does not rehearse objections against your own manuscript, and it does not
carry any individual's personal reviewing voice: the method is the transferable part.
