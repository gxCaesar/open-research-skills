# The run directory

A run is reproducible when its directory alone is enough to say what was executed, in
what environment, from which commit, and what came out. Reconstructing any of those from
memory afterwards produces a plausible answer rather than a true one.

## What each file holds

**`run.sh`.** The exact command, with every argument. Not a template, not a description.
A reader should be able to execute the file. Where a value comes from the environment,
set it in the file so the file remains complete.

**`env.txt`.** The environment as it actually was: the dependency listing, the commit,
and the interpreter version. Write it from the machine that will run the job, not from
the specification you intended to use.

**`config.yaml`.** The configuration this run used, copied rather than referenced. A
reference to a shared config that later changes silently rewrites what the run did.

**`logs/`.** Captured output, including stderr. A log that exists only in a terminal
scrollback is gone when the terminal closes.

**`ckpts/`.** The best checkpoint and the last few, not every epoch. Checkpoints fill a
disk faster than anything else in a project, and the ones in between are rarely used.

**`results/`.** Metrics, predictions and figures. These are small, and they are what
someone else reads first.

## Write it before launching

The two files that must exist before the run starts are `run.sh` and `env.txt`. Both are
about the state at launch, and both become guesses once the run is over. A job that dies
at hour six is fully reproducible if they exist and only approximately reproducible if
they do not.

## What the receiver needs from the layout

A receiver reading this directory should be able to answer four questions without asking:
what command produced this, in what environment, from which commit, and where the numbers
in the write-up came from. If any answer requires the author, the layout has a gap, and
the gap is worth fixing before the handover rather than during it.

## Naming

Use a dated, meaningful directory name rather than an incrementing number. `20260910-
baseline-seed42` says what it is a year later; `run7` does not, and by then the person who
knew is elsewhere.
