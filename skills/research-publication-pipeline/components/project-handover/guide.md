# Project-handover component

One question decides whether a handover worked: can a person who did not build this
project run it from the pack alone. Everything below is that question applied to a
specific part.

In the commands below, `$SKILL_DIR` is the resolved directory containing the entry
`SKILL.md`. This component sits under the `handoff` mode but answers a different question
from it: `handoff` transfers a locked scientific contract to manuscript or figure work,
while this transfers a running project to a person.

## Write the run layout before the run, not after

A run lives in a directory whose shape is fixed before anything starts:

| Path | Holds |
|---|---|
| `run.sh` | the exact command, reproducible without reconstruction |
| `env.txt` | the environment as it actually was, not as it was intended |
| `config.yaml` | the configuration that run used |
| `logs/` | captured output |
| `ckpts/` | checkpoints, pruned rather than accumulated |
| `results/` | the metrics, predictions and figures the run produced |

`run.sh` and `env.txt` are written **before** launching. A run that crashes at hour six
is still reproducible from what is on disk; a run whose command was only ever typed into
a terminal is not. `references/run-layout.md` covers what goes in each file.

## Build the pack

Start from `examples/handover-pack.example.json` and record the entry document, the run
layout, the pinned environment and how to create it, how the receiver obtains the data,
the first tasks, and what must not be changed.

A task needs four things or it cannot be started and finished by someone else: a goal, a
command, the output to expect, and a condition that says it is done. "Run the training"
is a goal with no command; "it should work" is not an expected output.

## Two answers that fail

**A command that names your machine.** An absolute home path or a named remote host in a
task command means the receiver has to translate before they can begin, and translation
is where a handover silently becomes a conversation. State the requirement, not your
setup.

**"Ask me."** A done-when that resolves to the author is not a done-when. If the receiver
genuinely cannot judge the result alone, that is a gap in the pack, and the fix is to
write the criterion down rather than to remain the criterion.

## Rehearse it with someone else

```bash
python3 "$SKILL_DIR/components/project-handover/scripts/validate_handover_pack.py" \
  /path/to/handover-pack.json --mode working --format markdown

python3 "$SKILL_DIR/components/project-handover/scripts/validate_handover_pack.py" \
  /path/to/handover-pack.json --mode final --format markdown
```

`final` requires a rehearsal, and requires that the person who ran it is not the author.
The author already knows what the pack leaves out, which is the entire difficulty. Record
what they ran, what happened, and what you changed as a result: the first rehearsal
almost always finds one missing step, and the record is what stops it being rediscovered.

## Boundaries

The validator reads the record. It does not run a command, check a path on any machine,
or confirm the rehearsal happened. It cannot tell you whether the receiver understood the
result, only whether the pack gave them something to act on.
