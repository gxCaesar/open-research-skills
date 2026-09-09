# Building an anonymized package

Double-blind review asks that the package not reveal who wrote it. The failure modes are
mechanical, and they are found by scanning the built package rather than by intending to
be careful.

## Where identity survives

Version control history, including commit author fields, committer emails and the remote
URL. A repository copied with its history carries every one of them.

Absolute paths in configuration files, notebooks, logs and environment exports. A home
directory name identifies a person; a cluster hostname identifies an institution.

Document and image metadata: author fields in office files and PDFs, camera or software
tags, and revision histories inside the file format.

Package and citation metadata: author lists, funding acknowledgements, licence headers
naming a group, and a project name that is searchable back to a public repository.

Filenames. A file named after a lab, a person or an internal project defeats a clean file
body.

## What to do instead of removing history

Build the package from a fresh directory containing only the allowlisted files, with no
version control metadata at all. Removing history from a copy is harder to verify than
never including it.

## Keep it usable

An anonymized package still has to run. Replace identifying paths with relative ones
rather than deleting the lines, keep the licence and third-party notices, and provide the
data access route even where the account that has access is yours.

Where anonymity and reproducibility genuinely conflict, say so in the package in one
sentence, and give the reviewer the closest runnable substitute.

## Before submitting

Run the identity scan on the built package. Then unpack it somewhere else and read the
top-level files as a stranger would: the title, the readme, the citation file, the first
comment in the entry-point script. Those five places carry most of what leaks.
