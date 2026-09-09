import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "research-publication-pipeline"
INIT = SKILL / "scripts" / "init_publication_project.py"
VALIDATE = SKILL / "scripts" / "validate_publication_project.py"
DEMO = SKILL / "examples" / "run_demo.py"
sys.path.insert(0, str(SKILL / "examples"))

from synthetic_workspace import PUBLIC_RELEASE_FILES, populate_ready_workspace as populate_synthetic_workspace


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class PublicationWorkspaceTest(unittest.TestCase):
    def test_copied_skill_runs_complete_synthetic_demo(self):
        """The independently installed skill includes a runnable complete synthetic case."""
        with tempfile.TemporaryDirectory() as tmp:
            copied_skill = Path(tmp) / "research-publication-pipeline"
            output = Path(tmp) / "synthetic-demo-output"
            shutil.copytree(SKILL, copied_skill)

            result = run_script(copied_skill / "examples" / "run_demo.py", str(output))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("SYNTHETIC DEMO ONLY", result.stdout)
            self.assertTrue(output.is_dir())
            for target in ("pilot", "development", "handoff"):
                self.assertIn(f"{target}: PASS", result.stdout)

    def test_demo_preserves_existing_output_and_validator_rejects_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied_skill = Path(tmp) / "research-publication-pipeline"
            output = Path(tmp) / "synthetic-demo-output"
            shutil.copytree(SKILL, copied_skill)
            demo = copied_skill / "examples" / "run_demo.py"
            self.assertEqual(0, run_script(demo, str(output)).returncode)
            project_path = output / "project.json"
            original_project = project_path.read_text(encoding="utf-8")
            sentinel = output / "do-not-overwrite.txt"
            sentinel.write_text("keep", encoding="utf-8")

            existing = run_script(demo, str(output))
            self.assertEqual(1, existing.returncode)
            self.assertEqual(original_project, project_path.read_text(encoding="utf-8"))
            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))

            in_skill = copied_skill / "generated-demo"
            contained = run_script(demo, str(in_skill))
            self.assertEqual(1, contained.returncode)
            self.assertFalse(in_skill.exists())

            sources_path = output / "evidence" / "source-register.json"
            sources = read_json(sources_path)
            sources["sources"] = [
                source for source in sources["sources"] if source["source_id"] != "S_RESULT"
            ]
            write_json(sources_path, sources)
            invalid = run_script(
                copied_skill / "scripts" / "validate_publication_project.py",
                str(output),
                "--target",
                "handoff",
                "--format",
                "json",
            )
            self.assertEqual(1, invalid.returncode, invalid.stdout + invalid.stderr)
            findings = json.loads(invalid.stdout)["findings"]
            self.assertIn("CLAIM_EVIDENCE", {item["rule_id"] for item in findings})

    def init_workspace(self, root: Path) -> subprocess.CompletedProcess:
        return run_script(
            INIT,
            str(root),
            "--project-id",
            "synthetic-publication",
            "--title",
            "A synthetic mechanism study",
            "--domain",
            "single-cell",
            "--contribution-lane",
            "sota-method",
        )

    def populate_ready_workspace(self, root: Path, public_release: bool = False) -> None:
        populate_synthetic_workspace(root, public_release)


    def validate(self, root: Path, target: str) -> subprocess.CompletedProcess:
        return run_script(VALIDATE, str(root), "--target", target, "--format", "json")

    def test_init_creates_workspace_and_working_validation_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            created = self.init_workspace(root)
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            expected = [
                "START_HERE.md",
                "project.json",
                "evidence/source-register.json",
                "intake/intake.json",
                "protocol/protocol.json",
                "development/headroom.json",
                "development/iteration-ledger.json",
                "claims/claim-register.json",
                "handoff/handoff.json",
            ]
            for relative in expected:
                with self.subTest(relative=relative):
                    self.assertTrue((root / relative).is_file())
            result = self.validate(root, "working")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual("PASS_WITH_WARNINGS", report["status"])
            self.assertGreater(len(report["warnings"]), 0)

    def test_initializer_refuses_to_overwrite_nonempty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            root.mkdir()
            (root / "keep.txt").write_text("user material", encoding="utf-8")
            result = self.init_workspace(root)
            self.assertEqual(1, result.returncode)
            self.assertEqual("user material", (root / "keep.txt").read_text(encoding="utf-8"))

    def test_fresh_workspace_fails_pilot_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            result = self.validate(root, "pilot")
            self.assertEqual(1, result.returncode)
            rules = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
            self.assertIn("DATA_FEASIBILITY", rules)
            self.assertIn("SCOOP_VERDICT", rules)
            self.assertIn("VENUE_FIT", rules)

    def test_complete_synthetic_project_passes_intake_development_and_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            for target in ["pilot", "development", "handoff"]:
                with self.subTest(target=target):
                    result = self.validate(root, target)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_scoop_judgment_must_match_contribution_lane(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            intake_path = root / "intake" / "intake.json"
            intake = read_json(intake_path)
            intake["scoop"]["contribution_lane"] = "benchmark"
            write_json(intake_path, intake)
            result = self.validate(root, "pilot")
            self.assertEqual(1, result.returncode)
            self.assertIn("SCOOP_LANE", result.stdout)

    def test_development_rejects_unsealed_locked_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            protocol_path = root / "protocol" / "protocol.json"
            protocol = read_json(protocol_path)
            protocol["locked_test"]["status"] = "OPENED"
            protocol["locked_test"]["accesses_used"] = 1
            write_json(protocol_path, protocol)
            result = self.validate(root, "development")
            self.assertEqual(1, result.returncode)
            self.assertIn("LOCKED_TEST", result.stdout)

    def test_protocol_cannot_silently_change_contribution_lane(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            protocol_path = root / "protocol" / "protocol.json"
            protocol = read_json(protocol_path)
            protocol["contribution_lane"] = "benchmark"
            write_json(protocol_path, protocol)
            result = self.validate(root, "development")
            self.assertEqual(1, result.returncode)
            self.assertIn("CONTRIBUTION_LANE", result.stdout)

    def test_architecture_cannot_skip_lower_construction_rungs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            ledger_path = root / "development" / "iteration-ledger.json"
            ledger = read_json(ledger_path)
            ledger["registered_candidates"][0]["rung"] = "architecture"
            write_json(ledger_path, ledger)
            result = self.validate(root, "development")
            self.assertEqual(1, result.returncode)
            self.assertIn("CONSTRUCTION_ORDER", result.stdout)

    def test_two_predicted_slice_misses_forbid_another_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            ledger_path = root / "development" / "iteration-ledger.json"
            ledger = read_json(ledger_path)
            ledger["cycles"] = [
                {
                    "cycle_id": "cycle-001",
                    "candidate_id": "C1",
                    "rung": "objective_alignment",
                    "status": "COMPLETED",
                    "predicted_slice_met": False,
                    "matched_control_status": "PASS",
                    "ablation_status": "PASS",
                    "mechanism_status": "FALSIFIED",
                    "decision": "REVISE",
                    "stop_reason": "NOT_APPLICABLE",
                    "locked_test_accessed": False,
                    "observed": [{"statement": "slice floor missed", "locator": "results/cycle-001.json"}],
                    "failed": [],
                    "not_run": [],
                    "inferred": ["candidate C1 remains uncertain after one miss"],
                },
                {
                    "cycle_id": "cycle-002",
                    "candidate_id": "C1",
                    "rung": "objective_alignment",
                    "status": "COMPLETED",
                    "predicted_slice_met": False,
                    "matched_control_status": "PASS",
                    "ablation_status": "PASS",
                    "mechanism_status": "FALSIFIED",
                    "decision": "REVISE",
                    "stop_reason": "NOT_APPLICABLE",
                    "locked_test_accessed": False,
                    "observed": [{"statement": "slice floor missed again", "locator": "results/cycle-002.json"}],
                    "failed": [],
                    "not_run": [],
                    "inferred": ["candidate C1 is falsified on its predicted slice"],
                },
            ]
            write_json(ledger_path, ledger)
            result = self.validate(root, "development")
            self.assertEqual(1, result.returncode)
            self.assertIn("MECHANISM_RECOVERY", result.stdout)

    def test_open_headroom_budget_and_untried_candidate_forbid_route_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            ledger_path = root / "development" / "iteration-ledger.json"
            ledger = read_json(ledger_path)
            ledger["cycles"] = [
                {
                    "cycle_id": "cycle-001",
                    "candidate_id": "C1",
                    "rung": "objective_alignment",
                    "status": "COMPLETED",
                    "predicted_slice_met": False,
                    "matched_control_status": "PASS",
                    "ablation_status": "PASS",
                    "mechanism_status": "FALSIFIED",
                    "decision": "STOP",
                    "stop_reason": "EXHAUSTED_BUDGET",
                    "locked_test_accessed": False,
                    "observed": [{"statement": "candidate C1 missed its slice", "locator": "results/cycle-001.json"}],
                    "failed": [],
                    "not_run": ["registered candidate C2"],
                    "inferred": ["C1 does not explain the predicted slice"],
                }
            ]
            write_json(ledger_path, ledger)
            result = self.validate(root, "development")
            self.assertEqual(1, result.returncode)
            rules = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
            self.assertIn("ROUTE_CLOSURE", rules)
            self.assertIn("MECHANISM_RECOVERY", rules)

    def test_handoff_rejects_included_result_claim_without_result_locator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root)
            claims_path = root / "claims" / "claim-register.json"
            claims = read_json(claims_path)
            claims["claims"][0]["result_locators"] = []
            write_json(claims_path, claims)
            result = self.validate(root, "handoff")
            self.assertEqual(1, result.returncode)
            self.assertIn("CLAIM_EVIDENCE", result.stdout)

    def test_public_release_accepts_complete_curated_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            clean = self.validate(root, "public-release")
            self.assertEqual(0, clean.returncode, clean.stdout + clean.stderr)
            self.assertEqual("PASS", json.loads(clean.stdout)["status"])

    def test_public_release_rejects_inline_contamination_after_real_rehearsal(self):
        """A real rehearsed release must fail on each independently added disclosure."""
        contaminations = {
            "mac_path": "Private source: /" + "Users/synthetic-reviewer/private-study/data.csv",
            "linux_path": "Private source: /" + "home/synthetic-reviewer/private-study/data.csv",
            "windows_path": "Private source: C:\\" + "Users\\synthetic-reviewer\\data.csv",
            "state": "Internal record: pipeline_state=ready",
            "receipt": 'Internal record: {"approval_receipt": "synthetic-only"}',
            "command": "After download, run " + "sha" + "256sum artifact.zip",
            "alternate_command": "Run " + "sha" + "sum -a 256 artifact.zip",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            demo = run_script(DEMO, str(root), "--with-public-release")
            self.assertEqual(0, demo.returncode, demo.stdout + demo.stderr)
            for relative in ("README.md", "LICENSE"):
                artifact = root / "public-release" / relative
                original = artifact.read_text(encoding="utf-8")
                for name, contamination in contaminations.items():
                    with self.subTest(artifact=relative, contamination=name):
                        artifact.write_text(original + "\n" + contamination + "\n", encoding="utf-8")
                        result = self.validate(root, "public-release")
                        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                        self.assertIn("PUBLIC_RELEASE_CONTENT", result.stdout)
                        self.assertNotIn(contamination, result.stdout + result.stderr)
                artifact.write_text(original, encoding="utf-8")
            self.assertEqual(0, self.validate(root, "public-release").returncode)

    def test_public_release_rejects_declared_integrity_sidecars(self):
        """Allowlisting a verification sidecar as documentation must not bypass scanning."""
        names = ("check" + "sums.txt", "SHA" + "256SUMS", "artifact." + "sha" + "256")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            handoff_path = root / "handoff" / "handoff.json"
            original = read_json(handoff_path)
            for name in names:
                with self.subTest(sidecar=name):
                    relative = "docs/" + name
                    sidecar = root / "public-release" / relative
                    sidecar.write_text("synthetic integrity side record\n", encoding="utf-8")
                    handoff = json.loads(json.dumps(original))
                    handoff["public_release"]["allowlist"].append(relative)
                    handoff["public_release"]["artifact_paths"]["expected_outputs"].append(relative)
                    write_json(handoff_path, handoff)
                    result = self.validate(root, "public-release")
                    sidecar.unlink()
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("PUBLIC_RELEASE_CONTENT", result.stdout)

    def test_public_release_preserves_code_urls_and_dependency_metadata(self):
        """The disclosure scan must not prohibit scientific links or ordinary code names."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            release = root / "public-release"
            source = release / "src" / "example.py"
            source.write_text(source.read_text(encoding="utf-8") + "\npipeline_state = {}\napproval_receipt = None\n", encoding="utf-8")
            readme = release / "README.md"
            scholarly_links = "https://example.org/" + "home/researcher/article and https://example.org/" + "Users/researcher/paper"
            readme.write_text(readme.read_text(encoding="utf-8") + "\nSee " + scholarly_links + ". The pipeline_state identifier is part of the example API.\n", encoding="utf-8")
            lock = release / "package-lock.json"
            write_json(lock, {"lockfileVersion": 3, "packages": {"node_modules/example": {"integrity": "sha512-synthetic-service-metadata"}}})
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append(lock.name)
            handoff["public_release"]["artifact_paths"]["dependency_spec"].append(lock.name)
            write_json(handoff_path, handoff)
            result = self.validate(root, "public-release")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_public_release_accepts_an_explicit_configuration_artifact(self):
        """A legitimate public config must not be mislabeled as source or rejected."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            config = root / "public-release" / "configs" / "train.yaml"
            config.parent.mkdir(parents=True)
            config.write_text("seed: 7\n", encoding="utf-8")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append("configs/train.yaml")
            handoff["public_release"]["artifact_paths"]["configuration"] = [
                "configs/train.yaml"
            ]
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_public_release_rejects_readme_only_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            for relative in PUBLIC_RELEASE_FILES:
                if relative != "README.md":
                    (root / "public-release" / relative).unlink()
            result = self.validate(root, "public-release")
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("PUBLIC_RELEASE_ARTIFACT", result.stdout)

    def test_public_release_rejects_each_missing_artifact_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            handoff_path = root / "handoff" / "handoff.json"
            complete = read_json(handoff_path)
            for category in complete["public_release"]["artifact_paths"]:
                with self.subTest(category=category):
                    handoff = json.loads(json.dumps(complete))
                    del handoff["public_release"]["artifact_paths"][category]
                    write_json(handoff_path, handoff)
                    result = self.validate(root, "public-release")
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("PUBLIC_RELEASE_ARTIFACT", result.stdout)

    def test_public_release_rejects_unallowlisted_extra_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            (root / "public-release" / "extra-notes.md").write_text("extra\n", encoding="utf-8")
            result = self.validate(root, "public-release")
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("PUBLIC_RELEASE_ALLOWLIST", result.stdout)

    def test_public_release_rejects_allowlisted_file_without_public_artifact_role(self):
        """Break caught: a renamed internal review record can hide as an allowlisted extra."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            extra = root / "public-release" / "release-audit.json"
            extra.write_text('{"status": "internal review"}\n', encoding="utf-8")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append("release-audit.json")
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("PUBLIC_RELEASE_ARTIFACT", result.stdout)

    def test_public_release_rejects_one_readme_mislabeled_as_every_artifact(self):
        """Break caught: category keys alone do not prove a runnable research release."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            for relative in PUBLIC_RELEASE_FILES:
                if relative != "README.md":
                    (root / "public-release" / relative).unlink()
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"] = ["README.md"]
            for category in handoff["public_release"]["artifact_paths"]:
                handoff["public_release"]["artifact_paths"][category] = ["README.md"]
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("PUBLIC_RELEASE_ARTIFACT", result.stdout)

    def test_public_release_rejects_each_incomplete_rehearsal_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            handoff_path = root / "handoff" / "handoff.json"
            complete = read_json(handoff_path)

            def set_status(record):
                record["public_release"]["rehearsal"]["status"] = "NOT_RUN"

            def clear_date(record):
                record["public_release"]["rehearsal"]["checked_on"] = ""

            def clear_environment(record):
                record["public_release"]["rehearsal"]["environment"] = ""

            def clear_commands(record):
                record["public_release"]["rehearsal"]["commands"] = []

            def set_failed_exit(record):
                record["public_release"]["rehearsal"]["commands"][0]["exit_code"] = 1

            def clear_observed_outputs(record):
                record["public_release"]["rehearsal"]["commands"][0]["observed_outputs"] = []

            for name, mutate in (
                ("status", set_status),
                ("checked_on", clear_date),
                ("environment", clear_environment),
                ("commands", clear_commands),
                ("exit_code", set_failed_exit),
                ("observed_outputs", clear_observed_outputs),
            ):
                with self.subTest(field=name):
                    handoff = json.loads(json.dumps(complete))
                    mutate(handoff)
                    write_json(handoff_path, handoff)
                    result = self.validate(root, "public-release")
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("PUBLIC_RELEASE_REHEARSAL", result.stdout)

    def test_public_release_rejects_control_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            (root / "public-release" / "pipeline-state.json").write_text("{}\n", encoding="utf-8")
            dirty = self.validate(root, "public-release")
            self.assertEqual(1, dirty.returncode)
            self.assertIn("PUBLIC_RELEASE_CONTENT", dirty.stdout)

    def test_public_release_rejects_declared_nested_repository_metadata(self):
        """Break caught: allowlisting and classifying .git/config used to certify it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            nested = root / "public-release" / ".git" / "config"
            nested.parent.mkdir()
            nested.write_text("synthetic repository metadata\n", encoding="utf-8")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append(".git/config")
            handoff["public_release"]["artifact_paths"]["data_instructions"].append(
                ".git/config"
            )
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode)
            self.assertIn("PUBLIC_RELEASE_CONTENT", result.stdout)

    def test_public_release_rejects_declared_agent_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            instruction = root / "public-release" / "AGENTS.md"
            instruction.write_text("synthetic agent instructions\n", encoding="utf-8")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append("AGENTS.md")
            handoff["public_release"]["artifact_paths"]["data_instructions"].append(
                "AGENTS.md"
            )
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode)
            self.assertIn("PUBLIC_RELEASE_CONTENT", result.stdout)

    def test_public_release_rejects_declared_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            link = root / "public-release" / "docs" / "linked-data.md"
            link.symlink_to("../README.md")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append("docs/linked-data.md")
            handoff["public_release"]["artifact_paths"]["data_instructions"].append(
                "docs/linked-data.md"
            )
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode)
            self.assertIn("PATH_CONTAINMENT", result.stdout)

    def test_public_release_inspects_extensionless_text_artifacts(self):
        """Break caught: an allowed Dockerfile could hide a credential marker."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "publication"
            self.assertEqual(0, self.init_workspace(root).returncode)
            self.populate_ready_workspace(root, public_release=True)
            dockerfile = root / "public-release" / "Dockerfile"
            marker = "api" + "_key="
            dockerfile.write_text(marker + "synthetic-placeholder\n", encoding="utf-8")
            handoff_path = root / "handoff" / "handoff.json"
            handoff = read_json(handoff_path)
            handoff["public_release"]["allowlist"].append("Dockerfile")
            handoff["public_release"]["artifact_paths"]["dependency_spec"].append(
                "Dockerfile"
            )
            write_json(handoff_path, handoff)

            result = self.validate(root, "public-release")

            self.assertEqual(1, result.returncode)
            self.assertIn("PUBLIC_RELEASE_CONTENT", result.stdout)


if __name__ == "__main__":
    unittest.main()
