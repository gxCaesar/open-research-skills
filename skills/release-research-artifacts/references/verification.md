# Verifying the built package

Verification runs against the archive, from outside the project. Every check performed in
the workspace is answered by files the recipient will not have.

## The sequence

Build the archive from the staged, allowlisted tree.

Unpack it into an empty directory on a path unrelated to the project.

Install the declared environment from the package's own specification, pinned to versions.

Run the project's own test or reproduction command from inside the unpacked directory,
with no path pointing back to the working repository.

Compare what it produced with what the paper reports, and record both.

## What this catches

The file that was never committed. The import that worked only because the interpreter
was started in the project root. The data path that resolves outside the package. The
dependency present on your machine and absent from the specification. The script that
reads an environment variable set in your shell profile.

None of these is visible from the workspace, and all of them are fatal to a reader.

## Recording what shipped

Write one record listing every released file with its size and a cryptographic hash,
computed over the built package. Add the source commit, the interpreter and dependency
versions used during verification, the platform, and the date.

Two questions must be answerable from that record alone: is the copy in hand the same
package, and what state of the source produced it.

## Report the failures too

A verification run that did not reproduce a number is a finding to resolve before
release, not a detail to omit. Where a result cannot be reproduced within the package,
because it needs restricted data or hardware you cannot ship, say which result, why, and
what the closest runnable substitute is.

A package whose own instructions were never followed end to end by someone without prior
knowledge has not been verified.
