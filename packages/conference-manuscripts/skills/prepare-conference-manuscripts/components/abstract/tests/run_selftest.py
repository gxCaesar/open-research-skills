#!/usr/bin/env python3
"""Discover and run this skill's standalone regression tests."""

import subprocess
import sys
from pathlib import Path


TESTS = Path(__file__).resolve().parent
EXPECTED = {"test_check_abstract.py"}


def main() -> int:
    found = sorted(path for path in TESTS.glob("test_*.py") if path.is_file())
    names = {path.name for path in found}
    missing = sorted(EXPECTED - names)
    if missing:
        print(f"Missing expected test files: {', '.join(missing)}")
        return 1
    if not found:
        print("No test files discovered.")
        return 1

    failures = []
    for path in found:
        result = subprocess.run(
            [sys.executable, "-B", str(path)],
            cwd=TESTS.parent,
            text=True,
            capture_output=True,
            check=False,
        )
        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"{status} {path.name}")
        if result.returncode != 0:
            failures.append(path.name)
            if result.stdout:
                print(result.stdout.rstrip())
            if result.stderr:
                print(result.stderr.rstrip())

    print(f"files={len(found)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
