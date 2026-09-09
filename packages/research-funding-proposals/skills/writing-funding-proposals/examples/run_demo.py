#!/usr/bin/env python3
"""Create and validate an archived synthetic funding-proposal workspace."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from synthetic_workspace import SNAPSHOT_AS_OF, populate_complete_workspace


SKILL_DIR = Path(__file__).resolve().parents[1]
INIT = SKILL_DIR / "scripts" / "init_proposal_workspace.py"
VALIDATE = SKILL_DIR / "scripts" / "validate_proposal_workspace.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    return parser.parse_args()


def reject_unsafe_output(root: Path) -> None:
    try:
        root.relative_to(SKILL_DIR.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit("refusing output inside the installed skill directory")
    if root.exists():
        raise SystemExit("refusing existing output directory")


def run(command: list) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def main() -> None:
    args = parse_args()
    root = args.output_directory.resolve()
    print("SYNTHETIC DEMO ONLY: records below are fictional and archived.")
    reject_unsafe_output(root)
    initialized = run([
        sys.executable, "-B", str(INIT), str(root), "--project-id", "synthetic-grant",
        "--program", "nsfc", "--year", "2026", "--project-type", "general",
    ])
    if initialized.returncode:
        raise SystemExit(initialized.stdout + initialized.stderr)
    populate_complete_workspace(root)
    validated = run([
        sys.executable, "-B", str(VALIDATE), str(root), "--mode", "final",
        "--as-of", SNAPSHOT_AS_OF, "--json",
    ])
    try:
        report = json.loads(validated.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit("validator did not return JSON: {0}".format(error))
    status = report.get("status")
    print("Observed validator status: {0}".format(status))
    print(
        "Observed validator scope: {0} (record-only)".format(
            report.get("validation_scope")
        )
    )
    if validated.returncode or status != "PASS":
        raise SystemExit(validated.stdout + validated.stderr)
    print("Output workspace: {0}".format(root))
    print("Do not publish this generated output as real evidence.")


if __name__ == "__main__":
    main()
