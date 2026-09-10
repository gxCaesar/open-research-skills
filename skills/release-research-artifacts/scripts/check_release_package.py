#!/usr/bin/env python3
"""Check a built release package from outside the workspace that produced it.

Point this at an unpacked package directory, not at a working repository. Findings are
printed as `rule_id: location`; the command exits 1 when any finding is reported.

What it establishes: the released file set matches the record that ships with it, every
listed file is present and unchanged, nothing is present that the record does not list,
every dependency in requirements.txt names one version, and no obvious identity survives
in the text. What it cannot establish: that the package reproduces the paper; and, when the
environment is declared in environment.yml or pyproject.toml instead, whether anything in
those files is pinned at all -- their presence is checked, their contents are not. Only running it does that, from a
fresh unpack, and the record is where that run is written down.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

RECORD_NAME = "RELEASED_FILES.json"
RECORD_FIELDS = ("built_from_commit", "built_on", "digest_algorithm", "files", "verification")
VERIFICATION_FIELDS = ("interpreter", "platform", "command", "result")
VERSION_CONTROL = {".git", ".hg", ".svn", ".bzr"}
ENVIRONMENT_FILES = ("requirements.txt", "environment.yml", "environment.yaml", "pyproject.toml")
# "Pinned" has to mean one version, not merely "an operator is present". The previous
# pattern accepted >=, !=, ~=, ==1.* and a direct reference to a moving branch, so a
# requirements file that resolves differently next week passed a check whose own header
# promises the environment is pinned. Accepted now: == or === to a version with no
# wildcard, a direct reference ending in a full commit sha, or a hash-pinned line.
PIN = re.compile(r"===?\s*[^*\s,;]+$|@\s*[0-9a-fA-F]{40}$|--hash=")


def requirement_core(line: str) -> str:
    """Drop the parts of a requirement line that a pin check must not read.

    A trailing comment and a PEP 508 environment marker are both ordinary in a correctly
    pinned file, and both sit after the version. Letting the pattern meet them made
    `numpy==1.2.3 ; python_version<"3.10"` report as unpinned -- a false rejection of a file
    that is pinned, which is worse than the loose pattern this replaced.
    """
    core = line.split(" #", 1)[0].split("\t#", 1)[0]
    core = core.split(";", 1)[0]
    return core.strip()
ABSOLUTE_HOME = re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".DS_Store"}


def path_free_exception_summary(error: BaseException) -> str:
    """Describe a read failure without repeating the caller's absolute path."""
    if isinstance(error, json.JSONDecodeError):
        return f"invalid JSON at line {error.lineno}, column {error.colno}"
    if isinstance(error, OSError):
        return f"{type(error).__name__}: {error.strerror}" if error.strerror else type(error).__name__
    return type(error).__name__


def blank(value) -> bool:
    return value in (None, "", [], {})


def digest_of(path: Path, algorithm: str) -> str:
    engine = hashlib.new(algorithm)
    engine.update(path.read_bytes())
    return engine.hexdigest()


def package_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = set(path.relative_to(root).parts)
        if parts & SKIP_DIRS or parts & VERSION_CONTROL:
            continue
        yield path


def check(root: Path, mode: str, deny_terms=()):  # noqa: C901 - one rule per branch
    findings = []
    record_path = root / RECORD_NAME
    if not record_path.is_file():
        return [("release_record_missing", RECORD_NAME)], 0
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except ValueError as error:
        return [("release_record_unreadable",
                 f"{RECORD_NAME} ({path_free_exception_summary(error)})")], 0

    for field in RECORD_FIELDS:
        if blank(record.get(field)):
            findings.append(("release_record_missing_field", field))

    verification = record.get("verification")
    if isinstance(verification, dict):
        for field in VERIFICATION_FIELDS:
            if blank(verification.get(field)):
                findings.append(("verification_missing_field", f"verification.{field}"))
    elif verification is not None:
        findings.append(("verification_is_not_an_object", "verification"))

    algorithm = record.get("digest_algorithm")
    usable = isinstance(algorithm, str) and algorithm in hashlib.algorithms_available
    if algorithm is not None and not usable:
        findings.append(("digest_algorithm_unavailable", "digest_algorithm"))

    listed = {}
    for index, entry in enumerate(record.get("files") or []):
        where = f"files[{index}]"
        if not isinstance(entry, dict):
            findings.append(("file_entry_is_not_an_object", where))
            continue
        relative = entry.get("path")
        if blank(relative):
            findings.append(("file_entry_without_a_path", where))
            continue
        if ".." in Path(str(relative)).parts or str(relative).startswith("/"):
            findings.append(("listed_path_escapes_the_package", f"{where}:{relative}"))
            continue
        listed[str(relative)] = entry
        target = root / str(relative)
        if not target.is_file():
            findings.append(("listed_file_absent", str(relative)))
            continue
        if entry.get("bytes") is None:
            findings.append(("file_entry_without_a_size", f"{where}.bytes"))
        elif entry["bytes"] != target.stat().st_size:
            findings.append(("size_does_not_match_the_record", str(relative)))
        if blank(entry.get("digest")):
            findings.append(("file_entry_without_a_digest", f"{where}.digest"))
        elif usable and digest_of(target, algorithm) != entry["digest"]:
            findings.append(("digest_does_not_match_the_record", str(relative)))

    # Everything in the package must be on the list; an exclusion list is a claim about
    # what you did not think of, and the leak is always in that set.
    present = []
    for path in package_files(root):
        relative = path.relative_to(root).as_posix()
        present.append(relative)
        if relative != RECORD_NAME and relative not in listed:
            findings.append(("file_present_but_not_listed", relative))

    # Recursive, not root-only. package_files() excludes these directories at every depth,
    # so a nested one was invisible to both the unlisted-file rule and the identity scan: a
    # src/.git/config carrying an author email passed a clean anonymised run. A checker that
    # promises no version-control metadata has to look where it excluded itself from looking.
    for path in sorted(root.rglob("*")):
        if not path.is_dir():
            continue
        name = path.name
        relative = path.relative_to(root).as_posix()
        if name in VERSION_CONTROL:
            findings.append(("version_control_metadata_present", relative))
        elif name in SKIP_DIRS and name != ".DS_Store":
            findings.append(("build_cache_present", relative))

    if not any((root / name).is_file() for name in ENVIRONMENT_FILES):
        findings.append(("environment_specification_missing", "|".join(ENVIRONMENT_FILES)))
    requirements = root / "requirements.txt"
    if requirements.is_file():
        for number, line in enumerate(requirements.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith(("-r", "--requirement", "-e", "--editable")):
                # An include pulls in pins this run never read; an editable install has none.
                # Skipping them silently is how a file with no pins at all passes.
                findings.append(("dependency_source_not_followed", f"requirements.txt:{number}"))
                continue
            if stripped.startswith("-"):
                continue
            if not PIN.search(requirement_core(stripped)):
                findings.append(("dependency_not_pinned", f"requirements.txt:{number}"))

    if not any((root / name).is_file() for name in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
        findings.append(("licence_missing", "LICENSE"))

    if mode == "named":
        if not any((root / n).is_file() for n in ("CITATION.cff", "codemeta.json")):
            findings.append(("citation_metadata_missing", "CITATION.cff"))
        if blank(record.get("persistent_identifier")):
            findings.append(("persistent_identifier_missing", "persistent_identifier"))
        if blank(record.get("code_licence")) or blank(record.get("data_licence")):
            findings.append(("code_and_data_licences_not_stated_separately", "code_licence|data_licence"))

    # --- identity -------------------------------------------------------------
    folded = tuple(term.casefold() for term in deny_terms)
    for relative in present:
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            findings.append(("file_not_readable_as_text_and_not_inspected", relative))
            continue
        if ABSOLUTE_HOME.search(text):
            findings.append(("absolute_home_path_in_released_file", relative))
        if EMAIL.search(text):
            findings.append(("email_address_in_released_file", relative))
        lowered = text.casefold()
        if any(term in lowered for term in folded):
            findings.append(("release_specific_term_in_released_file", relative))
        if any(term in relative.casefold() for term in folded):
            findings.append(("release_specific_term_in_a_filename", relative))
    return findings, len(present)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="an unpacked package directory")
    parser.add_argument("--mode", choices=("anonymized", "named"), default="anonymized")
    parser.add_argument("--deny-term-file", type=Path, default=None)
    args = parser.parse_args()

    if not args.package.is_dir():
        print(f"FAIL package_directory_missing: {args.package.name}")
        print("scanned=0 failures=1")
        return 1
    deny_terms = ()
    if args.deny_term_file is not None:
        deny_terms = tuple(
            line.strip()
            for line in args.deny_term_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    findings, scanned = check(args.package, args.mode, deny_terms)
    for rule, location in findings:
        print(f"FAIL {rule}: {location}")
    print(f"scanned={scanned} failures={len(findings)} mode={args.mode} deny_terms={len(deny_terms)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
