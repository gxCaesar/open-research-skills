#!/usr/bin/env python3
"""Create and validate a complete synthetic publication-workflow workspace."""

import argparse
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from synthetic_workspace import populate_ready_workspace, read_json, write_json


SKILL_ROOT = Path(__file__).resolve().parents[1]
INIT = SKILL_ROOT / "scripts" / "init_publication_project.py"
VALIDATE = SKILL_ROOT / "scripts" / "validate_publication_project.py"
TARGETS = ("pilot", "development", "handoff")


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def run_command(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", *args], text=True, capture_output=True, check=False
    )


def fail_process(label: str, result: subprocess.CompletedProcess) -> int:
    print(f"ERROR: {label} exited {result.returncode}", file=sys.stderr)
    if result.stdout:
        print(result.stdout, file=sys.stderr, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    return 1


def rehearse_public_release(output: Path) -> bool:
    """Run only this demo's two fixed commands in a fresh unpack of its curated tree."""
    handoff_path = output / "handoff" / "handoff.json"
    handoff = read_json(handoff_path)
    release = handoff["public_release"]
    rehearsal = {
        "status": "NOT_RUN",
        "checked_on": date.today().isoformat(),
        "environment": (
            f"Fresh unpack using existing Python {sys.version.split()[0]}; "
            "standard library only, no separate dependency environment"
        ),
        "commands": [],
        "not_run": ["other Python versions and operating systems", "external publication"],
    }
    release.update(status="IN_PROGRESS", rehearsal=rehearsal)
    write_json(handoff_path, handoff)
    source = output / "public-release"
    commands = (
        ("src/example.py", "examples/input.json", "result.json"),
        ("tests/test_example.py",),
    )
    pending_commands = list(commands)
    try:
        with tempfile.TemporaryDirectory(prefix="publication-release-") as temporary:
            temporary_root = Path(temporary)
            archive_path = temporary_root / "example.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                for relative in release["allowlist"]:
                    archive.write(source / relative, relative)
            unpacked = temporary_root / "unpacked"
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(unpacked)

            for index, arguments in enumerate(commands):
                command = [sys.executable, "-B", *arguments]
                pending_commands.pop(0)
                result = subprocess.run(
                    command, cwd=unpacked, text=True, capture_output=True,
                    check=False, timeout=30,
                )
                rehearsal["commands"].append({
                    "command": shlex.join(command),
                    "exit_code": result.returncode,
                    "observed_outputs": [
                        stream for stream in (result.stdout, result.stderr) if stream.strip()
                    ],
                })
                if result.returncode != 0:
                    raise ValueError(f"{arguments[0]} exited {result.returncode}")
                if index == 0:
                    observed = read_json(unpacked / "result.json")
                    if observed != {"count": 3, "total": 6}:
                        raise ValueError(f"example result differs from documented output: {observed!r}")
                    observed_stdout = json.loads(result.stdout)
                    if observed_stdout != {"count": 3, "total": 6}:
                        raise ValueError(
                            f"example stdout differs from documented output: {observed_stdout!r}"
                        )
                    shutil.copyfile(
                        unpacked / "result.json", output / "results" / "public-release-example.json"
                    )
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
        release["status"] = "FAILED"
        rehearsal.update(status="FAILED", failure=str(exc))
        rehearsal["not_run"].extend(
            shlex.join([sys.executable, "-B", *arguments]) for arguments in pending_commands
        )
        rehearsal["not_run"].append("public-release validator")
        write_json(handoff_path, handoff)
        print(f"ERROR: public-release rehearsal failed: {exc}", file=sys.stderr)
        return False

    release["status"] = "AUDITED"
    rehearsal["status"] = "PASS"
    write_json(handoff_path, handoff)
    return True


def run_demo(output: Path, with_public_release: bool = False) -> int:
    output = output.expanduser().resolve()
    if inside(SKILL_ROOT, output):
        print("ERROR: output directory must be outside the installed skill", file=sys.stderr)
        return 1
    if output.exists():
        print("ERROR: output directory must be new and must not already exist", file=sys.stderr)
        return 1

    print("SYNTHETIC DEMO ONLY: no real experiment, locked-test access, authorization, or publication occurred.")
    initialized = run_command(
        str(INIT),
        str(output),
        "--project-id",
        "synthetic-publication",
        "--title",
        "A synthetic mechanism study",
        "--domain",
        "single-cell",
        "--contribution-lane",
        "sota-method",
    )
    if initialized.returncode != 0:
        return fail_process("initializer", initialized)

    try:
        populate_ready_workspace(output, public_release=with_public_release)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: could not populate synthetic workspace: {exc}", file=sys.stderr)
        return 1

    targets = TARGETS + (("public-release",) if with_public_release else ())
    for target in targets:
        if target == "public-release" and not rehearse_public_release(output):
            return 1
        result = run_command(str(VALIDATE), str(output), "--target", target, "--format", "json")
        if result.returncode != 0:
            return fail_process(f"{target} validator", result)
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            print(f"ERROR: {target} validator did not emit JSON: {exc}", file=sys.stderr)
            return 1
        if report.get("status") != "PASS":
            print(
                f"ERROR: {target} validator returned unexpected status {report.get('status')!r}",
                file=sys.stderr,
            )
            return 1
        print(f"{target}: {report['status']}")
    print(f"synthetic workspace: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="new directory for the synthetic workspace")
    parser.add_argument(
        "--with-public-release", action="store_true",
        help="also package, unpack, run, and validate the bundled synthetic code example",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return run_demo(Path(args.output), with_public_release=args.with_public_release)


if __name__ == "__main__":
    raise SystemExit(main())
