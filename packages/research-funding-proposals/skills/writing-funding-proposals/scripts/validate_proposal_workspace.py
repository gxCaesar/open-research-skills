#!/usr/bin/env python3
"""Validate the public research-funding proposal workspace contract."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import re
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Set


STATUSES = {
    "VERIFIED",
    "UNVERIFIED",
    "NOT_FOUND",
    "COULD_NOT_OPEN",
    "INFERRED",
    "NOT_RUN",
    "FAILED",
    "DECISION_REQUIRED",
}
CONFIDENTIALITY = {"PUBLIC", "APPLICANT_PRIVATE", "RESTRICTED_CONFIDENTIAL"}
CONTRIBUTION_LANES = {"sota-method", "discovery", "benchmark", "UNVERIFIED"}
SCOOP_VERDICTS = {"IDENTICAL", "ADJACENT", "UNCERTAIN"}
DISPOSITIONS = {"FRAMING", "DATA", "TASK", "UNVERIFIED"}
DISPOSITION_ACTIONS = {"RECOMMEND", "HOLD", "EXCLUDE", "UNVERIFIED"}
REVIEW_PASSES = {"R1_FATAL", "R2_SCIENCE", "R3_READABILITY"}
REVIEW_SEVERITIES = {"fatal", "major", "minor", "note"}
REVIEW_RESOLUTIONS = {"OPEN", "RESOLVED", "NOT_APPLICABLE"}
AUTHORING_POLICY_STATUSES = {"VERIFIED", "VERIFIED_PROFILE", "UNVERIFIED"}
BUDGET_REQUIREMENT_STATUSES = {"VERIFIED", "UNVERIFIED"}
COMMITMENT_ARTIFACT_TYPES = {"research_content", "annual_task", "output"}
COMMITMENT_CLASSES = {
    "deliverable mainline",
    "cautious exploration",
    "boundary confirmation",
}
AUTHORITY_KINDS = {"funder", "institution"}
PROGRAMS = {"nsfc", "guangdong", "other"}
MIN_TARGET_YEAR = 2000
MAX_TARGET_YEAR = 2100
OFFICIAL_AUTHORITY_SCOPE = "official_authority"
OFFICIAL_AUTHORITY_SOURCE_TYPES = {"official authority"}
OFFICIAL_TEMPLATE_SCOPE = "official_template"
OFFICIAL_TEMPLATE_SOURCE_TYPES = {"official template"}
FINANCIAL_BUDGET_REQUIREMENT_SCOPE = "financial_budget_requirement"
FINANCIAL_BUDGET_REQUIREMENT_SOURCE_TYPES = {"financial budget requirement"}
MIN_SECTION_VISIBLE_CHARACTERS = 20
VALIDATION_SCOPE = "record_completeness"
VALIDATION_SCOPE_NOTE = (
    "validation_scope=record_completeness: file format, rendering, and visual quality "
    "are not checked"
)

REQUIRED_FILES = [
    "project.json",
    "authority/source-register.csv",
    "evidence/claim-ledger.csv",
    "topic/candidate-portfolio.json",
    "argument/argument-map.json",
    "sections/rationale.md",
    "sections/contents.md",
    "sections/foundation.md",
    "figures/figure-plan.csv",
    "reviews/review-findings.csv",
    "delivery/final-format.json",
    "budget/financial-budget.json",
    "commitments/commitment-records.json",
]

SOURCE_FIELDS = [
    "source_id",
    "issuer",
    "year",
    "program",
    "source_type",
    "url_or_path",
    "accessed_on",
    "clause_locator",
    "status",
    "scope",
    "data_classification",
    "search_query",
]
CLAIM_FIELDS = [
    "claim_id",
    "section",
    "claim_text",
    "claim_type",
    "source_id",
    "source_scope",
    "verification_status",
    "applicant_role",
    "last_verified",
    "notes",
]
FIGURE_FIELDS = [
    "figure_id",
    "class",
    "rhetorical_job",
    "body_anchor",
    "claim_ids",
    "source_ids",
    "editable_master",
    "rendered_output",
    "qa_status",
]
REVIEW_FIELDS = [
    "issue_id",
    "pass_id",
    "severity",
    "exact_location",
    "strongest_falsifier",
    "required_evidence",
    "cheapest_revision",
    "resolution_status",
    "resolution_evidence",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--mode", choices=["working", "final"], default="working")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--as-of", dest="as_of", default=date.today().isoformat())
    args = parser.parse_args()
    if not is_iso_date(args.as_of):
        parser.error("--as-of must be a valid ISO date")
    return args


def load_json(path: Path, errors: List[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.name}: invalid JSON: {error}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name}: top level must be an object")
        return {}
    return value


def load_csv(path: Path, expected: Sequence[str], errors: List[str]) -> List[dict]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != list(expected):
                errors.append(
                    f"{path.name}: header must be {','.join(expected)}"
                )
                return []
            return [dict(row) for row in reader]
    except OSError as error:
        errors.append(f"{path.name}: could not read CSV: {error}")
        return []


def require_fields(
    record: dict,
    fields: Iterable[str],
    label: str,
    errors: List[str],
) -> None:
    for field in fields:
        value = record.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"{label}: missing {field}")


def split_ids(value: str) -> List[str]:
    return [item.strip() for item in re.split(r"[,;]", value or "") if item.strip()]


def is_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def nonnegative_amount(value: object, label: str, errors: List[str]) -> Optional[Decimal]:
    if isinstance(value, bool):
        errors.append(f"{label}: amount must be a non-negative number")
        return None
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        errors.append(f"{label}: amount must be a non-negative number")
        return None
    if not amount.is_finite() or amount < 0:
        errors.append(f"{label}: amount must be a non-negative number")
        return None
    return amount


def is_workspace_regular_file(root: Path, relative_path: object) -> bool:
    if not isinstance(relative_path, str) or not relative_path.strip():
        return False
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        return False
    target = root / relative
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return False
    return target.is_file()


def check_unique(rows: Sequence[dict], key: str, label: str, errors: List[str]) -> Set[str]:
    observed: Set[str] = set()
    for index, row in enumerate(rows, start=1):
        value = (row.get(key) or "").strip()
        if not value:
            errors.append(f"{label} row {index}: missing {key}")
        elif value in observed:
            errors.append(f"{label}: duplicate {key} {value}")
        observed.add(value)
    return observed


def validate_sources(rows: Sequence[dict], errors: List[str], warnings: List[str]) -> Dict[str, dict]:
    if not rows:
        warnings.append("source register has no opened source")
        return {}
    check_unique(rows, "source_id", "source register", errors)
    sources: Dict[str, dict] = {}
    for index, row in enumerate(rows, start=1):
        label = f"source row {index}"
        source_id = (row.get("source_id") or "").strip()
        status = (row.get("status") or "").strip()
        if status not in STATUSES:
            errors.append(f"{label}: invalid status {status!r}")
        classification = (row.get("data_classification") or "").strip()
        if classification not in CONFIDENTIALITY:
            errors.append(f"{label}: invalid data_classification {classification!r}")
        require_fields(
            row,
            ["source_id", "issuer", "year", "program", "source_type", "status", "scope", "data_classification"],
            label,
            errors,
        )
        if status == "VERIFIED":
            require_fields(
                row,
                ["url_or_path", "accessed_on", "clause_locator"],
                label,
                errors,
            )
        if status == "NOT_FOUND" and not (row.get("search_query") or "").strip():
            errors.append(f"{label}: NOT_FOUND requires search_query")
        if source_id:
            sources[source_id] = row
    return sources


def validate_claims(
    rows: Sequence[dict],
    sources: Dict[str, dict],
    errors: List[str],
    warnings: List[str],
) -> Set[str]:
    if not rows:
        warnings.append("claim ledger has no load-bearing claim")
        return set()
    claim_ids = check_unique(rows, "claim_id", "claim ledger", errors)
    for index, row in enumerate(rows, start=1):
        label = f"claim row {index}"
        claim_id = (row.get("claim_id") or "").strip()
        if claim_id and not re.fullmatch(r"CL[1-9][0-9]*", claim_id):
            errors.append(f"{label}: claim_id must match CL1, CL2, ...")
        require_fields(
            row,
            [
                "claim_id",
                "section",
                "claim_text",
                "claim_type",
                "source_id",
                "source_scope",
                "verification_status",
                "applicant_role",
                "last_verified",
            ],
            label,
            errors,
        )
        status = (row.get("verification_status") or "").strip()
        if status not in STATUSES:
            errors.append(f"{label}: invalid verification_status {status!r}")
        source_id = (row.get("source_id") or "").strip()
        if source_id and source_id not in sources:
            errors.append(f"{label}: unknown source_id {source_id}")
        elif status == "VERIFIED" and sources.get(source_id, {}).get("status") != "VERIFIED":
            errors.append(f"{label}: VERIFIED claim requires a VERIFIED source")
    return claim_ids


def validate_portfolio(
    portfolio: dict,
    sources: Dict[str, dict],
    final: bool,
    errors: List[str],
    warnings: List[str],
) -> Set[str]:
    candidates = portfolio.get("candidates", [])
    if not isinstance(candidates, list):
        errors.append("candidate-portfolio.json: candidates must be a list")
        candidates = []
    if not candidates:
        (errors if final else warnings).append("candidate portfolio has no candidate")
    candidate_ids: Set[str] = set()
    required = [
        "candidate_id",
        "scientific_question",
        "contribution_lane",
        "data_feasibility",
        "linked_sample_variables",
        "independent_unit",
        "nearest_work",
        "delta_from_nearest_work",
        "strongest_cheap_baseline",
        "discriminating_validation",
        "failure_criterion",
        "scoop_verdict",
        "disposition",
        "disposition_action",
        "program_fit",
        "evidence_source_ids",
    ]
    for index, candidate in enumerate(candidates, start=1):
        label = f"candidate {index}"
        if not isinstance(candidate, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(candidate, required, label, errors)
        candidate_id = str(candidate.get("candidate_id", "")).strip()
        if candidate_id in candidate_ids:
            errors.append(f"candidate portfolio: duplicate candidate_id {candidate_id}")
        candidate_ids.add(candidate_id)
        if candidate.get("contribution_lane") not in CONTRIBUTION_LANES:
            errors.append(f"{label}: invalid contribution_lane")
        if candidate.get("scoop_verdict") not in SCOOP_VERDICTS:
            errors.append(f"{label}: invalid scoop_verdict")
        if candidate.get("disposition") not in DISPOSITIONS:
            errors.append(f"{label}: invalid disposition")
        if candidate.get("disposition_action") not in DISPOSITION_ACTIONS:
            errors.append(f"{label}: invalid disposition_action")
        evidence_ids = candidate.get("evidence_source_ids", [])
        if not isinstance(evidence_ids, list):
            errors.append(f"{label}: evidence_source_ids must be a list")
        else:
            for source_id in evidence_ids:
                if source_id not in sources:
                    errors.append(f"{label}: unknown evidence source {source_id}")

    decision = portfolio.get("topic_decision", {})
    if not isinstance(decision, dict):
        errors.append("candidate-portfolio.json: topic_decision must be an object")
        decision = {}
    selected = str(decision.get("selected_candidate_id", "")).strip()
    if selected not in {"", "UNVERIFIED"} and selected not in candidate_ids:
        errors.append(f"topic decision: unknown selected_candidate_id {selected}")
    if final:
        if decision.get("status") != "VERIFIED":
            errors.append("topic decision must be VERIFIED in final mode")
        if selected not in candidate_ids:
            errors.append("topic decision must select a recorded candidate in final mode")
        if decision.get("route_status") != "FROZEN":
            errors.append("topic route must be FROZEN in final mode")
        if decision.get("applicant_confirmation") != "VERIFIED":
            errors.append("topic decision requires applicant confirmation in final mode")
    return candidate_ids


def ids_for(records: object, prefix: str, label: str, errors: List[str]) -> Set[str]:
    if not isinstance(records, list):
        errors.append(f"argument map: {label} must be a list")
        return set()
    ids: Set[str] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"argument map {label} row {index}: must be an object")
            continue
        value = str(record.get("id", "")).strip()
        if not re.fullmatch(rf"{prefix}[1-9][0-9]*", value):
            errors.append(f"argument map {label} row {index}: invalid id {value!r}")
        if value in ids:
            errors.append(f"argument map {label}: duplicate id {value}")
        ids.add(value)
    return ids


def require_refs(
    record: dict,
    key: str,
    allowed: Set[str],
    label: str,
    errors: List[str],
) -> None:
    values = record.get(key)
    if not isinstance(values, list) or not values:
        errors.append(f"{label}: {key} must be a non-empty list")
        return
    for value in values:
        if value not in allowed:
            errors.append(f"{label}: unknown {key} value {value}")


def validate_argument(
    argument: dict,
    claim_ids: Set[str],
    final: bool,
    errors: List[str],
    warnings: List[str],
) -> Dict[str, Set[str]]:
    groups = {
        "Q": (argument.get("questions", []), "questions"),
        "C": (argument.get("contents", []), "contents"),
        "V": (argument.get("validations", []), "validations"),
        "O": (argument.get("outputs", []), "outputs"),
        "F": (argument.get("figures", []), "figures"),
    }
    all_empty = all(not records for records, _ in groups.values())
    if all_empty:
        (errors if final else warnings).append("argument map has no Q/C/V/O/F graph")
        return {prefix: set() for prefix in groups}
    ids = {
        prefix: ids_for(records, prefix, label, errors)
        for prefix, (records, label) in groups.items()
    }
    goal = str(argument.get("project_goal", "")).strip()
    if not goal or goal == "UNVERIFIED":
        (errors if final else warnings).append("argument map project_goal is UNVERIFIED")

    for record in argument.get("questions", []):
        if not isinstance(record, dict):
            continue
        label = f"question {record.get('id', '?')}"
        require_fields(record, ["text"], label, errors)
        require_refs(record, "content_ids", ids["C"], label, errors)
        require_refs(record, "validation_ids", ids["V"], label, errors)
    for record in argument.get("contents", []):
        if not isinstance(record, dict):
            continue
        label = f"content {record.get('id', '?')}"
        require_fields(record, ["data_or_object", "method_or_mechanism"], label, errors)
        require_refs(record, "question_ids", ids["Q"], label, errors)
        require_refs(record, "validation_ids", ids["V"], label, errors)
        require_refs(record, "output_ids", ids["O"], label, errors)
        require_refs(record, "prior_claim_ids", claim_ids, label, errors)
        figures = record.get("figure_ids", [])
        if not isinstance(figures, list):
            errors.append(f"{label}: figure_ids must be a list")
        else:
            for figure_id in figures:
                if figure_id not in ids["F"]:
                    errors.append(f"{label}: unknown figure_id {figure_id}")
    for record in argument.get("validations", []):
        if isinstance(record, dict):
            require_fields(
                record,
                ["comparison", "independent_unit", "evaluation_boundary", "failure_criterion", "action_on_failure"],
                f"validation {record.get('id', '?')}",
                errors,
            )
    for record in argument.get("outputs", []):
        if isinstance(record, dict):
            require_fields(
                record,
                ["text", "acceptance_evidence"],
                f"output {record.get('id', '?')}",
                errors,
            )
    for record in argument.get("figures", []):
        if isinstance(record, dict):
            require_fields(
                record,
                ["rhetorical_job", "body_anchor"],
                f"figure {record.get('id', '?')}",
                errors,
            )

    allowed_dependency_ids = set().union(*ids.values(), claim_ids)
    dependencies = argument.get("dependencies", [])
    if not isinstance(dependencies, list):
        errors.append("argument map: dependencies must be a list")
    else:
        for index, dependency in enumerate(dependencies, start=1):
            label = f"dependency {index}"
            if not isinstance(dependency, dict):
                errors.append(f"{label}: must be an object")
                continue
            require_fields(
                dependency,
                ["predecessor_id", "successor_id", "required_evidence", "status"],
                label,
                errors,
            )
            for key in ["predecessor_id", "successor_id"]:
                value = dependency.get(key)
                if value and value not in allowed_dependency_ids:
                    errors.append(f"{label}: unknown {key} {value}")
    return ids


def validate_sections(root: Path, final: bool, errors: List[str], warnings: List[str]) -> None:
    for name in ["rationale", "contents", "foundation"]:
        path = root / "sections" / f"{name}.md"
        text = path.read_text(encoding="utf-8", errors="replace")
        unresolved_status = re.search(
            r"(?mi)^\s*-\s*status:\s*UNVERIFIED\s*$", text
        ) is not None
        visible_characters = len(re.sub(r"\s+", "", text))
        incomplete = unresolved_status or visible_characters < MIN_SECTION_VISIBLE_CHARACTERS
        if incomplete:
            (errors if final else warnings).append(f"section {name} remains an incomplete brief")


def validate_allocation_total(
    rows: object,
    key: str,
    label: str,
    issues: List[str],
) -> Optional[Decimal]:
    if not isinstance(rows, list) or not rows:
        issues.append(f"financial budget requires {label}")
        return None
    observed: Set[str] = set()
    total = Decimal("0")
    for index, row in enumerate(rows, start=1):
        row_label = f"financial budget {label} row {index}"
        if not isinstance(row, dict):
            issues.append(f"{row_label}: must be an object")
            continue
        value = str(row.get(key, "")).strip()
        if not value:
            issues.append(f"{row_label}: missing {key}")
        elif value in observed:
            issues.append(f"{row_label}: duplicate {key} {value}")
        observed.add(value)
        amount = nonnegative_amount(row.get("amount"), row_label, issues)
        if amount is not None:
            total += amount
    return total


def validate_final_source_context(
    label: str,
    source_id: object,
    source: dict,
    project: dict,
    as_of: str,
    expected_scope: str,
    expected_source_types: Set[str],
    errors: List[str],
) -> None:
    if source.get("status") != "VERIFIED":
        return
    source_id = str(source_id).strip()
    project_program = str(project.get("program", "")).strip()
    project_year = str(project.get("target_year", "")).strip()
    if source.get("program") != project_program:
        errors.append(f"{label} source {source_id} program must match project program")
    if str(source.get("year", "")).strip() != project_year:
        errors.append(f"{label} source {source_id} year must match project target_year")
    if source.get("scope") != expected_scope:
        errors.append(f"{label} source {source_id} scope must be {expected_scope}")
    if source.get("source_type") not in expected_source_types:
        errors.append(
            f"{label} source {source_id} source_type must be one of "
            f"{', '.join(sorted(expected_source_types))}"
        )
    accessed_on = source.get("accessed_on")
    if not is_iso_date(accessed_on):
        errors.append(f"{label} source {source_id} accessed_on must be a valid ISO date")
    elif accessed_on != as_of:
        errors.append(f"{label} source {source_id} accessed_on must equal as_of {as_of}")


def validate_financial_budget(
    budget: dict,
    project: dict,
    sources: Dict[str, dict],
    content_ids: Set[str],
    final: bool,
    as_of: str,
    errors: List[str],
    warnings: List[str],
) -> None:
    issues = errors if final else warnings
    if budget.get("schema_version") != 1:
        issues.append("financial budget: schema_version must be 1")
    requirement = budget.get("requirement", {})
    if not isinstance(requirement, dict):
        issues.append("financial budget: requirement must be an object")
        return
    requirement_status = requirement.get("status")
    if requirement_status not in BUDGET_REQUIREMENT_STATUSES:
        issues.append("financial budget requirement has invalid status")
    if final and requirement_status != "VERIFIED":
        errors.append("financial budget requirement must be VERIFIED in final mode")
    requirement_sources = requirement.get("source_ids", [])
    if not isinstance(requirement_sources, list) or not requirement_sources:
        issues.append("financial budget requirement requires source_ids")
    else:
        for source_id in requirement_sources:
            source = sources.get(source_id, {})
            if source.get("status") != "VERIFIED":
                issues.append(f"financial budget requirement source {source_id} is not VERIFIED")
            elif final:
                validate_final_source_context(
                    "financial budget requirement",
                    source_id,
                    source,
                    project,
                    as_of,
                    FINANCIAL_BUDGET_REQUIREMENT_SCOPE,
                    FINANCIAL_BUDGET_REQUIREMENT_SOURCE_TYPES,
                    errors,
                )
    requirement_checked_on = requirement.get("checked_on")
    if not is_iso_date(requirement_checked_on):
        issues.append("financial budget requirement checked_on must be a valid ISO date")
    elif final and requirement_checked_on != as_of:
        errors.append(f"financial budget requirement checked_on must equal as_of {as_of}")
    if not str(requirement.get("scope", "")).strip():
        issues.append("financial budget requirement requires scope")
    elif final and requirement.get("scope") != FINANCIAL_BUDGET_REQUIREMENT_SCOPE:
        errors.append(
            "financial budget requirement scope must be "
            f"{FINANCIAL_BUDGET_REQUIREMENT_SCOPE}"
        )

    required = requirement.get("required")
    if not isinstance(required, bool):
        issues.append("financial budget requirement must declare required as true or false")
        return
    if not required:
        return

    if not str(budget.get("budget_method", "")).strip():
        issues.append("financial budget requires budget_method")
    budget_sources = budget.get("source_ids", [])
    if not isinstance(budget_sources, list) or not budget_sources:
        issues.append("financial budget requires source_ids")
    else:
        for source_id in budget_sources:
            if sources.get(source_id, {}).get("status") != "VERIFIED":
                issues.append(f"financial budget source {source_id} is not VERIFIED")

    total = nonnegative_amount(budget.get("total_amount"), "financial budget total_amount", issues)
    annual_total = validate_allocation_total(
        budget.get("annual_allocations"), "year", "annual_allocations", issues
    )
    category_total = validate_allocation_total(
        budget.get("category_allocations"), "category", "category_allocations", issues
    )
    if total is not None and annual_total is not None and annual_total != total:
        issues.append("financial budget annual allocations must total total_amount")
    if total is not None and category_total is not None and category_total != total:
        issues.append("financial budget category allocations must total total_amount")

    linkages = budget.get("task_resource_linkages", [])
    if not isinstance(linkages, list) or not linkages:
        issues.append("financial budget requires task_resource_linkages")
        return
    for index, linkage in enumerate(linkages, start=1):
        label = f"financial budget task_resource_linkages row {index}"
        if not isinstance(linkage, dict):
            issues.append(f"{label}: must be an object")
            continue
        require_fields(linkage, ["task_id", "resource", "amount"], label, issues)
        task_id = str(linkage.get("task_id", "")).strip()
        if task_id and task_id not in content_ids:
            issues.append(f"{label}: unknown task_id {task_id}")
        nonnegative_amount(linkage.get("amount"), label, issues)


def validate_commitments(
    commitments: dict,
    content_ids: Set[str],
    output_ids: Set[str],
    final: bool,
    errors: List[str],
    warnings: List[str],
) -> Set[str]:
    issues = errors if final else warnings
    if commitments.get("schema_version") != 1:
        issues.append("commitment records: schema_version must be 1")
    records = commitments.get("records", [])
    if not isinstance(records, list):
        issues.append("commitment records: records must be a list")
        return set()
    if not records:
        issues.append("commitment records have no entries")
        return set()

    record_ids: Set[str] = set()
    records_by_id: Dict[str, dict] = {}
    annual_task_ids: Set[str] = set()
    covered_contents: Set[str] = set()
    covered_outputs: Set[str] = set()
    covered_artifacts: Set[tuple] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            issues.append(f"commitment record row {index}: must be an object")
            continue
        record_id = str(record.get("record_id", "")).strip()
        label = f"commitment record {record_id or f'row {index}'}"
        require_fields(
            record,
            [
                "record_id",
                "artifact_type",
                "artifact_id",
                "primary_class",
                "finite_bound",
                "stop_rule",
            ],
            label,
            issues,
        )
        if record_id in record_ids:
            issues.append(f"commitment records: duplicate record_id {record_id}")
        if record_id:
            record_ids.add(record_id)
            records_by_id[record_id] = record

        artifact_type = record.get("artifact_type")
        artifact_id = str(record.get("artifact_id", "")).strip()
        if artifact_type not in COMMITMENT_ARTIFACT_TYPES:
            issues.append(f"{label}: invalid artifact_type {artifact_type!r}")
        else:
            artifact_key = (artifact_type, artifact_id)
            if artifact_key in covered_artifacts:
                issues.append(
                    f"commitment records: duplicate {artifact_type} artifact_id {artifact_id}"
                )
            covered_artifacts.add(artifact_key)
            if artifact_type == "research_content":
                if artifact_id not in content_ids:
                    issues.append(f"{label}: unknown research_content artifact_id {artifact_id}")
                else:
                    covered_contents.add(artifact_id)
            elif artifact_type == "output":
                if artifact_id not in output_ids:
                    issues.append(f"{label}: unknown output artifact_id {artifact_id}")
                else:
                    covered_outputs.add(artifact_id)
            else:
                annual_task_ids.add(artifact_id)
                linked_contents = record.get("linked_content_ids")
                if not isinstance(linked_contents, list) or not linked_contents:
                    issues.append(f"{label}: linked_content_ids must be a non-empty list")
                else:
                    for content_id in linked_contents:
                        if content_id not in content_ids:
                            issues.append(f"{label}: unknown linked_content_id {content_id}")

        if record.get("primary_class") not in COMMITMENT_CLASSES:
            issues.append(f"{label}: invalid primary_class {record.get('primary_class')!r}")
        dependencies = record.get("dependencies")
        if not isinstance(dependencies, list):
            issues.append(f"{label}: dependencies must be a list")
        sequence = record.get("sequence")
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
            issues.append(f"{label}: sequence must be a positive integer")

    for record_id, record in records_by_id.items():
        label = f"commitment record {record_id}"
        dependencies = record.get("dependencies")
        if not isinstance(dependencies, list):
            continue
        sequence = record.get("sequence")
        for dependency_id in dependencies:
            predecessor = records_by_id.get(str(dependency_id))
            if predecessor is None:
                issues.append(f"{label}: unknown dependency {dependency_id}")
                continue
            predecessor_sequence = predecessor.get("sequence")
            if (
                isinstance(sequence, int)
                and not isinstance(sequence, bool)
                and isinstance(predecessor_sequence, int)
                and not isinstance(predecessor_sequence, bool)
                and predecessor_sequence >= sequence
            ):
                issues.append(f"{label}: dependency {dependency_id} must precede it")

    if final:
        missing_contents = sorted(content_ids - covered_contents)
        if missing_contents:
            errors.append(
                f"final mode requires commitment records for research contents: {missing_contents}"
            )
        missing_outputs = sorted(output_ids - covered_outputs)
        if missing_outputs:
            errors.append(f"final mode requires commitment records for outputs: {missing_outputs}")
        if not annual_task_ids:
            errors.append("final mode requires at least one annual_task commitment record")
    return annual_task_ids


def validate_figures(
    root: Path,
    rows: Sequence[dict],
    source_ids: Set[str],
    claim_ids: Set[str],
    argument_figure_ids: Set[str],
    final: bool,
    errors: List[str],
    warnings: List[str],
) -> None:
    if not rows:
        if argument_figure_ids:
            errors.append("figure plan is empty but the argument map names figures")
        else:
            warnings.append("figure plan has no retained figure")
        return
    figure_ids = check_unique(rows, "figure_id", "figure plan", errors)
    missing = argument_figure_ids - figure_ids
    if missing:
        errors.append(f"figure plan is missing argument figures: {sorted(missing)}")
    for index, row in enumerate(rows, start=1):
        label = f"figure row {index}"
        require_fields(row, FIGURE_FIELDS, label, errors)
        for claim_id in split_ids(row.get("claim_ids", "")):
            if claim_id not in claim_ids:
                errors.append(f"{label}: unknown claim_id {claim_id}")
        for source_id in split_ids(row.get("source_ids", "")):
            if source_id not in source_ids:
                errors.append(f"{label}: unknown source_id {source_id}")
        if final:
            for field in ["editable_master", "rendered_output"]:
                if not is_workspace_regular_file(root, row.get(field)):
                    errors.append(
                        f"{label}: {field} must name an in-workspace regular file"
                    )
            if row.get("qa_status") != "PASS":
                errors.append(f"{label}: qa_status must be PASS in final mode")


def validate_reviews(
    rows: Sequence[dict], final: bool, errors: List[str], warnings: List[str]
) -> None:
    if not rows:
        (errors if final else warnings).append("review record has no findings or no-finding entries")
        return
    check_unique(rows, "issue_id", "review findings", errors)
    passes: Set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"review row {index}"
        require_fields(row, REVIEW_FIELDS, label, errors)
        review_pass = row.get("pass_id")
        passes.add(str(review_pass))
        if review_pass not in REVIEW_PASSES:
            errors.append(f"{label}: invalid pass_id {review_pass!r}")
        if row.get("severity") not in REVIEW_SEVERITIES:
            errors.append(f"{label}: invalid severity")
        resolution = row.get("resolution_status")
        if resolution not in REVIEW_RESOLUTIONS:
            errors.append(f"{label}: invalid resolution_status")
        if resolution in {"RESOLVED", "NOT_APPLICABLE"} and not row.get("resolution_evidence", "").strip():
            errors.append(f"{label}: {resolution} requires resolution_evidence")
        if final and row.get("severity") == "fatal" and resolution == "OPEN":
            errors.append(f"{label}: OPEN fatal finding blocks final mode")
    if final and passes != REVIEW_PASSES:
        errors.append(f"final mode requires R1/R2/R3 review entries; observed {sorted(passes)}")


def validate_final_authoring_policy(
    project: dict,
    sources: Dict[str, dict],
    as_of: str,
    errors: List[str],
) -> None:
    policy = project.get("authoring_policy", {})
    if policy.get("status") != "VERIFIED":
        errors.append("authoring policy must be VERIFIED in final mode")
    if policy.get("mode") not in {"EVIDENCE_AND_AUDIT_ONLY", "ASSISTED_DRAFTING_ALLOWED"}:
        errors.append("authoring policy mode is invalid")
    policy_source_ids = policy.get("source_ids", [])
    if not isinstance(policy_source_ids, list) or not policy_source_ids:
        errors.append("authoring policy requires source_ids in final mode")
        policy_source_ids = []
    else:
        for source_id in policy_source_ids:
            if sources.get(source_id, {}).get("status") != "VERIFIED":
                errors.append(f"authoring policy source {source_id} is not VERIFIED")

    checked_on = policy.get("checked_on")
    if not is_iso_date(checked_on):
        errors.append("authoring policy checked_on must be a valid ISO date")
    elif checked_on != as_of:
        errors.append(f"authoring policy checked_on must equal as_of {as_of}")
    scope = policy.get("scope")
    if scope != "authoring_policy":
        errors.append("authoring policy scope must be authoring_policy")
    coverage = policy.get("coverage", [])
    if not isinstance(coverage, list) or not {"funder", "institution"}.issubset(coverage):
        errors.append("authoring policy coverage must include funder and institution")
        coverage = []
    if policy.get("live_refresh_completed") is not True:
        errors.append("authoring policy live refresh must be completed")
    refresh_id = str(policy.get("live_refresh_id", "")).strip()
    if not refresh_id or refresh_id == "UNVERIFIED":
        errors.append("authoring policy requires live_refresh_id")
    completed_on = policy.get("live_refresh_completed_on")
    if not is_iso_date(completed_on):
        errors.append("authoring policy live refresh completed_on must be a valid ISO date")
    elif checked_on != completed_on:
        errors.append("authoring policy checked_on must match completed live refresh")
    elif completed_on != as_of:
        errors.append(f"authoring policy live refresh completed_on must equal as_of {as_of}")

    bindings = policy.get("source_bindings", [])
    if not isinstance(bindings, list) or not bindings:
        errors.append("authoring policy requires source_bindings in final mode")
        return
    project_program = str(project.get("program", "")).strip()
    project_year = str(project.get("target_year", "")).strip()
    bound_source_ids: Set[str] = set()
    bound_authority_kinds: Set[str] = set()
    bound_evidence_identities: Dict[str, Set[tuple[str, str, str]]] = {
        kind: set() for kind in AUTHORITY_KINDS
    }
    for index, binding in enumerate(bindings, start=1):
        label = f"authoring policy binding row {index}"
        if not isinstance(binding, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(
            binding,
            ["source_id", "authority_kind", "program", "year", "scope", "checked_on", "live_refresh_id"],
            label,
            errors,
        )
        source_id = str(binding.get("source_id", "")).strip()
        if source_id in bound_source_ids:
            errors.append(f"authoring policy bindings duplicate source_id {source_id}")
        bound_source_ids.add(source_id)
        if source_id not in policy_source_ids:
            errors.append(f"authoring policy binding {source_id} is not listed in source_ids")
        source = sources.get(source_id, {})
        if source.get("status") != "VERIFIED":
            errors.append(f"authoring policy source {source_id} is not VERIFIED")

        if "coverage" in binding:
            errors.append(
                f"authoring policy binding {source_id} must use authority_kind rather than coverage"
            )
        authority_kind = binding.get("authority_kind")
        if authority_kind not in AUTHORITY_KINDS:
            errors.append(f"authoring policy binding {source_id} has invalid authority_kind {authority_kind!r}")
        else:
            bound_authority_kinds.add(authority_kind)

        if binding.get("program") != project_program:
            errors.append(f"authoring policy binding {source_id} program must match project program")
        if str(binding.get("year", "")).strip() != project_year:
            errors.append(f"authoring policy binding {source_id} year must match project target_year")
        if binding.get("scope") != scope:
            errors.append(f"authoring policy binding {source_id} scope must match policy scope")
        binding_checked_on = binding.get("checked_on")
        if not is_iso_date(binding_checked_on):
            errors.append(f"authoring policy binding {source_id} checked_on must be a valid ISO date")
        elif binding_checked_on != checked_on:
            errors.append(f"authoring policy binding {source_id} checked_on must match policy checked_on")
        elif binding_checked_on != as_of:
            errors.append(f"authoring policy binding {source_id} checked_on must equal as_of {as_of}")
        if binding.get("live_refresh_id") != refresh_id:
            errors.append(
                f"authoring policy binding {source_id} is not part of the completed live refresh"
            )

        if source:
            if source.get("program") != project_program:
                errors.append(f"authoring policy source {source_id} program must match project program")
            if str(source.get("year", "")).strip() != project_year:
                errors.append(f"authoring policy source {source_id} year must match project target_year")
            if source.get("scope") != scope:
                errors.append(f"authoring policy source {source_id} scope must match policy scope")
            if source.get("accessed_on") != binding_checked_on:
                errors.append(
                    f"authoring policy source {source_id} accessed_on must match binding checked_on"
                )
            elif source.get("accessed_on") != as_of:
                errors.append(
                    f"authoring policy source {source_id} accessed_on must equal as_of {as_of}"
                )
            if authority_kind in AUTHORITY_KINDS:
                evidence_identity = tuple(
                    str(source.get(field, "")).strip()
                    for field in ("issuer", "url_or_path", "clause_locator")
                )
                if all(evidence_identity):
                    bound_evidence_identities[authority_kind].add(evidence_identity)

    if set(policy_source_ids) != bound_source_ids:
        errors.append("authoring policy source_ids must exactly match source_bindings")
    if not AUTHORITY_KINDS.issubset(bound_authority_kinds):
        errors.append("authoring policy source bindings must cover funder and institution")
    if len(bound_source_ids) < len(AUTHORITY_KINDS):
        errors.append("authoring policy funder and institution must use different source_ids")
    if (
        bound_evidence_identities["funder"]
        & bound_evidence_identities["institution"]
    ):
        errors.append(
            "authoring policy funder and institution bindings must not reuse evidence identity"
        )
    if set(coverage) != bound_authority_kinds:
        errors.append("authoring policy coverage must match source binding coverage")


def validate_final(
    root: Path,
    project: dict,
    delivery: dict,
    sources: Dict[str, dict],
    as_of: str,
    errors: List[str],
) -> None:
    authority = project.get("official_authority", {})
    if authority.get("status") != "VERIFIED":
        errors.append("official authority must be VERIFIED in final mode")
    authority_checked_on = authority.get("last_checked")
    if not is_iso_date(authority_checked_on):
        errors.append("official authority last_checked must be a valid ISO date")
    elif authority_checked_on != as_of:
        errors.append(f"official authority last_checked must equal as_of {as_of}")
    authority_ids = authority.get("source_ids", [])
    if not isinstance(authority_ids, list) or not authority_ids:
        errors.append("official authority requires source_ids in final mode")
    else:
        for source_id in authority_ids:
            source = sources.get(source_id, {})
            if source.get("status") != "VERIFIED":
                errors.append(f"official authority source {source_id} is not VERIFIED")
            else:
                validate_final_source_context(
                    "official authority",
                    source_id,
                    source,
                    project,
                    as_of,
                    OFFICIAL_AUTHORITY_SCOPE,
                    OFFICIAL_AUTHORITY_SOURCE_TYPES,
                    errors,
                )

    template = project.get("official_template", {})
    if template.get("status") != "VERIFIED":
        errors.append("official template must be VERIFIED in final mode")
    template_source = template.get("source_id")
    template_source_row = sources.get(template_source, {})
    if template_source_row.get("status") != "VERIFIED":
        errors.append("official template source must be VERIFIED in final mode")
    else:
        validate_final_source_context(
            "official template",
            template_source,
            template_source_row,
            project,
            as_of,
            OFFICIAL_TEMPLATE_SCOPE,
            OFFICIAL_TEMPLATE_SOURCE_TYPES,
            errors,
        )
    template_artifact_path = str(template.get("artifact_path", "")).strip()
    if not is_workspace_regular_file(root, template_artifact_path):
        errors.append(
            "official template artifact_path must name an in-workspace regular file"
        )
    template_source_path = str(template_source_row.get("url_or_path", "")).strip()
    if (
        template_source_row.get("status") == "VERIFIED"
        and template_source_path
        and not re.match(r"https?://", template_source_path, flags=re.IGNORECASE)
        and template_source_path != template_artifact_path
    ):
        errors.append("official template artifact_path must match local source url_or_path")

    if project.get("applicant_review_status") != "VERIFIED":
        errors.append("applicant review must be VERIFIED in final mode")
    if project.get("route_status") != "FROZEN":
        errors.append("project route must be FROZEN in final mode")
    validate_final_authoring_policy(project, sources, as_of, errors)

    if delivery.get("build_status") != "PASS":
        errors.append("final build_status must be PASS")
    if delivery.get("visual_review_status") != "PASS":
        errors.append("final visual_review_status must be PASS")
    if delivery.get("applicant_confirmation") != "VERIFIED":
        errors.append("final artifact requires applicant confirmation")
    if not is_workspace_regular_file(root, delivery.get("rendered_artifact")):
        errors.append(
            "final rendered_artifact must name an in-workspace regular file"
        )


def main() -> None:
    args = parse_args()
    root = args.workspace.resolve()
    errors: List[str] = []
    warnings: List[str] = []
    notes: List[str] = []
    notes.append(VALIDATION_SCOPE_NOTE)
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        report = {
            "status": "FAIL",
            "mode": args.mode,
            "as_of": args.as_of,
            "validation_scope": VALIDATION_SCOPE,
            "errors": errors,
            "warnings": warnings,
            "notes": notes,
        }
        if args.json:
            print(json.dumps(report, ensure_ascii=False))
        else:
            print(
                f"Status: FAIL | mode={args.mode} | as_of={args.as_of} "
                f"| validation_scope={VALIDATION_SCOPE}"
            )
            print(f"NOTE {VALIDATION_SCOPE_NOTE}")
            for item in errors:
                print(f"ERROR {item}", file=sys.stderr)
        raise SystemExit(1)

    project = load_json(root / "project.json", errors)
    if project.get("schema_version") != 1:
        errors.append("project.json: schema_version must be 1")
    require_fields(
        project,
        ["project_id", "program", "target_year", "project_type", "confidentiality", "authoring_policy"],
        "project.json",
        errors,
    )
    if project.get("program") not in PROGRAMS:
        errors.append("project.json: invalid program")
    target_year = project.get("target_year")
    if (
        not isinstance(target_year, int)
        or isinstance(target_year, bool)
        or not MIN_TARGET_YEAR <= target_year <= MAX_TARGET_YEAR
    ):
        errors.append("project.json: invalid target_year")
    if project.get("confidentiality") not in CONFIDENTIALITY:
        errors.append("project.json: invalid confidentiality")
    policy = project.get("authoring_policy", {})
    if not isinstance(policy, dict):
        errors.append("project.json: authoring_policy must be an object")
    else:
        if policy.get("mode") not in {"EVIDENCE_AND_AUDIT_ONLY", "ASSISTED_DRAFTING_ALLOWED"}:
            errors.append("project.json: invalid authoring_policy mode")
        if policy.get("status") not in AUTHORING_POLICY_STATUSES:
            errors.append("project.json: invalid authoring_policy status")
        if policy.get("status") == "UNVERIFIED":
            warnings.append("authoring policy is UNVERIFIED; evidence-and-audit-only mode remains in force")
        if policy.get("status") == "VERIFIED_PROFILE":
            warnings.append("authoring policy is a bundled profile; final mode requires a live refresh")
        if policy.get("mode") == "EVIDENCE_AND_AUDIT_ONLY":
            notes.append("application prose must remain applicant-authored under the recorded policy")

    source_rows = load_csv(root / "authority/source-register.csv", SOURCE_FIELDS, errors)
    sources = validate_sources(source_rows, errors, warnings)
    claim_rows = load_csv(root / "evidence/claim-ledger.csv", CLAIM_FIELDS, errors)
    claim_ids = validate_claims(claim_rows, sources, errors, warnings)
    portfolio = load_json(root / "topic/candidate-portfolio.json", errors)
    validate_portfolio(portfolio, sources, args.mode == "final", errors, warnings)
    argument = load_json(root / "argument/argument-map.json", errors)
    argument_ids = validate_argument(argument, claim_ids, args.mode == "final", errors, warnings)
    validate_sections(root, args.mode == "final", errors, warnings)
    figure_rows = load_csv(root / "figures/figure-plan.csv", FIGURE_FIELDS, errors)
    validate_figures(
        root,
        figure_rows,
        set(sources),
        claim_ids,
        argument_ids.get("F", set()),
        args.mode == "final",
        errors,
        warnings,
    )
    review_rows = load_csv(root / "reviews/review-findings.csv", REVIEW_FIELDS, errors)
    validate_reviews(review_rows, args.mode == "final", errors, warnings)
    delivery = load_json(root / "delivery/final-format.json", errors)
    commitments = load_json(root / "commitments/commitment-records.json", errors)
    annual_task_ids = validate_commitments(
        commitments,
        argument_ids.get("C", set()),
        argument_ids.get("O", set()),
        args.mode == "final",
        errors,
        warnings,
    )
    budget = load_json(root / "budget/financial-budget.json", errors)
    validate_financial_budget(
        budget,
        project,
        sources,
        argument_ids.get("C", set()) | annual_task_ids,
        args.mode == "final",
        args.as_of,
        errors,
        warnings,
    )

    if args.mode == "final":
        validate_final(root, project, delivery, sources, args.as_of, errors)
    else:
        if project.get("official_authority", {}).get("status") != "VERIFIED":
            warnings.append("official authority is not yet VERIFIED")
        if project.get("official_template", {}).get("status") != "VERIFIED":
            warnings.append("official template is not yet VERIFIED; no final-format claim is available")
        if project.get("route_status") != "FROZEN":
            warnings.append("project route is not FROZEN")
        if delivery.get("build_status") != "PASS":
            warnings.append("final artifact has not been built and checked")

    status = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    report = {
        "status": status,
        "mode": args.mode,
        "as_of": args.as_of,
        "validation_scope": VALIDATION_SCOPE,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "notes": sorted(set(notes)),
        "counts": {
            "sources": len(source_rows),
            "claims": len(claim_rows),
            "candidates": len(portfolio.get("candidates", [])) if isinstance(portfolio.get("candidates", []), list) else 0,
            "questions": len(argument.get("questions", [])) if isinstance(argument.get("questions", []), list) else 0,
            "figures": len(figure_rows),
            "review_entries": len(review_rows),
        },
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print(
            f"Status: {status} | mode={args.mode} | as_of={args.as_of} "
            f"| validation_scope={VALIDATION_SCOPE}"
        )
        for item in report["errors"]:
            print(f"ERROR {item}", file=sys.stderr)
        for item in report["warnings"]:
            print(f"WARNING {item}", file=sys.stderr)
        for item in report["notes"]:
            print(f"NOTE {item}")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
