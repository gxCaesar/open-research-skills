#!/usr/bin/env python3
"""Create a portable, human-facing research-proposal workspace."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
import shutil
from typing import Dict, Iterable


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_ROOT / "assets" / "templates"
PROGRAMS = {"nsfc", "guangdong", "other"}


CSV_TEMPLATES = {
    "source-register.csv": "authority/source-register.csv",
    "claim-ledger.csv": "evidence/claim-ledger.csv",
    "figure-plan.csv": "figures/figure-plan.csv",
    "review-findings.csv": "reviews/review-findings.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a public research-funding proposal workspace."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--program", choices=sorted(PROGRAMS), required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--project-type", required=True)
    return parser.parse_args()


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def ensure_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if len(rows) != 1 or not rows[0]:
        raise SystemExit(f"invalid public CSV template: {path.name}")


def copy_templates(root: Path, mapping: Dict[str, str]) -> None:
    for source_name, target_name in mapping.items():
        source = TEMPLATES / source_name
        if source.suffix == ".csv":
            ensure_header(source)
        target = root / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def policy_for(program: str, year: int) -> dict:
    if program == "nsfc" and year == 2026:
        return {
            "status": "VERIFIED_PROFILE",
            "mode": "EVIDENCE_AND_AUDIT_ONLY",
            "profile": "references/profiles/nsfc-2026.md",
            "reason": (
                "The checked 2026 notice prohibits directly AI-generated applications "
                "and unverified generated content."
            ),
            "live_refresh_required": True,
            "source_ids": [],
            "checked_on": "UNVERIFIED",
            "scope": "authoring_policy",
            "coverage": [],
            "live_refresh_completed": False,
            "live_refresh_id": "UNVERIFIED",
            "live_refresh_completed_on": "UNVERIFIED",
            "source_bindings": [],
        }
    return {
        "status": "UNVERIFIED",
        "mode": "EVIDENCE_AND_AUDIT_ONLY",
        "profile": (
            "references/profiles/guangdong-2026.md"
            if program == "guangdong" and year == 2026
            else "UNVERIFIED"
        ),
        "reason": "Current program and institutional authoring rules have not been verified.",
        "live_refresh_required": True,
        "source_ids": [],
        "checked_on": "UNVERIFIED",
        "scope": "authoring_policy",
        "coverage": [],
        "live_refresh_completed": False,
        "live_refresh_id": "UNVERIFIED",
        "live_refresh_completed_on": "UNVERIFIED",
        "source_bindings": [],
    }


def create_sections(root: Path, names: Iterable[str]) -> None:
    template = (TEMPLATES / "section-brief.md").read_text(encoding="utf-8")
    for name in names:
        rendered = template.replace("{{SECTION_ID}}", name).replace(
            "{{SECTION_NAME}}", name.title()
        )
        (root / "sections" / f"{name}.md").write_text(rendered, encoding="utf-8")


def main() -> None:
    args = parse_args()
    if not args.project_id.strip():
        raise SystemExit("--project-id must not be empty")
    if not 2000 <= args.year <= 2100:
        raise SystemExit("--year must be between 2000 and 2100")

    root = args.output.resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"refusing to initialize non-empty directory: {root}")
    root.mkdir(parents=True, exist_ok=True)
    for relative in [
        "authority",
        "evidence",
        "topic",
        "argument",
        "sections",
        "figures",
        "reviews",
        "delivery",
        "budget",
        "commitments",
    ]:
        (root / relative).mkdir(parents=True, exist_ok=True)

    project = {
        "schema_version": 1,
        "project_id": args.project_id,
        "program": args.program,
        "target_year": args.year,
        "project_type": args.project_type,
        "confidentiality": "APPLICANT_PRIVATE",
        "official_authority": {
            "status": "UNVERIFIED",
            "source_ids": [],
            "last_checked": "UNVERIFIED",
        },
        "authoring_policy": policy_for(args.program, args.year),
        "official_template": {
            "status": "UNVERIFIED",
            "source_id": "UNVERIFIED",
            "artifact_path": "",
        },
        "applicant_review_status": "UNVERIFIED",
        "route_status": "UNFROZEN",
        "external_submission_status": "NOT_RUN",
        "initialized_on": date.today().isoformat(),
    }
    write_json(root / "project.json", project)
    copy_templates(root, CSV_TEMPLATES)
    copy_templates(
        root,
        {
            "candidate-portfolio.json": "topic/candidate-portfolio.json",
            "argument-map.json": "argument/argument-map.json",
            "final-format.json": "delivery/final-format.json",
            "financial-budget.json": "budget/financial-budget.json",
            "commitment-records.json": "commitments/commitment-records.json",
        },
    )
    create_sections(root, ["rationale", "contents", "foundation"])
    shutil.copyfile(TEMPLATES / "START_HERE.md", root / "START_HERE.md")

    print(f"PASS: initialized public proposal workspace: {root}")
    print(
        "Authoring mode: "
        f"{project['authoring_policy']['mode']} "
        f"({project['authoring_policy']['status']})"
    )


if __name__ == "__main__":
    main()
