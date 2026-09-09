"""Regression tests for scripts/check_abstract.py.

Run from the skill root:  python3 -m pytest tests/ -q
(No third-party deps beyond pytest; the script is stdlib-only.)
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_abstract.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_abstract", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CA = _load_module()


def run(text: str, *args: str):
    """Invoke the CLI with `text` on stdin; return (exit_code, stdout)."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=text,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout


def words(n: int) -> str:
    """A body of exactly n words (each a bare token)."""
    return " ".join(["word"] * n)


# --- tokenization -----------------------------------------------------------

def test_hyphen_and_apostrophe_count_as_one_word():
    assert len(CA.WORD_RE.findall("one two-three don't four")) == 4
    assert len(CA.WORD_RE.findall("state-of-the-art")) == 1


# --- citation detection -----------------------------------------------------

def test_find_citations_catches_all_forms():
    text = (
        "prior work [12] and [1, 2] and (Smith, 2020) and (Smith et al., 2020) "
        "and (Smith and Jones, 2019b) and (Doe & Roe, 2018); "
        "see https://example.com and doi:10.1/x and \\citep{foo}"
    )
    hits = CA.find_citations(text)
    assert "[12]" in hits
    assert "(Smith, 2020)" in hits
    assert "(Smith et al., 2020)" in hits
    assert "(Smith and Jones, 2019b)" in hits
    assert "(Doe & Roe, 2018)" in hits
    assert any(h.startswith("https://") for h in hits)
    assert any("doi" in h for h in hits)
    assert any(h.startswith("\\cite") for h in hits)


def test_find_citations_no_false_positive_on_prose_with_numbers():
    text = "we improve accuracy by 12 points over the 2020 baseline in Figure 2"
    assert CA.find_citations(text) == []


# --- CLI: length ------------------------------------------------------------

def test_default_window_pass():
    code, out = run(words(160))
    assert code == 0 and "PASS" in out


def test_default_window_too_short():
    code, out = run(words(100))
    assert code == 1 and "Add at least" in out


def test_default_window_too_long():
    code, out = run(words(220))
    assert code == 1 and "Remove at least" in out


def test_custom_window_allows_short_theory_abstract():
    code, _ = run(words(52), "--min-words", "50", "--max-words", "250")
    assert code == 0


# --- CLI: paragraphs (structured abstracts) ---------------------------------

def test_structured_fails_at_one_paragraph_default():
    text = "Background: a.\n\nMethods: b.\n\nResults: c.\n\nConclusions: d."
    code, out = run(text, "--min-words", "3", "--max-words", "250")
    assert code == 1 and "one paragraph" in out


def test_structured_passes_with_max_paragraphs():
    text = "Background: a.\n\nMethods: b.\n\nResults: c.\n\nConclusions: d."
    code, _ = run(text, "--min-words", "3", "--max-words", "250", "--max-paragraphs", "4")
    assert code == 0


# --- CLI: citation guard ----------------------------------------------------

def test_forbid_citations_fails_when_present():
    code, out = run(words(20) + " [12]", "--min-words", "5", "--max-words", "300",
                    "--forbid-citations")
    assert code == 1 and "[12]" in out


def test_citations_ignored_without_flag():
    code, _ = run(words(160) + " [12]")
    assert code == 0  # length ok, citation not checked


# --- CLI: error codes -------------------------------------------------------

def test_empty_input_is_usage_error():
    code, _ = run("   ")
    assert code == 2


def test_invalid_range_is_usage_error():
    code, _ = run(words(160), "--min-words", "200", "--max-words", "100")
    assert code == 2


def test_zero_max_paragraphs_is_usage_error():
    code, _ = run(words(160), "--max-paragraphs", "0")
    assert code == 2


# --- CLI: json shape --------------------------------------------------------

def test_json_output_shape():
    code, out = run(words(160), "--json")
    data = json.loads(out)
    for key in ("status", "word_count", "paragraphs", "max_paragraphs",
                "forbid_citations", "citations_found", "preset_kind"):
        assert key in data
    assert data["status"] == "PASS" and data["word_count"] == 160


# --- CLI: --venue presets ---------------------------------------------------

def test_venue_eccv_applies_70_150_window():
    # 120 words is valid for ECCV (70-150) but would fail the 150-200 default.
    assert run(words(120), "--venue", "eccv")[0] == 0
    assert run(words(160), "--venue", "eccv")[0] == 1  # over the 150 cap


def test_venue_preset_forbids_citations():
    code, out = run(words(160) + " [12]", "--venue", "neurips")
    assert code == 1 and "[12]" in out


def test_venue_nature_allows_citations():
    # The bundled Nature editorial preset permits citations.
    code, _ = run(words(160) + " [12]", "--venue", "nature")
    assert code == 0


def test_explicit_flag_overrides_venue():
    # ECCV caps at 150, but an explicit --max-words widens it.
    assert run(words(160), "--venue", "eccv", "--max-words", "300")[0] == 0


def test_venue_alias_resolves():
    assert run(words(120), "--venue", "nips")[1]  # 'nips' -> neurips, runs fine
    code, out = run(words(120), "--venue", "nips", "--json")
    assert json.loads(out)["venue"] == "neurips"


def test_venue_structured_journal_allows_multiple_paragraphs():
    text = "Motivation: a.\n\nResults: b.\n\nAvailability: c."
    code, _ = run(text, "--venue", "bioinformatics", "--min-words", "3")
    assert code == 0  # bioinformatics preset allows up to 5 paragraphs


def test_unknown_venue_is_usage_error():
    code, _ = run(words(160), "--venue", "nosuchvenue")
    assert code == 2


def test_venue_list_exits_zero():
    code, out = run("", "--venue", "list")
    assert code == 0 and "neurips" in out and "eccv" in out


def test_venue_field_in_json():
    data = json.loads(run(words(120), "--venue", "eccv", "--json")[1])
    assert data["venue"] == "eccv" and "venue_note" in data


def test_no_venue_json_venue_is_null():
    data = json.loads(run(words(160), "--json")[1])
    assert data["venue"] is None and data["preset_kind"] is None


if __name__ == "__main__":
    # Standalone runner so the suite works without pytest installed.
    tests = sorted(
        (name, obj)
        for name, obj in dict(globals()).items()
        if name.startswith("test_") and callable(obj)
    )
    failures = []
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as exc:  # noqa: BLE001 - report every failure
            failures.append(name)
            print(f"  FAIL  {name}: {exc!r}")
    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
