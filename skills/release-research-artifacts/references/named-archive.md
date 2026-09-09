# Building the citable archive

The named version is the one that outlives the submission. It is deposited, it has a
persistent identifier, and it is what a reader five years later actually downloads.

## Deposit rather than link to a working repository

A repository URL points at a moving target and can disappear. Deposit the built package
with an archive that issues a persistent identifier, and cite that identifier in the
paper. Keep the development repository as well, but do not make it the only route.

Reserve the identifier before the manuscript's availability statement is written, so the
statement can name it rather than promise it.

## Version the release

Tag the exact state the paper describes and deposit that state. A later fix gets a new
version and a new identifier, with the original left in place: a reader following the
paper must land on what the paper describes, not on the improved version.

## Citation metadata

Ship a machine-readable citation file so that the package can be cited correctly without
guessing. Record the authors with their persistent researcher identifiers, the title, the
version, the persistent identifier of the deposit, the licence, and the date.

State the licence for code and for data separately. They are frequently different, and a
single licence line covering both is usually wrong about one of them.

## Third-party material

List every included third-party component with its origin, version and licence, and keep
its notices. Confirm redistribution rights for data before including it: a dataset you
were granted access to is often not a dataset you may redistribute, and the access route
belongs in the package instead.

## What the deposit should contain

The allowlisted source, the environment specification pinned to versions, the data or its
access route, the cards describing data and model, the citation file, the licence and
notices, the record of what shipped, and instructions that were followed by someone who
had never seen the project.
