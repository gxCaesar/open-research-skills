# Routes and statement wording

## Picking the route

Work down this order and stop at the first one you can honestly claim.

**Archived with a persistent identifier.** Deposit the exact state the paper describes
and cite the identifier of that version, not of the concept record. This is the only
route that still works when the repository moves.

**Public repository.** Acceptable while drafting. Before final, deposit the tagged
version as well: a URL identifies a location, and the paper needs to identify a state.

**Within the paper or supplement.** Suitable for short, self-contained code. It carries
no dependency resolution, so name the environment it was run in.

**Reused public.** Cite the implementation at the version you actually ran. "The
official implementation" without a version does not identify what produced your numbers.

**Third-party restricted.** Name the controller, the conditions, and what a reader can
still do without it. The last part is what makes the statement usable rather than an
apology.

**Justified request.** The weakest answer. It needs a durable contact that outlives a
graduate student's address, who qualifies, and a response window. Several journals no
longer accept it for code central to the conclusions.

**Not applicable.** Only when no code underlies the claim, with the reason stated. Custom
code behind a figure never qualifies.

## What a usable statement contains

For each component: what it is, where it is, at which version, under which licence, and
what a reader needs installed. A statement that omits the version is the most common
failure, and it is the one that makes the rest unusable.

## Wording that does not survive review

| Written | Problem |
|---|---|
| Code will be made available upon reasonable request | Promises rather than provides; the reader cannot act, and "reasonable" is undefined |
| Code is available at <repository URL> | No version, no licence, no environment; the URL may not hold the state described |
| Code available upon publication | The reviewer needs it before publication, and the sentence often survives into the published paper |
| Standard software was used | Names nothing; a reader cannot tell what to install |
| Custom scripts are available from the corresponding author | Same as the first row, with a contact that changes when the author moves |

## Before submitting

Read the statement as someone who has the paper and nothing else. If you cannot list what
to install and at which version from the statement alone, it is not finished.
