"""Hold every bundled script to three things the repository already assumed.

Each was assumed rather than checked, and each had drifted somewhere:

- A validator must not print the caller's absolute path. One copy of the statistics
  validator had been hardened for this and its twin had not, so the journal copy
  reported `"target": "<absolute path>"` while the conference copy reported a basename.
- Scripts bundled into more than one install unit must stay byte-identical. Nothing
  asserted it, which is how that pair drifted apart in the first place.
- Everything must run on the oldest interpreter the project supports.
"""

import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Built by concatenation so this file does not itself contain the literal the
# repository's content scan rejects.
MACHINE_PATH = re.compile(r"/(?:" + "Users" + "|" + "home" + r")/[A-Za-z0-9._-]+/")
MISSING_INPUT = "/" + "Users" + "/nobody-xyz/missing-input.json"

# Validators with a shipped example, run on their own clean input.
WITH_EXAMPLES = (
    ("skills/prepare-journal-manuscripts/components/statistics-reporting/scripts/validate_analysis_register.py",
     "skills/prepare-journal-manuscripts/components/statistics-reporting/examples/analysis-register.example.json",
     ("--mode", "final")),
    ("skills/prepare-conference-manuscripts/components/statistics-reporting/scripts/validate_analysis_register.py",
     "skills/prepare-conference-manuscripts/components/statistics-reporting/examples/analysis-register.example.json",
     ("--mode", "final")),
    ("skills/prepare-journal-manuscripts/components/data-availability/scripts/validate_data_inventory.py",
     "skills/prepare-journal-manuscripts/components/data-availability/examples/data-inventory.example.json",
     ("--mode", "final")),
    ("skills/prepare-journal-manuscripts/components/code-availability/scripts/validate_code_inventory.py",
     "skills/prepare-journal-manuscripts/components/code-availability/examples/code-inventory.example.json",
     ("--mode", "final")),
    ("skills/research-publication-pipeline/components/project-handover/scripts/validate_handover_pack.py",
     "skills/research-publication-pipeline/components/project-handover/examples/handover-pack.example.json",
     ("--mode", "final")),
    ("skills/release-research-artifacts/scripts/check_release_package.py",
     "skills/release-research-artifacts/examples/release-package", ("--mode", "named")),
    ("skills/develop-method-to-sota/scripts/check_iteration_ledger.py",
     "skills/develop-method-to-sota/examples/iteration-ledger/clean.json", ()),
    ("skills/survey-and-audit-novelty/scripts/check_survey_ledger.py",
     "skills/survey-and-audit-novelty/examples/survey-ledger/clean.json", ()),
    ("skills/run-cold-review-panel/scripts/check_panel_round.py",
     "skills/run-cold-review-panel/examples/panel-round/clean.json", ()),
    ("skills/review-others-manuscripts/scripts/check_referee_report.py",
     "skills/review-others-manuscripts/examples/referee-report/clean.json", ()),
)

# Scripts bundled into more than one install unit. Copies must match byte for byte.
SHARED_IMPLEMENTATIONS = {
    "render_evidence_figure.py": 4,
    "check_abstract.py": 2,
    "validate_analysis_register.py": 2,
    "run_selftest.py": 2,
}
# Same basename, different skill, genuinely different code. Listed so the two sets
# together account for every repeated basename and no group escapes the check.
INDEPENDENT_NAMESAKES = {"render.py", "run_demo.py", "synthetic_workspace.py",
                         "test_check_abstract.py"}


def bundled_validators() -> list:
    return sorted(
        path for pattern in ("skills/**/validate_*.py", "skills/**/check_*.py")
        for path in ROOT.glob(pattern) if "__pycache__" not in str(path)
    )


def run(script: Path, *args) -> str:
    result = subprocess.run(
        [sys.executable, "-B", str(script), *args], text=True, capture_output=True, check=False
    )
    return result.stdout + result.stderr


def repeated_basenames() -> dict:
    groups = defaultdict(list)
    for path in ROOT.glob("skills/**/*.py"):
        if "__pycache__" not in str(path):
            groups[path.name].append(path)
    return {name: paths for name, paths in groups.items() if len(paths) > 1}


OLDEST = (3, 9)
BUILTIN_GENERICS = {"list", "dict", "set", "tuple", "frozenset", "type"}


def bundled_scripts() -> list:
    scripts = [p for p in ROOT.glob("skills/**/*.py") if "__pycache__" not in str(p)]
    scripts += sorted(ROOT.glob("scripts/*.py"))
    assert len(scripts) >= 50, "the sweep found almost nothing"
    return sorted(scripts)


def defers_annotations(tree: ast.Module) -> bool:
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == "__future__"
        and any(alias.name == "annotations" for alias in node.names)
        for node in tree.body
    )


def eager_modern_annotations(tree: ast.Module) -> list:
    """Annotations that Python 3.9 evaluates at definition time and cannot resolve."""
    found = []

    def scan(annotation, where):
        for node in ast.walk(annotation):
            if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name)
                    and node.value.id in BUILTIN_GENERICS):
                found.append(f"{where}: {node.value.id}[...]")
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                found.append(f"{where}: X | Y")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            arguments = list(node.args.args) + list(node.args.kwonlyargs) + list(node.args.posonlyargs)
            for argument in arguments:
                if argument.annotation is not None:
                    scan(argument.annotation, node.name)
            if node.returns is not None:
                scan(node.returns, node.name)
        elif isinstance(node, ast.AnnAssign) and node.annotation is not None:
            scan(node.annotation, "module annotation")
    return found


REPORTERS = {"add", "error", "warn", "mapping", "sequence",
             "require_text", "require_enum", "require_verified_sources"}
# Rules that nothing exercises. Empty on purpose: the repository-wide count was 32 when
# this sweep was first run and reached zero by writing the missing witnesses.
UNEXERCISED_RULES: frozenset = frozenset()


def declared_rule_ids(source: str) -> set:
    """Rule identifiers a checker can emit, including those passed through helpers."""
    rules = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else (
            node.func.id if isinstance(node.func, ast.Name) else "")
        if name in REPORTERS:
            for argument in node.args:
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str) \
                   and re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", argument.value):
                    rules.add(argument.value)
        if name == "add":
            for argument in node.args:
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str) \
                   and re.fullmatch(r"[a-z][a-z0-9_]{4,}", argument.value):
                    rules.add(argument.value)
        for keyword in node.keywords:
            if keyword.arg == "rule_id" and isinstance(keyword.value, ast.Constant):
                rules.add(keyword.value.value)
    return rules


def witness_corpus() -> str:
    sources = [p.read_text(encoding="utf-8") for p in ROOT.glob("tests/**/*.py")]
    sources.append((ROOT / "scripts" / "check_rule_coverage.py").read_text(encoding="utf-8"))
    return " ".join(sources)


def unexercised_rules() -> dict:
    corpus = witness_corpus()
    missing = {}
    for path in bundled_scripts():
        gap = sorted(
            rule for rule in declared_rule_ids(path.read_text(encoding="utf-8"))
            if not re.search(r"\b" + re.escape(rule) + r"\b", corpus)
        )
        if gap:
            missing[str(path.relative_to(ROOT))] = gap
    return missing


class BundledScriptHygieneTest(unittest.TestCase):
    def test_no_validator_prints_a_machine_path_on_bad_input(self):
        validators = bundled_validators()
        self.assertGreaterEqual(len(validators), 17, "the sweep found almost nothing")
        for script in validators:
            with self.subTest(script=script.relative_to(ROOT)):
                self.assertIsNone(MACHINE_PATH.search(run(script, MISSING_INPUT)))

    def test_no_validator_prints_a_machine_path_on_its_own_example(self):
        for relative, target, extra in WITH_EXAMPLES:
            with self.subTest(script=relative):
                output = run(ROOT / relative, str(ROOT / target), *extra)
                self.assertIsNone(MACHINE_PATH.search(output))

    def test_the_leak_detector_catches_a_planted_leak(self):
        """A sweep that reports nothing and a sweep that is not running look the same."""
        with tempfile.TemporaryDirectory() as tmp:
            leaky = Path(tmp) / "check_leaky.py"
            leaky.write_text(
                "import sys\nprint('target: /' + 'Users' + '/someone/project/x.json')\n",
                encoding="utf-8",
            )
            self.assertIsNotNone(MACHINE_PATH.search(run(leaky, MISSING_INPUT)))

    def test_every_rule_any_bundled_checker_can_emit_is_exercised(self):
        """A rule nothing reaches could stop working with this suite still green."""
        missing = unexercised_rules()
        self.assertEqual({}, missing)
        self.assertEqual(frozenset(), UNEXERCISED_RULES)

    def test_the_rule_sweep_reaches_a_meaningful_number_of_rules(self):
        """A sweep that finds nothing reports the same clean result as a healthy one."""
        total = sum(len(declared_rule_ids(p.read_text(encoding="utf-8")))
                    for p in bundled_scripts())
        self.assertGreaterEqual(total, 150, total)

    def test_the_rule_sweep_reports_a_rule_nothing_exercises(self):
        # The name is composed at runtime. Written as one literal it would appear in this
        # file, which the corpus reads, and the control would report itself as covered.
        planted_rule = "PLANTED" + "_RULE_" + "WITH_NO_WITNESS"
        with tempfile.TemporaryDirectory() as tmp:
            planted = Path(tmp) / "check_planted.py"
            planted.write_text(
                "def add(findings, rule_id, severity, location, message):\n"
                "    findings.append(rule_id)\n\n\n"
                "def check(findings):\n"
                f'    add(findings, "{planted_rule}", "error", "x", "y")\n',
                encoding="utf-8",
            )
            declared = declared_rule_ids(planted.read_text(encoding="utf-8"))
            self.assertIn(planted_rule, declared)
            self.assertNotIn(planted_rule, witness_corpus())

    def test_shared_implementations_are_byte_identical(self):
        groups = repeated_basenames()
        for name, expected in SHARED_IMPLEMENTATIONS.items():
            with self.subTest(script=name):
                paths = groups.get(name, [])
                self.assertEqual(expected, len(paths), name)
                digests = {hashlib.blake2b(path.read_bytes()).hexdigest() for path in paths}
                self.assertEqual(1, len(digests),
                                 [str(p.relative_to(ROOT)) for p in paths])

    def test_every_repeated_basename_is_declared_one_way_or_the_other(self):
        """A new shared script must be declared, not silently left unchecked."""
        declared = set(SHARED_IMPLEMENTATIONS) | INDEPENDENT_NAMESAKES
        self.assertEqual(set(), set(repeated_basenames()) - declared)
        self.assertEqual(set(), declared - set(repeated_basenames()))

    def test_every_bundled_script_is_valid_on_the_oldest_supported_python(self):
        for path in bundled_scripts():
            with self.subTest(script=path.relative_to(ROOT)):
                ast.parse(path.read_text(encoding="utf-8"), str(path), feature_version=OLDEST)

    def test_no_bundled_script_evaluates_a_modern_annotation_eagerly(self):
        """Syntax alone does not catch this, and it is what actually broke here before.

        `def f(x: list[str])` parses on 3.9 and raises at import time, because the
        annotation is evaluated when the function is defined. `from __future__ import
        annotations` defers it. A whole-file syntax check passes such a file.
        """
        for path in bundled_scripts():
            tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
            if defers_annotations(tree):
                continue
            with self.subTest(script=path.relative_to(ROOT)):
                self.assertEqual([], eager_modern_annotations(tree))

    def test_the_annotation_check_catches_a_planted_violation(self):
        planted = ast.parse("def f(x: list[str]) -> dict[str, int]:\n    return {}\n")
        self.assertFalse(defers_annotations(planted))
        self.assertNotEqual([], eager_modern_annotations(planted))
        deferred = ast.parse(
            "from __future__ import annotations\n\n\ndef f(x: list[str]):\n    return x\n"
        )
        self.assertTrue(defers_annotations(deferred))


if __name__ == "__main__":
    unittest.main()
