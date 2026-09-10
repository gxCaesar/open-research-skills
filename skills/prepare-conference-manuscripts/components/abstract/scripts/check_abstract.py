#!/usr/bin/env python3
"""Validate the word count, paragraph form, and reference-freedom of an abstract.

Backward compatible with the original AAAI checker: with no flags it enforces a
150-200 word, single-paragraph abstract. Flags widen it to other venues:

  --min-words / --max-words   length window (from the live CFP).
  --max-paragraphs N          allow up to N blocks, for journal *structured*
                              abstracts (IMRaD: Background/Methods/Results/...).
  --forbid-citations          FAIL if the abstract contains a citation, \\cite
                              command, DOI, or URL (many conferences ban these).
  --venue NAME                apply an editorial length/paragraph/citation preset
                              (see --venue list). Explicit flags override it.

Venue presets are editing aids, not submission rules. Confirm the live CFP or submission
form (see references/venue-conventions.md). Explicit --min-words/--max-words/
--max-paragraphs/--forbid-citations always override the preset.

Exit codes: 0 = PASS, 1 = FAIL (out of range / too many paragraphs /
citations found when forbidden), 2 = usage or empty-input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


# One word = a run of alphanumerics, keeping internal apostrophes and hyphens
# as a single token ("state-of-the-art" and "don't" each count once).
WORD_RE = re.compile(
    r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*(?:-[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*)*"
)

# Citation / reference signals, checked only under --forbid-citations. Kept
# high-precision to avoid flagging ordinary prose. Each entry is (label, regex).
CITATION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("bracket-numeric", re.compile(r"\[\s*\d+(?:\s*[-,;]\s*\d+)*\s*\]")),
    ("latex-cite", re.compile(r"\\cite[a-zA-Z]*\b")),
    (
        "author-year",
        re.compile(
            r"\([A-Z][A-Za-z.'-]+"
            r"(?:\s+et\s+al\.?|\s+(?:and|&)\s+[A-Z][A-Za-z.'-]+)?"
            r",?\s*\d{4}[a-z]?\)"
        ),
    ),
    ("url", re.compile(r"https?://\S+|\bwww\.\S+", re.IGNORECASE)),
    ("doi", re.compile(r"\bdoi:\s*\S+|\bdoi\.org/\S+", re.IGNORECASE)),
]

# Provisional per-venue defaults, sourced from references/venue-conventions.md.
# Keys: min, max, paras, forbid, note. These are convenience defaults only; the
# live CFP is authoritative and explicit CLI flags override them. "No hard cap"
# conferences use soft guardrails (100-300) — set --min/--max for a real target.
_NOCAP_CONF = "broad single-paragraph editorial range; set explicit values from the current venue instructions."
VENUES: dict[str, dict] = {
    # --- conferences: single paragraph, no references in the abstract ---
    "aaai": {"min": 150, "max": 200, "paras": 1, "forbid": True,
             "note": "150-200 editorial target; not verified as a current official limit."},
    "neurips": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "icml": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "iclr": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "cvpr": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "iccv": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "eccv": {"min": 70, "max": 150, "paras": 1, "forbid": True,
             "note": "70-150 editorial range; confirm the current official limit."},
    "acl": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "emnlp": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "kdd": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "www": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    "sigir": {"min": 100, "max": 300, "paras": 1, "forbid": True, "note": _NOCAP_CONF},
    # --- journals ---
    "nature": {"min": 100, "max": 200, "paras": 1, "forbid": False,
               "note": "100-200 editorial range with citations allowed by this preset."},
    "nature-communications": {"min": 100, "max": 200, "paras": 1, "forbid": True,
                              "note": "100-200 editorial range; confirm current instructions."},
    "nature-methods": {"min": 80, "max": 150, "paras": 1, "forbid": True,
                       "note": "80-150 unstructured editorial range; confirm current instructions."},
    "bioinformatics": {"min": 100, "max": 300, "paras": 5, "forbid": True,
                       "note": "structured editorial preset with up to five blocks; confirm required headings."},
    "cell": {"min": 80, "max": 150, "paras": 1, "forbid": True,
             "note": "80-150 unstructured editorial range; confirm current article-type rules."},
    "tpami": {"min": 150, "max": 250, "paras": 1, "forbid": True,
              "note": "150-250 editorial range; confirm current journal instructions."},
    "plos": {"min": 100, "max": 300, "paras": 1, "forbid": True,
             "note": "100-300 unstructured editorial range; confirm the target journal."},
    "elsevier-structured": {"min": 100, "max": 250, "paras": 4, "forbid": True,
                            "note": "four-block editorial preset; confirm journal-specific headings and limit."},
}
VENUE_ALIASES = {
    "nips": "neurips",
    "thewebconf": "www",
    "www2026": "www",
    "ncomms": "nature-communications",
    "nature-comms": "nature-communications",
    "nat-methods": "nature-methods",
    "bioinf": "bioinformatics",
    "elsevier": "elsevier-structured",
}


def resolve_venue(name: str) -> Optional[tuple[str, dict]]:
    """Return (canonical_name, preset) for a venue string, or None if unknown."""
    key = name.strip().lower()
    key = VENUE_ALIASES.get(key, key)
    if key in VENUES:
        return key, VENUES[key]
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that an abstract meets a venue's length, paragraph, and reference rules."
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="UTF-8 text file containing only the abstract body; read stdin if omitted.",
    )
    # Defaults are None so we can tell "user passed it" from "use venue/fallback".
    parser.add_argument("--min-words", type=int, default=None)
    parser.add_argument("--max-words", type=int, default=None)
    parser.add_argument(
        "--max-paragraphs",
        type=int,
        default=None,
        help="Maximum blank-line-separated blocks (>1 for structured journal abstracts).",
    )
    parser.add_argument(
        "--forbid-citations",
        action="store_true",
        help="Fail if the abstract contains a citation, \\cite command, DOI, or URL.",
    )
    parser.add_argument(
        "--venue",
        default=None,
        help="Apply a venue preset (e.g. aaai, neurips, eccv, bioinformatics). "
        "Pass 'list' to print known venues. Explicit flags override the preset.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def read_text(path: Optional[Path]) -> str:
    if path is None:
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def path_free_exception_summary(error: BaseException) -> str:
    """Describe a read failure without repeating the caller's absolute path."""
    if isinstance(error, OSError):
        return f"{type(error).__name__}: {error.strerror}" if error.strerror else type(error).__name__
    return type(error).__name__


def find_citations(text: str) -> list[str]:
    """Return sorted unique citation-like snippets found in the text."""
    hits: set[str] = set()
    for _label, pattern in CITATION_PATTERNS:
        for match in pattern.findall(text):
            snippet = match if isinstance(match, str) else match[0]
            hits.add(snippet.strip())
    return sorted(hits)


def main() -> int:
    args = parse_args()

    # --venue list -> print the roster and exit cleanly.
    if args.venue is not None and args.venue.strip().lower() == "list":
        print("Known venues (editorial presets — confirm the live venue rules):")
        for name in sorted(VENUES):
            v = VENUES[name]
            forbid = "no-refs" if v["forbid"] else "refs-ok"
            print(f"  {name:24s} {v['min']}-{v['max']} words, <={v['paras']} para, {forbid}")
        return 0

    # Resolve the venue preset, if any.
    preset = None
    venue_name = None
    if args.venue is not None:
        resolved = resolve_venue(args.venue)
        if resolved is None:
            print(
                f"Unknown venue '{args.venue}'. Run with --venue list to see options.",
                file=sys.stderr,
            )
            return 2
        venue_name, preset = resolved

    # Effective settings: explicit CLI flag > venue preset > built-in default.
    def pick(cli_value, preset_key, fallback):
        if cli_value is not None:
            return cli_value
        if preset is not None:
            return preset[preset_key]
        return fallback

    min_words = pick(args.min_words, "min", 150)
    max_words = pick(args.max_words, "max", 200)
    max_paragraphs = pick(args.max_paragraphs, "paras", 1)
    # forbid-citations is a store_true flag; an explicit --forbid-citations (True)
    # always wins, otherwise fall back to the venue preset (or False).
    forbid_citations = args.forbid_citations or (preset["forbid"] if preset else False)

    if min_words < 0 or max_words < min_words:
        print("Invalid word range.", file=sys.stderr)
        return 2
    if max_paragraphs < 1:
        print("--max-paragraphs must be at least 1.", file=sys.stderr)
        return 2

    try:
        text = read_text(args.file).strip()
    except (OSError, UnicodeDecodeError) as error:
        name = args.file.name if args.file is not None else "standard input"
        print(f"Could not read {name}: {path_free_exception_summary(error)}", file=sys.stderr)
        return 2
    if not text:
        print("No abstract text supplied.", file=sys.stderr)
        return 2

    word_count = len(WORD_RE.findall(text))
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    citations = find_citations(text) if forbid_citations else []

    count_ok = min_words <= word_count <= max_words
    paragraph_ok = len(paragraphs) <= max_paragraphs
    citations_ok = not citations
    passed = count_ok and paragraph_ok and citations_ok

    venue_note = f"[venue={venue_name}] {preset['note']}" if preset else None

    result = {
        "status": "PASS" if passed else "FAIL",
        "word_count": word_count,
        "min_words": min_words,
        "max_words": max_words,
        "paragraphs": len(paragraphs),
        "max_paragraphs": max_paragraphs,
        "forbid_citations": forbid_citations,
        "citations_found": citations,
        "venue": venue_name,
        "preset_kind": "editorial_default" if preset else None,
    }

    if args.as_json:
        if venue_note:
            result["venue_note"] = venue_note
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    else:
        if venue_note:
            print(venue_note)
        print(f"Word count: {word_count}")
        print(f"Paragraphs: {len(paragraphs)}")
        if not count_ok:
            if word_count < min_words:
                print(f"Add at least {min_words - word_count} word(s).")
            else:
                print(f"Remove at least {word_count - max_words} word(s).")
        if not paragraph_ok:
            if max_paragraphs == 1:
                print("Merge the abstract into one paragraph.")
            else:
                print(
                    f"Reduce to at most {max_paragraphs} paragraph(s); "
                    f"found {len(paragraphs)}."
                )
        if not citations_ok:
            print(
                f"Remove {len(citations)} citation/URL marker(s): "
                f"{', '.join(citations)}"
            )
        print(f"Status: {result['status']}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
