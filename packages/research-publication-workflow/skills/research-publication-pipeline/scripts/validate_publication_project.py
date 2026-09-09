#!/usr/bin/env python3
"""Validate a portable research-publication project at a named decision boundary."""

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FILES = {
    "project": Path("project.json"),
    "sources": Path("evidence/source-register.json"),
    "intake": Path("intake/intake.json"),
    "protocol": Path("protocol/protocol.json"),
    "headroom": Path("development/headroom.json"),
    "iterations": Path("development/iteration-ledger.json"),
    "claims": Path("claims/claim-register.json"),
    "handoff": Path("handoff/handoff.json"),
}

CONSTRUCTION_ORDER = [
    "recipe_parity",
    "objective_alignment",
    "data_or_representation",
    "ensemble",
    "test_time_compute",
    "architecture",
]

BOUNDARY_VALUE = "EXPLICIT_AUTHORIZATION_REQUIRED"
BOUNDARY_KEYS = {
    "remote_compute",
    "locked_test",
    "canonical_manuscript_mutation",
    "external_write",
}

PUBLIC_SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".go", ".h", ".hpp", ".ipynb", ".java", ".jl",
    ".js", ".kt", ".m", ".py", ".r", ".rs", ".scala", ".sh", ".sql", ".ts",
}
PUBLIC_DEPENDENCY_NAMES = {
    "cargo.toml", "description", "dockerfile", "environment.yml", "environment.yaml",
    "go.mod", "manifest.toml", "package.json", "package-lock.json", "pipfile",
    "poetry.lock", "project.toml", "pyproject.toml", "renv.lock", "setup.py", "uv.lock",
}
PUBLIC_DOCUMENT_SUFFIXES = {"", ".md", ".rst", ".txt"}
VALIDATION_SCOPE = "records_and_local_artifact_checks"
PRIVATE_MACHINE_PATH = re.compile(
    r"(?<![\w:/\\])(?:/(?:Users|home)/[A-Za-z0-9._-]+/"
    r"|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+[\\/])"
)
INLINE_CONTROL_RECORD = re.compile(
    r"\b(?:pipeline[_-]state|(?:approval|execution|delegated[_-]decision)[_-]receipt)"
    r"[\"']?\s*[:=]",
    re.IGNORECASE,
)
INTEGRITY_COMMAND = re.compile(
    r"\b(?:sha(?:1|224|256|384|512)sum|shasum|md5sum)\s+\S",
    re.IGNORECASE,
)
INTEGRITY_SIDECAR = re.compile(
    r"(?:^(?:checksums?|sha(?:1|224|256|384|512)sums?|md5sums?)(?:\.|$)"
    r"|\.(?:sha(?:1|224|256|384|512)|md5)(?:\.|$))",
    re.IGNORECASE,
)


def matches_public_artifact_role(category, relative):
    """Apply small role checks without prescribing one language or project layout."""
    path = Path(relative)
    name = path.name.casefold()
    parts = {part.casefold() for part in path.parts}
    if category == "source":
        return path.suffix.casefold() in PUBLIC_SOURCE_SUFFIXES or name in {"makefile"}
    if category == "dependency_spec":
        return name in PUBLIC_DEPENDENCY_NAMES or (
            name.startswith("requirements") and path.suffix.casefold() == ".txt"
        )
    if category == "example":
        return bool(parts & {"example", "examples", "sample", "samples"})
    if category == "configuration":
        return path.suffix.casefold() in {".json", ".toml", ".yaml", ".yml"} and (
            bool(parts & {"config", "configs", "configuration", "configurations"})
            or name.startswith("config")
        )
    if category == "tests":
        return bool(parts & {"test", "tests"}) or name.startswith("test_")
    if category == "license":
        return name.startswith("license") or name.startswith("copying")
    if category == "citation":
        return name in {"citation.cff", "codemeta.json"} or path.suffix.casefold() == ".bib"
    if category == "limitations":
        return name.startswith("limitations") and path.suffix.casefold() in PUBLIC_DOCUMENT_SUFFIXES
    if category in {"data_instructions", "run_instructions", "expected_outputs"}:
        return path.suffix.casefold() in PUBLIC_DOCUMENT_SUFFIXES
    return False


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def nonempty_text_list(value):
    return isinstance(value, list) and bool(value) and all(nonempty_text(item) for item in value)


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def read_public_text(path: Path):
    """Read UTF-8 public text without relying on a filename extension."""
    content = path.read_bytes()
    if b"\x00" in content:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None


class ProjectValidator:
    def __init__(self, root: Path, target: str):
        self.root = root.resolve()
        self.target = target
        self.findings = []
        self.documents = {}
        self.sources = {}

    def add(self, level: str, rule_id: str, path: str, message: str) -> None:
        self.findings.append(
            {
                "level": level,
                "rule_id": rule_id,
                "path": path,
                "message": message,
            }
        )

    def error(self, rule_id: str, path: str, message: str) -> None:
        self.add("error", rule_id, path, message)

    def warn(self, rule_id: str, path: str, message: str) -> None:
        self.add("warning", rule_id, path, message)

    def mapping(self, value, rule_id: str, path: str):
        if not isinstance(value, dict):
            self.error(rule_id, path, "must be an object")
            return {}
        return value

    def sequence(self, value, rule_id: str, path: str):
        if not isinstance(value, list):
            self.error(rule_id, path, "must be a list")
            return []
        return value

    def require_text(self, obj, key: str, rule_id: str, path: str) -> str:
        value = obj.get(key) if isinstance(obj, dict) else None
        if not nonempty_text(value):
            self.error(rule_id, f"{path}.{key}", "must be non-empty text")
            return ""
        return value.strip()

    def require_enum(self, obj, key: str, allowed, rule_id: str, path: str):
        value = obj.get(key) if isinstance(obj, dict) else None
        if value not in allowed:
            rendered = ", ".join(sorted(allowed))
            self.error(rule_id, f"{path}.{key}", f"must be one of: {rendered}")
        return value

    def load_documents(self) -> None:
        if not self.root.is_dir():
            self.error("PROJECT_ROOT", ".", "project root is not a directory")
            return
        for key, relative in REQUIRED_FILES.items():
            path = self.root / relative
            if not path.is_file():
                self.error("REQUIRED_FILE", str(relative), "required JSON record is missing")
                self.documents[key] = {}
                continue
            if path.is_symlink() or not inside(self.root, path):
                self.error("PATH_CONTAINMENT", str(relative), "record must be a regular in-project file")
                self.documents[key] = {}
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                self.error("JSON_PARSE", str(relative), f"could not parse JSON: {exc}")
                self.documents[key] = {}
                continue
            if not isinstance(payload, dict):
                self.error("JSON_OBJECT", str(relative), "top-level JSON value must be an object")
                payload = {}
            if payload.get("schema_version") != 1:
                self.error("SCHEMA_VERSION", str(relative), "schema_version must equal 1")
            self.documents[key] = payload

        for path in self.root.rglob("*"):
            if path.is_symlink():
                self.error(
                    "PATH_CONTAINMENT",
                    str(path.relative_to(self.root)),
                    "workspace must not contain symlinks",
                )

    def validate_common(self) -> None:
        self.load_documents()
        project = self.documents.get("project", {})
        self.require_text(project, "project_id", "PROJECT_ID", "project.json")
        self.require_text(project, "title", "PROJECT_TITLE", "project.json")
        self.require_text(project, "domain", "PROJECT_DOMAIN", "project.json")
        self.require_enum(
            project,
            "contribution_lane",
            {"sota-method", "discovery", "benchmark"},
            "CONTRIBUTION_LANE",
            "project.json",
        )
        self.require_enum(
            project,
            "route",
            {"undecided", "top-cs", "nature-family", "dual-track", "stop"},
            "PROJECT_ROUTE",
            "project.json",
        )
        self.require_enum(
            project,
            "current_stage",
            {"intake", "pilot", "development", "evaluation", "handoff", "stopped"},
            "PROJECT_STAGE",
            "project.json",
        )

        boundaries = self.mapping(project.get("boundaries"), "AUTHORITY_BOUNDARY", "project.json.boundaries")
        if set(boundaries) != BOUNDARY_KEYS:
            self.error(
                "AUTHORITY_BOUNDARY",
                "project.json.boundaries",
                "must name exactly the four public authority boundaries",
            )
        for key in BOUNDARY_KEYS:
            if boundaries.get(key) != BOUNDARY_VALUE:
                self.error(
                    "AUTHORITY_BOUNDARY",
                    f"project.json.boundaries.{key}",
                    f"must remain {BOUNDARY_VALUE}",
                )

        source_doc = self.documents.get("sources", {})
        sources = self.sequence(source_doc.get("sources"), "SOURCE_REGISTER", "evidence/source-register.json.sources")
        for index, raw_source in enumerate(sources):
            path = f"evidence/source-register.json.sources[{index}]"
            source = self.mapping(raw_source, "SOURCE_RECORD", path)
            source_id = self.require_text(source, "source_id", "SOURCE_ID", path)
            if source_id:
                if source_id in self.sources:
                    self.error("SOURCE_ID", f"{path}.source_id", "source_id must be unique")
                self.sources[source_id] = source
            self.require_enum(
                source,
                "status",
                {"VERIFIED", "UNVERIFIED", "COULD_NOT_OPEN", "NOT_FOUND"},
                "SOURCE_STATUS",
                path,
            )
            if source.get("status") == "VERIFIED":
                for field in ("kind", "locator", "accessed_on", "inspected_location", "scope"):
                    self.require_text(source, field, "VERIFIED_SOURCE", path)

    def require_verified_sources(self, ids, rule_id: str, path: str) -> None:
        if not nonempty_text_list(ids):
            self.error(rule_id, path, "must contain at least one source_id")
            return
        for source_id in ids:
            source = self.sources.get(source_id)
            if source is None:
                self.error(rule_id, path, f"unknown source_id: {source_id}")
            elif source.get("status") != "VERIFIED":
                self.error(rule_id, path, f"source is not VERIFIED: {source_id}")

    def validate_working(self) -> None:
        project = self.documents.get("project", {})
        intake = self.documents.get("intake", {})
        protocol = self.documents.get("protocol", {})
        headroom = self.documents.get("headroom", {})
        claims = self.documents.get("claims", {})
        handoff = self.documents.get("handoff", {})

        authority = project.get("authority", {}) if isinstance(project.get("authority"), dict) else {}
        if authority.get("status") != "VERIFIED":
            self.warn("AUTHORITY", "project.json.authority", "project authority is not yet VERIFIED")
        data = intake.get("data_feasibility", {}) if isinstance(intake.get("data_feasibility"), dict) else {}
        if data.get("status") != "PASS":
            self.warn("DATA_FEASIBILITY", "intake/intake.json.data_feasibility", "data feasibility is not yet PASS")
        scoop = intake.get("scoop", {}) if isinstance(intake.get("scoop"), dict) else {}
        if scoop.get("verdict") == "UNCERTAIN":
            self.warn("SCOOP_VERDICT", "intake/intake.json.scoop", "lane-specific scoop verdict remains UNCERTAIN")
        venue = intake.get("venue_fit", {}) if isinstance(intake.get("venue_fit"), dict) else {}
        if venue.get("status") != "PASS":
            self.warn("VENUE_FIT", "intake/intake.json.venue_fit", "venue fit is not yet PASS")
        if protocol.get("status") != "FROZEN":
            self.warn("PROTOCOL_FREEZE", "protocol/protocol.json.status", "development protocol is not frozen")
        if headroom.get("status") != "MEASURED":
            self.warn("HEADROOM", "development/headroom.json.status", "headroom has not been measured")
        if not claims.get("claims"):
            self.warn("CLAIM_REGISTER", "claims/claim-register.json.claims", "no claims are registered")
        if handoff.get("terminal_outcome") == "NOT_READY":
            self.warn("HANDOFF", "handoff/handoff.json.terminal_outcome", "terminal handoff is not ready")

    def validate_pilot(self) -> None:
        project = self.documents.get("project", {})
        intake = self.documents.get("intake", {})

        authority = self.mapping(project.get("authority"), "AUTHORITY", "project.json.authority")
        if authority.get("status") != "VERIFIED":
            self.error("AUTHORITY", "project.json.authority.status", "pilot requires VERIFIED project authority")
        conflicts = authority.get("conflicts")
        if not isinstance(conflicts, list) or conflicts:
            self.error("AUTHORITY", "project.json.authority.conflicts", "pilot requires an explicit empty conflict list")
        self.require_verified_sources(authority.get("source_ids"), "AUTHORITY", "project.json.authority.source_ids")

        data = self.mapping(intake.get("data_feasibility"), "DATA_FEASIBILITY", "intake/intake.json.data_feasibility")
        if data.get("status") != "PASS":
            self.error("DATA_FEASIBILITY", "intake/intake.json.data_feasibility.status", "pilot requires data feasibility PASS")
        if not nonempty_text_list(data.get("required_joint_variables")):
            self.error("DATA_FEASIBILITY", "intake/intake.json.data_feasibility.required_joint_variables", "name the variables that must coexist")
        for field in ("coexistence_evidence", "independent_unit", "strongest_cheap_baseline", "leakage_safe_split"):
            self.require_text(data, field, "DATA_FEASIBILITY", "intake/intake.json.data_feasibility")
        unit_count = data.get("independent_unit_count")
        if not isinstance(unit_count, int) or isinstance(unit_count, bool) or unit_count <= 0:
            self.error("DATA_FEASIBILITY", "intake/intake.json.data_feasibility.independent_unit_count", "must be a positive independent-unit count")
        self.require_verified_sources(data.get("data_source_ids"), "DATA_FEASIBILITY", "intake/intake.json.data_feasibility.data_source_ids")

        scoop = self.mapping(intake.get("scoop"), "SCOOP_VERDICT", "intake/intake.json.scoop")
        verdict = self.require_enum(
            scoop,
            "verdict",
            {"IDENTICAL", "ADJACENT", "UNCERTAIN"},
            "SCOOP_VERDICT",
            "intake/intake.json.scoop",
        )
        if verdict != "ADJACENT":
            reason = "UNCERTAIN cannot support a pilot" if verdict == "UNCERTAIN" else "IDENTICAL must return to intake or stop"
            self.error("SCOOP_VERDICT", "intake/intake.json.scoop.verdict", reason)
        if scoop.get("contribution_lane") != project.get("contribution_lane"):
            self.error("SCOOP_LANE", "intake/intake.json.scoop.contribution_lane", "scoop judgment must use the project's contribution lane")
        for field in ("searched_on", "delta_from_closest_work", "matched_protocol_assessment"):
            self.require_text(scoop, field, "SCOOP_VERDICT", "intake/intake.json.scoop")
        self.require_verified_sources(scoop.get("closest_work_source_ids"), "SCOOP_VERDICT", "intake/intake.json.scoop.closest_work_source_ids")

        venue = self.mapping(intake.get("venue_fit"), "VENUE_FIT", "intake/intake.json.venue_fit")
        if venue.get("status") != "PASS":
            self.error("VENUE_FIT", "intake/intake.json.venue_fit.status", "pilot requires venue fit PASS")
        if venue.get("route") != project.get("route") or project.get("route") in {"undecided", "stop"}:
            self.error("VENUE_FIT", "intake/intake.json.venue_fit.route", "venue route must match a nonterminal project route")
        for field in ("target_venue", "article_type", "rules_checked_on", "rationale"):
            self.require_text(venue, field, "VENUE_FIT", "intake/intake.json.venue_fit")
        self.require_verified_sources(venue.get("official_rule_source_ids"), "VENUE_FIT", "intake/intake.json.venue_fit.official_rule_source_ids")

        hypothesis = self.mapping(intake.get("hypothesis"), "HYPOTHESIS", "intake/intake.json.hypothesis")
        for field in ("hypothesis_id", "claim", "endpoint", "uncertainty_method", "validation_path", "kill_criterion"):
            self.require_text(hypothesis, field, "HYPOTHESIS", "intake/intake.json.hypothesis")
        self.require_enum(hypothesis, "direction", {"higher", "lower"}, "HYPOTHESIS", "intake/intake.json.hypothesis")
        if not is_number(hypothesis.get("minimum_effect")) or hypothesis.get("minimum_effect", 0) <= 0:
            self.error("HYPOTHESIS", "intake/intake.json.hypothesis.minimum_effect", "must be a positive finite effect floor")

        decision = self.mapping(intake.get("decision"), "INTAKE_DECISION", "intake/intake.json.decision")
        if decision.get("status") != "PASS" or decision.get("action") != "ADVANCE":
            self.error("INTAKE_DECISION", "intake/intake.json.decision", "pilot requires a PASS/ADVANCE intake decision")
        if decision.get("kill_layer") != "NONE":
            self.error("INTAKE_DECISION", "intake/intake.json.decision.kill_layer", "an advancing candidate cannot retain a kill layer")
        self.require_text(decision, "rationale", "INTAKE_DECISION", "intake/intake.json.decision")

    def validate_protocol(self) -> None:
        project = self.documents.get("project", {})
        intake = self.documents.get("intake", {})
        protocol = self.documents.get("protocol", {})
        hypothesis = intake.get("hypothesis", {}) if isinstance(intake.get("hypothesis"), dict) else {}
        data = intake.get("data_feasibility", {}) if isinstance(intake.get("data_feasibility"), dict) else {}

        if protocol.get("status") != "FROZEN":
            self.error("PROTOCOL_FREEZE", "protocol/protocol.json.status", "development requires a FROZEN protocol")
        self.require_text(protocol, "frozen_on", "PROTOCOL_FREEZE", "protocol/protocol.json")
        if protocol.get("hypothesis_id") != hypothesis.get("hypothesis_id"):
            self.error("PROTOCOL_HYPOTHESIS", "protocol/protocol.json.hypothesis_id", "must match the intake hypothesis")
        if protocol.get("contribution_lane") != project.get("contribution_lane"):
            self.error("CONTRIBUTION_LANE", "protocol/protocol.json.contribution_lane", "protocol cannot silently change contribution lane")
        if not nonempty_text_list(protocol.get("dataset_versions")):
            self.error("PROTOCOL_DATA", "protocol/protocol.json.dataset_versions", "freeze at least one dataset version")
        self.require_text(protocol, "preprocessing", "PROTOCOL_DATA", "protocol/protocol.json")

        split = self.mapping(protocol.get("split"), "SPLIT_CONTRACT", "protocol/protocol.json.split")
        for field in ("description", "independent_unit", "leakage_guard"):
            self.require_text(split, field, "SPLIT_CONTRACT", "protocol/protocol.json.split")
        if split.get("independent_unit") != data.get("independent_unit"):
            self.error("SPLIT_CONTRACT", "protocol/protocol.json.split.independent_unit", "must match the intake independent unit")
        if split.get("guard_test_status") != "PASS":
            self.error("SPLIT_CONTRACT", "protocol/protocol.json.split.guard_test_status", "a known-bad leakage case must be detected before development")

        metric = self.mapping(protocol.get("primary_metric"), "PRIMARY_METRIC", "protocol/protocol.json.primary_metric")
        for field in ("name", "implementation"):
            self.require_text(metric, field, "PRIMARY_METRIC", "protocol/protocol.json.primary_metric")
        self.require_enum(metric, "direction", {"higher", "lower"}, "PRIMARY_METRIC", "protocol/protocol.json.primary_metric")
        if metric.get("direction") != hypothesis.get("direction"):
            self.error("PRIMARY_METRIC", "protocol/protocol.json.primary_metric.direction", "must match the intake effect direction")

        baselines = self.sequence(protocol.get("baselines"), "BASELINE_PARITY", "protocol/protocol.json.baselines")
        baseline_ids = set()
        classes = set()
        for index, raw_baseline in enumerate(baselines):
            path = f"protocol/protocol.json.baselines[{index}]"
            baseline = self.mapping(raw_baseline, "BASELINE_PARITY", path)
            baseline_id = self.require_text(baseline, "baseline_id", "BASELINE_PARITY", path)
            if baseline_id in baseline_ids:
                self.error("BASELINE_PARITY", f"{path}.baseline_id", "baseline_id must be unique")
            baseline_ids.add(baseline_id)
            baseline_class = self.require_enum(
                baseline,
                "class",
                {"cheap", "domain-standard", "recent-strong", "compute-matched"},
                "BASELINE_PARITY",
                path,
            )
            classes.add(baseline_class)
            for field in ("name", "version_or_source", "tuning_budget"):
                self.require_text(baseline, field, "BASELINE_PARITY", path)
        if "cheap" not in classes or not ({"recent-strong", "domain-standard"} & classes):
            self.error("BASELINE_PARITY", "protocol/protocol.json.baselines", "include a cheap and a strong field comparator")

        uncertainty = self.mapping(protocol.get("uncertainty"), "UNCERTAINTY", "protocol/protocol.json.uncertainty")
        for field in ("unit", "method"):
            self.require_text(uncertainty, field, "UNCERTAINTY", "protocol/protocol.json.uncertainty")
        if uncertainty.get("unit") != data.get("independent_unit"):
            self.error("UNCERTAINTY", "protocol/protocol.json.uncertainty.unit", "uncertainty must use the independent unit")

        selection = self.mapping(protocol.get("selection"), "SELECTION_CONTRACT", "protocol/protocol.json.selection")
        for field in ("development_metric", "seed_policy", "checkpoint_rule", "baseline_tuning_parity"):
            self.require_text(selection, field, "SELECTION_CONTRACT", "protocol/protocol.json.selection")

        budgets = self.mapping(protocol.get("budgets"), "BUDGET", "protocol/protocol.json.budgets")
        for field in ("development_cycles", "locked_test_accesses"):
            value = budgets.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                self.error("BUDGET", f"protocol/protocol.json.budgets.{field}", "must be a positive integer")

        locked = self.mapping(protocol.get("locked_test"), "LOCKED_TEST", "protocol/protocol.json.locked_test")
        if locked.get("status") != "SEALED" or locked.get("accesses_used") != 0:
            self.error("LOCKED_TEST", "protocol/protocol.json.locked_test", "development requires a sealed test with zero accesses")
        self.require_text(locked, "custodian", "LOCKED_TEST", "protocol/protocol.json.locked_test")
        if not nonempty_text_list(protocol.get("allowed_changes")):
            self.error("PROTOCOL_CHANGE", "protocol/protocol.json.allowed_changes", "freeze the allowed development changes")
        stop_rules = self.mapping(protocol.get("stop_rules"), "STOP_RULES", "protocol/protocol.json.stop_rules")
        for field in ("advance", "revise", "pivot", "stop"):
            self.require_text(stop_rules, field, "STOP_RULES", "protocol/protocol.json.stop_rules")

    def validate_headroom(self) -> None:
        intake = self.documents.get("intake", {})
        protocol = self.documents.get("protocol", {})
        headroom = self.documents.get("headroom", {})
        data = intake.get("data_feasibility", {}) if isinstance(intake.get("data_feasibility"), dict) else {}
        metric = protocol.get("primary_metric", {}) if isinstance(protocol.get("primary_metric"), dict) else {}
        baselines = protocol.get("baselines", []) if isinstance(protocol.get("baselines"), list) else []
        baseline_ids = {item.get("baseline_id") for item in baselines if isinstance(item, dict)}

        if headroom.get("status") != "MEASURED" or headroom.get("conclusion") != "OPEN":
            self.error("HEADROOM", "development/headroom.json", "development requires measured OPEN headroom")
        for field in ("task", "strongest_representation", "strongest_baseline_id", "paired_independent_unit"):
            self.require_text(headroom, field, "HEADROOM", "development/headroom.json")
        if headroom.get("strongest_baseline_id") not in baseline_ids:
            self.error("HEADROOM", "development/headroom.json.strongest_baseline_id", "must reference a frozen baseline")
        if headroom.get("metric_direction") != metric.get("direction"):
            self.error("HEADROOM", "development/headroom.json.metric_direction", "must match the frozen primary metric")
        if headroom.get("paired_independent_unit") != data.get("independent_unit"):
            self.error("HEADROOM", "development/headroom.json.paired_independent_unit", "must use the intake independent unit")

        numeric_fields = (
            "baseline_value",
            "oracle_or_upper_bound",
            "noise_floor",
            "minimum_claimed_margin",
            "measured_headroom",
        )
        values = {}
        for field in numeric_fields:
            value = headroom.get(field)
            values[field] = value
            if not is_number(value):
                self.error("HEADROOM", f"development/headroom.json.{field}", "must be a finite number")
        if all(is_number(values[field]) for field in numeric_fields):
            expected = (
                values["oracle_or_upper_bound"] - values["baseline_value"]
                if headroom.get("metric_direction") == "higher"
                else values["baseline_value"] - values["oracle_or_upper_bound"]
            )
            if not math.isclose(expected, values["measured_headroom"], rel_tol=1e-9, abs_tol=1e-9):
                self.error("HEADROOM", "development/headroom.json.measured_headroom", "does not match the baseline-to-bound gap")
            if values["noise_floor"] < 0 or values["minimum_claimed_margin"] <= 0:
                self.error("HEADROOM", "development/headroom.json", "noise floor must be nonnegative and claimed margin positive")
            if values["measured_headroom"] <= max(values["noise_floor"], values["minimum_claimed_margin"]):
                self.error("HEADROOM", "development/headroom.json.conclusion", "OPEN requires headroom above both noise and the claimed margin")
        self.require_verified_sources(headroom.get("evidence_source_ids"), "HEADROOM", "development/headroom.json.evidence_source_ids")
        if not nonempty_text_list(headroom.get("result_locators")):
            self.error("HEADROOM", "development/headroom.json.result_locators", "record the measured comparison output")

    def validate_iterations(self) -> None:
        project = self.documents.get("project", {})
        protocol = self.documents.get("protocol", {})
        headroom = self.documents.get("headroom", {})
        ledger = self.documents.get("iterations", {})

        if ledger.get("construction_order") != CONSTRUCTION_ORDER:
            self.error("CONSTRUCTION_ORDER", "development/iteration-ledger.json.construction_order", "construction order must remain fixed")
        rungs = self.sequence(ledger.get("rungs"), "CONSTRUCTION_ORDER", "development/iteration-ledger.json.rungs")
        if [item.get("name") for item in rungs if isinstance(item, dict)] != CONSTRUCTION_ORDER:
            self.error("CONSTRUCTION_ORDER", "development/iteration-ledger.json.rungs", "rungs must appear exactly once in fixed order")
        rung_status = {}
        for index, raw_rung in enumerate(rungs):
            path = f"development/iteration-ledger.json.rungs[{index}]"
            rung = self.mapping(raw_rung, "CONSTRUCTION_ORDER", path)
            status = self.require_enum(
                rung,
                "status",
                {"UNTRIED", "TRIED", "RULED_OUT", "NOT_APPLICABLE"},
                "CONSTRUCTION_ORDER",
                path,
            )
            rung_status[rung.get("name")] = status
            if status in {"TRIED", "RULED_OUT", "NOT_APPLICABLE"}:
                self.require_text(rung, "evidence", "CONSTRUCTION_ORDER", path)

        candidates = self.sequence(ledger.get("registered_candidates"), "CANDIDATE_REGISTER", "development/iteration-ledger.json.registered_candidates")
        minimum_candidates = 2 if project.get("contribution_lane") == "sota-method" else 1
        if len(candidates) < minimum_candidates:
            self.error("CANDIDATE_REGISTER", "development/iteration-ledger.json.registered_candidates", f"this lane requires at least {minimum_candidates} causal candidate(s)")
        candidate_map = {}
        for index, raw_candidate in enumerate(candidates):
            path = f"development/iteration-ledger.json.registered_candidates[{index}]"
            candidate = self.mapping(raw_candidate, "CANDIDATE_REGISTER", path)
            candidate_id = self.require_text(candidate, "candidate_id", "CANDIDATE_REGISTER", path)
            if candidate_id in candidate_map:
                self.error("CANDIDATE_REGISTER", f"{path}.candidate_id", "candidate_id must be unique")
            candidate_map[candidate_id] = candidate
            for field in ("mechanism", "failure_node", "predicted_slice", "matched_control", "falsifier"):
                self.require_text(candidate, field, "CANDIDATE_REGISTER", path)
            rung = self.require_enum(candidate, "rung", set(CONSTRUCTION_ORDER), "CANDIDATE_REGISTER", path)
            if rung in CONSTRUCTION_ORDER:
                for prior in CONSTRUCTION_ORDER[: CONSTRUCTION_ORDER.index(rung)]:
                    if rung_status.get(prior) == "UNTRIED":
                        self.error(
                            "CONSTRUCTION_ORDER",
                            f"{path}.rung",
                            f"cannot register {rung} while lower rung {prior} is UNTRIED",
                        )

        cycles = self.sequence(ledger.get("cycles"), "ITERATION_LEDGER", "development/iteration-ledger.json.cycles")
        budget = protocol.get("budgets", {}).get("development_cycles") if isinstance(protocol.get("budgets"), dict) else None
        if isinstance(budget, int) and len(cycles) > budget:
            self.error("BUDGET", "development/iteration-ledger.json.cycles", "cycle count exceeds the frozen budget")
        cycle_ids = set()
        misses = {}
        attempted_candidates = set()
        for index, raw_cycle in enumerate(cycles):
            path = f"development/iteration-ledger.json.cycles[{index}]"
            cycle = self.mapping(raw_cycle, "ITERATION_LEDGER", path)
            cycle_id = self.require_text(cycle, "cycle_id", "ITERATION_LEDGER", path)
            if cycle_id in cycle_ids:
                self.error("ITERATION_LEDGER", f"{path}.cycle_id", "cycle_id must be unique")
            cycle_ids.add(cycle_id)
            candidate_id = self.require_text(cycle, "candidate_id", "ITERATION_LEDGER", path)
            candidate = candidate_map.get(candidate_id)
            if candidate is None:
                self.error("ITERATION_LEDGER", f"{path}.candidate_id", "cycle must reference a registered candidate")
            else:
                attempted_candidates.add(candidate_id)
                if cycle.get("rung") != candidate.get("rung"):
                    self.error("ITERATION_LEDGER", f"{path}.rung", "cycle rung must match its registered candidate")
            status = self.require_enum(
                cycle,
                "status",
                {"PLANNED", "RUNNING", "COMPLETED", "FAILED", "INVALIDATED", "NOT_RUN"},
                "ITERATION_LEDGER",
                path,
            )
            self.require_enum(
                cycle,
                "mechanism_status",
                {"SUPPORTED", "FALSIFIED", "INCONCLUSIVE", "INTEGRITY_ANOMALY", "NOT_EVALUATED"},
                "ITERATION_LEDGER",
                path,
            )
            decision = self.require_enum(
                cycle,
                "decision",
                {"ADVANCE", "REVISE", "PIVOT", "STOP", "NEW_PROTOCOL", "NOT_DECIDED"},
                "ITERATION_LEDGER",
                path,
            )
            if cycle.get("locked_test_accessed") is not False:
                self.error("LOCKED_TEST", f"{path}.locked_test_accessed", "development cycles must not access the locked test")
            for evidence_key in ("observed", "failed", "not_run", "inferred"):
                value = cycle.get(evidence_key)
                if not isinstance(value, list):
                    self.error("EVIDENCE_STATUS", f"{path}.{evidence_key}", "must be a list")
            if status == "COMPLETED":
                observed = cycle.get("observed")
                if not isinstance(observed, list) or not observed:
                    self.error("EVIDENCE_STATUS", f"{path}.observed", "completed cycles require observed evidence")
                else:
                    for obs_index, observation in enumerate(observed):
                        obs_path = f"{path}.observed[{obs_index}]"
                        if not isinstance(observation, dict) or not nonempty_text(observation.get("statement")) or not nonempty_text(observation.get("locator")):
                            self.error("EVIDENCE_STATUS", obs_path, "observations require statement and locator")
                if not isinstance(cycle.get("predicted_slice_met"), bool):
                    self.error("PREDICTED_SLICE", f"{path}.predicted_slice_met", "completed cycles require a boolean slice result")
            if cycle.get("predicted_slice_met") is False and candidate_id:
                misses[candidate_id] = misses.get(candidate_id, 0) + 1
                if misses[candidate_id] >= 2 and decision == "REVISE":
                    self.error(
                        "MECHANISM_RECOVERY",
                        f"{path}.decision",
                        "two predicted-slice misses kill this mechanism; pivot to a registered alternative or stop for a valid route-level reason",
                    )
            if decision == "ADVANCE" and (
                cycle.get("mechanism_status") != "SUPPORTED"
                or cycle.get("predicted_slice_met") is not True
                or cycle.get("matched_control_status") != "PASS"
                or cycle.get("ablation_status") != "PASS"
            ):
                self.error("ADVANCE_EVIDENCE", f"{path}.decision", "advance requires supported mechanism, slice floor, matched control, and ablation")
            if decision == "STOP":
                reason = cycle.get("stop_reason")
                if reason not in {"CLOSED_HEADROOM", "EXHAUSTED_BUDGET", "LANE_IDENTICAL_SCOOP"}:
                    self.error("ROUTE_CLOSURE", f"{path}.stop_reason", "stop requires a permitted route-level reason")
                if reason == "CLOSED_HEADROOM" and headroom.get("conclusion") != "CLOSED":
                    self.error("ROUTE_CLOSURE", f"{path}.stop_reason", "closed-headroom stop conflicts with the headroom record")
                if reason == "EXHAUSTED_BUDGET" and isinstance(budget, int) and len(cycles) < budget:
                    self.error("ROUTE_CLOSURE", f"{path}.stop_reason", "budget is not exhausted")
                if reason == "LANE_IDENTICAL_SCOOP":
                    scoop = self.documents.get("intake", {}).get("scoop", {})
                    if not isinstance(scoop, dict) or scoop.get("verdict") != "IDENTICAL":
                        self.error("ROUTE_CLOSURE", f"{path}.stop_reason", "lane-identical stop requires an IDENTICAL scoop verdict")

        if cycles:
            final = cycles[-1]
            if isinstance(final, dict) and final.get("decision") == "STOP":
                remaining = isinstance(budget, int) and len(cycles) < budget
                alternatives = set(candidate_map) - attempted_candidates
                if headroom.get("conclusion") == "OPEN" and remaining and alternatives:
                    self.error("MECHANISM_RECOVERY", "development/iteration-ledger.json.cycles[-1].decision", "open headroom, remaining budget, and an untried registered candidate require a pivot")

    def validate_development(self) -> None:
        self.validate_protocol()
        self.validate_headroom()
        self.validate_iterations()

    def validate_claims(self) -> None:
        claim_doc = self.documents.get("claims", {})
        claims = self.sequence(claim_doc.get("claims"), "CLAIM_REGISTER", "claims/claim-register.json.claims")
        if not claims:
            self.error("CLAIM_REGISTER", "claims/claim-register.json.claims", "handoff requires at least one claim record")
        claim_ids = set()
        for index, raw_claim in enumerate(claims):
            path = f"claims/claim-register.json.claims[{index}]"
            claim = self.mapping(raw_claim, "CLAIM_REGISTER", path)
            claim_id = self.require_text(claim, "claim_id", "CLAIM_REGISTER", path)
            if claim_id in claim_ids:
                self.error("CLAIM_REGISTER", f"{path}.claim_id", "claim_id must be unique")
            claim_ids.add(claim_id)
            self.require_text(claim, "text", "CLAIM_REGISTER", path)
            self.require_enum(claim, "claim_type", {"RESULT", "METHOD", "PRIOR_WORK", "LIMITATION"}, "CLAIM_REGISTER", path)
            status = self.require_enum(
                claim,
                "status",
                {"PROSPECTIVE", "SUPPORTED", "NARROWED", "REFUTED", "UNVERIFIED"},
                "CLAIM_REGISTER",
                path,
            )
            disposition = self.require_enum(
                claim,
                "disposition",
                {"INCLUDE", "REPORT_NEGATIVE", "EXCLUDE"},
                "CLAIM_REGISTER",
                path,
            )
            for evidence_key in ("observed", "inferred", "not_run", "limitations"):
                if not isinstance(claim.get(evidence_key), list):
                    self.error("EVIDENCE_STATUS", f"{path}.{evidence_key}", "must be a list")
            if disposition == "INCLUDE":
                if status not in {"SUPPORTED", "NARROWED"}:
                    self.error("CLAIM_STATUS", f"{path}.status", "included claims must be supported or narrowed")
                self.require_text(claim, "scope", "CLAIM_EVIDENCE", path)
                self.require_verified_sources(claim.get("evidence_source_ids"), "CLAIM_EVIDENCE", f"{path}.evidence_source_ids")
                if claim.get("claim_type") == "RESULT":
                    if not nonempty_text_list(claim.get("result_locators")):
                        self.error("CLAIM_EVIDENCE", f"{path}.result_locators", "included result claims require result locators")
                    self.require_text(claim, "uncertainty", "CLAIM_EVIDENCE", path)
                    if not claim.get("observed"):
                        self.error("CLAIM_EVIDENCE", f"{path}.observed", "included result claims require observed evidence")
            if status == "REFUTED" and disposition == "INCLUDE":
                self.error("CLAIM_STATUS", f"{path}.disposition", "refuted claims cannot be included as positive claims")

    def validate_handoff(self) -> None:
        project = self.documents.get("project", {})
        protocol = self.documents.get("protocol", {})
        handoff = self.documents.get("handoff", {})
        outcome = self.require_enum(
            handoff,
            "terminal_outcome",
            {"MANUSCRIPT", "NEGATIVE_RESULT", "RETURN_TO_INTAKE", "STOPPED"},
            "HANDOFF",
            "handoff/handoff.json",
        )

        if outcome in {"MANUSCRIPT", "NEGATIVE_RESULT"}:
            self.validate_claims()

        if outcome == "MANUSCRIPT":
            evaluation = self.mapping(handoff.get("final_evaluation"), "FINAL_EVALUATION", "handoff/handoff.json.final_evaluation")
            if evaluation.get("status") != "PASS" or evaluation.get("protocol_match") != "PASS":
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation", "manuscript handoff requires a protocol-matched PASS")
            budget = protocol.get("budgets", {}).get("locked_test_accesses") if isinstance(protocol.get("budgets"), dict) else None
            accesses = evaluation.get("locked_test_accesses_used")
            if not isinstance(accesses, int) or isinstance(accesses, bool) or accesses <= 0 or (isinstance(budget, int) and accesses > budget):
                self.error("LOCKED_TEST", "handoff/handoff.json.final_evaluation.locked_test_accesses_used", "locked-test use must be positive and within the frozen budget")
            baseline_ids = {
                item.get("baseline_id")
                for item in protocol.get("baselines", [])
                if isinstance(item, dict)
            }
            if evaluation.get("strongest_comparator_id") not in baseline_ids:
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.strongest_comparator_id", "must reference a frozen comparator")
            if not is_number(evaluation.get("effect_estimate")):
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.effect_estimate", "must be a finite number")
            interval = evaluation.get("confidence_interval")
            if not isinstance(interval, list) or len(interval) != 2 or not all(is_number(value) for value in interval):
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.confidence_interval", "must contain two finite bounds")
            elif is_number(evaluation.get("effect_estimate")) and not interval[0] <= evaluation["effect_estimate"] <= interval[1]:
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.confidence_interval", "must contain the effect estimate")
            intake = self.documents.get("intake", {})
            data = intake.get("data_feasibility", {}) if isinstance(intake.get("data_feasibility"), dict) else {}
            if evaluation.get("independent_unit") != data.get("independent_unit"):
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.independent_unit", "must match the frozen independent unit")
            if not nonempty_text_list(evaluation.get("result_locators")):
                self.error("FINAL_EVALUATION", "handoff/handoff.json.final_evaluation.result_locators", "record final comparison outputs")

            external = self.mapping(handoff.get("external_validation"), "EXTERNAL_VALIDATION", "handoff/handoff.json.external_validation")
            allowed = {"PASS", "NOT_APPLICABLE"} if project.get("route") == "top-cs" else {"PASS"}
            if external.get("status") not in allowed:
                self.error("EXTERNAL_VALIDATION", "handoff/handoff.json.external_validation.status", "the selected route lacks its required independent validation")
            self.require_text(external, "type", "EXTERNAL_VALIDATION", "handoff/handoff.json.external_validation")
            if external.get("status") == "PASS" and not nonempty_text_list(external.get("result_locators")):
                self.error("EXTERNAL_VALIDATION", "handoff/handoff.json.external_validation.result_locators", "passing external validation requires result locators")

            specialists = self.mapping(handoff.get("specialist_handoffs"), "SPECIALIST_HANDOFF", "handoff/handoff.json.specialist_handoffs")
            expected = {"abstract", "statistics", "data_availability", "figures", "venue_manuscript"}
            if set(specialists) != expected:
                self.error("SPECIALIST_HANDOFF", "handoff/handoff.json.specialist_handoffs", "must name exactly the five downstream handoffs")
            for name in expected:
                if specialists.get(name) not in {"READY", "NOT_APPLICABLE"}:
                    self.error("SPECIALIST_HANDOFF", f"handoff/handoff.json.specialist_handoffs.{name}", "must be READY or NOT_APPLICABLE")

        elif outcome == "NEGATIVE_RESULT":
            claims = self.documents.get("claims", {}).get("claims", [])
            has_negative = any(
                isinstance(claim, dict)
                and claim.get("disposition") == "REPORT_NEGATIVE"
                and claim.get("status") in {"REFUTED", "NARROWED"}
                for claim in claims
            )
            if not has_negative:
                self.error("NEGATIVE_RESULT", "claims/claim-register.json.claims", "negative handoff must preserve at least one refuted or narrowed claim")
        elif outcome == "RETURN_TO_INTAKE":
            intake = self.documents.get("intake", {})
            scoop = intake.get("scoop", {}) if isinstance(intake.get("scoop"), dict) else {}
            decision = intake.get("decision", {}) if isinstance(intake.get("decision"), dict) else {}
            if scoop.get("verdict") != "IDENTICAL" and decision.get("action") not in {"REFRAME", "HOLD", "STOP"}:
                self.error("RETURN_TO_INTAKE", "handoff/handoff.json.terminal_outcome", "return requires a named intake-level reason")
        elif outcome == "STOPPED":
            headroom = self.documents.get("headroom", {})
            cycles = self.documents.get("iterations", {}).get("cycles", [])
            budget = protocol.get("budgets", {}).get("development_cycles") if isinstance(protocol.get("budgets"), dict) else None
            exhausted = isinstance(cycles, list) and isinstance(budget, int) and len(cycles) >= budget
            if headroom.get("conclusion") != "CLOSED" and not exhausted:
                self.error("ROUTE_CLOSURE", "handoff/handoff.json.terminal_outcome", "stopped outcome requires measured closed headroom or exhausted budget")

        if handoff.get("external_action_status") != "NOT_AUTHORIZED":
            self.error("EXTERNAL_BOUNDARY", "handoff/handoff.json.external_action_status", "local handoff cannot authorize an external action")
        if not isinstance(handoff.get("limitations"), list) or not isinstance(handoff.get("not_run"), list):
            self.error("HANDOFF", "handoff/handoff.json", "limitations and not_run must be explicit lists")

        release = self.mapping(handoff.get("public_release"), "PUBLIC_RELEASE_PATH", "handoff/handoff.json.public_release")
        release_path = release.get("path")
        if not nonempty_text(release_path):
            self.error("PUBLIC_RELEASE_PATH", "handoff/handoff.json.public_release.path", "must name a relative public-release path")
        else:
            relative = Path(release_path)
            if relative.is_absolute() or ".." in relative.parts or not relative.parts or relative.parts[0] != "public-release":
                self.error("PUBLIC_RELEASE_PATH", "handoff/handoff.json.public_release.path", "must stay inside the project's public-release directory")

    def validate_public_release(self) -> None:
        handoff = self.documents.get("handoff", {})
        release = handoff.get("public_release", {}) if isinstance(handoff.get("public_release"), dict) else {}
        if release.get("status") != "AUDITED":
            self.error("PUBLIC_RELEASE_STATUS", "handoff/handoff.json.public_release.status", "public release target requires status AUDITED")
        relative = release.get("path")
        if not nonempty_text(relative):
            return
        release_root = self.root / relative
        if not inside(self.root / "public-release", release_root) or not release_root.is_dir():
            self.error("PUBLIC_RELEASE_PATH", "handoff/handoff.json.public_release.path", "release directory is missing or escapes public-release")
            return
        files = [path for path in release_root.rglob("*") if path.is_file()]
        if not files:
            self.error("PUBLIC_RELEASE_CONTENT", relative, "curated release directory contains no files")
            return
        actual_files = {path.relative_to(release_root).as_posix() for path in files}
        allowlist = release.get("allowlist")
        allowed_files = set()
        if not nonempty_text_list(allowlist):
            self.error(
                "PUBLIC_RELEASE_ALLOWLIST",
                "handoff/handoff.json.public_release.allowlist",
                "must list every curated file exactly once",
            )
        else:
            if len(allowlist) != len(set(allowlist)):
                self.error(
                    "PUBLIC_RELEASE_ALLOWLIST",
                    "handoff/handoff.json.public_release.allowlist",
                    "must not contain duplicate paths",
                )
            for index, item in enumerate(allowlist):
                candidate = Path(item)
                path = f"handoff/handoff.json.public_release.allowlist[{index}]"
                if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
                    self.error("PUBLIC_RELEASE_ALLOWLIST", path, "must be a relative in-release path")
                    continue
                normalized = candidate.as_posix()
                allowed_files.add(normalized)
                target = release_root / candidate
                if not inside(release_root, target) or not target.is_file():
                    self.error(
                        "PUBLIC_RELEASE_ALLOWLIST",
                        path,
                        "allowlisted file is missing or escapes the release tree",
                    )
            if allowed_files != actual_files:
                missing = sorted(allowed_files - actual_files)
                extra = sorted(actual_files - allowed_files)
                self.error(
                    "PUBLIC_RELEASE_ALLOWLIST",
                    "handoff/handoff.json.public_release.allowlist",
                    f"must exactly match curated files; missing={missing} extra={extra}",
                )

        required_artifacts = {
            "source",
            "dependency_spec",
            "example",
            "data_instructions",
            "run_instructions",
            "expected_outputs",
            "tests",
            "license",
            "citation",
            "limitations",
        }
        optional_artifacts = {"configuration"}
        artifact_paths = self.mapping(
            release.get("artifact_paths"),
            "PUBLIC_RELEASE_ARTIFACT",
            "handoff/handoff.json.public_release.artifact_paths",
        )
        artifact_categories = set(artifact_paths)
        missing_categories = required_artifacts - artifact_categories
        unknown_categories = artifact_categories - required_artifacts - optional_artifacts
        if missing_categories or unknown_categories:
            self.error(
                "PUBLIC_RELEASE_ARTIFACT",
                "handoff/handoff.json.public_release.artifact_paths",
                f"must name every required and only supported optional public artifact category; "
                f"missing={sorted(missing_categories)} unknown={sorted(unknown_categories)}",
            )
        declared_artifact_files = set()
        role_files = {}
        for category in sorted(artifact_categories & (required_artifacts | optional_artifacts)):
            values = artifact_paths.get(category)
            path = f"handoff/handoff.json.public_release.artifact_paths.{category}"
            if not nonempty_text_list(values):
                self.error(
                    "PUBLIC_RELEASE_ARTIFACT",
                    path,
                    "must contain at least one relative file path",
                )
                continue
            role_files[category] = set()
            for item in values:
                candidate = Path(item)
                target = release_root / candidate
                normalized = candidate.as_posix()
                declared_artifact_files.add(normalized)
                role_files[category].add(normalized)
                if (
                    candidate.is_absolute()
                    or ".." in candidate.parts
                    or not inside(release_root, target)
                    or not target.is_file()
                ):
                    self.error(
                        "PUBLIC_RELEASE_ARTIFACT",
                        path,
                        f"artifact path is missing or escapes the release tree: {item}",
                    )
                if normalized not in allowed_files:
                    self.error(
                        "PUBLIC_RELEASE_ARTIFACT",
                        path,
                        f"artifact path is not allowlisted: {item}",
                    )
                if not matches_public_artifact_role(category, normalized):
                    self.error(
                        "PUBLIC_RELEASE_ARTIFACT",
                        path,
                        f"artifact path does not match the declared {category} role: {item}",
                    )

        if declared_artifact_files != actual_files:
            uncategorized = sorted(actual_files - declared_artifact_files)
            nonexistent = sorted(declared_artifact_files - actual_files)
            self.error(
                "PUBLIC_RELEASE_ARTIFACT",
                "handoff/handoff.json.public_release.artifact_paths",
                f"must classify every curated file exactly within the public artifact contract; "
                f"uncategorized={uncategorized} missing={nonexistent}",
            )

        distinct_roles = (
            "source", "dependency_spec", "example", "configuration", "tests", "license",
            "citation", "limitations",
        )
        for index, first in enumerate(distinct_roles):
            for second in distinct_roles[index + 1 :]:
                overlap = sorted(role_files.get(first, set()) & role_files.get(second, set()))
                if overlap:
                    self.error(
                        "PUBLIC_RELEASE_ARTIFACT",
                        "handoff/handoff.json.public_release.artifact_paths",
                        f"{first} and {second} require distinct public artifacts; overlap={overlap}",
                    )

        rehearsal = self.mapping(
            release.get("rehearsal"),
            "PUBLIC_RELEASE_REHEARSAL",
            "handoff/handoff.json.public_release.rehearsal",
        )
        if rehearsal.get("status") != "PASS":
            self.error(
                "PUBLIC_RELEASE_REHEARSAL",
                "handoff/handoff.json.public_release.rehearsal.status",
                "fresh-unpack rehearsal must have status PASS",
            )
        checked_on = rehearsal.get("checked_on")
        try:
            date.fromisoformat(checked_on)
        except (TypeError, ValueError):
            self.error(
                "PUBLIC_RELEASE_REHEARSAL",
                "handoff/handoff.json.public_release.rehearsal.checked_on",
                "must be an ISO date",
            )
        self.require_text(
            rehearsal,
            "environment",
            "PUBLIC_RELEASE_REHEARSAL",
            "handoff/handoff.json.public_release.rehearsal",
        )
        commands = self.sequence(
            rehearsal.get("commands"),
            "PUBLIC_RELEASE_REHEARSAL",
            "handoff/handoff.json.public_release.rehearsal.commands",
        )
        if not commands:
            self.error(
                "PUBLIC_RELEASE_REHEARSAL",
                "handoff/handoff.json.public_release.rehearsal.commands",
                "must record at least one observed command",
            )
        for index, command in enumerate(commands):
            path = f"handoff/handoff.json.public_release.rehearsal.commands[{index}]"
            if not isinstance(command, dict):
                self.error("PUBLIC_RELEASE_REHEARSAL", path, "must be an object")
                continue
            self.require_text(command, "command", "PUBLIC_RELEASE_REHEARSAL", path)
            if command.get("exit_code") != 0 or isinstance(command.get("exit_code"), bool):
                self.error(
                    "PUBLIC_RELEASE_REHEARSAL",
                    f"{path}.exit_code",
                    "must record observed exit code 0",
                )
            if not nonempty_text_list(command.get("observed_outputs")):
                self.error(
                    "PUBLIC_RELEASE_REHEARSAL",
                    f"{path}.observed_outputs",
                    "must record observed outputs",
                )
        if not isinstance(rehearsal.get("not_run"), list):
            self.error(
                "PUBLIC_RELEASE_REHEARSAL",
                "handoff/handoff.json.public_release.rehearsal.not_run",
                "must be an explicit list",
            )
        forbidden_names = {
            "pipeline-state.json",
            "execution-receipt.json",
            "approval-receipt.json",
            "delegated-decision-receipt.json",
            "project.json",
            "source-register.json",
            "intake.json",
            "headroom.json",
            "iteration-ledger.json",
            "claim-register.json",
            "handoff.json",
            ".env",
            "auth.json",
            "agents.md",
            "claude.md",
        }
        forbidden_parts = {"research-control", ".agents", ".codex", ".git", "prompts"}
        sensitive_markers = ("BEGIN PRIVATE KEY", "api_key=", "secret_key=")
        required_text_suffixes = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".toml", ".csv"}
        for path in files:
            display = str(path.relative_to(self.root))
            relative_parts = {
                part.casefold() for part in path.relative_to(release_root).parts
            }
            if path.name.lower() in forbidden_names or relative_parts & forbidden_parts:
                self.error("PUBLIC_RELEASE_CONTENT", display, "internal control or credential artifact is not public-release material")
            if INTEGRITY_SIDECAR.search(path.name):
                self.error("PUBLIC_RELEASE_CONTENT", display, "author-created integrity side record is not public-release material")
            try:
                text = read_public_text(path)
            except OSError:
                self.error("PUBLIC_RELEASE_CONTENT", display, "text artifact could not be inspected")
                continue
            if text is None:
                if path.suffix.lower() in required_text_suffixes:
                    self.error("PUBLIC_RELEASE_CONTENT", display, "text artifact could not be inspected")
                continue
            if any(marker.lower() in text.lower() for marker in sensitive_markers):
                self.error("PUBLIC_RELEASE_CONTENT", display, "possible credential material found")
            if PRIVATE_MACHINE_PATH.search(text):
                self.error("PUBLIC_RELEASE_CONTENT", display, "possible private machine path found")
            # Record-like text in documentation/config is distinct from ordinary code identifiers.
            if path.suffix.casefold() not in PUBLIC_SOURCE_SUFFIXES and INLINE_CONTROL_RECORD.search(text):
                self.error("PUBLIC_RELEASE_CONTENT", display, "possible internal workflow record found")
            if INTEGRITY_COMMAND.search(text):
                self.error("PUBLIC_RELEASE_CONTENT", display, "author-created integrity verification instruction found")

    def run(self):
        self.validate_common()
        if self.target == "working":
            self.validate_working()
        else:
            outcome = self.documents.get("handoff", {}).get("terminal_outcome")
            needs_development = self.target == "development" or (
                self.target in {"handoff", "public-release"}
                and outcome in {"MANUSCRIPT", "NEGATIVE_RESULT"}
            )
            needs_pilot = self.target == "pilot" or needs_development
            if needs_pilot:
                self.validate_pilot()
            if needs_development:
                self.validate_development()
            if self.target in {"handoff", "public-release"}:
                self.validate_handoff()
            if self.target == "public-release":
                self.validate_public_release()
        errors = [item for item in self.findings if item["level"] == "error"]
        warnings = [item for item in self.findings if item["level"] == "warning"]
        status = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
        return {
            "status": status,
            "validation_scope": VALIDATION_SCOPE,
            "target": self.target,
            "project": str(self.root),
            "errors": [item["message"] for item in errors],
            "warnings": [item["message"] for item in warnings],
            "findings": self.findings,
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="publication project directory")
    parser.add_argument(
        "--target",
        choices=("working", "pilot", "development", "handoff", "public-release"),
        default="working",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    report = ProjectValidator(Path(args.project), args.target).run()
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for finding in report["findings"]:
            print(f"{finding['level'].upper()} {finding['rule_id']} {finding['path']}: {finding['message']}")
        print(f"status={report['status']} target={report['target']} validation_scope={VALIDATION_SCOPE}")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
