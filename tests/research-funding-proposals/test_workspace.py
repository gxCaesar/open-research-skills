import csv
from datetime import date
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "writing-funding-proposals"
SCRIPTS = SKILL / "scripts"
INIT = SCRIPTS / "init_proposal_workspace.py"
VALIDATE = SCRIPTS / "validate_proposal_workspace.py"
AUDIT = SCRIPTS / "audit_chinese_prose.py"
SNAPSHOT_AS_OF = "2024-02-29"


def load_synthetic_workspace():
    helper_path = SKILL / "examples" / "synthetic_workspace.py"
    spec = importlib.util.spec_from_file_location("synthetic_workspace", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load synthetic workspace helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


populate_complete_workspace = load_synthetic_workspace().populate_complete_workspace


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def run_final(root: Path, *, as_of: str = SNAPSHOT_AS_OF, json_output: bool = True) -> subprocess.CompletedProcess:
    args = [str(root), "--mode", "final", "--as-of", as_of]
    if json_output:
        args.append("--json")
    return run_script(VALIDATE, *args)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_source_register(root: Path):
    source_path = root / "authority" / "source-register.csv"
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("source register has no header")
        return source_path, reader.fieldnames, list(reader)


def replace_source_rows(root: Path, updates, appended_rows=()) -> None:
    source_path, source_fields, source_rows = read_source_register(root)
    seen = set()
    for row in source_rows:
        if row["source_id"] in updates:
            row.update(updates[row["source_id"]])
            seen.add(row["source_id"])
    missing = set(updates) - seen
    if missing:
        raise ValueError(f"source rows missing: {sorted(missing)}")
    source_rows.extend(appended_rows)
    write_csv(source_path, source_fields, source_rows)


def stale_wrong_context_source(source_id: str) -> dict:
    return {
        "source_id": source_id,
        "issuer": "Synthetic stale issuer",
        "year": "1900",
        "program": "other-program",
        "source_type": "unrelated source",
        "url_or_path": "https://example.org/stale-unrelated",
        "accessed_on": "1900-01-01",
        "clause_locator": "obsolete section",
        "status": "VERIFIED",
        "scope": "unrelated",
        "data_classification": "PUBLIC",
        "search_query": "",
    }


class FundingWorkspaceTest(unittest.TestCase):
    def init_workspace(self, root: Path) -> subprocess.CompletedProcess:
        return run_script(
            INIT,
            str(root),
            "--project-id",
            "synthetic-grant",
            "--program",
            "nsfc",
            "--year",
            "2026",
            "--project-type",
            "general",
        )
    def populate_complete_workspace(self, root: Path, budget_required: bool = False) -> None:
        populate_complete_workspace(root, budget_required)

    def test_init_creates_human_facing_workspace_and_working_validation_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            created = self.init_workspace(root)
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            expected = [
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
            for relative in expected:
                with self.subTest(relative=relative):
                    self.assertTrue((root / relative).is_file())
            result = run_script(VALIDATE, str(root), "--mode", "working", "--json")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("PASS_WITH_WARNINGS", report["status"])
            self.assertGreater(len(report["warnings"]), 0)

    def test_fresh_workspace_fails_final_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            report = json.loads(result.stdout)
            self.assertEqual("FAIL", report["status"])
            self.assertTrue(any("official template" in item.lower() for item in report["errors"]))

    def test_initializer_marks_bundled_policy_as_working_only_until_live_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            policy = read_json(root / "project.json")["authoring_policy"]
            self.assertEqual("VERIFIED_PROFILE", policy["status"])
            self.assertEqual([], policy.get("source_ids"))
            self.assertEqual("UNVERIFIED", policy.get("checked_on"))
            self.assertEqual("authoring_policy", policy.get("scope"))
            self.assertEqual([], policy.get("coverage"))
            self.assertIs(False, policy.get("live_refresh_completed"))
            self.assertEqual("UNVERIFIED", policy.get("live_refresh_id"))
            self.assertEqual("UNVERIFIED", policy.get("live_refresh_completed_on"))
            self.assertEqual([], policy.get("source_bindings"))

    def test_complete_synthetic_workspace_passes_final_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            result = run_final(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("PASS", report["status"])
            self.assertEqual("record_completeness", report["validation_scope"])

    def test_complete_final_text_output_reports_record_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)

            result = run_script(
                VALIDATE, str(root), "--mode", "final", "--as-of", SNAPSHOT_AS_OF
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "Status: PASS | mode=final | as_of=2024-02-29 | validation_scope=record_completeness",
                result.stdout,
            )

    def test_final_mode_rejects_bundled_verified_profile_without_live_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            project_path = root / "project.json"
            project = read_json(project_path)
            project["authoring_policy"]["status"] = "VERIFIED_PROFILE"
            write_json(project_path, project)
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("authoring policy must be VERIFIED", result.stdout)

    def test_final_authoring_policy_requires_current_covered_refresh_record(self):
        cases = [
            ("source_ids", [], "authoring policy requires source_ids"),
            ("source_ids", ["MISSING"], "authoring policy source MISSING is not VERIFIED"),
            ("checked_on", "not-a-date", "authoring policy checked_on must be a valid ISO date"),
            ("scope", "scientific evidence", "authoring policy scope must be authoring_policy"),
            ("coverage", ["funder"], "authoring policy coverage must include funder and institution"),
            ("live_refresh_completed", False, "authoring policy live refresh must be completed"),
        ]
        for field, value, expected in cases:
            with self.subTest(field=field, value=value):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "proposal"
                    self.assertEqual(0, self.init_workspace(root).returncode)
                    self.populate_complete_workspace(root)
                    project_path = root / "project.json"
                    project = read_json(project_path)
                    project["authoring_policy"][field] = value
                    write_json(project_path, project)
                    result = run_final(root)
                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stdout)

    def test_final_authoring_policy_binds_each_source_to_coverage_and_live_refresh(self):
        cases = [
            ("source_coverage", "authoring policy source bindings must cover funder and institution"),
            ("binding_program", "authoring policy binding SRC1 program must match project program"),
            ("source_year", "authoring policy source SRC1 year must match project target_year"),
            ("source_scope", "authoring policy source SRC3 scope must match policy scope"),
            ("source_checked_on", "authoring policy source SRC1 accessed_on must match binding checked_on"),
            ("stale_refresh", "authoring policy checked_on must match completed live refresh"),
            ("noncurrent_refresh", "authoring policy binding SRC1 is not part of the completed live refresh"),
        ]
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "proposal"
                    self.assertEqual(0, self.init_workspace(root).returncode)
                    self.populate_complete_workspace(root)
                    project_path = root / "project.json"
                    project = read_json(project_path)
                    source_path = root / "authority" / "source-register.csv"
                    with source_path.open("r", encoding="utf-8", newline="") as handle:
                        reader = csv.DictReader(handle)
                        source_fields = reader.fieldnames
                        source_rows = list(reader)
                    self.assertIsNotNone(source_fields)
                    if mutation == "source_coverage":
                        project["authoring_policy"]["source_bindings"][1]["authority_kind"] = "funder"
                    elif mutation == "binding_program":
                        project["authoring_policy"]["source_bindings"][0]["program"] = "guangdong"
                    elif mutation == "source_year":
                        source_rows[0]["year"] = "2025"
                    elif mutation == "source_scope":
                        source_rows[2]["scope"] = "scientific evidence"
                    elif mutation == "source_checked_on":
                        source_rows[0]["accessed_on"] = "2025-01-01"
                    elif mutation == "stale_refresh":
                        project["authoring_policy"]["checked_on"] = "1900-01-01"
                    elif mutation == "noncurrent_refresh":
                        project["authoring_policy"]["source_bindings"][0]["live_refresh_id"] = "OLD-REFRESH"
                    write_json(project_path, project)
                    write_csv(source_path, source_fields, source_rows)
                    result = run_final(root)
                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stdout)

    def test_final_authoring_policy_requires_distinct_source_authority_kinds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            project_path = root / "project.json"
            project = read_json(project_path)
            policy = project["authoring_policy"]
            single_binding = dict(policy["source_bindings"][0])
            single_binding["coverage"] = ["funder", "institution"]
            policy["source_ids"] = ["SRC1"]
            policy["coverage"] = ["funder", "institution"]
            policy["source_bindings"] = [single_binding]
            write_json(project_path, project)
            result = run_script(VALIDATE, str(root), "--mode", "final", "--json")
            self.assertEqual(1, result.returncode)
            self.assertIn("authoring policy source bindings must cover funder and institution", result.stdout)

    def test_final_authoring_policy_rejects_cloned_evidence_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            source_path = root / "authority" / "source-register.csv"
            with source_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                source_fields = reader.fieldnames
                source_rows = list(reader)
            self.assertIsNotNone(source_fields)
            source_by_id = {row["source_id"]: row for row in source_rows}
            for field in ("issuer", "source_type", "url_or_path", "clause_locator"):
                source_by_id["SRC3"][field] = source_by_id["SRC1"][field]
            write_csv(source_path, source_fields, source_rows)

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "authoring policy funder and institution bindings must not reuse evidence identity",
                result.stdout,
            )

    def test_final_authoring_policy_allows_joint_document_with_distinct_clause_locators(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            source_path = root / "authority" / "source-register.csv"
            with source_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                source_fields = reader.fieldnames
                source_rows = list(reader)
            self.assertIsNotNone(source_fields)
            source_by_id = {row["source_id"]: row for row in source_rows}
            for field in ("issuer", "source_type", "url_or_path"):
                source_by_id["SRC3"][field] = source_by_id["SRC1"][field]
            self.assertNotEqual(
                source_by_id["SRC1"]["clause_locator"],
                source_by_id["SRC3"]["clause_locator"],
            )
            write_csv(source_path, source_fields, source_rows)

            result = run_final(root)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_final_authoring_policy_requires_dates_equal_as_of(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            project_path = root / "project.json"
            project = read_json(project_path)
            policy = project["authoring_policy"]
            policy["checked_on"] = "1900-01-01"
            policy["live_refresh_completed_on"] = "1900-01-01"
            for binding in policy["source_bindings"]:
                binding["checked_on"] = "1900-01-01"
                binding["coverage"] = [binding["authority_kind"]]
            write_json(project_path, project)
            source_path = root / "authority" / "source-register.csv"
            with source_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                source_fields = reader.fieldnames
                source_rows = list(reader)
            self.assertIsNotNone(source_fields)
            for row in source_rows:
                if row["source_id"] in {"SRC1", "SRC3"}:
                    row["accessed_on"] = "1900-01-01"
            write_csv(source_path, source_fields, source_rows)
            result = run_script(VALIDATE, str(root), "--mode", "final", "--json")
            self.assertEqual(1, result.returncode)
            report = json.loads(result.stdout)
            self.assertEqual(date.today().isoformat(), report["as_of"])
            self.assertTrue(
                any("must equal as_of" in error for error in report["errors"]),
                report,
            )

    def test_historical_as_of_override_is_explicit_and_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            json_result = run_final(root)
            self.assertEqual(0, json_result.returncode, json_result.stdout + json_result.stderr)
            self.assertEqual(SNAPSHOT_AS_OF, json.loads(json_result.stdout)["as_of"])
            text_result = run_final(root, json_output=False)
            self.assertEqual(0, text_result.returncode, text_result.stdout + text_result.stderr)
            self.assertIn(f"as_of={SNAPSHOT_AS_OF}", text_result.stdout)

    def test_project_program_and_year_follow_initializer_contract(self):
        cases = [
            ("program", "not-a-program", "project.json: invalid program"),
            ("target_year", "not-a-year", "project.json: invalid target_year"),
        ]
        for field, invalid_value, expected in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "proposal"
                    self.assertEqual(0, self.init_workspace(root).returncode)
                    self.populate_complete_workspace(root)
                    project_path = root / "project.json"
                    project = read_json(project_path)
                    project[field] = invalid_value
                    binding_field = "program" if field == "program" else "year"
                    for binding in project["authoring_policy"]["source_bindings"]:
                        binding[binding_field] = invalid_value
                    write_json(project_path, project)
                    source_path, source_fields, source_rows = read_source_register(root)
                    for row in source_rows:
                        row[binding_field] = str(invalid_value)
                    write_csv(source_path, source_fields, source_rows)

                    result = run_final(root)

                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stdout)

    def test_final_official_authority_requires_current_context_bound_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            project_path = root / "project.json"
            project = read_json(project_path)
            project["official_authority"]["source_ids"] = ["SRC6"]
            project["official_authority"]["last_checked"] = "1900-01-01"
            write_json(project_path, project)
            replace_source_rows(root, {}, [stale_wrong_context_source("SRC6")])

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "official authority source SRC6 program must match project program", result.stdout
            )

    def test_final_official_template_requires_current_context_bound_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            replace_source_rows(
                root,
                {
                    "SRC2": {
                        "year": "1900",
                        "program": "other-program",
                        "source_type": "unrelated source",
                        "accessed_on": "1900-01-01",
                        "scope": "unrelated",
                    }
                },
            )

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "official template source SRC2 program must match project program", result.stdout
            )

    def test_final_official_template_binds_local_artifact_to_registered_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            replace_source_rows(root, {"SRC2": {"url_or_path": "delivery/other-template.pdf"}})

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "official template artifact_path must match local source url_or_path", result.stdout
            )

    def test_final_official_template_rejects_path_outside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            outside_path = Path(tmp) / "outside-template.pdf"
            outside_path.write_bytes(b"synthetic outside template fixture")
            project_path = root / "project.json"
            project = read_json(project_path)
            project["official_template"]["artifact_path"] = "../outside-template.pdf"
            write_json(project_path, project)
            replace_source_rows(
                root,
                {"SRC2": {"url_or_path": "../outside-template.pdf"}},
            )

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "official template artifact_path must name an in-workspace regular file",
                result.stdout,
            )

    def test_final_rendered_and_figure_artifacts_stay_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            for name in ("outside-master.svg", "outside-figure.pdf", "outside-final.pdf"):
                (Path(tmp) / name).write_bytes(b"synthetic outside artifact")
            figure_path = root / "figures" / "figure-plan.csv"
            with figure_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                figure_fields = reader.fieldnames
                figure_rows = list(reader)
            self.assertIsNotNone(figure_fields)
            figure_rows[0]["editable_master"] = "../outside-master.svg"
            figure_rows[0]["rendered_output"] = "../outside-figure.pdf"
            write_csv(figure_path, figure_fields, figure_rows)
            delivery_path = root / "delivery" / "final-format.json"
            delivery = read_json(delivery_path)
            delivery["rendered_artifact"] = "../outside-final.pdf"
            write_json(delivery_path, delivery)

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn("editable_master must name an in-workspace regular file", result.stdout)
            self.assertIn("rendered_output must name an in-workspace regular file", result.stdout)
            self.assertIn(
                "final rendered_artifact must name an in-workspace regular file",
                result.stdout,
            )

    def test_final_financial_budget_requirement_requires_current_context_bound_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root, budget_required=True)
            budget_path = root / "budget" / "financial-budget.json"
            budget = read_json(budget_path)
            budget["requirement"].update(
                {
                    "source_ids": ["SRC6"],
                    "checked_on": "1900-01-01",
                    "scope": "unrelated",
                }
            )
            write_json(budget_path, budget)
            replace_source_rows(root, {}, [stale_wrong_context_source("SRC6")])

            result = run_final(root)

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "financial budget requirement checked_on must equal as_of", result.stdout
            )

    def test_final_required_budget_rejects_missing_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root, budget_required=True)
            (root / "budget" / "financial-budget.json").unlink()
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            report = json.loads(result.stdout)
            self.assertEqual("record_completeness", report["validation_scope"])
            self.assertIn("missing required file: budget/financial-budget.json", report["errors"])

    def test_missing_required_file_text_output_reports_record_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root, budget_required=True)
            (root / "budget" / "financial-budget.json").unlink()

            result = run_script(VALIDATE, str(root), "--mode", "final")

            self.assertEqual(1, result.returncode)
            self.assertIn(
                "NOTE validation_scope=record_completeness: file format, rendering, and visual quality are not checked",
                result.stdout,
            )

    def test_final_required_budget_rejects_incomplete_or_unbalanced_record(self):
        cases = [
            ("requirement.required", "UNVERIFIED", "financial budget requirement must declare required as true or false"),
            ("budget_method", "", "financial budget requires budget_method"),
            ("source_ids", [], "financial budget requires source_ids"),
            ("annual_allocations", [{"year": "2026", "amount": 119}], "financial budget annual allocations must total total_amount"),
            ("category_allocations", [{"category": "custom synthetic resource", "amount": 119}], "financial budget category allocations must total total_amount"),
            ("task_resource_linkages", [], "financial budget requires task_resource_linkages"),
        ]
        for field, value, expected in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "proposal"
                    self.assertEqual(0, self.init_workspace(root).returncode)
                    self.populate_complete_workspace(root, budget_required=True)
                    budget_path = root / "budget" / "financial-budget.json"
                    budget = read_json(budget_path)
                    if field.startswith("requirement."):
                        budget["requirement"][field.split(".", 1)[1]] = value
                    else:
                        budget[field] = value
                    write_json(budget_path, budget)
                    result = run_final(root)
                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stdout)

    def test_final_required_budget_allows_profile_defined_category_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root, budget_required=True)
            result = run_final(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_final_commitment_records_allow_distinct_artifact_classes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            result = run_final(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_final_commitment_records_reject_missing_critical_fields(self):
        cases = [
            ("primary_class", "", "commitment record CM1: missing primary_class"),
            ("finite_bound", "", "commitment record CM1: missing finite_bound"),
            ("stop_rule", "", "commitment record CM1: missing stop_rule"),
            ("dependencies", None, "commitment record CM1: dependencies must be a list"),
            ("sequence", None, "commitment record CM1: sequence must be a positive integer"),
        ]
        for field, value, expected in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "proposal"
                    self.assertEqual(0, self.init_workspace(root).returncode)
                    self.populate_complete_workspace(root)
                    commitments_path = root / "commitments" / "commitment-records.json"
                    commitments = read_json(commitments_path)
                    record = commitments["records"][0]
                    if field == "dependencies":
                        record.pop(field)
                    else:
                        record[field] = value
                    write_json(commitments_path, commitments)
                    result = run_final(root)
                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stdout)

    def test_final_commitment_records_reject_nonpreceding_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            commitments_path = root / "commitments" / "commitment-records.json"
            commitments = read_json(commitments_path)
            commitments["records"][1]["sequence"] = 1
            write_json(commitments_path, commitments)
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("commitment record CM2: dependency CM1 must precede it", result.stdout)

    def test_final_commitment_records_reject_missing_output_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            commitments_path = root / "commitments" / "commitment-records.json"
            commitments = read_json(commitments_path)
            commitments["records"] = [
                record
                for record in commitments["records"]
                if record["artifact_type"] != "output"
            ]
            write_json(commitments_path, commitments)
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("final mode requires commitment records for outputs: ['O1']", result.stdout)

    def test_isolated_skill_copy_initializes_and_validates_a_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolated_skill = Path(tmp) / "writing-funding-proposals"
            shutil.copytree(SKILL, isolated_skill)
            root = Path(tmp) / "proposal"
            created = run_script(
                isolated_skill / "scripts" / "init_proposal_workspace.py",
                str(root),
                "--project-id",
                "isolated-copy",
                "--program",
                "other",
                "--year",
                "2030",
                "--project-type",
                "synthetic",
            )
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(
                isolated_skill / "scripts" / "validate_proposal_workspace.py",
                str(root),
                "--mode",
                "working",
                "--json",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_chinese_section_completeness_uses_visible_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "known-good"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            (root / "sections" / "rationale.md").write_text(
                "# 立项依据\n\n"
                "本项目围绕真实临床样本中的机制差异开展研究，"
                "通过预先定义的对照和独立验证边界检验核心科学问题。\n",
                encoding="utf-8",
            )
            result = run_final(root)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "known-bad"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            (root / "sections" / "rationale.md").write_text(
                "# 立项依据\n\n很短。\n", encoding="utf-8"
            )
            result = run_final(root)
            self.assertEqual(1, result.returncode)
            self.assertIn("section rationale remains an incomplete brief", result.stdout)

    def test_broken_claim_source_reference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            ledger = root / "evidence" / "claim-ledger.csv"
            text = ledger.read_text(encoding="utf-8").replace("SRC1,synthetic test only", "MISSING,synthetic test only")
            ledger.write_text(text, encoding="utf-8")
            result = run_script(VALIDATE, str(root), "--mode", "working", "--json")
            self.assertEqual(1, result.returncode)
            self.assertIn("unknown source_id", result.stdout)

    def test_incomplete_discriminating_validation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proposal"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_complete_workspace(root)
            argument_path = root / "argument" / "argument-map.json"
            argument = read_json(argument_path)
            argument["validations"][0]["failure_criterion"] = ""
            write_json(argument_path, argument)
            result = run_script(VALIDATE, str(root), "--mode", "working", "--json")
            self.assertEqual(1, result.returncode)
            self.assertIn("failure_criterion", result.stdout)

    def test_prose_audit_reports_surface_risks_without_authorship_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "draft.md"
            draft.write_text("首先，本项目将实现国际领先的突破；其次，形成平台；最后，全面推广。", encoding="utf-8")
            result = run_script(AUDIT, str(draft), "--json")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            codes = {item["code"] for item in report["findings"]}
            self.assertIn("PROMOTIONAL_CLAIM", codes)
            self.assertIn("FORMULAIC_SEQUENCE", codes)
            rendered = json.dumps(report, ensure_ascii=False).lower()
            self.assertNotIn("ai-generated", rendered)
            self.assertNotIn("ai generated", rendered)


if __name__ == "__main__":
    unittest.main()
