# Evidence and provenance

Use the smallest applicable label:

| Label | Meaning | Required support |
|---|---|---|
| `[Paper]` | directly reported or claimed by the paper | page, section, figure, table, equation, or source-block pointer allowed by the locator mode |
| `[External]` | supported by a source outside the paper | direct citation and access level |
| `[Analysis]` | reasoned interpretation from identified evidence | reasoning plus relevant source pointers |
| `[Hypothesis]` | testable, unverified explanation or direction | proposed test and falsifier |
| `[User]` | judgment or connection supplied by the user | the user's supplied statement or source |

For external evidence, record `full-text verified`, `abstract-only`, `metadata-only`, or
`unavailable`. Abstract and metadata records can establish bibliographic facts but not
detailed method, result, or negative novelty claims.

## Pointers

Use only locators established by the source:

```text
[Paper: PDF p. 3, Figure 2]
[Paper: Methods, Training objective]
[Paper: S041]
[Paper: Abstract]
```

In page-grounded mode, `PDF p. N` is the file page index. In structure-grounded mode,
omit every page number. In source-limited mode, use only `Abstract`, `Metadata`, or
`User-provided excerpt`.

When a claim comes from a display, cite the display and caption. Add the relevant Methods
or Results pointer when interpretation depends on prose. Mark unreadable equations or
image-only symbols low-confidence or not assessable; do not reconstruct them from
context.

## Claim strength and conflicts

Use verbs that fit the design: `reports`, `observes`, `is associated with`, `supports`,
`is consistent with`, or `suggests`. State necessity, sufficiency, causality, mechanism,
or generalization only when the design directly earns it.

When prose, figures, tables, or supplements disagree, record both values and locations,
mark the affected conclusion uncertain, and name the evidence needed to resolve it.
