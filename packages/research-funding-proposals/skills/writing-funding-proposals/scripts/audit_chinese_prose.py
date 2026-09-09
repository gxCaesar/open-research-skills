#!/usr/bin/env python3
"""Report reviewable surface risks in Chinese research-proposal prose."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Tuple


PROMOTIONAL = [
    "全新",
    "国际领先",
    "国内首创",
    "填补空白",
    "颠覆性",
    "系统性突破",
    "重大突破",
]
FORMULAIC_GROUPS = [
    ("首先", "其次", "最后"),
    ("一方面", "另一方面"),
    ("一是", "二是", "三是"),
    ("第一", "第二", "第三"),
]
SENTENCE_SPLIT = re.compile(r"(?<=[。！？!?])")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-visible-characters", type=int, default=80)
    parser.add_argument("--fail-on", choices=["none", "warning", "error"], default="none")
    return parser.parse_args()


def location(text: str, offset: int) -> Tuple[int, int]:
    prefix = text[:offset]
    line = prefix.count("\n") + 1
    last_newline = prefix.rfind("\n")
    column = offset + 1 if last_newline < 0 else offset - last_newline
    return line, column


def add_finding(
    findings: List[dict],
    path: Path,
    text: str,
    offset: int,
    code: str,
    severity: str,
    excerpt: str,
    action: str,
) -> None:
    line, column = location(text, offset)
    findings.append(
        {
            "file": str(path),
            "line": line,
            "column": column,
            "code": code,
            "severity": severity,
            "excerpt": excerpt,
            "action": action,
        }
    )


def visible_length(value: str) -> int:
    without_commands = re.sub(r"\\[A-Za-z]+(?:\{[^{}]*\})?", "", value)
    without_space = re.sub(r"\s+", "", without_commands)
    return len(without_space)


def audit(path: Path, max_characters: int) -> List[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: List[dict] = []
    for phrase in PROMOTIONAL:
        for match in re.finditer(re.escape(phrase), text):
            add_finding(
                findings,
                path,
                text,
                match.start(),
                "PROMOTIONAL_CLAIM",
                "warning",
                phrase,
                "Remove it or bind the exact comparison and scope to verified evidence.",
            )

    for group in FORMULAIC_GROUPS:
        present = [(text.find(item), item) for item in group if item in text]
        if len(present) >= 2:
            offset, first = min(present)
            add_finding(
                findings,
                path,
                text,
                offset,
                "FORMULAIC_SEQUENCE",
                "warning",
                "/".join(item for _, item in sorted(present)),
                "Use the scientific dependency or evidence transition instead of manufactured symmetry.",
            )

    for match in re.finditer(r"[；;]", text):
        add_finding(
            findings,
            path,
            text,
            match.start(),
            "SEMICOLON_STACK",
            "warning",
            match.group(0),
            "Check whether the joined clauses should become separate evidence-bearing sentences.",
        )
    for match in re.finditer(r"——|--", text):
        add_finding(
            findings,
            path,
            text,
            match.start(),
            "DASH_ASIDE",
            "error",
            match.group(0),
            "Rewrite the aside as a complete sentence while preserving qualifiers.",
        )

    cursor = 0
    for sentence in SENTENCE_SPLIT.split(text):
        if sentence and visible_length(sentence) > max_characters:
            excerpt = re.sub(r"\s+", " ", sentence.strip())[:80]
            add_finding(
                findings,
                path,
                text,
                cursor,
                "LONG_SENTENCE",
                "warning",
                excerpt,
                "Split at a scientific decision boundary without removing scope or citations.",
            )
        cursor += len(sentence)
    return findings


def main() -> None:
    args = parse_args()
    findings: List[dict] = []
    read_errors: List[str] = []
    for path in args.files:
        if not path.is_file():
            read_errors.append(f"not a regular file: {path}")
            continue
        findings.extend(audit(path, args.max_visible_characters))

    counts: Dict[str, int] = {"error": 0, "warning": 0}
    for finding in findings:
        counts[finding["severity"]] += 1
    report = {
        "status": "FAILED" if read_errors else ("REVIEW_REQUIRED" if findings else "PASS"),
        "scope": "surface prose cues only; scientific claims and authorship require separate evidence",
        "files": len(args.files),
        "findings": findings,
        "counts": counts,
        "errors": read_errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print(
            f"Status: {report['status']} | errors={counts['error']} "
            f"warnings={counts['warning']}"
        )
        for finding in findings:
            print(
                f"{finding['file']}:{finding['line']}:{finding['column']} "
                f"{finding['severity'].upper()} {finding['code']}: {finding['excerpt']}"
            )
        for error in read_errors:
            print(f"ERROR {error}", file=sys.stderr)

    if read_errors:
        raise SystemExit(2)
    if args.fail_on == "error" and counts["error"]:
        raise SystemExit(1)
    if args.fail_on == "warning" and findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
