# ICCV 2025 official sources

Checked on 2026-09-10 for the Main Conference. The profile's hard rules map only to the
`VERIFIED` first-party records below; refresh them before a real submission.

| ID | Status | Official source | Checked scope |
|---|---|---|---|
| `ICCV2025_AUTHOR_GUIDELINES` | `VERIFIED` | <https://iccv.thecvf.com/Conferences/2025/AuthorGuidelines> | page limit, anonymity, supplement boundary, consequences of non-compliance |
| `ICCV2025_CALL_FOR_PAPERS` | `VERIFIED` | <https://iccv.thecvf.com/Conferences/2025/CallForPapers> | dual-submission window and submission deadline |
| `ICCV2025_AUTHOR_KIT` | `VERIFIED` | <https://media.eventhosts.cc/Conferences/ICCV2025/ICCV2025-Author-Kit-Feb.zip> | document class and options, style package and its review/rebuttal/camera-ready modes, page-number rule |
| `ICCV2027_AUTHOR_GUIDELINES` | `NOT_FOUND` | <https://iccv.thecvf.com/Conferences/2027/AuthorGuidelines> | returned HTTP 404 on 2026-09-10; iccv.thecvf.com presented ICCV 2025 only, with no 2027 entry in its year selector |

ICCV is biennial, so the dated scope above is the most recent completed cycle rather than
an upcoming one. Nothing here is inherited by ICCV 2027. Run `recon` against the 2027
pages when they appear, and do not carry the deadline or the kit edition forward.

The author kit is the shared CVPR/ICCV/3DV template, which is why the LaTeX contract
matches the CVPR adapter's. That is a fact about the kit, verified by opening it, not an
assumption that the two venues share policy: the page limit, the supplement rule and the
rebuttal boundary are read from ICCV's own pages.

## What the pages state, verbatim

Page limit and consequences, `ICCV2025_AUTHOR_GUIDELINES`:

> Papers are limited to eight pages, including figures and tables, in the ICCV style.
> Additional pages containing only cited references are allowed.

> Papers that are not properly anonymized, or do not use the template, or have more than
> eight pages (excluding references) will be rejected without review.

Anonymity, `ICCV2025_AUTHOR_GUIDELINES`:

> ICCV reviewing is double blind, in that authors do not know the names of the area
> chairs or reviewers for their papers, and the area chairs/reviewers cannot, beyond a
> reasonable doubt, infer the names of the authors from the submission and the additional
> material.

Posting a submission to arXiv is answered "Yes." on the same page.

Supplementary material, `ICCV2025_AUTHOR_GUIDELINES`:

> Reviewers will be encouraged to look at it, but are not obligated to do so.

The same page states there are no formatting requirements for PDFs in the supplementary
material. A numeric file-size cap is not stated.

Dual submission and deadline, `ICCV2025_CALL_FOR_PAPERS`:

> no paper substantially similar in content has been or will be submitted to another
> conference or workshop during the review period (March 7, 2025 – June 20, 2025)

> The paper and supplementary materials submission deadline is March 7th, 2025 11:59pm
> HST and will not be changed.

Page numbering, `ICCV2025_AUTHOR_KIT`, `sec/2_formatting.tex`:

> The review version should have page numbers, yet the final version submitted as camera
> ready should not show any page numbers.

## Not established

| What | Where it was searched |
|---|---|
| A rebuttal page limit | ICCV 2025 AuthorGuidelines and CallForPapers; the kit ships `rebuttal.tex` but states no page count. The CVPR one-page limit is not inherited. |
| A supplementary file-size cap in numbers | ICCV 2025 AuthorGuidelines, which refers to supplementary material without giving a size |
| Whether an appendix may sit inside the main PDF | ICCV 2025 AuthorGuidelines allows additional pages "containing only cited references" and states no permission for an appendix. Treat an in-paper appendix as unsupported rather than forbidden by a quoted sentence. |
| Any ICCV 2027 rule | iccv.thecvf.com on 2026-09-10, see the `NOT_FOUND` row above |

An earlier internal record for this venue quoted a sentence forbidding an appendix in the
main paper. That sentence was not present on the page when it was re-read on 2026-09-10,
so it is recorded here as not established rather than carried forward.
