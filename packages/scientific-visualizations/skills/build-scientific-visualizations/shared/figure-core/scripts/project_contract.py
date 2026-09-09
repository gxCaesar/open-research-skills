#!/usr/bin/env python3
"""Shared schema-1.2 contracts for scientific-figure projects."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import ipaddress
import json
from pathlib import Path
import re
from typing import Any, Optional
from urllib.parse import urlparse


CORE_ROOT = Path(__file__).resolve().parent.parent
VENUE_PROFILES_PATH = CORE_ROOT / "assets" / "venue-profiles.json"
METHOD_KINDS = {"flowchart", "method", "model_architecture"}
SOLID_EDGE_ROLES = {"primary", "sequence", "inference", "measured", "causal"}
DASHED_EDGE_ROLES = {
    "predicted",
    "prospective",
    "conditioning",
    "control",
    "parallel",
    "optional",
    "training_only",
}
SOURCE_AVAILABILITY = {"file", "repository", "controlled_access", "not_applicable"}
SOURCE_KINDS = {"numeric", "image", "structure", "repository_object"}
PORTABLE_FORMATS = {"CSV", "TSV", "XLSX", "JSON", "TXT"}
AUDIENCES = {"author", "reviewer", "public"}
DATA_PANEL_KINDS = {"data", "result", "negative_result"}
DELIVERY_OUTPUT_SUFFIXES = {".pdf", ".svg", ".png", ".pptx"}
EVIDENCE_STATUSES = {
    "schematic",
    "decorative",
    "measured",
    "observed",
    "inferred",
    "predicted",
    "prospective",
    "hypothesis",
    "training_only",
    "unresolved",
}
EVIDENCE_STATUS_FAMILIES = (
    {"measured", "observed"},
    {"inferred", "predicted"},
    {"prospective", "hypothesis"},
    {"training_only"},
    {"unresolved"},
)
WORD_RE = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*")
IMAGE_FIELDS = {
    "acquisition",
    "channels",
    "lut",
    "crop",
    "registration",
    "segmentation",
    "processing",
}
PRIVATE_LOCATOR_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9_])file:(?:/{1,3}|[A-Za-z]:[\\/])", re.IGNORECASE),
    re.compile(r"(?<![A-Za-z0-9_])(?:smb|afp|nfs)://", re.IGNORECASE),
    re.compile(r"(?:^|[\s\"'=,(])/(?:Users|home|private/var|Volumes|mnt|media)(?:/|\\)", re.IGNORECASE),
    re.compile(r"(?:^|[\s\"'=,(])~(?:/|\\)"),
    re.compile(r"\\\\[^\\/\s]+\\[^\\\s]+"),
    re.compile(r"[A-Za-z]:[\\/](?:Users|Documents|Desktop|AppData)[\\/]", re.IGNORECASE),
)


def is_private_locator(value: str) -> bool:
    """Return whether text contains a machine-local or private-share locator."""

    return isinstance(value, str) and any(pattern.search(value) for pattern in PRIVATE_LOCATOR_PATTERNS)


def is_public_https_url(value: Any) -> bool:
    """Accept an HTTPS route with a non-local host and no embedded credentials."""

    if not isinstance(value, str) or is_private_locator(value):
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    if parsed.scheme.casefold() != "https" or not parsed.hostname or parsed.username or parsed.password:
        return False
    host = parsed.hostname.casefold().rstrip(".")
    if host == "localhost" or host.endswith(".local"):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return "." in host
    return address.is_global


def load_venue_profiles() -> dict[str, Any]:
    """Return the bundled dated profile registry."""

    return json.loads(VENUE_PROFILES_PATH.read_text(encoding="utf-8"))


def caption_word_count(text: str) -> int:
    """Count caption prose while excluding common TeX commands and formula spans."""

    text = re.sub(r"\\(?:ref|label|cite[a-zA-Z]*)\*?\{[^{}]*\}", " ", text)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\\[[\s\S]*?\\\]", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD_RE.findall(text))


def profile_height_limit(profile: dict[str, Any], words: int) -> Optional[float]:
    """Resolve a caption-dependent maximum figure height from a venue profile."""

    limits = profile.get("geometry", {}).get("caption_height_limits", [])
    for band in limits:
        if words < band["caption_words_lt"]:
            return float(band["max_height_mm"])
    return None


def evidence_status_compatible(symbol_status: str, claim_status: str) -> bool:
    """Return whether a pictogram status does not overstate its anchored claim."""

    if symbol_status in {"schematic", "decorative"}:
        return True
    return any(symbol_status in family and claim_status in family for family in EVIDENCE_STATUS_FAMILIES)


def resolve_layout_profile(name: str) -> tuple[dict[str, Any], list[str]]:
    """Resolve a dated profile or a backward-compatible legacy alias."""

    registry = load_venue_profiles()
    profiles = registry.get("profiles", {})
    aliases = registry.get("legacy_aliases", {})
    if name in profiles:
        contract = deepcopy(profiles[name])
        contract["profile_id"] = name
        return contract, []
    if name in aliases:
        alias = aliases[name]
        profile_id = alias.get("profile_id")
        if profile_id:
            contract = deepcopy(profiles[profile_id])
        else:
            contract = {
                "target_context": "journal_submission",
                "journal": "Nature-family journal",
                "article_type": "unspecified",
                "submission_stage": "unspecified",
                "authority": {
                    "title": "Legacy undated layout alias",
                    "url": None,
                    "checked_date": None,
                    "scope": alias["note"],
                },
                "geometry": {
                    "selected_width_mm": alias["width_mm"],
                    "max_height_mm": None,
                },
                "technical": {
                    "font_family": "Arial",
                    "text_range_pt": [5.0, 7.0],
                    "min_resolution_dpi": 300,
                    "colour_space": "RGB",
                    "preferred_formats": ["PDF", "SVG", "PNG"],
                },
            }
        contract["profile_id"] = name
        contract["authority_status"] = "unverified_legacy_alias"
        contract["legacy_alias"] = name
        contract["geometry"]["selected_width_mm"] = alias["width_mm"]
        warning = f"legacy layout profile {name!r} is unverified: {alias['note']}"
        return contract, [warning]
    supported = sorted(set(profiles) | set(aliases) | {"custom"})
    raise ValueError(f"unknown layout profile {name!r}; supported profiles: {', '.join(supported)}")


def validate_v12_project(
    root: Path,
    spec: dict[str, Any],
    ledger: dict[str, Any],
    manifest: dict[str, Any],
    *,
    stage: str,
    allow_missing_outputs: bool = False,
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate schema-1.2 cross-file records without changing the project."""

    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}
    if stage not in {"draft", "layout", "final"}:
        return [f"invalid validation stage {stage!r}"], [], checks

    records: dict[str, dict[str, Any]] = {}
    for name in ("venue_contract.json", "layout_blueprint.json", "source_data_manifest.json"):
        path = root / name
        if not path.is_file():
            errors.append(f"schema 1.2 project is missing {name}")
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{name}: cannot read valid JSON: {error}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{name}: top level must be an object")
            continue
        records[name] = value
        if value.get("schema_version") != "1.2":
            errors.append(f"{name}: schema_version must be 1.2")
        if value.get("figure_id") != spec.get("figure_id"):
            errors.append(f"{name}: figure_id must match figure_spec.json")

    if len(records) != 3:
        return errors, warnings, checks

    venue = records["venue_contract.json"]
    blueprint = records["layout_blueprint.json"]
    source_manifest = records["source_data_manifest.json"]
    checks["stage"] = stage

    _find_prohibited_manifest_content(
        manifest,
        errors,
        location="asset_manifest.json",
        document_name="asset_manifest.json",
    )

    _validate_venue_contract(root, venue, spec, stage, errors, warnings, checks)
    _validate_content_ledger(ledger, spec, errors, checks)
    _validate_blueprint(blueprint, spec, ledger, source_manifest, errors, warnings, checks)
    flow_errors, flow_warnings, flow_checks = validate_flowcharts(root, spec, ledger)
    errors.extend(flow_errors)
    warnings.extend(flow_warnings)
    if flow_checks:
        checks["flowcharts"] = flow_checks
    source_errors, source_warnings, source_checks = validate_source_data(
        root,
        spec,
        blueprint,
        source_manifest,
        manifest,
        stage=stage,
        allow_missing_outputs=allow_missing_outputs,
    )
    errors.extend(source_errors)
    warnings.extend(source_warnings)
    checks["source_data"] = source_checks
    if stage == "final":
        _validate_layout_review(root, spec, venue, blueprint, errors, checks)
    return errors, warnings, checks


def _validate_venue_contract(
    root: Path,
    venue: dict[str, Any],
    spec: dict[str, Any],
    stage: str,
    errors: list[str],
    warnings: list[str],
    checks: dict[str, Any],
) -> None:
    allowed_contexts = {"journal_submission", "preprint", "presentation", "custom"}
    allowed_statuses = {"verified", "custom", "unverified_legacy_alias"}
    context = venue.get("target_context")
    status = venue.get("authority_status")
    if context not in allowed_contexts:
        errors.append(f"venue_contract.json: invalid target_context {context!r}")
    if status not in allowed_statuses:
        errors.append(f"venue_contract.json: invalid authority_status {status!r}")

    authority = venue.get("authority", {})
    checked_date = authority.get("checked_date") if isinstance(authority, dict) else None
    if status == "verified":
        if not isinstance(authority, dict) or not authority.get("title") or not authority.get("url"):
            errors.append("venue_contract.json: verified authority requires title and URL")
        try:
            if not isinstance(checked_date, str):
                raise ValueError
            date.fromisoformat(checked_date)
        except ValueError:
            errors.append(f"venue_contract.json: invalid authority checked date {checked_date!r}")
    elif status == "unverified_legacy_alias":
        warnings.append("venue authority is an unverified legacy alias; select a dated profile before final delivery")

    geometry = venue.get("geometry", {})
    selected_width = geometry.get("selected_width_mm") if isinstance(geometry, dict) else None
    spec_width = spec.get("journal_profile", {}).get("page_width_mm")
    composite_width = spec.get("composite", {}).get("size_mm", [None])[0]
    if not isinstance(selected_width, (int, float)) or selected_width <= 0:
        errors.append("venue_contract.json: selected_width_mm must be positive")
    elif not isinstance(spec_width, (int, float)) or abs(selected_width - spec_width) > 0.2:
        errors.append(
            f"venue width {selected_width:g} mm does not match figure_spec journal width {spec_width!r}"
        )
    elif not isinstance(composite_width, (int, float)) or abs(selected_width - composite_width) > 0.2:
        errors.append(
            f"venue width {selected_width:g} mm does not match composite width {composite_width!r}"
        )

    composite_size = spec.get("composite", {}).get("size_mm", [])
    composite_height = composite_size[1] if isinstance(composite_size, list) and len(composite_size) == 2 else None
    if not isinstance(composite_height, (int, float)) or composite_height <= 0:
        errors.append("figure_spec.json: composite height must be positive")
    max_height = geometry.get("max_height_mm") if isinstance(geometry, dict) else None
    caption_words = None
    caption_limits = geometry.get("caption_height_limits", []) if isinstance(geometry, dict) else []
    if caption_limits:
        caption_file = venue.get("caption_file")
        if not _nonempty(caption_file):
            message = "venue_contract.json: caption_file is required for caption-dependent height validation"
            if stage == "final":
                errors.append(message)
            else:
                warnings.append(message)
            max_height = None
        elif not _safe_relative_path(caption_file):
            errors.append(f"venue_contract.json: unsafe caption_file path {caption_file!r}")
            max_height = None
        elif not is_regular_project_file(root, caption_file):
            errors.append(
                "venue_contract.json: caption_file must resolve to a regular non-symlink file within the project"
            )
            max_height = None
        else:
            try:
                caption_words = caption_word_count((root / caption_file).read_text(encoding="utf-8"))
            except OSError as error:
                errors.append(f"venue_contract.json: cannot read caption_file: {error}")
                max_height = None
            else:
                max_height = profile_height_limit(venue, caption_words)
                if max_height is None:
                    errors.append(
                        f"caption has {caption_words} words; venue profile has no 300-word-or-longer height allowance"
                    )
    if max_height is not None:
        if not isinstance(max_height, (int, float)) or max_height <= 0:
            errors.append("venue_contract.json: maximum height must be positive")
        elif isinstance(composite_height, (int, float)) and composite_height - max_height > 0.2:
            errors.append(
                f"composite height {composite_height:g} mm exceeds venue maximum height {max_height:g} mm"
            )

    profile_id = venue.get("profile_id")
    registry = load_venue_profiles()
    registered = registry.get("profiles", {}).get(profile_id)
    if status == "verified" and registered:
        registered_width = registered.get("geometry", {}).get("selected_width_mm")
        if (
            isinstance(selected_width, (int, float))
            and isinstance(registered_width, (int, float))
            and abs(selected_width - registered_width) > 0.001
        ):
            errors.append(
                f"venue width {selected_width:g} mm differs from dated profile {profile_id} ({registered_width:g} mm)"
            )
        for key in (
            "target_context",
            "journal",
            "article_type",
            "submission_stage",
            "authority",
            "geometry",
            "technical",
        ):
            if venue.get(key) != registered.get(key):
                errors.append(f"venue_contract.json: {key} differs from dated profile {profile_id}")

    if stage == "final" and context == "journal_submission" and status != "verified":
        errors.append("final journal submission requires verified venue authority")

    checks["venue"] = {
        "profile_id": profile_id,
        "target_context": context,
        "authority_status": status,
        "selected_width_mm": selected_width,
        "composite_height_mm": composite_height,
        "max_height_mm": max_height,
        "caption_words": caption_words,
    }


def _validate_content_ledger(
    ledger: dict[str, Any],
    spec: dict[str, Any],
    errors: list[str],
    checks: dict[str, Any],
) -> None:
    if ledger.get("schema_version") != "1.2":
        errors.append("content_ledger.json: schema_version must be 1.2")
    claims = ledger.get("claims", [])
    if not isinstance(claims, list) or not claims:
        errors.append("content_ledger.json: claims must contain at least one claim")
        claims = []
    claim_ids = _ids(claims, "id")
    if _duplicates(claim_ids):
        errors.append(f"content_ledger.json: duplicate claim IDs {_duplicates(claim_ids)}")
    spec_panel_ids = set(_ids(spec.get("panels"), "id"))
    claim_by_id = {
        claim.get("id"): claim
        for claim in claims
        if isinstance(claim, dict) and claim.get("id")
    }
    for claim_id, claim in claim_by_id.items():
        panel_id = claim.get("panel_id")
        if panel_id not in spec_panel_ids:
            errors.append(f"content ledger claim {claim_id}: unknown panel {panel_id}")
        if not _nonempty(claim.get("claim")):
            errors.append(f"content ledger claim {claim_id}: claim text is required")
        if not isinstance(claim.get("source_anchors"), list):
            errors.append(f"content ledger claim {claim_id}: source_anchors must be a list")
        evidence_status = claim.get("evidence_status")
        if evidence_status not in EVIDENCE_STATUSES:
            errors.append(
                f"content ledger claim {claim_id}: evidence_status must be one of {sorted(EVIDENCE_STATUSES)}"
            )
    for panel in ledger.get("panels", []):
        if not isinstance(panel, dict):
            errors.append("content_ledger.json: each panel must be an object")
            continue
        panel_id = panel.get("id")
        panel_claim_ids = panel.get("claim_ids")
        if not isinstance(panel_claim_ids, list) or not panel_claim_ids:
            errors.append(f"content ledger panel {panel_id}: claim_ids must be non-empty")
            continue
        for claim_id in panel_claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                errors.append(f"content ledger panel {panel_id}: unknown claim {claim_id}")
            elif claim.get("panel_id") != panel_id:
                errors.append(
                    f"content ledger panel {panel_id}: claim {claim_id} belongs to panel {claim.get('panel_id')}"
                )
    checks["content_ledger"] = {"claims": len(claim_by_id)}


def _ids(records: Any, key: str) -> list[Any]:
    if not isinstance(records, list):
        return []
    return [record.get(key) for record in records if isinstance(record, dict)]


def _duplicates(values: list[Any]) -> list[Any]:
    return sorted({value for value in values if value is not None and values.count(value) > 1})


def layout_geometry_record(spec: dict[str, Any], blueprint: dict[str, Any]) -> dict[str, Any]:
    """Build the exact page geometry reviewed by the placeholder proof."""

    composite_size = spec.get("composite", {}).get("size_mm", [])
    if (
        not isinstance(composite_size, list)
        or len(composite_size) != 2
        or not all(isinstance(value, (int, float)) and value > 0 for value in composite_size)
    ):
        raise ValueError("figure_spec.json: composite.size_mm must contain positive numeric width and height")
    width_mm, height_mm = composite_size
    panels = {
        panel.get("id"): panel
        for panel in spec.get("panels", [])
        if isinstance(panel, dict) and panel.get("id")
    }
    raw_placements = spec.get("composite", {}).get("placements", [])
    if not isinstance(raw_placements, list):
        raise ValueError("figure_spec.json: composite placements must be a list")
    placed_panel_ids = [
        placement.get("panel")
        for placement in raw_placements
        if isinstance(placement, dict)
    ]
    if (
        len(raw_placements) != len(panels)
        or len(placed_panel_ids) != len(raw_placements)
        or set(placed_panel_ids) != set(panels)
    ):
        raise ValueError("composite placements must contain every panel exactly once")
    placements: list[dict[str, Any]] = []
    for placement in raw_placements:
        if not isinstance(placement, dict):
            raise ValueError("figure_spec.json: each composite placement must be an object")
        panel_id = placement.get("panel")
        panel = panels.get(panel_id)
        if panel is None:
            raise ValueError(f"figure_spec.json: placement references unknown panel {panel_id}")
        panel_size = panel.get("size_mm", [])
        if not isinstance(panel_size, list) or len(panel_size) != 2:
            raise ValueError(f"figure_spec.json: panel {panel_id} has invalid size_mm")
        resolved = {
            "panel": panel_id,
            "x_mm": placement.get("x_mm"),
            "y_mm": placement.get("y_mm"),
            "w_mm": placement.get("w_mm", panel_size[0]),
            "h_mm": placement.get("h_mm", panel_size[1]),
        }
        numeric_values = [resolved[key] for key in ("x_mm", "y_mm", "w_mm", "h_mm")]
        if not all(isinstance(value, (int, float)) for value in numeric_values):
            raise ValueError(f"figure_spec.json: placement {panel_id} must be numeric")
        if resolved["x_mm"] < 0 or resolved["y_mm"] < 0 or resolved["w_mm"] <= 0 or resolved["h_mm"] <= 0:
            raise ValueError(f"figure_spec.json: placement {panel_id} must be positive and on-page")
        if resolved["x_mm"] + resolved["w_mm"] > width_mm + 0.01 or resolved["y_mm"] + resolved["h_mm"] > height_mm + 0.01:
            raise ValueError(f"figure_spec.json: placement {panel_id} exceeds composite page")
        placements.append(resolved)
    return {
        "schema_version": "1.2",
        "figure_id": spec.get("figure_id"),
        "blueprint_revision": blueprint.get("blueprint_revision"),
        "composite_size_mm": composite_size,
        "placements": placements,
    }


def _validate_blueprint(
    blueprint: dict[str, Any],
    spec: dict[str, Any],
    ledger: dict[str, Any],
    source_manifest: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    checks: dict[str, Any],
) -> None:
    revision = blueprint.get("blueprint_revision")
    if not isinstance(revision, int) or revision < 1:
        errors.append("layout_blueprint.json: blueprint_revision must be a positive integer")
    for key in ("question", "narrative_job", "decision_unlocked", "layout_rationale"):
        if not isinstance(blueprint.get(key), str) or not blueprint[key].strip():
            errors.append(f"layout_blueprint.json: {key} must be non-empty")

    spec_ids = _ids(spec.get("panels"), "id")
    ledger_ids = _ids(ledger.get("panels"), "id")
    blueprint_ids = _ids(blueprint.get("panels"), "id")
    source_ids = _ids(source_manifest.get("panels"), "panel_id")
    if _duplicates(blueprint_ids):
        errors.append(f"layout_blueprint.json: duplicate panel IDs {_duplicates(blueprint_ids)}")
    if set(blueprint_ids) != set(spec_ids) or set(blueprint_ids) != set(ledger_ids) or set(blueprint_ids) != set(source_ids):
        errors.append(
            "panel IDs differ across figure specification, content ledger, layout blueprint, and source-data manifest"
        )

    groups = blueprint.get("groups", [])
    group_ids = _ids(groups, "id")
    if _duplicates(group_ids):
        errors.append(f"layout_blueprint.json: duplicate group IDs {_duplicates(group_ids)}")
    group_id_set = set(group_ids)
    reading_path = blueprint.get("reading_path", [])
    if not isinstance(reading_path, list) or not reading_path:
        errors.append("layout_blueprint.json: reading_path must contain at least one group")
        reading_path = []
    for group_id in reading_path:
        if group_id not in group_id_set:
            errors.append(f"layout_blueprint.json: reading_path references unknown group {group_id}")
    if len(reading_path) != len(set(reading_path)):
        errors.append("layout_blueprint.json: reading_path contains a duplicate group")

    memberships: dict[Any, int] = {panel_id: 0 for panel_id in spec_ids}
    for group in groups if isinstance(groups, list) else []:
        if not isinstance(group, dict):
            errors.append("layout_blueprint.json: each group must be an object")
            continue
        owned = group.get("panels", [])
        if not isinstance(owned, list) or not owned:
            errors.append(f"layout group {group.get('id')}: must own at least one panel")
            continue
        for panel_id in owned:
            if panel_id not in memberships:
                errors.append(f"layout group {group.get('id')}: unknown panel {panel_id}")
            else:
                memberships[panel_id] += 1
    for panel_id, count in memberships.items():
        if count != 1:
            errors.append(f"layout blueprint: panel {panel_id} belongs to {count} groups")

    panel_records = {
        record.get("id"): record
        for record in blueprint.get("panels", [])
        if isinstance(record, dict) and record.get("id") is not None
    }
    for panel_id, panel in panel_records.items():
        group_id = panel.get("group_id")
        if group_id not in group_id_set:
            errors.append(f"layout panel {panel_id}: unknown group {group_id}")
        elif isinstance(groups, list):
            owning_group = next((group for group in groups if group.get("id") == group_id), None)
            if owning_group and panel_id not in owning_group.get("panels", []):
                errors.append(f"layout panel {panel_id}: group_id disagrees with group membership")

    anchor = blueprint.get("visual_anchor", {})
    anchor_id = anchor.get("panel_id") if isinstance(anchor, dict) else None
    if anchor_id not in set(spec_ids):
        errors.append(f"layout blueprint: visual anchor references unknown panel {anchor_id}")
    anchor_priorities = [
        panel_id for panel_id, panel in panel_records.items() if panel.get("priority") == "anchor"
    ]
    if len(anchor_priorities) != 1 or anchor_priorities[0] != anchor_id:
        errors.append("layout blueprint: exactly one priority anchor must match visual_anchor.panel_id")

    scale_ids = set(_ids(blueprint.get("shared_scale_groups", []), "id"))
    for panel_id, panel in panel_records.items():
        scale_id = panel.get("shared_scale_group")
        if scale_id is not None and scale_id not in scale_ids:
            errors.append(f"layout panel {panel_id}: unknown shared-scale group {scale_id}")
        legend_owner = panel.get("legend_owner")
        if legend_owner is not None and legend_owner not in set(spec_ids):
            errors.append(f"layout panel {panel_id}: unknown legend owner {legend_owner}")

    geometry = None
    try:
        geometry = layout_geometry_record(spec, blueprint)
    except ValueError as error:
        errors.append(str(error))
    placement_boxes = (
        [(placement["w_mm"], placement["h_mm"]) for placement in geometry["placements"]]
        if geometry is not None
        else []
    )
    if len(placement_boxes) >= 4 and len(set(placement_boxes)) == 1:
        rationale = blueprint.get("uniform_size_rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            warnings.append(
                "mechanical-grid risk: four or more equal-sized panels require a scientific uniform_size_rationale"
            )

    checks["layout_blueprint"] = {
        "blueprint_revision": revision,
        "panel_ids": blueprint_ids,
        "reading_path": reading_path,
        "visual_anchor": anchor_id,
        "geometry": geometry,
    }


def validate_flowcharts(
    root: Path,
    spec: dict[str, Any],
    ledger: dict[str, Any],
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Cross-check semantic flowcharts against claims and visible elements."""

    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}
    panel_by_id = {
        panel.get("id"): panel
        for panel in spec.get("panels", [])
        if isinstance(panel, dict) and panel.get("id")
    }
    method_panel_ids = {
        panel_id
        for panel_id, panel in panel_by_id.items()
        if panel.get("panel_kind") in METHOD_KINDS
    }
    flowchart_path = root / "flowchart_spec.json"
    if not method_panel_ids and not flowchart_path.exists():
        return errors, warnings, checks
    if not flowchart_path.is_file():
        return [
            "flowchart_spec.json is required when a panel is flowchart, method, or model_architecture"
        ], warnings, checks
    try:
        payload = json.loads(flowchart_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"flowchart_spec.json: cannot read valid JSON: {error}"], warnings, checks
    if payload.get("schema_version") != "1.2":
        errors.append("flowchart_spec.json: schema_version must be 1.2")
    if payload.get("figure_id") != spec.get("figure_id"):
        errors.append("flowchart_spec.json: figure_id must match figure_spec.json")

    claims = {
        claim.get("id"): claim
        for claim in ledger.get("claims", [])
        if isinstance(claim, dict) and claim.get("id")
    }
    flowcharts = payload.get("flowcharts", [])
    if not isinstance(flowcharts, list) or not flowcharts:
        errors.append("flowchart_spec.json: flowcharts must contain at least one semantic diagram")
        flowcharts = []
    flowchart_ids = _ids(flowcharts, "flowchart_id")
    if _duplicates(flowchart_ids):
        errors.append(f"flowchart_spec.json: duplicate flowchart IDs {_duplicates(flowchart_ids)}")
    owner_ids = _ids(flowcharts, "panel_id")
    if _duplicates(owner_ids):
        errors.append(f"flowchart_spec.json: more than one flowchart owns panel(s) {_duplicates(owner_ids)}")
    if set(owner_ids) != method_panel_ids:
        errors.append(
            "flowchart_spec.json: owning panel IDs must exactly match flowchart, method, and model_architecture panels"
        )

    diagram_checks = []
    for flowchart in flowcharts:
        if not isinstance(flowchart, dict):
            errors.append("flowchart_spec.json: each flowchart must be an object")
            continue
        flowchart_id = flowchart.get("flowchart_id")
        owner_id = flowchart.get("panel_id")
        prefix = f"flowchart {flowchart_id}"
        panel = panel_by_id.get(owner_id)
        if panel is None:
            errors.append(f"{prefix}: unknown owning panel {owner_id}")
            continue
        if panel.get("panel_kind") not in METHOD_KINDS:
            errors.append(f"{prefix}: panel {owner_id} is not method-like")
        elements = {
            element.get("id"): element
            for element in panel.get("elements", [])
            if isinstance(element, dict) and element.get("id")
        }
        visible_arrows = {
            element_id
            for element_id, element in elements.items()
            if element.get("type") == "arrow"
        }

        stages = flowchart.get("stages", [])
        edges = flowchart.get("edges", [])
        formulas = flowchart.get("formulas", [])
        if not isinstance(stages, list) or not stages:
            errors.append(f"{prefix}: stages must contain at least one stage")
            stages = []
        if not isinstance(edges, list):
            errors.append(f"{prefix}: edges must be a list")
            edges = []
        if not isinstance(formulas, list):
            errors.append(f"{prefix}: formulas must be a list")
            formulas = []
        stage_ids = _ids(stages, "id")
        edge_ids = _ids(edges, "id")
        formula_ids = _ids(formulas, "id")
        for label, values in (("stage", stage_ids), ("edge", edge_ids), ("formula", formula_ids)):
            duplicates = _duplicates(values)
            if duplicates:
                errors.append(f"{prefix}: duplicate {label} IDs {duplicates}")
        stage_id_set = set(stage_ids)
        formula_id_set = set(formula_ids)
        formula_reference_counts = {formula_id: 0 for formula_id in formula_ids}

        for formula in formulas:
            if not isinstance(formula, dict):
                errors.append(f"{prefix}: each formula must be an object")
                continue
            formula_id = formula.get("id")
            formula_prefix = f"{prefix} formula {formula_id}"
            for key in ("expression", "meaning"):
                if not isinstance(formula.get(key), str) or not formula[key].strip():
                    errors.append(f"{formula_prefix}: {key} must be non-empty")
            variables = formula.get("variables")
            if not isinstance(variables, (dict, list)) or not variables:
                errors.append(f"{formula_prefix}: variables must define every displayed symbol")
            source_anchor = formula.get("source_anchor")
            if source_anchor not in claims:
                errors.append(f"{formula_prefix}: unknown claim {source_anchor}")

        for stage_record in stages:
            if not isinstance(stage_record, dict):
                errors.append(f"{prefix}: each stage must be an object")
                continue
            stage_id = stage_record.get("id")
            stage_prefix = f"{prefix} stage {stage_id}"
            if not stage_record.get("semantic_role") or not stage_record.get("label"):
                errors.append(f"{stage_prefix}: semantic_role and label are required")
            content_anchor = stage_record.get("content_anchor")
            if content_anchor not in claims:
                errors.append(f"{stage_prefix}: unknown claim {content_anchor}")
            _validate_visual_references(
                stage_prefix,
                stage_record.get("visual_element_ids"),
                elements,
                errors,
            )
            for formula_id in stage_record.get("formula_refs", []):
                if formula_id not in formula_id_set:
                    errors.append(f"{stage_prefix}: unknown formula {formula_id}")
                else:
                    formula_reference_counts[formula_id] += 1
            pictogram = stage_record.get("pictogram")
            if not isinstance(pictogram, dict):
                errors.append(f"{stage_prefix}: pictogram record is required")
            else:
                for key in ("kind", "meaning", "evidence_status", "source_anchor"):
                    if not pictogram.get(key):
                        errors.append(f"{stage_prefix}: pictogram.{key} is required")
                pictogram_status = pictogram.get("evidence_status")
                if pictogram_status not in EVIDENCE_STATUSES:
                    errors.append(
                        f"{stage_prefix}: pictogram.evidence_status must be one of {sorted(EVIDENCE_STATUSES)}"
                    )
                pictogram_anchor = pictogram.get("source_anchor")
                anchor_claim = claims.get(pictogram_anchor)
                if anchor_claim is None:
                    errors.append(
                        f"{stage_prefix}: pictogram references unknown claim {pictogram_anchor}"
                    )
                elif pictogram_status in EVIDENCE_STATUSES and not evidence_status_compatible(
                    pictogram_status,
                    anchor_claim.get("evidence_status"),
                ):
                    errors.append(
                        f"{stage_prefix}: pictogram evidence status {pictogram_status!r} is incompatible with anchored claim {pictogram_anchor} status {anchor_claim.get('evidence_status')!r}"
                    )

        arrow_coverage = {arrow_id: 0 for arrow_id in visible_arrows}
        for edge in edges:
            if not isinstance(edge, dict):
                errors.append(f"{prefix}: each edge must be an object")
                continue
            edge_id = edge.get("id")
            edge_prefix = f"{prefix} edge {edge_id}"
            for endpoint_key in ("from", "to"):
                endpoint = edge.get(endpoint_key)
                if endpoint not in stage_id_set:
                    errors.append(f"{edge_prefix}: unknown endpoint {endpoint}")
            role = edge.get("role")
            line_style = edge.get("line_style")
            if role not in SOLID_EDGE_ROLES | DASHED_EDGE_ROLES:
                errors.append(f"{edge_prefix}: invalid semantic role {role!r}")
            elif role in SOLID_EDGE_ROLES and line_style != "solid":
                errors.append(f"{edge_prefix}: {role} edge must be solid")
            elif role in DASHED_EDGE_ROLES and line_style != "dashed":
                errors.append(f"{edge_prefix}: {role} edge must be dashed")
            redundancy = edge.get("redundancy")
            if not isinstance(redundancy, list) or not redundancy:
                errors.append(f"{edge_prefix}: requires non-colour redundancy")
            content_anchor = edge.get("content_anchor")
            if content_anchor not in claims:
                errors.append(f"{edge_prefix}: unknown claim {content_anchor}")
            visual_ids = edge.get("visual_element_ids")
            _validate_visual_references(edge_prefix, visual_ids, elements, errors)
            covered_arrow_ids = []
            if isinstance(visual_ids, list):
                for element_id in visual_ids:
                    element = elements.get(element_id)
                    if element and element.get("type") == "arrow":
                        covered_arrow_ids.append(element_id)
                        arrow_coverage[element_id] += 1
                        if element.get("role") != role:
                            errors.append(
                                f"{edge_prefix}: semantic role {role} disagrees with visible arrow {element_id} role {element.get('role')}"
                            )
                        if element.get("line_style", "solid") != line_style:
                            errors.append(
                                f"{edge_prefix}: line_style disagrees with visible arrow {element_id}"
                            )
            if not covered_arrow_ids:
                errors.append(f"{edge_prefix}: must reference at least one visible arrow")

        for formula_id, count in formula_reference_counts.items():
            if count == 0:
                errors.append(f"{prefix}: formula {formula_id} is not referenced by a stage")
        for arrow_id, count in arrow_coverage.items():
            if count == 0:
                errors.append(f"{prefix}: visible arrow {arrow_id} is not covered by a semantic edge")
            elif count != 1:
                errors.append(f"{prefix}: visible arrow {arrow_id} is covered {count} times")
        diagram_checks.append(
            {
                "flowchart_id": flowchart_id,
                "panel_id": owner_id,
                "stages": len(stages),
                "edges": len(edges),
                "formulas": len(formulas),
                "visible_arrows": len(visible_arrows),
            }
        )
    checks["diagrams"] = diagram_checks
    return errors, warnings, checks


def _validate_visual_references(
    owner: str,
    visual_ids: Any,
    elements: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    if not isinstance(visual_ids, list) or not visual_ids:
        errors.append(f"{owner}: visual_element_ids must be non-empty")
        return
    for element_id in visual_ids:
        if element_id not in elements:
            errors.append(f"{owner}: unknown visible element {element_id}")


def _safe_relative_path(value: Any, required_parent: str = "") -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return False
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    if required_parent and (not path.parts or path.parts[0] != required_parent):
        return False
    return True


def is_regular_project_file(root: Path, path_value: str) -> bool:
    """Reject missing files, symlinks, and paths that resolve outside the project."""

    relative = Path(path_value)
    project_root = root.resolve()
    current = project_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return False
    try:
        current.resolve(strict=True).relative_to(project_root)
    except (FileNotFoundError, OSError, ValueError):
        return False
    return current.is_file()


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def validate_source_data(
    root: Path,
    spec: dict[str, Any],
    blueprint: dict[str, Any],
    source_manifest: dict[str, Any],
    asset_manifest: dict[str, Any],
    *,
    stage: str,
    allow_missing_outputs: bool = False,
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate per-panel source-data coverage and portable delivery records."""

    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}
    _find_prohibited_manifest_content(source_manifest, errors)
    datasets = source_manifest.get("datasets", [])
    if not isinstance(datasets, list):
        return ["source_data_manifest.json: datasets must be a list"], warnings, checks
    dataset_ids = _ids(datasets, "id")
    duplicates = _duplicates(dataset_ids)
    if duplicates:
        errors.append(f"source_data_manifest.json: duplicate dataset IDs {duplicates}")
    dataset_by_id = {
        dataset.get("id"): dataset
        for dataset in datasets
        if isinstance(dataset, dict) and dataset.get("id")
    }
    registry = asset_manifest.get("assets", {})
    if not isinstance(registry, dict):
        errors.append("asset_manifest.json: assets must be an object")
        registry = {}
    declared_paths: set[str] = set()

    for dataset in datasets:
        if not isinstance(dataset, dict):
            errors.append("source_data_manifest.json: each dataset must be an object")
            continue
        dataset_id = dataset.get("id")
        prefix = f"dataset {dataset_id}"
        for key in ("id", "title", "description"):
            if not _nonempty(dataset.get(key)):
                errors.append(f"{prefix}: {key} is required")
        kind = dataset.get("kind")
        availability = dataset.get("availability")
        if kind not in SOURCE_KINDS:
            errors.append(f"{prefix}: invalid kind {kind!r}")
        if availability not in SOURCE_AVAILABILITY:
            errors.append(f"{prefix}: invalid availability {availability!r}")
        audiences = dataset.get("audiences")
        if (
            not isinstance(audiences, list)
            or not audiences
            or any(audience not in AUDIENCES for audience in audiences)
        ):
            errors.append(f"{prefix}: audiences must contain author, reviewer, or public")

        if availability == "file":
            path_value = dataset.get("path")
            if not _safe_relative_path(path_value, "source-data") or not str(path_value).startswith(
                "source-data/files/"
            ):
                errors.append(f"{prefix}: unsafe project-relative path {path_value!r}")
            else:
                declared_paths.add(path_value)
                if (root / path_value).exists() and not is_regular_project_file(root, path_value):
                    errors.append(
                        f"{prefix}: path must resolve to a regular non-symlink file within the project"
                    )
                elif not (root / path_value).is_file():
                    errors.append(f"{prefix}: missing file {path_value}")
            portable_format = str(dataset.get("portable_format", "")).upper()
            if portable_format not in PORTABLE_FORMATS:
                errors.append(f"{prefix}: portable_format must be one of {sorted(PORTABLE_FORMATS)}")
            for key in (
                "data_dictionary",
                "variables",
                "conditions",
                "independent_unit",
                "sample_identifiers",
                "transformations",
                "normalizations",
                "exclusions",
                "missing_values",
                "estimates",
                "uncertainty",
            ):
                if not _nonempty(dataset.get(key)):
                    errors.append(f"{prefix}: {key} is required for a file dataset")
            if kind in {"numeric", "structure"}:
                entrypoint = dataset.get("render_entrypoint")
                if not _safe_relative_path(entrypoint, "scripts"):
                    errors.append(f"{prefix}: render_entrypoint must be a safe path beneath scripts/")
                elif (root / entrypoint).exists() and not is_regular_project_file(root, entrypoint):
                    errors.append(
                        f"{prefix}: render_entrypoint must resolve to a regular non-symlink file within the project"
                    )
                elif not (root / entrypoint).is_file():
                    errors.append(f"{prefix}: missing render_entrypoint {entrypoint}")
        elif availability in {"repository", "controlled_access"}:
            if not _nonempty(dataset.get("repository_or_accession")):
                errors.append(f"{prefix}: repository_or_accession is required")
            if "path" in dataset:
                errors.append(f"{prefix}: repository or controlled-access record must not contain a file path")
            if availability == "controlled_access":
                for key in ("access_conditions", "access_route"):
                    if not _nonempty(dataset.get(key)):
                        errors.append(f"{prefix}: {key} is required for controlled_access")
                if _nonempty(dataset.get("access_route")) and not is_public_https_url(
                    dataset.get("access_route")
                ):
                    errors.append(f"{prefix}: access_route must be a public HTTPS URL")
        elif availability == "not_applicable" and not _nonempty(dataset.get("reason")):
            errors.append(f"{prefix}: reason is required for not_applicable")

        if kind == "image":
            for key in sorted(IMAGE_FIELDS):
                if not _nonempty(dataset.get(key)):
                    errors.append(f"{prefix}: {key} is required for image source data")
            if not _nonempty(dataset.get("render_entrypoint")) and not _nonempty(
                dataset.get("render_entrypoint_not_applicable_reason")
            ):
                errors.append(
                    f"{prefix}: render_entrypoint or render_entrypoint_not_applicable_reason is required"
                )

    source_root = root / "source-data" / "files"
    observed_paths = {
        path.relative_to(root).as_posix()
        for path in source_root.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    } if source_root.is_dir() else set()
    for orphan in sorted(observed_paths - declared_paths):
        errors.append(f"source_data_manifest.json: undeclared source-data file {orphan}")

    delivery_outputs = source_manifest.get("delivery_outputs", [])
    if not isinstance(delivery_outputs, list):
        errors.append("source_data_manifest.json: delivery_outputs must be a list")
        delivery_outputs = []
    output_paths: list[str] = []
    mixed_access = any(
        isinstance(dataset, dict) and dataset.get("availability") == "controlled_access"
        for dataset in datasets
    ) or any(
        isinstance(record, dict) and record.get("distribution") == "controlled_access"
        for record in registry.values()
    )
    for index, record in enumerate(delivery_outputs):
        prefix = f"delivery output {index}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        path_value = record.get("path")
        if not _safe_relative_path(path_value, "outputs") or not str(path_value).startswith("outputs/"):
            errors.append(f"{prefix}: unsafe project-relative path {path_value!r}")
        else:
            output_paths.append(path_value)
            if Path(path_value).suffix.lower() not in DELIVERY_OUTPUT_SUFFIXES:
                errors.append(
                    f"{prefix}: output suffix must be one of {sorted(DELIVERY_OUTPUT_SUFFIXES)}"
                )
            if stage == "final" and not allow_missing_outputs:
                if (root / path_value).exists() and not is_regular_project_file(root, path_value):
                    errors.append(
                        f"{prefix}: path must resolve to a regular non-symlink file within the project"
                    )
                elif not (root / path_value).is_file():
                    errors.append(f"{prefix}: missing output file {path_value}")
        audiences = record.get("audiences")
        if (
            not isinstance(audiences, list)
            or not audiences
            or any(audience not in AUDIENCES for audience in audiences)
        ):
            errors.append(f"{prefix}: audiences must contain author, reviewer, or public")
            audiences = []
        content_scope = record.get("content_scope")
        if not _nonempty(content_scope):
            errors.append(f"{prefix}: content_scope is required")
        contains_controlled = record.get("contains_controlled_visual_content")
        if not isinstance(contains_controlled, bool):
            errors.append(f"{prefix}: contains_controlled_visual_content must be boolean")
        elif contains_controlled and any(audience in {"reviewer", "public"} for audience in audiences):
            errors.append(
                f"{prefix}: controlled visual content cannot be authorized for reviewer or public delivery"
            )
        if content_scope == "layout_proof":
            allowed_layout_paths = {
                f"outputs/layout/{spec.get('figure_id')}_layout-proof.svg",
                f"outputs/layout/{spec.get('figure_id')}_layout-proof.png",
            }
            if path_value not in allowed_layout_paths:
                errors.append(f"{prefix}: layout_proof path must use the generated figure-id filename")
        external_audiences = set(audiences) & {"reviewer", "public"}
        if mixed_access and external_audiences and content_scope != "quantitative_only":
            for audience in sorted(external_audiences):
                errors.append(
                    f"mixed-access {audience} output {path_value}: only a source-bound quantitative_only output may be delivered"
                )
        if content_scope == "quantitative_only" and external_audiences:
            if Path(str(path_value)).suffix.lower() not in {".pdf", ".svg"}:
                errors.append(f"{prefix}: quantitative_only external output must be PDF or SVG")
            output_dataset_ids = record.get("dataset_ids")
            if not isinstance(output_dataset_ids, list) or not output_dataset_ids:
                errors.append(f"{prefix}: quantitative_only output requires dataset_ids")
                output_dataset_ids = []
            for dataset_id in output_dataset_ids:
                dataset = dataset_by_id.get(dataset_id)
                if dataset is None:
                    errors.append(f"{prefix}: unknown quantitative dataset {dataset_id}")
                    continue
                if dataset.get("kind") != "numeric" or dataset.get("availability") not in {
                    "file",
                    "repository",
                }:
                    errors.append(
                        f"{prefix}: quantitative dataset {dataset_id} must be reviewer-safe numeric data"
                    )
                for audience in external_audiences:
                    if audience not in dataset.get("audiences", []):
                        errors.append(
                            f"{prefix}: quantitative dataset {dataset_id} is not eligible for {audience}"
                        )
    duplicate_output_paths = _duplicates(output_paths)
    if duplicate_output_paths:
        errors.append(
            f"source_data_manifest.json: duplicate delivery output paths {duplicate_output_paths}"
        )
    if stage == "final" and not delivery_outputs:
        errors.append("source_data_manifest.json: final stage requires declared delivery_outputs")

    panel_records = source_manifest.get("panels", [])
    if not isinstance(panel_records, list):
        errors.append("source_data_manifest.json: panels must be a list")
        panel_records = []
    panel_record_by_id = {
        record.get("panel_id"): record
        for record in panel_records
        if isinstance(record, dict) and record.get("panel_id")
    }
    if _duplicates(_ids(panel_records, "panel_id")):
        errors.append("source_data_manifest.json: duplicate panel coverage records")

    blueprint_by_id = {
        panel.get("id"): panel
        for panel in blueprint.get("panels", [])
        if isinstance(panel, dict) and panel.get("id")
    }
    asset_by_id = spec.get("assets", {})
    required_panels: set[str] = set()
    claim_image_panels: set[str] = set()
    for asset_id, spec_asset in asset_by_id.items():
        if not isinstance(spec_asset, dict):
            continue
        manifest_asset = registry.get(asset_id, {})
        if not isinstance(manifest_asset, dict):
            manifest_asset = {}
        role = spec_asset.get("evidence_role") or manifest_asset.get("evidence_role")
        if role != "claim_supporting":
            continue
        source_dataset_ids = manifest_asset.get("source_dataset_ids")
        if not isinstance(source_dataset_ids, list) or not source_dataset_ids:
            errors.append(f"claim-supporting asset {asset_id}: source_dataset_ids must be non-empty")
            source_dataset_ids = []
        declared_asset_audiences = manifest_asset.get("audiences", [])
        external_audiences = (
            set(declared_asset_audiences) & {"reviewer", "public"}
            if isinstance(declared_asset_audiences, list)
            else set()
        )
        distribution = manifest_asset.get("distribution")
        if distribution in {"shareable", "public"}:
            external_audiences.update({"reviewer", "public"})
        elif distribution == "reviewer":
            external_audiences.add("reviewer")
        for dataset_id in source_dataset_ids:
            dataset = dataset_by_id.get(dataset_id)
            if dataset is None:
                errors.append(f"claim-supporting asset {asset_id}: unknown source dataset {dataset_id}")
                continue
            availability = dataset.get("availability")
            if availability == "not_applicable":
                errors.append(
                    f"claim-supporting asset {asset_id}: cannot use not_applicable source dataset {dataset_id}"
                )
            if external_audiences and availability == "controlled_access":
                errors.append(
                    f"claim-supporting asset {asset_id}: controlled source cannot be externally distributed"
                )
            for audience in sorted(external_audiences):
                if audience not in dataset.get("audiences", []):
                    errors.append(
                        f"claim-supporting asset {asset_id}: source dataset {dataset_id} is not eligible for {audience}"
                    )
    for panel in spec.get("panels", []):
        panel_id = panel.get("id")
        if panel.get("panel_kind") in DATA_PANEL_KINDS:
            required_panels.add(panel_id)
        if blueprint_by_id.get(panel_id, {}).get("source_data_required") is True:
            required_panels.add(panel_id)
        for element in panel.get("elements", []):
            if element.get("type") != "image":
                continue
            asset_id = element.get("asset")
            spec_asset = asset_by_id.get(asset_id, {})
            manifest_asset = registry.get(asset_id, {})
            role = spec_asset.get("evidence_role") or manifest_asset.get("evidence_role")
            if role == "claim_supporting":
                required_panels.add(panel_id)
                claim_image_panels.add(panel_id)

    for panel in spec.get("panels", []):
        panel_id = panel.get("id")
        record = panel_record_by_id.get(panel_id)
        if record is None:
            if panel_id in required_panels:
                errors.append(f"source_data_manifest.json: panel {panel_id} requires source-data coverage")
            continue
        coverage = record.get("coverage")
        if coverage not in {"complete", "partial", "not_applicable"}:
            errors.append(f"source-data panel {panel_id}: invalid coverage {coverage!r}")
        dataset_refs = record.get("dataset_ids", [])
        if not isinstance(dataset_refs, list):
            errors.append(f"source-data panel {panel_id}: dataset_ids must be a list")
            dataset_refs = []
        for dataset_id in dataset_refs:
            dataset = dataset_by_id.get(dataset_id)
            if dataset is None:
                errors.append(f"source-data panel {panel_id}: unknown dataset {dataset_id}")
            elif coverage in {"complete", "partial"} and dataset.get("availability") == "not_applicable":
                errors.append(
                    f"source-data panel {panel_id}: {coverage} coverage cannot use not_applicable dataset {dataset_id}"
                )
        if coverage == "not_applicable":
            if not _nonempty(record.get("reason")):
                errors.append(f"source-data panel {panel_id}: not_applicable requires a reason")
            if dataset_refs:
                errors.append(f"source-data panel {panel_id}: not_applicable must not reference datasets")
            if panel_id in claim_image_panels:
                errors.append(f"claim-supporting image panel {panel_id} cannot be not_applicable")
            elif panel_id in required_panels:
                errors.append(f"panel {panel_id} requires source-data coverage")
        elif panel_id in required_panels and coverage != "complete":
            errors.append(f"panel {panel_id} requires complete source-data coverage")
        elif coverage in {"complete", "partial"}:
            if not dataset_refs:
                errors.append(f"source-data panel {panel_id}: {coverage} coverage requires dataset_ids")
            if not _nonempty(record.get("supports")):
                errors.append(f"source-data panel {panel_id}: supports must identify visible marks or images")

    checks.update(
        {
            "datasets": len(dataset_by_id),
            "declared_files": len(declared_paths),
            "panel_records": len(panel_record_by_id),
            "required_panels": sorted(required_panels),
            "delivery_outputs": len(output_paths),
            "mixed_access": mixed_access,
        }
    )
    return errors, warnings, checks


def _find_prohibited_manifest_content(
    value: Any,
    errors: list[str],
    location: str = "source_data_manifest.json",
    document_name: str = "source_data_manifest.json",
) -> None:
    prohibited_keys = {
        "private_locator",
        "local_path",
        "credential",
        "credentials",
        "password",
        "secret",
        "token",
        "prompt",
        "prompt_record",
        "agent_instruction",
        "approval_record",
        "pipeline_state",
        "automation_trace",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{location}.{key}"
            if str(key).casefold() in prohibited_keys:
                errors.append(f"{document_name}: prohibited private locator or internal field at {child}")
            _find_prohibited_manifest_content(item, errors, child, document_name)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _find_prohibited_manifest_content(
                item,
                errors,
                f"{location}[{index}]",
                document_name,
            )
    elif isinstance(value, str):
        if is_private_locator(value):
            errors.append(f"{document_name}: prohibited private locator at {location}")


def _validate_layout_review(
    root: Path,
    spec: dict[str, Any],
    venue: dict[str, Any],
    blueprint: dict[str, Any],
    errors: list[str],
    checks: dict[str, Any],
) -> None:
    figure_id = spec.get("figure_id")
    proof_stem = root / "outputs" / "layout" / f"{figure_id}_layout-proof"
    if not proof_stem.with_suffix(".svg").is_file() or not proof_stem.with_suffix(".png").is_file():
        errors.append("layout proof is required before final rendering or packaging")
    geometry_receipt_path = root / "qa" / "layout_proof.json"
    expected_geometry = None
    try:
        expected_geometry = layout_geometry_record(spec, blueprint)
    except ValueError as error:
        errors.append(str(error))
    if not geometry_receipt_path.is_file():
        errors.append("qa/layout_proof.json geometry receipt is required at final stage")
        geometry_receipt = None
    elif not is_regular_project_file(root, "qa/layout_proof.json"):
        errors.append("qa/layout_proof.json must be a regular non-symlink file within the project")
        geometry_receipt = None
    else:
        try:
            geometry_receipt = json.loads(geometry_receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"qa/layout_proof.json: cannot read valid JSON: {error}")
            geometry_receipt = None
    if expected_geometry is not None and geometry_receipt != expected_geometry:
        errors.append("stale layout proof geometry: qa/layout_proof.json does not match current page placements")
    review_path = root / "qa" / "layout_review.json"
    if not review_path.is_file():
        errors.append("qa/layout_review.json is required at final stage")
        return
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"qa/layout_review.json: cannot read valid JSON: {error}")
        return
    if review.get("schema_version") != "1.2":
        errors.append("qa/layout_review.json: schema_version must be 1.2")
    if review.get("figure_id") != spec.get("figure_id"):
        errors.append("qa/layout_review.json: figure_id must match figure_spec.json")
    if review.get("status") != "PASS":
        errors.append("layout review must be PASS before final rendering or packaging")
    revision = blueprint.get("blueprint_revision")
    reviewed_revision = review.get("reviewed_blueprint_revision")
    if reviewed_revision != revision:
        errors.append(
            f"stale layout review: reviewed blueprint revision {reviewed_revision!r}, current revision {revision!r}"
        )
    ordered_panel_ids = _ids(blueprint.get("panels"), "id")
    if review.get("ordered_panel_ids") != ordered_panel_ids:
        errors.append("stale layout review: ordered panel IDs do not match layout_blueprint.json")
    selected_width = venue.get("geometry", {}).get("selected_width_mm")
    reviewed_width = review.get("selected_width_mm")
    if (
        not isinstance(reviewed_width, (int, float))
        or not isinstance(selected_width, (int, float))
        or abs(reviewed_width - selected_width) > 0.001
    ):
        errors.append("stale layout review: selected venue width does not match venue_contract.json")
    review_checks = review.get("checks", {})
    required_checks = {
        "question_and_reading_path",
        "anchor_and_hierarchy",
        "grouping_and_whitespace",
        "final_width_allowance",
        "shared_encodings",
        "mechanical_grid_risk",
        "semantic_coverage",
    }
    if not isinstance(review_checks, dict):
        errors.append("qa/layout_review.json: checks must be an object")
        review_checks = {}
    for check_id in sorted(required_checks):
        value = review_checks.get(check_id)
        if not isinstance(value, str) or value.upper() != "PASS":
            errors.append(f"layout review check {check_id} must be PASS")
    checks["layout_review"] = {
        "status": review.get("status"),
        "reviewed_blueprint_revision": reviewed_revision,
        "ordered_panel_ids": review.get("ordered_panel_ids"),
        "selected_width_mm": reviewed_width,
        "geometry_receipt": "current" if geometry_receipt == expected_geometry else "stale_or_missing",
    }


def declared_source_files(
    root: Path,
    source_manifest: dict[str, Any],
    *,
    audience: str,
) -> list[Path]:
    """Return existing, declared source-data files eligible for an audience."""

    if audience not in AUDIENCES:
        raise ValueError(f"unknown source-data audience {audience!r}")
    result: list[Path] = []
    for dataset in source_manifest.get("datasets", []):
        if not isinstance(dataset, dict) or audience not in dataset.get("audiences", []):
            continue
        if dataset.get("availability") == "file":
            path_value = dataset.get("path")
            if not _safe_relative_path(path_value, "source-data") or not str(path_value).startswith(
                "source-data/files/"
            ):
                raise ValueError(f"dataset {dataset.get('id')}: unsafe project-relative path {path_value!r}")
            path = root / path_value
            if not is_regular_project_file(root, path_value):
                raise ValueError(
                    f"dataset {dataset.get('id')}: path must resolve to a regular non-symlink file within the project"
                )
            result.append(path)
        entrypoint = dataset.get("render_entrypoint")
        if entrypoint:
            if not _safe_relative_path(entrypoint, "scripts"):
                raise ValueError(
                    f"dataset {dataset.get('id')}: render_entrypoint must be a safe path beneath scripts/"
                )
            script_path = root / entrypoint
            if not is_regular_project_file(root, entrypoint):
                raise ValueError(
                    f"dataset {dataset.get('id')}: render_entrypoint must resolve to a regular non-symlink file within the project"
                )
            result.append(script_path)
    return sorted(set(result))


def declared_output_files(
    root: Path,
    source_manifest: dict[str, Any],
    *,
    audience: str,
) -> list[Path]:
    """Return existing figure outputs explicitly authorized for one audience."""

    if audience not in AUDIENCES:
        raise ValueError(f"unknown delivery audience {audience!r}")
    result: list[Path] = []
    substantive = 0
    records = source_manifest.get("delivery_outputs", [])
    if not isinstance(records, list):
        raise ValueError("source_data_manifest.json: delivery_outputs must be a list")
    for index, record in enumerate(records):
        if not isinstance(record, dict) or audience not in record.get("audiences", []):
            continue
        path_value = record.get("path")
        if not _safe_relative_path(path_value, "outputs") or not str(path_value).startswith("outputs/"):
            raise ValueError(f"delivery output {index}: unsafe project-relative path {path_value!r}")
        if Path(path_value).suffix.lower() not in DELIVERY_OUTPUT_SUFFIXES:
            raise ValueError(
                f"delivery output {index}: output suffix must be one of {sorted(DELIVERY_OUTPUT_SUFFIXES)}"
            )
        if record.get("contains_controlled_visual_content") is not False and audience in {
            "reviewer",
            "public",
        }:
            raise ValueError(
                f"delivery output {index}: reviewer/public output must explicitly exclude controlled visual content"
            )
        path = root / path_value
        if not is_regular_project_file(root, path_value):
            raise ValueError(
                f"delivery output {index}: path must resolve to a regular non-symlink file within the project"
            )
        result.append(path)
        if record.get("content_scope") != "layout_proof":
            substantive += 1
    if audience in {"reviewer", "public"} and substantive == 0:
        raise ValueError(
            f"{audience} delivery requires at least one explicitly authorized substantive figure output"
        )
    return sorted(set(result))
