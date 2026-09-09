# Synthetic demonstration

This is a complete, synthetic local record demonstration. From an installed
`research-publication-pipeline` directory, run:

```bash
python3 examples/run_demo.py OUTPUT_DIRECTORY
```

Or resolve the script directly:

```bash
python3 /path/to/research-publication-pipeline/examples/run_demo.py OUTPUT_DIRECTORY
```

`OUTPUT_DIRECTORY` must be a new directory outside the installed skill. The
demo refuses an existing path, including a populated directory, without
changing its contents. On success it creates a synthetic workspace and prints
the observed `PASS` status for `pilot`, `development`, and `handoff`.

The generated workspace is a runtime output, not part of the installed skill
or a release artifact. Its records exercise only the local validator contract.
They are not real data, a research experiment, locked-test access,
authorization, publication, or evidence of scientific effectiveness.

## Rehearse a small code release

Add the optional flag to exercise packaging and execution, not just record checking:

```bash
python3 examples/run_demo.py OUTPUT_DIRECTORY --with-public-release
```

This creates a ten-file synthetic code tree under `OUTPUT_DIRECTORY/public-release/`,
packages it, and unpacks it in a fresh temporary directory. It runs the two fixed
README commands: a standard-library arithmetic example and its two unit tests. It
checks the produced JSON against the documented `{"count": 3, "total": 6}` result,
then runs the `public-release` validator. Success adds `public-release: PASS` to stdout.
A failed command or incorrect output causes a nonzero exit and a failed rehearsal record.

The observed output is retained at `results/public-release-example.json`; actual
commands, outputs, exit codes, and the environment are recorded in `handoff/handoff.json`.
Both stay outside the curated code tree. The temporary archive and unpack are removed
automatically. The rehearsal uses the current Python interpreter without installing
dependencies or claiming a separate clean environment. It does not execute arbitrary
commands from project records or publish anything. All surrounding scientific records
remain synthetic; successful arithmetic is not a research result.
