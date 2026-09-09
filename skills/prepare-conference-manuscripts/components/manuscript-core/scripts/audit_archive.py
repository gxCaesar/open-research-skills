#!/usr/bin/env python3
"""Inspect a ZIP supplement without extracting it."""

from __future__ import annotations

import argparse
import json
from pathlib import PurePosixPath, Path
import re
import stat
import sys
from typing import List
import zipfile

from profile_contract import path_free_exception_summary


TEXT_SUFFIXES = {
    ".bib",
    ".cfg",
    ".csv",
    ".json",
    ".md",
    ".py",
    ".rst",
    ".sh",
    ".tex",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
REPOSITORY_PARTS = {".git", ".hg", ".svn"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--identity", action="append", default=[])
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args()


def unsafe_path(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return (
        path.is_absolute()
        or any(part == ".." for part in path.parts)
        or bool(re.match(r"^[A-Za-z]:", normalized))
        or "\x00" in normalized
    )


def is_symlink(info: zipfile.ZipInfo) -> bool:
    return info.create_system == 3 and stat.S_ISLNK(info.external_attr >> 16)


def safe_member_location(member: str) -> str:
    if unsafe_path(member):
        return "<archive member>"
    basename = PurePosixPath(member.replace("\\", "/")).name
    return basename if basename and "\x00" not in basename else "<archive member>"


def add_finding(findings: List[dict], rule_id: str, member: str, observed: str, action: str) -> None:
    findings.append(
        {
            "id": f"ARCHIVE-{len(findings) + 1:03d}",
            "rule_id": rule_id,
            "basis": "manuscript_fact",
            "priority": "P0" if rule_id in {"ARCHIVE_IDENTITY", "ARCHIVE_UNSAFE_PATH"} else "P1",
            "status": "observed",
            "location": safe_member_location(member),
            "observed": observed,
            "expected": "A portable, anonymous, review-safe archive member.",
            "impact": "The supplement can expose identity, leak repository internals, or be unsafe to inspect.",
            "minimal_action": action,
            "verification": "Rebuild from an explicit allowlist and rerun archive inspection.",
            "sources": [],
        }
    )


def audit(path: Path, identities: List[str]) -> dict:
    findings: List[dict] = []
    members = []
    identity_needles = [value.casefold() for value in identities if value.strip()]
    with zipfile.ZipFile(path) as archive:
        seen = set()
        for info in archive.infolist():
            name = info.filename
            normalized = name.replace("\\", "/")
            members.append(name)
            if normalized in seen:
                add_finding(
                    findings,
                    "ARCHIVE_DUPLICATE_MEMBER",
                    name,
                    "The archive contains a duplicate member path.",
                    "Create each public path once.",
                )
            seen.add(normalized)
            if unsafe_path(name):
                add_finding(
                    findings,
                    "ARCHIVE_UNSAFE_PATH",
                    name,
                    "The member path is absolute, traverses upward, or uses a drive prefix.",
                    "Remove the member and rebuild the archive without extraction-unsafe paths.",
                )
            if REPOSITORY_PARTS.intersection(PurePosixPath(normalized).parts):
                add_finding(
                    findings,
                    "ARCHIVE_REPOSITORY_METADATA",
                    name,
                    "Version-control metadata is included.",
                    "Exclude repository metadata from the supplementary archive.",
                )
            if is_symlink(info):
                add_finding(
                    findings,
                    "ARCHIVE_SYMLINK",
                    name,
                    "A symbolic-link member is included.",
                    "Replace the link with an explicitly reviewed regular file or omit it.",
                )

            path_identity = next((needle for needle in identity_needles if needle in normalized.casefold()), None)
            if path_identity:
                add_finding(
                    findings,
                    "ARCHIVE_IDENTITY",
                    name,
                    "A supplied identity pattern matched.",
                    "Rename or omit the member, then inspect the rebuilt archive.",
                )
                continue
            suffix = PurePosixPath(normalized).suffix.casefold()
            if suffix not in TEXT_SUFFIXES or info.file_size > 2_000_000 or is_symlink(info):
                continue
            try:
                text = archive.read(info).decode("utf-8", errors="replace").casefold()
            except (OSError, RuntimeError, zipfile.BadZipFile):
                continue
            matched = next((needle for needle in identity_needles if needle in text), None)
            if matched:
                add_finding(
                    findings,
                    "ARCHIVE_IDENTITY",
                    name,
                    "A supplied identity pattern matched.",
                    "Remove or anonymize the exact content and review the archive again.",
                )

    return {
        "schema_version": 1,
        "tool": "audit_archive.py",
        "target": path.name,
        "member_count": len(members),
        "findings": findings,
        "limitations": [
            "Only supplied identity patterns are searched; manual anonymity review remains required.",
            "Binary scientific content is inventoried but not semantically validated.",
            "The archive is inspected without extraction and is never uploaded.",
        ],
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Supplement archive audit",
        "",
        f"- Members: {report['member_count']}",
        f"- Findings: {len(report['findings'])}",
    ]
    for item in report["findings"]:
        lines.extend(
            [
                "",
                f"## {item['id']} — {item['rule_id']}",
                "",
                f"- Member: `{item['location']}`",
                f"- Observed: {item['observed']}",
                f"- Action: {item['minimal_action']}",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    try:
        report = audit(args.archive, args.identity)
    except (OSError, zipfile.BadZipFile) as error:
        print(
            f"error: could not read supplement archive {args.archive.name}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    raise SystemExit(1 if report["findings"] else 0)


if __name__ == "__main__":
    main()
