# Synthetic demonstration

This is a complete, synthetic local record demonstration. For a readable output sample,
open the [result-to-paragraph walkthrough](result-to-paragraph.md). It separates the
arithmetic result actually computed by the example from the unmeasured scientific
claims that a real paper would need to establish.

## Five-minute run from the repository

Python 3.9+ and its standard library are sufficient. No package installation, API key,
network, remote machine or agent runtime is needed:

```bash
demo_root=$(mktemp -d)
python3 -B skills/research-publication-pipeline/examples/run_demo.py "$demo_root/publication-demo" --with-public-release
```

The shell example uses macOS/Linux syntax; another shell can supply a new temporary
path instead. The generated workspace stays outside the checkout and must not become
public research evidence. The linked walkthrough is the curated public sample.

For only the record demonstration, omit `--with-public-release`. From an installed
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

## Expected results and where to look

With `--with-public-release`, the observed status lines are:

```text
pilot: PASS
development: PASS
handoff: PASS
public-release: PASS
```

The ordinary run without that flag prints only the first three status lines. Both runs
also print a synthetic-use warning and the output location. A successful exit is zero.

| Output path, relative to the generated workspace | What to inspect |
|---|---|
| `START_HERE.md` | Local project navigation |
| `results/public-release-example.json` | The actually computed `{"count": 3, "total": 6}` result; only present with the flag |
| `public-release/README.md` | The two commands actually rehearsed on the packaged example |
| `public-release/src/example.py` | The arithmetic implementation |
| `public-release/tests/test_example.py` | One non-empty input test and one empty-input test |
| `results/final-comparison.json` | A synthetic marker, not measured scientific comparison results |

The demo does not write a manuscript. The linked manuscript-style excerpt is a
hand-curated explanation of software behavior, not a hidden extra output of the script.

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

## Use the example honestly

The scientific records contain fixed illustrative values, source labels and statuses.
They are not fitted estimates or independently verified sources. In particular, the
presence of an uncertainty interval in a fixture does not mean the demo computed one.
No real data access, baseline training, locked-test evaluation, full manuscript, figure
rendering or external publication occurs.

The actual packaging rehearsal is useful software evidence: the documented small
example and its tests run after a fresh unpack using the existing Python interpreter.
It is not a fresh dependency installation or independent research reproduction. Keep
the generated workspace local; do not export the surrounding records as a public code
artifact. For a real project, replace the scientific work with actual observed data,
results and source inspection, not by changing the fixture's labels.
