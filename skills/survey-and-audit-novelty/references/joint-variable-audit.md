# The joint random-variable audit

The question is not whether each variable the hypothesis needs is available somewhere.
It is whether they are observed on the same samples, in one collection you can obtain.

## Producing the table

List the variables the hypothesis relates. For each candidate source, count the samples
carrying every one of them, not the samples carrying each one separately. The output is a
table of joint counts with the source, the accession or release, and the date checked.

Produce this table before writing analysis code. Once code exists, an empty intersection
is discovered late and usually gets rationalised into a smaller question.

Check the counting tool against the file's real format before trusting a count. Read the
bytes, not the assumed format: line endings, quoting, an index column, a header repeated
mid-file, an identifier stored as a number. A line-oriented field splitter run over a file
with foreign line endings silently attributes the terminator to the last column and can
return a count that is the exact opposite of the truth, with no error. Verify on a case
whose answer you already know, and build that case in the same format as the material, not
in the format your tool prefers.

## Reading an empty intersection

An empty cell closes a source, not a direction. Three moves follow, and a report that
skips them and concludes "the data does not exist" has overstated its evidence.

**Widen or substitute the source.** Repositories differ in what they record; a second
archive, a consortium release, or a supplementary table attached to a paper often carries
the pairing the primary source drops.

**Relax the matching level.** Exact identity matching between two vocabularies frequently
yields nothing while a coarser but still meaningful unit — a pathway, a complex, a
mechanism class, a grouped category — yields a usable count. State the level you used and
what it costs in interpretation.

**Assemble the pairing yourself.** Linking two sources on a shared identifier is a
legitimate contribution when the linkage is documented, the failure rate is reported, and
the assembled set is released.

## Recording the result

| Field | Content |
|---|---|
| Variables | The exact fields the hypothesis relates |
| Sources checked | Each with its release or accession and the date |
| Joint count | Samples carrying every variable, per source |
| Matching level | Exact, or the coarser unit used, with its cost |
| Disposition | Proceed, widen, relax, assemble, or stop |

The count with its procedure is reusable. The same count without the procedure will be
re-derived by the next person at full cost.
