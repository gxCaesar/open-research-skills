# Executing the artifact

One lens does not read the released material. It runs it, from the released package
only, in a directory that contains nothing else.

## The procedure

Unpack the artifact exactly as a reader would receive it. Follow its own instructions
without consulting the working repository, the authors, or memory of how the project is
laid out. Where the instructions are ambiguous, take the reading a stranger would take
and record that you did.

Run whatever the artifact claims to reproduce. Capture every command and its output
verbatim, including the failures, the version conflicts and the missing files.

## What counts as a finding

| Reported | Status |
|---|---|
| The command was run and produced this output | Finding |
| The command failed with this error | Finding, and usually the most valuable one |
| The package contains a script that should reproduce the figure | Not a finding |
| Installation appears straightforward | Not a finding |
| The environment file lists the dependencies | Not a finding |

A reproducibility lens that never executed anything must say so in one sentence at the
top of its report. An unmarked report of that kind is worse than no report, because the
adjudication will treat it as evidence.

## Reporting the gap

Distinguish three outcomes: the claimed result was reproduced, the artifact ran but
produced something different, and the artifact did not run. The second is a finding about
the paper. The third is a finding about the package, and it is repairable before
submission, which is the entire reason the panel is run early.

Record the environment: interpreter version, platform, and how long the run took. A
result that reproduces only on the authors' machine is a finding too.
