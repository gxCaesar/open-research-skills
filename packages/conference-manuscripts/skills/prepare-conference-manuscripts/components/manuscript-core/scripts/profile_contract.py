#!/usr/bin/env python3
"""Minimal readiness checks shared by conference venue-profile auditors."""

from __future__ import annotations

from datetime import date
from json import JSONDecodeError
from math import isfinite
import re
from typing import Optional


CONTROL_WORD_RE = re.compile(r"[A-Za-z@]+")


def path_free_exception_summary(error: BaseException) -> str:
    """Summarize a CLI exception without interpolating an input filename."""
    if isinstance(error, JSONDecodeError):
        return f"invalid JSON at line {error.lineno}, column {error.colno}"
    if isinstance(error, OSError):
        if error.strerror:
            return f"{type(error).__name__}: {error.strerror}"
        return type(error).__name__
    return type(error).__name__


def contains_placeholder(value) -> bool:
    if isinstance(value, str):
        return "REPLACE_WITH_" in value
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    return False


def string_list_error(value, field: str, *, allowed_stages: Optional[set] = None) -> Optional[str]:
    if not isinstance(value, list):
        return f"{field} must be a list"
    for item in value:
        if not isinstance(item, str) or not item.strip():
            return f"{field} must contain non-empty strings"
        if allowed_stages is not None and item not in allowed_stages:
            return f"{field} references unsupported stage {item!r}"
    return None


def stage_map_error(value, field: str, allowed_stages: set) -> Optional[str]:
    if not isinstance(value, dict):
        return f"{field} must be an object"
    for stage, items in value.items():
        if not isinstance(stage, str) or not stage.strip():
            return f"{field} contains an invalid stage key"
        if stage not in allowed_stages:
            return f"{field} references unsupported stage {stage!r}"
        error = string_list_error(items, f"{field}.{stage}")
        if error:
            return error
    return None


def positive_integer_stage_map_error(value, field: str, allowed_stages: set) -> Optional[str]:
    if not isinstance(value, dict):
        return f"{field} must be an object"
    for stage, limit in value.items():
        if not isinstance(stage, str) or not stage.strip():
            return f"{field} contains an invalid stage key"
        if stage not in allowed_stages:
            return f"{field} references unsupported stage {stage!r}"
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            return f"{field}.{stage} must be a positive integer"
    return None


def positive_number_stage_map_error(value, field: str, allowed_stages: set) -> Optional[str]:
    if not isinstance(value, dict):
        return f"{field} must be an object"
    for stage, limit in value.items():
        if not isinstance(stage, str) or not stage.strip():
            return f"{field} contains an invalid stage key"
        if stage not in allowed_stages:
            return f"{field} references unsupported stage {stage!r}"
        if (
            not isinstance(limit, (int, float))
            or isinstance(limit, bool)
            or not isfinite(float(limit))
            or limit <= 0
        ):
            return f"{field}.{stage} must be a positive number"
    return None


def allowed_stages_error(profile: dict) -> Optional[str]:
    allowed_stages = profile.get("allowed_stages")
    error = string_list_error(allowed_stages, "allowed_stages")
    if error:
        return error
    if not allowed_stages:
        return "allowed_stages must not be empty"
    if len(set(allowed_stages)) != len(allowed_stages):
        return "allowed_stages contains duplicate stages"
    return None


def tex_contract_error(contract: dict, allowed_stages: set) -> Optional[str]:
    if "required_document_class_options" in contract:
        error = string_list_error(
            contract["required_document_class_options"],
            "tex_contract.required_document_class_options",
        )
        if error:
            return error

    for field in ("required_options", "forbidden_options", "required_headings"):
        if field in contract:
            error = stage_map_error(contract[field], f"tex_contract.{field}", allowed_stages)
            if error:
                return error

    for field in ("anonymous_stages", "require_abstract", "final_copy_required_stages"):
        if field in contract:
            error = string_list_error(contract[field], f"tex_contract.{field}", allowed_stages=allowed_stages)
            if error:
                return error

    if "forbidden_layout_packages" in contract:
        error = string_list_error(contract["forbidden_layout_packages"], "tex_contract.forbidden_layout_packages")
        if error:
            return error
    if "anonymous_source_identity_commands" in contract:
        identity_commands = contract["anonymous_source_identity_commands"]
        error = string_list_error(identity_commands, "tex_contract.anonymous_source_identity_commands")
        if error:
            return error
        if any(CONTROL_WORD_RE.fullmatch(command) is None for command in identity_commands):
            return "tex_contract.anonymous_source_identity_commands must contain bare TeX control-word names"

    mode = contract.get("anonymous_source_author_mode", "render_hidden")
    if mode not in {"flag", "render_hidden"}:
        return "tex_contract.anonymous_source_author_mode must be 'flag' or 'render_hidden'"
    if mode == "flag" and "anonymous_source_identity_commands" in contract and not contract[
        "anonymous_source_identity_commands"
    ]:
        return "tex_contract.anonymous_source_identity_commands must not be empty in flag mode"
    if "forbid_acknowledgments_in_anonymous" in contract and not isinstance(
        contract["forbid_acknowledgments_in_anonymous"], bool
    ):
        return "tex_contract.forbid_acknowledgments_in_anonymous must be a boolean"

    final_command = contract.get("final_copy_command", "")
    if not isinstance(final_command, str):
        return "tex_contract.final_copy_command must be a string"
    if final_command and CONTROL_WORD_RE.fullmatch(final_command) is None:
        return "tex_contract.final_copy_command must be a bare TeX control-word name"
    final_rule_ids = contract.get("final_copy_rule_ids")
    if final_rule_ids is not None:
        if not isinstance(final_rule_ids, dict):
            return "tex_contract.final_copy_rule_ids must be an object"
        for key in ("disabled", "enabled"):
            value = final_rule_ids.get(key)
            if not isinstance(value, str) or not value.strip():
                return f"tex_contract.final_copy_rule_ids.{key} must be a non-empty string"
    if final_command.strip():
        if final_rule_ids is None:
            return "tex_contract.final_copy_rule_ids is required when final_copy_command is set"
        if "final_copy_required_stages" not in contract:
            return "tex_contract.final_copy_required_stages is required when final_copy_command is set"
    return None


def pdf_contract_error(contract: dict, allowed_stages: set, *, require_geometry: bool) -> Optional[str]:
    if "anonymous_stages" in contract:
        error = string_list_error(
            contract["anonymous_stages"],
            "pdf_contract.anonymous_stages",
            allowed_stages=allowed_stages,
        )
        if error:
            return error
    for field in ("max_total_pages", "manual_content_page_limit"):
        if field in contract:
            error = positive_integer_stage_map_error(contract[field], f"pdf_contract.{field}", allowed_stages)
            if error:
                return error
    if "max_file_size_mb" in contract:
        error = positive_number_stage_map_error(
            contract["max_file_size_mb"],
            "pdf_contract.max_file_size_mb",
            allowed_stages,
        )
        if error:
            return error

    if not require_geometry:
        return None
    for field in ("page_width_points", "page_height_points"):
        value = contract.get(field)
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not isfinite(float(value))
            or value <= 0
        ):
            return f"pdf_contract.{field} is not positive"
    tolerance = contract.get("page_tolerance_points", 2.0)
    if (
        not isinstance(tolerance, (int, float))
        or isinstance(tolerance, bool)
        or not isfinite(float(tolerance))
        or tolerance < 0
    ):
        return "pdf_contract.page_tolerance_points is not a non-negative number"
    return None


def required_rule_source_ids(profile: dict, *, include_pdf: bool) -> set:
    """Return official-rule IDs that the configured auditors can emit."""
    contract = profile["tex_contract"]
    required = {"DOCUMENT_CLASS", contract["style_rule_id"]}
    anonymous_stages = contract.get("anonymous_stages", [])
    if anonymous_stages and contract.get("anonymous_source_author_mode", "render_hidden") == "flag":
        required.add("ANON_SOURCE_IDENTITY")
    if anonymous_stages and contract.get("forbid_acknowledgments_in_anonymous"):
        required.add("ANON_ACKNOWLEDGMENTS")
    final_command = contract.get("final_copy_command", "").strip()
    if final_command:
        final_rule_ids = contract["final_copy_rule_ids"]
        required.update({final_rule_ids["disabled"], final_rule_ids["enabled"]})
    if contract.get("require_abstract"):
        required.add("ABSTRACT_REQUIRED")
    headings = contract.get("required_headings", {})
    if isinstance(headings, dict) and any(headings.values()):
        required.add("REQUIRED_HEADING")

    if include_pdf:
        pdf_contract = profile["pdf_contract"]
        required.add("PDF_PAGE_SIZE")
        if pdf_contract.get("max_total_pages"):
            required.add("PDF_TOTAL_PAGE_LIMIT")
        if pdf_contract.get("max_file_size_mb"):
            required.add("PDF_FILE_SIZE")
        if pdf_contract.get("anonymous_stages"):
            required.add("PDF_AUTHOR_METADATA")
    return required


def rule_sources_error(profile: dict, *, include_pdf: bool) -> Optional[str]:
    rule_sources = profile.get("rule_sources")
    if not isinstance(rule_sources, dict):
        return "rule_sources is missing"
    for rule_id, source_ids in rule_sources.items():
        if not isinstance(rule_id, str) or not rule_id.strip():
            return "rule_sources contains an invalid rule ID"
        if not isinstance(source_ids, list) or not source_ids:
            return f"rule_sources.{rule_id} must be a non-empty list"
        if any(not isinstance(source_id, str) or not source_id.strip() for source_id in source_ids):
            return f"rule_sources.{rule_id} contains an invalid source ID"
    for rule_id in sorted(required_rule_source_ids(profile, include_pdf=include_pdf)):
        if rule_id not in rule_sources:
            return f"rule_sources.{rule_id} is missing"
    return None


def readiness_error(profile: dict, *, require_pdf_geometry: bool = False) -> Optional[str]:
    """Return why a profile is not usable, or ``None`` when the contract is ready."""
    if contains_placeholder(profile):
        return "one or more fields are still placeholders"

    required_text = {
        "venue": profile.get("venue"),
        "track": profile.get("track"),
        "checked_on": profile.get("checked_on"),
    }
    tex_contract = profile.get("tex_contract")
    if not isinstance(tex_contract, dict):
        return "tex_contract is missing"
    required_text.update(
        {
            "tex_contract.document_class": tex_contract.get("document_class"),
            "tex_contract.style_package": tex_contract.get("style_package"),
            "tex_contract.style_rule_id": tex_contract.get("style_rule_id"),
        }
    )
    for field, value in required_text.items():
        if not isinstance(value, str) or not value.strip():
            return f"{field} is missing"

    year = profile.get("year")
    if not isinstance(year, int) or isinstance(year, bool) or year <= 0:
        return "year is not a positive integer"
    try:
        date.fromisoformat(required_text["checked_on"])
    except ValueError:
        return "checked_on is not an ISO date"

    stages_error = allowed_stages_error(profile)
    if stages_error:
        return stages_error
    allowed_stages = set(profile["allowed_stages"])
    contract_error = tex_contract_error(tex_contract, allowed_stages)
    if contract_error:
        return contract_error

    pdf_contract = profile.get("pdf_contract")
    if pdf_contract is None:
        if require_pdf_geometry:
            return "pdf_contract is missing"
    elif not isinstance(pdf_contract, dict):
        return "pdf_contract must be an object"
    else:
        contract_error = pdf_contract_error(
            pdf_contract,
            allowed_stages,
            require_geometry=require_pdf_geometry,
        )
        if contract_error:
            return contract_error

    sources_error = rule_sources_error(profile, include_pdf=require_pdf_geometry)
    if sources_error:
        return sources_error
    return None
