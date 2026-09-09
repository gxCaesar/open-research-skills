#!/usr/bin/env python3
"""Run conservative venue-profile checks on one LaTeX manuscript tree."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
from typing import Dict, List, Optional, Sequence, Tuple

from profile_contract import path_free_exception_summary, readiness_error


LITERAL_ENVIRONMENTS = {"verbatim", "Verbatim", "lstlisting", "minted"}
CONTROLLED_LENGTHS = {
    "baselineskip",
    "columnsep",
    "evensidemargin",
    "headsep",
    "oddsidemargin",
    "paperheight",
    "paperwidth",
    "parindent",
    "parskip",
    "textheight",
    "textwidth",
    "topmargin",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser.parse_args()


def strip_comment(line: str) -> str:
    for index, character in enumerate(line):
        if character != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def mask_inline_literals(line: str) -> str:
    pattern = re.compile(r"\\(?:verb\*?|lstinline(?:\[[^\]]*\])?)")
    cursor = 0
    while True:
        match = pattern.search(line, cursor)
        if match is None or match.end() >= len(line):
            return line
        delimiter = line[match.end()]
        if delimiter.isspace() or delimiter.isalpha():
            cursor = match.end()
            continue
        end = line.find(delimiter, match.end() + 1)
        if end < 0:
            return line[: match.start()]
        line = line[: match.start()] + " " * (end + 1 - match.start()) + line[end + 1 :]
        cursor = match.start() + 1


def preprocess(lines: Sequence[str]) -> List[str]:
    stripped = [strip_comment(mask_inline_literals(line)) for line in lines]
    result: List[str] = []
    literal: Optional[str] = None
    false_depth = 0
    ended = False
    for line in stripped:
        starts_false = len(re.findall(r"\\iffalse\b", line))
        ends_false = len(re.findall(r"\\fi\b", line))
        begin = re.search(
            r"\\begin\{(" + "|".join(map(re.escape, LITERAL_ENVIRONMENTS)) + r")\}",
            line,
        )
        masked = ended or false_depth > 0 or literal is not None or starts_false > 0 or begin is not None
        result.append("" if masked else line)
        if literal is not None and re.search(r"\\end\{" + re.escape(literal) + r"\}", line):
            literal = None
        elif literal is None and begin is not None:
            literal = begin.group(1)
            if re.search(r"\\end\{" + re.escape(literal) + r"\}", line[begin.end() :]):
                literal = None
        false_depth = max(0, false_depth + starts_false - ends_false)
        if re.search(r"\\end\{document\}", line):
            ended = True
    return result


def relative_display_path(path: Path, root: Path) -> str:
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    try:
        return resolved_path.relative_to(resolved_root).as_posix()
    except ValueError:
        return f"<external>/{resolved_path.name}"


def project_sources(main_path: Path) -> Tuple[List[Tuple[Path, List[str], List[str]]], List[str]]:
    sources: List[Tuple[Path, List[str], List[str]]] = []
    limitations: List[str] = []
    seen = set()
    include_re = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
    main_directory = main_path.resolve().parent

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        if len(seen) >= 64:
            limitations.append("Stopped include discovery after 64 TeX files.")
            return
        seen.add(resolved)
        try:
            raw = resolved.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as error:
            limitations.append(
                f"Could not read {relative_display_path(resolved, main_directory)} ({type(error).__name__})."
            )
            return
        active = preprocess(raw)
        sources.append((resolved, raw, active))
        for line in active:
            for target in include_re.findall(line):
                if not target.strip() or "\\" in target or "#" in target:
                    display_target = target.strip()
                    if Path(display_target).is_absolute():
                        display_target = relative_display_path(Path(display_target), main_directory)
                    limitations.append(
                        "Did not resolve dynamic include "
                        f"{display_target!r} in {relative_display_path(resolved, main_directory)}."
                    )
                    continue
                child = resolved.parent / target.strip()
                if not child.suffix:
                    child = child.with_suffix(".tex")
                visit(child)

    visit(main_path)
    return sources, limitations


def make_finding(
    sequence: int,
    rule_id: str,
    priority: str,
    basis: str,
    location_path: str,
    line: int,
    observed: str,
    expected: str,
    action: str,
    sources: List[str],
) -> dict:
    impacts = {
        "DOCUMENT_CLASS": "The manuscript may not compile or render in the required venue format.",
        "AAAI_STYLE_SUBMISSION": "The submission can violate the required anonymous venue format.",
        "ICLR_STYLE_CURRENT": "The submission can violate the current venue format.",
        "VENUE_STYLE_CURRENT": "The submission can violate the configured venue format.",
        "LAYOUT_OVERRIDE": "Template geometry may drift and create a format-compliance defect.",
        "ICLR_FINALCOPY_DISABLED": "Author identity can be exposed during double-blind review.",
        "ICLR_FINALCOPY_ENABLED": "The publication PDF can retain anonymous-review formatting.",
        "ANON_SOURCE_IDENTITY": "Author identity can be exposed in review material.",
        "ANON_ACKNOWLEDGMENTS": "Acknowledgments can reveal identity or violate review-stage rules.",
        "ABSTRACT_REQUIRED": "The manuscript is incomplete for the selected stage.",
        "REQUIRED_HEADING": "A mandatory venue section is absent.",
    }
    return {
        "id": f"TEX-{sequence:03d}",
        "rule_id": rule_id,
        "basis": basis,
        "priority": priority,
        "status": "observed",
        "location": f"{location_path}:{line}",
        "observed": observed.strip(),
        "expected": expected,
        "impact": impacts.get(rule_id, "The venue or scientific contract may be violated."),
        "minimal_action": action,
        "verification": "Re-run the source audit, compile, and inspect the rendered PDF.",
        "sources": sources,
    }


def normalize_heading(value: str) -> str:
    value = re.sub(r"\\[A-Za-z@]+\*?", " ", value)
    value = re.sub(r"[{}~]", " ", value)
    return " ".join(value.casefold().split())


def audit(main_path: Path, profile: dict, stage: str) -> dict:
    contract = profile["tex_contract"]
    sources, limitations = project_sources(main_path)
    if not sources:
        raise OSError(f"could not read main TeX source: {main_path}")
    main_source, main_raw, main_active = sources[0]
    main_directory = main_source.parent
    findings: List[dict] = []

    def display_path(path: Path) -> str:
        return relative_display_path(path, main_directory)

    def add(rule_id: str, priority: str, path: Path, line: int, observed: str, expected: str, action: str) -> None:
        findings.append(
            make_finding(
                len(findings) + 1,
                rule_id,
                priority,
                "official_hard_rule" if rule_id not in {"LAYOUT_OVERRIDE"} else "manuscript_fact",
                display_path(path),
                line,
                observed,
                expected,
                action,
                list(profile.get("rule_sources", {}).get(rule_id, [])),
            )
        )

    active_lines = [
        (path, line_number, raw[line_number - 1], line)
        for path, raw, active in sources
        for line_number, line in enumerate(active, start=1)
    ]
    active_text = "\n".join(line for _, _, _, line in active_lines)

    def find_active(pattern: re.Pattern) -> Optional[Tuple[Path, int, str]]:
        for path, line_number, raw_line, line in active_lines:
            if pattern.search(line):
                return path, line_number, raw_line
        return None

    class_pattern = re.compile(r"\\documentclass(?:\[([^\]]*)\])?\s*\{([^}]*)\}")
    document_classes: List[Tuple[Path, int, List[str], str, str]] = []
    for line_number, line in enumerate(main_active, start=1):
        for option_text, name in class_pattern.findall(line):
            options = [item.strip() for item in option_text.split(",") if item.strip()]
            document_classes.append((main_source, line_number, options, name.strip(), main_raw[line_number - 1]))
    expected_class = contract["document_class"]
    required_class_options = contract.get("required_document_class_options", [])
    class_is_valid = len(document_classes) == 1 and document_classes[0][3] == expected_class and all(
        option in document_classes[0][2] for option in required_class_options
    )
    if not class_is_valid:
        source, line_number, _, _, raw_line = document_classes[0] if document_classes else (main_source, 1, [], "", "")
        add(
            "DOCUMENT_CLASS",
            "P1",
            source,
            line_number,
            raw_line or "No active document class",
            f"Use the current official shell's {expected_class} document class with required options {required_class_options}.",
            "Restore the current official document class and rebuild.",
        )

    packages: List[Tuple[Path, int, List[str], str, str]] = []
    package_pattern = re.compile(r"\\usepackage(?:\[([^\]]*)\])?\s*\{([^}]*)\}")
    for path, raw, active in sources:
        for line_number, line in enumerate(active, start=1):
            for option_text, names in package_pattern.findall(line):
                options = [item.strip() for item in option_text.split(",") if item.strip()]
                for name in names.split(","):
                    packages.append((path, line_number, options, name.strip(), raw[line_number - 1]))
    style_name = contract["style_package"]
    style_packages = [item for item in packages if item[3] == style_name]
    required_options = contract.get("required_options", {}).get(stage, [])
    forbidden_options = contract.get("forbidden_options", {}).get(stage, [])
    style_is_valid = len(style_packages) == 1 and all(
        option in style_packages[0][2] for option in required_options
    ) and not any(option in style_packages[0][2] for option in forbidden_options)
    if not style_is_valid:
        observed = "; ".join(item[4].strip() for item in style_packages) or "No active venue style package"
        rule = str(contract.get("style_rule_id", "")).strip()
        if not rule:
            venue = str(profile.get("venue", ""))
            if venue.startswith("AAAI"):
                rule = "AAAI_STYLE_SUBMISSION"
            elif venue.startswith("ICLR"):
                rule = "ICLR_STYLE_CURRENT"
            else:
                rule = "VENUE_STYLE_CURRENT"
        add(
            rule,
            "P0",
            style_packages[0][0] if style_packages else main_source,
            style_packages[0][1] if style_packages else 1,
            observed,
            f"Load {style_name} exactly once with required options {required_options} and without forbidden options {forbidden_options}.",
            "Restore the current official style invocation without modifying the style file.",
        )

    forbidden_packages = set(contract.get("forbidden_layout_packages", []))
    for path, line_number, _, name, raw_line in packages:
        if name in forbidden_packages:
            add(
                "LAYOUT_OVERRIDE",
                "P1",
                path,
                line_number,
                raw_line,
                "Do not override the current official layout.",
                f"Remove {name} and solve the content or layout issue within the official template.",
            )

    controlled = "|".join(sorted(map(re.escape, CONTROLLED_LENGTHS)))
    length_re = re.compile(r"\\(?:setlength|addtolength)\s*\{\\(?:" + controlled + r")\}")
    direct_re = re.compile(r"\\(?:" + controlled + r")\s*(?:=|[-+]?\d)")
    for path, raw, active in sources:
        for line_number, line in enumerate(active, start=1):
            if length_re.search(line) or direct_re.search(line) or re.search(r"\\v(?:space|skip)\*?\s*\{\s*-", line):
                add(
                    "LAYOUT_OVERRIDE",
                    "P1",
                    path,
                    line_number,
                    raw[line_number - 1],
                    "Keep template-controlled spacing and dimensions unchanged.",
                    "Remove the override and reflow the content legitimately.",
                )

    final_command = str(contract.get("final_copy_command", "")).strip()
    final_copy_match = find_active(re.compile(r"\\" + re.escape(final_command) + r"\b")) if final_command else None
    if final_command:
        final_rule_ids = contract["final_copy_rule_ids"]
        final_copy_required_stages = contract["final_copy_required_stages"]
        if stage not in final_copy_required_stages and final_copy_match:
            path, line, _ = final_copy_match
            add(
                final_rule_ids["disabled"],
                "P0",
                path,
                line,
                "Final-copy command is active outside a configured final-copy stage.",
                "Final-copy mode is disabled outside configured final-copy stages.",
                "Disable final-copy mode and inspect the rendered author block and header.",
            )
        if stage in final_copy_required_stages and not final_copy_match:
            add(
                final_rule_ids["enabled"],
                "P0",
                main_source,
                1,
                "No active final-copy command was found.",
                "Final-copy mode is enabled for the configured final-copy stage.",
                "Enable final-copy mode and inspect the publication PDF.",
            )

    anonymous = stage in contract.get("anonymous_stages", [])
    if anonymous and contract.get("anonymous_source_author_mode") == "flag":
        identity_commands = contract.get("anonymous_source_identity_commands", ["author", "affiliation"])
        identity_pattern = re.compile(
            r"\\(?:" + "|".join(map(re.escape, identity_commands)) + r")\s*\{",
            re.I,
        )
        identity_match = find_active(identity_pattern)
        if identity_match:
            path, line, _ = identity_match
            add(
                "ANON_SOURCE_IDENTITY",
                "P0",
                path,
                line,
                "An active configured identity command remains in the review source.",
                "Review materials omit configured identity commands.",
                "Use the official anonymous template pattern and inspect source plus rendered PDF.",
            )

    if anonymous and contract.get("forbid_acknowledgments_in_anonymous"):
        acknowledgement = find_active(
            re.compile(
                r"\\(?:section|subsection)\*?\s*\{\s*acknowledg(?:e)?ments?\s*\}|\\begin\{acknowledg(?:e)?ments?\}",
                re.I,
            )
        )
        if acknowledgement:
            path, line, _ = acknowledgement
            add(
                "ANON_ACKNOWLEDGMENTS",
                "P0",
                path,
                line,
                "An acknowledgments block is active in anonymous review material.",
                "Acknowledgments and identifying assistance or funding text are absent during review.",
                "Remove the block from review materials and inspect the rendered PDF and supplement.",
            )

    if stage in contract.get("require_abstract", []) and not re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", active_text, re.S):
        add(
            "ABSTRACT_REQUIRED",
            "P1",
            main_source,
            1,
            "No complete active abstract environment was found.",
            "The manuscript contains one complete abstract.",
            "Restore the abstract and inspect the compiled first page.",
        )

    headings = [
        normalize_heading(value)
        for _, _, _, line in active_lines
        for value in re.findall(r"\\(?:section|subsection)\*?\s*\{([^{}]+)\}", line)
    ]
    for required in contract.get("required_headings", {}).get(stage, []):
        normalized = normalize_heading(required)
        if not any(normalized == heading for heading in headings):
            add(
                "REQUIRED_HEADING",
                "P0",
                main_source,
                1,
                f"Required heading not found: {required}",
                f"Include the current required {required} section.",
                "Add the truthful section from the current template and inspect its placement.",
            )

    return {
        "schema_version": 1,
        "tool": "audit_tex.py",
        "venue": profile["venue"],
        "stage": stage,
        "target": display_path(main_source),
        "findings": findings,
        "limitations": limitations + [
            "Source checks cannot prove rendered anonymity, page boundaries, or visual compliance."
        ],
    }


def render_markdown(report: dict) -> str:
    lines = [
        f"# {report['venue']} TeX audit",
        "",
        f"- Stage: `{report['stage']}`",
        f"- Findings: {len(report['findings'])}",
    ]
    for finding in report["findings"]:
        lines.extend(
            [
                "",
                f"## {finding['id']} — {finding['rule_id']}",
                "",
                f"- Priority: `{finding['priority']}`",
                f"- Location: `{finding['location']}`",
                f"- Observed: {finding['observed']}",
                f"- Action: {finding['minimal_action']}",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except OSError as error:
        print(
            f"error: could not read profile {args.profile.name or 'profile'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    except json.JSONDecodeError as error:
        print(
            f"error: invalid profile {args.profile.name or 'profile'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if not isinstance(profile, dict):
        print(
            f"error: invalid profile {args.profile.name or 'profile'}: expected a JSON object",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if profile.get("schema_version") != 1 or args.stage not in profile.get("allowed_stages", []):
        print("error: unsupported profile or stage", file=sys.stderr)
        raise SystemExit(2)
    profile_error = readiness_error(profile)
    if profile_error:
        print(f"error: incomplete profile: {profile_error}", file=sys.stderr)
        raise SystemExit(2)
    try:
        report = audit(args.tex, profile, args.stage)
    except OSError as error:
        print(
            f"error: could not read TeX source {args.tex.name or 'input'}: "
            f"{path_free_exception_summary(error)}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    except KeyError:
        print("error: profile contract could not be applied", file=sys.stderr)
        raise SystemExit(2)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    raise SystemExit(1 if report["findings"] else 0)


if __name__ == "__main__":
    main()
