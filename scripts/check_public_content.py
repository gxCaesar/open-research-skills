#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile


RULES = {
    "absolute_macos_user_path": re.compile(
        re.escape("/" + "Users" + "/") + r"[A-Za-z0-9._-]+/"
    ),
    "absolute_linux_home_path": re.compile(
        re.escape("/" + "home" + "/") + r"[A-Za-z0-9._-]+/"
    ),
    "private_account_path": re.compile(
        r"~/(?:\.ssh|\.aws|\.codex|\.codex-cli|\.claude)(?:/|\b)"
    ),
    "integrity_side_record": re.compile(
        r"\b(?:"
        + "sha"
        + r"-?"
        + "256"
        + "|check"
        + r"\s*"
        + "sum manifest"
        + "|digest"
        + " manifest)"
        + r"\b",
        re.IGNORECASE,
    ),
}
INTERNAL_CONTROL_NAMES = {
    "-".join(("pipeline", "state")) + ".json",
    "-".join(("execution", "receipt")) + ".json",
    "-".join(("approval", "receipt")) + ".json",
    "-".join(("delegated", "decision", "receipt")) + ".json",
    "-".join(("release", "manifest")) + ".json",
    ("AG" + "ENTS.md").casefold(),
    ("CLAU" + "DE.md").casefold(),
}
INTERNAL_CONTROL_PARTS = {
    "." + "agents",
    "." + "codex",
    ".git",
    "prom" + "pts",
}
# A local virtualenv is gitignored and never published, so scanning it says nothing about
# what would ship -- but its bin/python symlinks fail the symlink rule and make the
# repository look broken to anyone who followed README's own setup instructions.
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}


def load_deny_terms(path: Path) -> Sequence[str]:
    return tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def candidate_paths(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if (relative.parts and relative.parts[0] == ".git") or set(relative.parts) & SKIP_PARTS:
            continue
        yield path


def read_utf8_text(path: Path):
    """Return readable UTF-8 text without guessing from a filename extension."""
    content = path.read_bytes()
    if b"\x00" in content:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None


def text_findings(location: Path, text: str, folded_terms: Sequence[str]):
    findings = [(location, name) for name, pattern in RULES.items() if pattern.search(text)]
    if any(term in text.casefold() for term in folded_terms):
        findings.append((location, "release_specific_term"))
    return findings


def path_findings(location: Path, folded_terms: Sequence[str]):
    findings = text_findings(location, location.as_posix(), folded_terms)
    if location.name.casefold() in INTERNAL_CONTROL_NAMES or set(location.parts) & INTERNAL_CONTROL_PARTS:
        findings.append((location, "internal_control_artifact"))
    if location.name.casefold() == ".ds_store":
        findings.append((location, "operating_system_metadata"))
    return findings


def scan(root: Path, deny_terms: Sequence[str] = ()):
    findings = []
    scanned = 0
    if not root.is_dir():
        return scanned, [(Path("."), "candidate_root")]
    folded_terms = tuple(term.casefold() for term in deny_terms)
    for path in candidate_paths(root):
        relative = path.relative_to(root)
        if path.is_symlink():
            findings.append((relative, "symlink"))
            continue
        findings.extend(path_findings(relative, folded_terms))
        if not path.is_file():
            continue
        if path.suffix.casefold() == ".pptx":
            try:
                with ZipFile(path) as archive:
                    for member in archive.infolist():
                        location = Path(relative.as_posix() + "!/") / member.filename
                        findings.extend(path_findings(location, folded_terms))
                        if not member.filename.casefold().endswith((".xml", ".rels")):
                            continue
                        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
                        document = ET.fromstring(archive.read(member), parser=parser)
                        # Parse the declared XML encoding and entities; retain attributes,
                        # comments and text split across formatting runs without extraction.
                        text = ET.tostring(document, encoding="unicode") + "\n" + "".join(document.itertext())
                        scanned += 1
                        findings.extend(text_findings(location, text, folded_terms))
            except (OSError, BadZipFile, ET.ParseError, RuntimeError, LookupError):
                findings.append((relative, "unreadable_pptx"))
            continue
        text = read_utf8_text(path)
        if text is None:
            continue
        scanned += 1
        findings.extend(text_findings(relative, text, folded_terms))
    return scanned, findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan one public-release candidate tree.")
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--deny-term-file",
        type=Path,
        help="Optional private newline-delimited terms used only for this scan.",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    deny_terms = load_deny_terms(args.deny_term_file) if args.deny_term_file else ()
    scanned, findings = scan(root, deny_terms)
    for path, rule in findings:
        display_path = str(path)
        for term in sorted(deny_terms, key=len, reverse=True):
            display_path = re.sub(re.escape(term), "[redacted]", display_path, flags=re.IGNORECASE)
        print(f"FAIL {rule}: {display_path}")
    print(f"scanned={scanned} failures={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
