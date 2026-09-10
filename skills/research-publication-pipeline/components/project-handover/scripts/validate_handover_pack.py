#!/usr/bin/env python3
"""Validate a handover pack against the one question that decides whether it works.

Can a person who did not build this project run it from the pack alone. Everything the
pack asserts is checked against that: the environment is pinned, every task carries a
command and a way to tell it finished, no instruction points at a machine only the author
has, and no answer is "ask me".

It reads a record. It cannot confirm that a command runs, that a path exists on the
receiving machine, or that the rehearsal actually happened.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROUTES = {"in_repository", "public_download", "shared_storage", "request_from_owner"}
# Built by concatenation so the pattern itself is not an absolute path.
MACHINE_PATH = re.compile(r"/(?:" + "Users" + "|" + "home" + r")/[A-Za-z0-9._-]+/")
SSH_TARGET = re.compile(r"\bssh\s+[A-Za-z0-9._-]+\b|\bscp\s|\brsync\s+[^\s]*[A-Za-z0-9._-]+:")
DEFERS = re.compile(
    r"(?:ask (?:me|the author|us)|contact (?:me|the author)|check with (?:me|the author)"
    r"|I will (?:tell|send|share)|reach out to (?:me|the author))",
    re.I,
)
UNRESOLVED = re.compile(
    r"(?:AUTHOR_INPUT_NEEDED|\bTBD\b|\bTODO\b|\[(?:replace|insert|unknown|required|path|"
    r"command|version|contact|dataset)[^\]]*\])",
    re.I,
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("--mode", choices=["working", "final"], default="working")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args(argv)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(text(item) for item in value)


def add(findings: List[Dict[str, Any]], rule_id: str, severity: str, location: str, message: str) -> None:
    findings.append({"rule_id": rule_id, "severity": severity, "location": location, "message": message})


def validate(payload: Any, mode: str) -> List[Dict[str, Any]]:  # noqa: C901 - one rule per branch
    findings: List[Dict[str, Any]] = []
    final = mode == "final"
    if not isinstance(payload, dict):
        add(findings, "pack", "error", "pack", "top-level value must be an object")
        return findings

    if payload.get("schema_version") != 1:
        add(findings, "schema_version", "error", "schema_version", "must equal 1")
    for key in ("project", "prepared_on", "entry_document"):
        if not text(payload.get(key)):
            add(findings, key, "error", key, "must be non-empty text")

    layout = payload.get("run_layout")
    if not isinstance(layout, dict):
        add(findings, "run_layout", "error", "run_layout",
            "describe the directory a run lives in; a receiver cannot invent it")
        layout = {}
    else:
        for key in ("root", "run_command_file", "environment_file", "log_directory",
                    "checkpoint_directory", "results_directory"):
            if not text(layout.get(key)):
                add(findings, "run_layout_field", "error", f"run_layout.{key}",
                    "must be a path relative to the project")
            elif str(layout[key]).startswith("/") or ".." in Path(str(layout[key])).parts:
                add(findings, "run_layout_escapes_the_project", "error", f"run_layout.{key}",
                    "must stay inside the project rather than name a location on one machine")
        if layout.get("written_before_launch") is not True:
            add(findings, "layout_not_written_before_launch", "warning", "run_layout.written_before_launch",
                "the run command and environment are written before the run starts, or a crashed run "
                "cannot be reproduced")

    environment = payload.get("environment")
    if not isinstance(environment, dict):
        add(findings, "environment", "error", "environment", "must describe how to build the environment")
        environment = {}
    else:
        for key in ("specification", "interpreter_or_runtime", "create_command"):
            if not text(environment.get(key)):
                add(findings, "environment_field", "error", f"environment.{key}",
                    "must be non-empty text")
        if environment.get("pinned") is not True:
            add(findings, "environment_not_pinned", "error", "environment.pinned",
                "an unpinned environment resolves differently on the receiver's machine")

    data = payload.get("data_access")
    if not isinstance(data, dict):
        add(findings, "data_access", "error", "data_access", "must state how the receiver obtains the data")
    else:
        if data.get("route") not in ROUTES:
            add(findings, "data_route", "error", "data_access.route",
                f"must be one of: {', '.join(sorted(ROUTES))}")
        if not text(data.get("obtainable_by_receiver")):
            add(findings, "data_obtainability", "error", "data_access.obtainable_by_receiver",
                "say what the receiver can get without the author present")

    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        add(findings, "tasks", "error", "tasks", "must list at least one runnable first task")
        tasks = []
    seen: set = set()
    for index, task in enumerate(tasks):
        where = f"tasks[{index}]"
        if not isinstance(task, dict):
            add(findings, "task", "error", where, "must be an object")
            continue
        name = task.get("task_id") if text(task.get("task_id")) else where
        if not text(task.get("task_id")):
            add(findings, "task_id", "error", f"{where}.task_id", "must be non-empty text")
        elif task["task_id"] in seen:
            add(findings, "task_id", "error", f"{where}.task_id", "must be unique")
        else:
            seen.add(task["task_id"])
        for key in ("goal", "command", "expected_output", "done_when"):
            if not text(task.get(key)):
                add(findings, "task_field", "error", f"{name}.{key}",
                    "a task without this cannot be started or finished by someone else")
        command = task.get("command")
        if text(command):
            if MACHINE_PATH.search(command):
                add(findings, "command_names_one_machine", "error", f"{name}.command",
                    "the command contains an absolute home path; a receiver has a different one")
            if SSH_TARGET.search(command):
                add(findings, "command_assumes_the_authors_hosts", "error", f"{name}.command",
                    "the command reaches a named remote host; name the requirement, not your machine")
        for key in ("expected_output", "done_when"):
            if text(task.get(key)) and DEFERS.search(task[key]):
                add(findings, "answer_defers_to_the_author", "error", f"{name}.{key}",
                    "a receiver who has to ask the author is not able to run this alone")

    frozen = payload.get("do_not_change")
    if not text_list(frozen):
        add(findings, "do_not_change", "error", "do_not_change",
            "list what the receiver must not modify, or a frozen artifact will be edited in good faith")

    rehearsal = payload.get("rehearsal")
    if not isinstance(rehearsal, dict):
        if final:
            add(findings, "rehearsal", "error", "rehearsal",
                "final mode requires that someone other than the author ran the pack")
        else:
            add(findings, "rehearsal", "warning", "rehearsal",
                "until someone else has run it, the pack is a plan rather than a handover")
    else:
        for key in ("performed_by", "commands_run", "outcome"):
            if key == "commands_run":
                if not text_list(rehearsal.get(key)):
                    add(findings, "rehearsal_field", "error", f"rehearsal.{key}",
                        "record the commands verbatim")
            elif not text(rehearsal.get(key)):
                add(findings, "rehearsal_field", "error", f"rehearsal.{key}", "must be non-empty text")
        if rehearsal.get("performed_by") == payload.get("prepared_by"):
            add(findings, "rehearsal_by_the_author", "error", "rehearsal.performed_by",
                "the author already knows what the pack omits; that is the whole difficulty")

    if final:
        rendered = json.dumps(payload, ensure_ascii=False)
        if UNRESOLVED.search(rendered):
            add(findings, "unresolved_placeholder", "error", "pack",
                "resolve every placeholder before handing the pack over")
    return findings


def build_report(payload: Any, mode: str, target: Path) -> Dict[str, Any]:
    findings = validate(payload, mode)
    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema_version": 1,
        "tool": "validate_handover_pack.py",
        "target": str(target.resolve()),
        "mode": mode,
        "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "limitations": [
            "The validator reads the record; it does not run a command or check a path on any machine.",
            "It cannot confirm that the rehearsal happened or that the receiver understood the result.",
        ],
    }


def render_markdown(result: Dict[str, Any]) -> str:
    lines = [
        "# Handover-pack validation",
        "",
        f"- Status: `{result['status']}`",
        f"- Errors: {result['errors']}",
        f"- Warnings: {result['warnings']}",
    ]
    for item in result["findings"]:
        lines.append(
            f"- [{item['severity']}] `{item['rule_id']}` at `{item['location']}`: {item['message']}"
        )
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        payload = json.loads(args.pack.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    result = build_report(payload, args.mode, args.pack)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
