---
name: release-research-artifacts
description: Use when packaging the code and data a reader or reviewer will download, including releasing the code for a paper, building an anonymized repository for double-blind submission, preparing an archive with a DOI for a journal, writing citation metadata, producing a data card or model card, or preparing a submission for artifact evaluation. Use once the results are frozen, so that what ships is what produced them.
---

# Release Research Artifacts

Build the package someone else downloads, then verify the package rather than the
workspace it came from. Almost every release defect is invisible from inside the working
directory, because the working directory contains the missing file.

## Select one mode

| Mode | Responsibility | Read first |
|---|---|---|
| `anonymized-submission` | Build a package that carries no author or institution identity, for double-blind review | `references/anonymized-submission.md` |
| `named-archive` | Build the citable, deposited version with persistent identifiers | `references/named-archive.md` |
| `data-card` | Describe the data and any model well enough to be used without asking you | `references/cards.md` |
| `manifest-verification` | Prove the built package is complete, runnable and unchanged | `references/verification.md` |

## Resolve the installed skill and components

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through a package parent.

## Resolve the file set by allowlist

List what goes in. Do not build the package by excluding what should stay out.

An exclusion list is a claim about everything you did not think of, and the things nobody
thinks of are exactly the ones that carry identity: editor backup files, notebook
checkpoints, cached credentials, environment dumps naming a home directory, log files with
absolute paths, and files with no extension that a text scan skips by default.

Write the allowlist as paths and patterns, resolve it into an explicit file list, and
review that list before staging. The reviewed list is the artifact; the command that
produced it is not.

## Stage, then scan every byte

Copy the allowlisted files into an empty staging directory. Scan the staged tree, not the
source tree, for author names, institutions, email addresses, absolute home paths,
internal hostnames, project codenames, credentials and tokens.

Scan file contents and file names. Scan inside container formats that hold text: office
documents, notebooks, archives. A scanner that reads only files with known text
extensions will pass a tree whose cache files are the leak.

Seed a known string that should be caught and confirm the scan catches it. A scan
reporting zero findings on a clean tree and a scan that is silently not running produce
the same output.

Plant the seed in the real formats the tree actually holds, not in a convenient one. A
seed placed in a plain text file proves only that the scanner reads plain text files; the
formats that leak are the notebook output cell, the archive member, the office document
body and the file name itself. A control built in a format the tool already handles
validates the control, not the tool.

## Test inside the built package

Unpack the built archive into an empty directory and run the project's own test or
reproduction command there, with no access to the working repository.

This is the step that catches the file that was never committed, the import that resolves
only because of the working directory, the data path that points outside the package, and
the dependency that is installed on your machine and nowhere else.

A test run in the workspace proves nothing about the archive.

## Record what shipped

Write a listing of the released files with their sizes and a cryptographic hash for each,
computed over the built package. Record the commit the package was built from, the
interpreter and dependency versions used for the verification run, and the date.

Someone who downloads the package later needs to answer two questions from that record
alone: is this the same package, and what produced it.

## Boundaries

This skill builds and verifies the package. It does not write the availability statements
that point at it, does not grant rights you do not hold over third-party data, and cannot
make a restricted dataset shareable. Where the data cannot be released, the package
carries the access route and the exact identifiers instead, and says which.
