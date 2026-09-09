# Proving reviewer isolation

The panel's only advantage is ignorance. Every leak of the project's own framing removes
part of the reason to run it.

## Construct the reviewer's directory

Assemble a directory holding exactly what an external reviewer would receive: the
manuscript as it would be submitted, the figures at their submission resolution, the
supplementary material, and the artifact as released. Nothing else.

Leave out the planning documents, the survey, the iteration ledger, the internal
correspondence and the earlier drafts. Those are the material that repairs a reviewer's
misreading before it happens, which is precisely the misreading you are trying to observe.

## Record the manifest

Write the directory listing with sizes and modification times into the round's output.
That listing is the isolation manifest. It is an observation about the filesystem, and it
survives disagreement about what a reviewer "had in context".

Do not substitute a reviewer's own statement about its inputs. A model asked what it can
see produces a plausible description, not a measurement, and it will describe a clean
context whether or not the context is clean. The same caution applies to a claim that a
subagent started fresh: prove it by construction and by listing, not by asking.

## Between rounds

A second round is only cold if the second panel has not read the first. Keep rounds in
separate directories, and do not carry the previous meta review into the new reviewers'
inputs. Carrying it forward turns round two into a check of whether the repairs were
applied, which is a useful but different exercise, and should be labelled as such.
