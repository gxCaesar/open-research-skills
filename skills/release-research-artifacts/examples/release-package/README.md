# Synthetic release package

A minimal, complete example of the shape `check_release_package.py` expects. It is
teaching material: the numbers are generated, and nothing here is a research result.

Verify it from outside the workspace that produced it:

```bash
python3 ../../scripts/check_release_package.py . --mode named
```

Reproduce the single reported number:

```bash
python3 src/reproduce.py
```

Both commands use only the Python standard library.

## Why there is no bad package next to this one

A package that demonstrates the failures would have to contain the things the checker
looks for: an absolute home path, an address, a file the record does not list. Those are
exactly the strings this repository's own content scan rejects, so shipping such a
directory would make the repository fail its own gate.

The failing cases are therefore built inside the test, one per rule, and torn down with
the temporary directory. `tests/artifact-release/test_release_package.py` is where they
live, and each one names the rule it is a witness for.

## Changing anything here

Every file except the record is listed in `RELEASED_FILES.json` with its size and
digest, so editing one byte makes the check fail until the record is regenerated. That
is the property the record exists to have.
