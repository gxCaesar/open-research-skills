"""Populate the archived, synthetic record-completeness workspace used by the demo."""

import csv
import json
from pathlib import Path


SNAPSHOT_AS_OF = "2024-02-29"


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_csv(path: Path, fieldnames: list, rows: list) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def populate_complete_workspace(root: Path, budget_required: bool = False) -> None:
    """Write a deliberately synthetic final-mode fixture to an initialized workspace."""
    project_path = root / "project.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project.update(
        {
            "official_authority": {
                "status": "VERIFIED",
                "source_ids": ["SRC4"],
                "last_checked": SNAPSHOT_AS_OF,
            },
            "official_template": {
                "status": "VERIFIED",
                "source_id": "SRC2",
                "artifact_path": "delivery/official-template.pdf",
            },
            "applicant_review_status": "VERIFIED",
            "route_status": "FROZEN",
            "authoring_policy": {
                "status": "VERIFIED",
                "mode": "EVIDENCE_AND_AUDIT_ONLY",
                "profile": "synthetic",
                "reason": "Synthetic fixture policy record.",
                "live_refresh_required": True,
                "source_ids": ["SRC1", "SRC3"],
                "checked_on": SNAPSHOT_AS_OF,
                "scope": "authoring_policy",
                "coverage": ["funder", "institution"],
                "live_refresh_completed": True,
                "live_refresh_id": "SYNTHETIC-LIVE-REFRESH",
                "live_refresh_completed_on": SNAPSHOT_AS_OF,
                "source_bindings": [
                    {
                        "source_id": "SRC1",
                        "authority_kind": "funder",
                        "program": "nsfc",
                        "year": 2026,
                        "scope": "authoring_policy",
                        "checked_on": SNAPSHOT_AS_OF,
                        "live_refresh_id": "SYNTHETIC-LIVE-REFRESH",
                    },
                    {
                        "source_id": "SRC3",
                        "authority_kind": "institution",
                        "program": "nsfc",
                        "year": 2026,
                        "scope": "authoring_policy",
                        "checked_on": SNAPSHOT_AS_OF,
                        "live_refresh_id": "SYNTHETIC-LIVE-REFRESH",
                    },
                ],
            },
        }
    )
    write_json(project_path, project)
    (root / "delivery" / "official-template.pdf").write_bytes(
        b"synthetic template fixture"
    )

    source_fields = [
        "source_id", "issuer", "year", "program", "source_type", "url_or_path",
        "accessed_on", "clause_locator", "status", "scope", "data_classification",
        "search_query",
    ]
    sources = [
        ("SRC1", "Synthetic funder", "funder authoring policy", "https://example.org/notice", "section 1", "authoring_policy"),
        ("SRC2", "Synthetic funder", "official template", "delivery/official-template.pdf", "complete artifact", "official_template"),
        ("SRC3", "Synthetic host institution", "institutional authoring policy", "https://example.org/institution-policy", "section 2", "authoring_policy"),
        ("SRC4", "Synthetic funder", "official authority", "https://example.org/authority", "section 3", "official_authority"),
        ("SRC5", "Synthetic funder", "financial budget requirement", "https://example.org/budget-requirement", "section 4", "financial_budget_requirement"),
    ]
    write_csv(
        root / "authority" / "source-register.csv",
        source_fields,
        [
            {
                "source_id": source_id,
                "issuer": issuer,
                "year": "2026",
                "program": "nsfc",
                "source_type": source_type,
                "url_or_path": url_or_path,
                "accessed_on": SNAPSHOT_AS_OF,
                "clause_locator": clause_locator,
                "status": "VERIFIED",
                "scope": scope,
                "data_classification": "PUBLIC",
                "search_query": "",
            }
            for source_id, issuer, source_type, url_or_path, clause_locator, scope in sources
        ],
    )
    write_csv(
        root / "evidence" / "claim-ledger.csv",
        ["claim_id", "section", "claim_text", "claim_type", "source_id", "source_scope", "verification_status", "applicant_role", "last_verified", "notes"],
        [{
            "claim_id": "CL1", "section": "rationale",
            "claim_text": "Synthetic prior evidence supports a bounded premise.",
            "claim_type": "literature", "source_id": "SRC1",
            "source_scope": "synthetic test only", "verification_status": "VERIFIED",
            "applicant_role": "NOT_APPLICABLE", "last_verified": "2026-09-04",
            "notes": "fixture",
        }],
    )
    write_json(
        root / "topic" / "candidate-portfolio.json",
        {
            "schema_version": 1,
            "candidates": [{
                "candidate_id": "T1",
                "scientific_question": "Can mechanism M distinguish outcome Y?",
                "contribution_lane": "sota-method",
                "data_feasibility": "VERIFIED",
                "linked_sample_variables": "X and Y coexist in each synthetic unit",
                "independent_unit": "synthetic subject",
                "nearest_work": "Synthetic baseline",
                "delta_from_nearest_work": "Tests mechanism M under a matched protocol",
                "strongest_cheap_baseline": "Synthetic linear baseline",
                "discriminating_validation": "Paired comparison on held-out subjects",
                "failure_criterion": "Reframe if the paired margin is not positive",
                "scoop_verdict": "ADJACENT", "disposition": "TASK",
                "disposition_action": "RECOMMEND", "program_fit": "VERIFIED",
                "evidence_source_ids": ["SRC1"],
            }],
            "topic_decision": {
                "status": "VERIFIED", "selected_candidate_id": "T1",
                "route_status": "FROZEN", "route_or_code": "synthetic route",
                "applicant_confirmation": "VERIFIED",
            },
        },
    )
    write_json(
        root / "argument" / "argument-map.json",
        {
            "schema_version": 1,
            "project_goal": "Test a bounded synthetic mechanism claim.",
            "questions": [{"id": "Q1", "text": "Does mechanism M distinguish Y?", "content_ids": ["C1"], "validation_ids": ["V1"]}],
            "contents": [{
                "id": "C1", "question_ids": ["Q1"],
                "data_or_object": "Synthetic paired observations",
                "method_or_mechanism": "Mechanism M", "validation_ids": ["V1"],
                "output_ids": ["O1"], "prior_claim_ids": ["CL1"], "figure_ids": ["F1"],
            }],
            "validations": [{
                "id": "V1", "comparison": "Mechanism M versus the synthetic baseline",
                "independent_unit": "synthetic subject",
                "evaluation_boundary": "held-out synthetic subjects",
                "failure_criterion": "The paired margin is not positive",
                "action_on_failure": "Reframe the mechanism claim",
            }],
            "outputs": [{"id": "O1", "text": "Paired estimate with uncertainty", "acceptance_evidence": "validated result table"}],
            "figures": [{"id": "F1", "rhetorical_job": "Show the discriminating comparison", "body_anchor": "contents paragraph 2"}],
            "dependencies": [{"predecessor_id": "CL1", "successor_id": "C1", "required_evidence": "bounded premise", "status": "VERIFIED"}],
        },
    )
    for name in ("rationale", "contents", "foundation"):
        (root / "sections" / f"{name}.md").write_text(
            "# {0}\n\nApplicant-authored synthetic text linked to Q1, C1, V1, O1, CL1, and F1.\n".format(name.title()),
            encoding="utf-8",
        )
    write_csv(
        root / "figures" / "figure-plan.csv",
        ["figure_id", "class", "rhetorical_job", "body_anchor", "claim_ids", "source_ids", "editable_master", "rendered_output", "qa_status"],
        [{
            "figure_id": "F1", "class": "main", "rhetorical_job": "Show the discriminating comparison",
            "body_anchor": "contents paragraph 2", "claim_ids": "CL1", "source_ids": "SRC1",
            "editable_master": "figures/F1.svg", "rendered_output": "figures/F1.pdf", "qa_status": "PASS",
        }],
    )
    (root / "figures" / "F1.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L1 1"/></svg>', encoding="utf-8"
    )
    (root / "figures" / "F1.pdf").write_bytes(b"synthetic figure fixture")
    write_csv(
        root / "reviews" / "review-findings.csv",
        ["issue_id", "pass_id", "severity", "exact_location", "strongest_falsifier", "required_evidence", "cheapest_revision", "resolution_status", "resolution_evidence"],
        [
            {"issue_id": "R1-0", "pass_id": "R1_FATAL", "severity": "note", "exact_location": "whole draft", "strongest_falsifier": "none found in fixture", "required_evidence": "source and policy audit", "cheapest_revision": "none", "resolution_status": "NOT_APPLICABLE", "resolution_evidence": "synthetic fixture review"},
            {"issue_id": "R2-0", "pass_id": "R2_SCIENCE", "severity": "note", "exact_location": "whole draft", "strongest_falsifier": "none found in fixture", "required_evidence": "argument audit", "cheapest_revision": "none", "resolution_status": "NOT_APPLICABLE", "resolution_evidence": "synthetic fixture review"},
            {"issue_id": "R3-0", "pass_id": "R3_READABILITY", "severity": "note", "exact_location": "whole draft", "strongest_falsifier": "none found in fixture", "required_evidence": "rendered read", "cheapest_revision": "none", "resolution_status": "NOT_APPLICABLE", "resolution_evidence": "synthetic fixture review"},
        ],
    )
    delivery_path = root / "delivery" / "final-format.json"
    delivery = json.loads(delivery_path.read_text(encoding="utf-8"))
    delivery.update({
        "rendered_artifact": "delivery/final.pdf", "build_status": "PASS",
        "visual_review_status": "PASS", "applicant_confirmation": "VERIFIED",
        "external_submission_status": "NOT_RUN",
    })
    write_json(delivery_path, delivery)
    (root / "delivery" / "final.pdf").write_bytes(b"synthetic rendered fixture")

    budget = {
        "schema_version": 1,
        "requirement": {"status": "VERIFIED", "required": budget_required, "source_ids": ["SRC5"], "checked_on": SNAPSHOT_AS_OF, "scope": "financial_budget_requirement"},
        "budget_method": "", "source_ids": [], "total_amount": None,
        "annual_allocations": [], "category_allocations": [], "task_resource_linkages": [],
    }
    if budget_required:
        budget.update({
            "budget_method": "Synthetic activity-based allocation", "source_ids": ["SRC5"], "total_amount": 120,
            "annual_allocations": [{"year": "2026", "amount": 120}],
            "category_allocations": [{"category": "custom synthetic resource", "amount": 120}],
            "task_resource_linkages": [{"task_id": "C1", "resource": "Synthetic research resource", "amount": 120}],
        })
    write_json(root / "budget" / "financial-budget.json", budget)
    write_json(
        root / "commitments" / "commitment-records.json",
        {"schema_version": 1, "records": [
            {"record_id": "CM1", "artifact_type": "research_content", "artifact_id": "C1", "primary_class": "deliverable mainline", "finite_bound": "One bounded held-out validation cycle.", "stop_rule": "Stop after the registered validation cycle.", "dependencies": [], "sequence": 1},
            {"record_id": "CM2", "artifact_type": "annual_task", "artifact_id": "AT1", "linked_content_ids": ["C1"], "primary_class": "boundary confirmation", "finite_bound": "One prespecified feasibility decision.", "stop_rule": "Do not begin dependent work after a no-go decision.", "dependencies": ["CM1"], "sequence": 2},
            {"record_id": "CM3", "artifact_type": "output", "artifact_id": "O1", "primary_class": "cautious exploration", "finite_bound": "One bounded output assessment.", "stop_rule": "Retain the negative result without expanding scope.", "dependencies": ["CM2"], "sequence": 3},
        ]},
    )
