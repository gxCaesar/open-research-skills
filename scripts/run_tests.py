#!/usr/bin/env python3
"""Run repository and individual skill suites in separate Python processes."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    tests = ROOT / "tests"
    suites = [tests] + sorted(
        path for path in tests.iterdir()
        if path.is_dir() and any(path.glob("test_*.py"))
    )
    failed = []
    for suite in suites:
        relative = suite.relative_to(ROOT).as_posix()
        command = [
            sys.executable, "-B", "-m", "unittest", "discover",
            "-s", relative, "-p", "test_*.py",
        ]
        print(f"Running {relative}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"suite={relative} status={status} exit_code={result.returncode}", flush=True)
        if result.returncode:
            failed.append(relative)
    print(f"suites={len(suites)} failed={len(failed)}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
