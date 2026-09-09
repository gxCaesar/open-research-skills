import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from pypdf import PdfWriter


PACKAGE = Path(__file__).resolve().parents[1]
CORE = PACKAGE / "skills" / "build-scientific-visualizations" / "shared" / "figure-core"
SCRIPTS = CORE / "scripts"
INIT = SCRIPTS / "init_figure_project.py"
VALIDATE = SCRIPTS / "validate_figure_project.py"
JOURNAL = SCRIPTS / "validate_journal_pdf.py"
PACKAGE_DELIVERABLES = SCRIPTS / "package_deliverables.py"
RENDER = SCRIPTS / "render_matplotlib.py"
LAYOUT_PROOF = SCRIPTS / "render_layout_proof.py"
WORKFLOW = SCRIPTS / "run_workflow.py"
QA = SCRIPTS / "qa_figure.py"
MM_TO_PT = 72 / 25.4


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def write_blank_pdf(path: Path, width_mm: float, height_mm: float) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=width_mm * MM_TO_PT, height=height_mm * MM_TO_PT)
    with path.open("wb") as handle:
        writer.write(handle)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rewrite_json(path: Path, mutate) -> None:
    payload = read_json(path)
    mutate(payload)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def geometry_receipt(spec: dict, blueprint: dict) -> dict:
    panels = {panel["id"]: panel for panel in spec["panels"]}
    placements = []
    for placement in spec["composite"]["placements"]:
        panel = panels[placement["panel"]]
        placements.append(
            {
                "panel": placement["panel"],
                "x_mm": placement["x_mm"],
                "y_mm": placement["y_mm"],
                "w_mm": placement.get("w_mm", panel["size_mm"][0]),
                "h_mm": placement.get("h_mm", panel["size_mm"][1]),
            }
        )
    return {
        "schema_version": "1.2",
        "figure_id": spec["figure_id"],
        "blueprint_revision": blueprint["blueprint_revision"],
        "composite_size_mm": spec["composite"]["size_mm"],
        "placements": placements,
    }


def make_equal_four_panel_project(project: Path) -> None:
    spec = read_json(project / "figure_spec.json")
    starter = spec["panels"][0]
    panels = []
    placements = []
    ledger_panels = []
    claims = []
    blueprint_panels = []
    source_panels = []
    panel_ids = ["a", "b", "c", "d"]
    for index, panel_id in enumerate(panel_ids):
        panel = json.loads(json.dumps(starter))
        panel["id"] = panel_id
        panel["title"] = f"Panel {panel_id}"
        panel["size_mm"] = [40.0, 40.0]
        for element in panel["elements"]:
            element["id"] = element["id"].replace("a-", f"{panel_id}-", 1)
            if element.get("text") == "a":
                element["text"] = panel_id
        panels.append(panel)
        placements.append({"panel": panel_id, "x_mm": index * 45.0, "y_mm": 0.0})
        claim_id = f"claim-{panel_id}"
        claims.append(
            {
                "id": claim_id,
                "panel_id": panel_id,
                "claim": f"Schematic placeholder for panel {panel_id}.",
                "source_anchors": [],
                "evidence_status": "schematic",
                "prohibited_implications": [],
            }
        )
        ledger_panels.append(
            {
                "id": panel_id,
                "claim_ids": [claim_id],
                "claim": f"Schematic placeholder for panel {panel_id}.",
                "source_anchors": [],
                "required_objects": [],
                "evidence_status": "schematic",
                "wet_data": None,
                "decisive_control": None,
                "prohibited_implications": [],
            }
        )
        blueprint_panels.append(
            {
                "id": panel_id,
                "group_id": "results",
                "evidence_role": "design",
                "priority": "anchor" if panel_id == "a" else "supporting",
                "preferred_aspect": "square",
                "shared_scale_group": None,
                "legend_owner": "a",
                "source_data_required": False,
            }
        )
        source_panels.append(
            {
                "panel_id": panel_id,
                "coverage": "not_applicable",
                "dataset_ids": [],
                "supports": [],
                "reason": "Purely schematic placeholder.",
            }
        )
    spec["panels"] = panels
    spec["composite"] = {"size_mm": [180.0, 40.0], "placements": placements}
    (project / "figure_spec.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    ledger = read_json(project / "content_ledger.json")
    ledger["claims"] = claims
    ledger["panels"] = ledger_panels
    (project / "content_ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    blueprint = read_json(project / "layout_blueprint.json")
    blueprint["reading_path"] = ["results"]
    blueprint["visual_anchor"] = {"panel_id": "a", "reason": "Overview anchor."}
    blueprint["groups"] = [
        {"id": "results", "panels": panel_ids, "role": "outcome", "emphasis": "primary"}
    ]
    blueprint["panels"] = blueprint_panels
    blueprint["layout_rationale"] = "Four aligned schematic slots support one direct comparison."
    (project / "layout_blueprint.json").write_text(
        json.dumps(blueprint, indent=2) + "\n", encoding="utf-8"
    )

    source = read_json(project / "source_data_manifest.json")
    source["panels"] = source_panels
    (project / "source_data_manifest.json").write_text(
        json.dumps(source, indent=2) + "\n", encoding="utf-8"
    )

    review = read_json(project / "qa" / "layout_review.json")
    review["ordered_panel_ids"] = panel_ids
    (project / "qa" / "layout_review.json").write_text(
        json.dumps(review, indent=2) + "\n", encoding="utf-8"
    )


def make_two_stage_flowchart(project: Path) -> None:
    spec = read_json(project / "figure_spec.json")
    spec["mode"] = "flowchart"
    spec["panels"][0]["panel_kind"] = "flowchart"
    spec["panels"][0]["elements"] = [
        {
            "type": "round_rect",
            "id": "a-input-box",
            "x": 0.06,
            "y": 0.34,
            "w": 0.28,
            "h": 0.28,
            "fill": "blue_pale",
            "stroke": "blue",
        },
        {
            "type": "text",
            "id": "a-input-label",
            "x": 0.09,
            "y": 0.41,
            "w": 0.22,
            "h": 0.12,
            "text": "Measured tissue input",
            "font_pt": 7.0,
            "bold": False,
            "color": "ink",
            "align": "center",
            "valign": "center",
        },
        {
            "type": "round_rect",
            "id": "a-output-box",
            "x": 0.66,
            "y": 0.34,
            "w": 0.28,
            "h": 0.28,
            "fill": "teal_pale",
            "stroke": "teal",
        },
        {
            "type": "text",
            "id": "a-output-label",
            "x": 0.69,
            "y": 0.41,
            "w": 0.22,
            "h": 0.12,
            "text": "Inferred spatial state",
            "font_pt": 7.0,
            "bold": False,
            "color": "ink",
            "align": "center",
            "valign": "center",
        },
        {
            "type": "arrow",
            "id": "a-route",
            "x1": 0.36,
            "y1": 0.48,
            "x2": 0.64,
            "y2": 0.48,
            "role": "inference",
            "line_style": "solid",
            "redundancy": ["label"],
        },
    ]
    (project / "figure_spec.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    ledger = read_json(project / "content_ledger.json")
    ledger["claims"] = [
        {
            "id": "claim-a-input",
            "panel_id": "a",
            "claim": "Tissue input is measured.",
            "source_anchors": ["methods:assay"],
            "evidence_status": "measured",
            "prohibited_implications": [],
        },
        {
            "id": "claim-a-output",
            "panel_id": "a",
            "claim": "Spatial state is inferred.",
            "source_anchors": ["methods:model-output"],
            "evidence_status": "inferred",
            "prohibited_implications": ["measured state"],
        },
        {
            "id": "claim-a-route",
            "panel_id": "a",
            "claim": "The model maps the measured input to the inferred state.",
            "source_anchors": ["methods:inference"],
            "evidence_status": "inferred",
            "prohibited_implications": ["causal effect"],
        },
    ]
    ledger["panels"][0]["claim_ids"] = [
        "claim-a-input",
        "claim-a-output",
        "claim-a-route",
    ]
    (project / "content_ledger.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )

    rewrite_json(project / "layout_blueprint.json", lambda value: value.update(mode="flowchart"))
    flowchart = {
        "schema_version": "1.2",
        "figure_id": "fig1",
        "flowcharts": [
            {
                "flowchart_id": "method-a",
                "panel_id": "a",
                "stages": [
                    {
                        "id": "input",
                        "semantic_role": "measured_input",
                        "label": "Measured tissue input",
                        "content_anchor": "claim-a-input",
                        "visual_element_ids": ["a-input-box", "a-input-label"],
                        "formula_refs": [],
                        "pictogram": {
                            "kind": "tissue-section",
                            "meaning": "measured tissue input",
                            "evidence_status": "schematic",
                            "source_anchor": "claim-a-input",
                        },
                    },
                    {
                        "id": "output",
                        "semantic_role": "inferred_output",
                        "label": "Inferred spatial state",
                        "content_anchor": "claim-a-output",
                        "visual_element_ids": ["a-output-box", "a-output-label"],
                        "formula_refs": [],
                        "pictogram": {
                            "kind": "spatial-state-map",
                            "meaning": "model-inferred spatial state",
                            "evidence_status": "schematic",
                            "source_anchor": "claim-a-output",
                        },
                    },
                ],
                "edges": [
                    {
                        "id": "route",
                        "from": "input",
                        "to": "output",
                        "role": "inference",
                        "line_style": "solid",
                        "label": "infer",
                        "redundancy": ["label"],
                        "content_anchor": "claim-a-route",
                        "visual_element_ids": ["a-route"],
                    }
                ],
                "formulas": [],
            }
        ],
    }
    (project / "flowchart_spec.json").write_text(
        json.dumps(flowchart, indent=2) + "\n", encoding="utf-8"
    )


def numeric_dataset(dataset_id: str, path: str, audiences=None) -> dict:
    return {
        "id": dataset_id,
        "title": f"Source data for {dataset_id}",
        "description": "De-identified values used for the displayed quantitative marks.",
        "kind": "numeric",
        "availability": "file",
        "path": path,
        "portable_format": "CSV",
        "data_dictionary": [
            {"name": "specimen_id", "description": "Opaque specimen identifier", "unit": "identifier"},
            {"name": "value", "description": "Displayed measurement", "unit": "arbitrary_unit"},
        ],
        "variables": ["specimen_id", "value"],
        "conditions": ["observed"],
        "independent_unit": "specimen",
        "sample_identifiers": "reviewer-safe opaque specimen_id",
        "transformations": ["none"],
        "normalizations": ["none"],
        "exclusions": ["none"],
        "missing_values": "none",
        "estimates": ["individual values"],
        "uncertainty": "not applicable to the individual-value fixture",
        "render_entrypoint": "scripts/plot_panel_a.py",
        "audiences": audiences or ["author", "reviewer"],
    }


def make_numeric_source_project(project: Path) -> None:
    source_file = project / "source-data" / "files" / "panel-a.csv"
    source_file.write_text("specimen_id,value\ns1,1.0\ns2,2.0\n", encoding="utf-8")
    script = project / "scripts" / "plot_panel_a.py"
    script.write_text("# Reproduce panel a from source-data/files/panel-a.csv\n", encoding="utf-8")
    rewrite_json(
        project / "figure_spec.json",
        lambda value: value["panels"][0].update(panel_kind="data"),
    )
    rewrite_json(
        project / "layout_blueprint.json",
        lambda value: value["panels"][0].update(
            evidence_role="measurement", source_data_required=True
        ),
    )
    rewrite_json(
        project / "source_data_manifest.json",
        lambda value: value.update(
            datasets=[numeric_dataset("panel-a-data", "source-data/files/panel-a.csv")],
            panels=[
                {
                    "panel_id": "a",
                    "coverage": "complete",
                    "dataset_ids": ["panel-a-data"],
                    "supports": ["individual plotted values"],
                    "reason": None,
                }
            ],
        ),
    )


def mark_project_ready(project: Path) -> None:
    spec = read_json(project / "figure_spec.json")
    blueprint = read_json(project / "layout_blueprint.json")
    venue = read_json(project / "venue_contract.json")
    review_path = project / "qa" / "layout_review.json"
    review = read_json(review_path)
    review.update(
        status="PASS",
        reviewed_blueprint_revision=blueprint["blueprint_revision"],
        ordered_panel_ids=[panel["id"] for panel in blueprint["panels"]],
        selected_width_mm=venue["geometry"]["selected_width_mm"],
    )
    review["checks"] = {key: "PASS" for key in review.get("checks", {})}
    review_path.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    (project / "qa" / "layout_proof.json").write_text(
        json.dumps(geometry_receipt(spec, blueprint), indent=2) + "\n",
        encoding="utf-8",
    )
    (project / "qa" / "qa_report.json").write_text(
        json.dumps({"status": "PASS", "errors": [], "checks": {}}) + "\n",
        encoding="utf-8",
    )
    layout = project / "outputs" / "layout"
    (layout / f"{spec['figure_id']}_layout-proof.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L1 1"/></svg>\n',
        encoding="utf-8",
    )
    Image.new(
        "RGB",
        (
            round(spec["composite"]["size_mm"][0] * 4),
            round(spec["composite"]["size_mm"][1] * 4),
        ),
        "white",
    ).save(
        layout / f"{spec['figure_id']}_layout-proof.png"
    )
    summary = project / "outputs" / "summary"
    write_blank_pdf(
        summary / f"{spec['figure_id']}_complete.pdf",
        spec["composite"]["size_mm"][0],
        spec["composite"]["size_mm"][1],
    )
    (summary / f"{spec['figure_id']}_complete.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L1 1"/></svg>\n',
        encoding="utf-8",
    )
    rewrite_json(
        project / "source_data_manifest.json",
        lambda value: value.update(
            delivery_outputs=[
                {
                    "path": f"outputs/layout/{spec['figure_id']}_layout-proof.svg",
                    "audiences": ["author", "reviewer"],
                    "content_scope": "layout_proof",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/layout/{spec['figure_id']}_layout-proof.png",
                    "audiences": ["author", "reviewer"],
                    "content_scope": "layout_proof",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/summary/{spec['figure_id']}_complete.pdf",
                    "audiences": ["author", "reviewer"],
                    "content_scope": "complete_figure",
                    "contains_controlled_visual_content": False,
                },
                {
                    "path": f"outputs/summary/{spec['figure_id']}_complete.svg",
                    "audiences": ["author", "reviewer"],
                    "content_scope": "complete_figure",
                    "contains_controlled_visual_content": False,
                },
            ]
        ),
    )


class FigureCoreTest(unittest.TestCase):
    def init_project(
        self,
        root: Path,
        profile: str = "nature-double",
        mode=None,
    ) -> subprocess.CompletedProcess:
        arguments = [str(root), "--figure-id", "fig1", "--layout-profile", profile]
        if mode is not None:
            arguments.extend(["--mode", mode])
        return run_script(INIT, *arguments)

    def test_initializer_creates_schema_12_project_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            for name in (
                "figure_spec.json",
                "content_ledger.json",
                "asset_manifest.json",
                "venue_contract.json",
                "layout_blueprint.json",
                "source_data_manifest.json",
            ):
                self.assertTrue((project / name).is_file(), name)
            self.assertEqual("1.2", read_json(project / "figure_spec.json")["schema_version"])
            self.assertEqual(
                183.0,
                read_json(project / "venue_contract.json")["geometry"]["selected_width_mm"],
            )
            self.assertTrue((project / "source-data" / "files").is_dir())
            self.assertTrue((project / "outputs" / "layout").is_dir())

    def test_legacy_layout_alias_is_preserved_but_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            contract = read_json(project / "venue_contract.json")
            self.assertEqual("unverified_legacy_alias", contract["authority_status"])
            self.assertIn("legacy", created.stderr.lower())

    def test_pdf_validator_and_initializer_share_profile_width(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            contract = read_json(project / "venue_contract.json")
            pdf = root / "figure.pdf"
            caption = root / "caption.txt"
            write_blank_pdf(pdf, 183.0, 100.0)
            caption.write_text("measured tissue response", encoding="utf-8")
            checked = run_script(
                JOURNAL,
                str(pdf),
                "--profile",
                "nature-figure-guide-2026-09-double",
                "--caption-file",
                str(caption),
                "--json",
            )
            self.assertEqual(183.0, contract["geometry"]["selected_width_mm"])
            self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
            self.assertEqual("PASS", json.loads(checked.stdout)["status"])

    def assert_validation_error(self, project: Path, expected: str, stage: str = "draft") -> None:
        result = run_script(VALIDATE, str(project), "--stage", stage)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(expected, result.stderr)

    def test_schema_12_rejects_blueprint_panel_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value["panels"][0].update(id="missing-panel"),
            )
            self.assert_validation_error(project, "panel IDs differ")

    def test_schema_12_rejects_unknown_reading_path_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value.update(reading_path=["unknown-group"]),
            )
            self.assert_validation_error(project, "reading_path references unknown group")

    def test_schema_12_rejects_venue_width_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "venue_contract.json",
                lambda value: value["geometry"].update(selected_width_mm=89.0),
            )
            self.assert_validation_error(project, "venue width")

    def test_schema_12_rejects_verified_profile_identity_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            rewrite_json(
                project / "venue_contract.json",
                lambda value: value.update(journal="Different journal"),
            )
            self.assert_validation_error(project, "differs from dated profile")

    def test_equal_four_panel_layout_warns_without_uniform_size_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            make_equal_four_panel_project(project)
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("mechanical-grid risk", result.stderr)

    def test_mechanical_grid_uses_resolved_placement_boxes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            make_equal_four_panel_project(project)

            def make_sources_unequal_but_boxes_equal(spec):
                for index, panel in enumerate(spec["panels"]):
                    panel["size_mm"] = [30.0 + index, 32.0 + index]
                for placement in spec["composite"]["placements"]:
                    placement.update(w_mm=40.0, h_mm=40.0)

            rewrite_json(project / "figure_spec.json", make_sources_unequal_but_boxes_equal)
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("mechanical-grid risk", result.stderr)

    def test_schema_12_rejects_missing_visual_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value.update(visual_anchor={"panel_id": "absent", "reason": "none"}),
            )
            self.assert_validation_error(project, "visual anchor references unknown panel")

    def test_schema_12_rejects_duplicate_group_membership(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value["groups"].append(
                    {"id": "duplicate", "panels": ["a"], "role": "control", "emphasis": "supporting"}
                ),
            )
            self.assert_validation_error(project, "panel a belongs to 2 groups")

    def test_schema_12_rejects_unknown_shared_scale_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value["panels"][0].update(shared_scale_group="absent"),
            )
            self.assert_validation_error(project, "unknown shared-scale group absent")

    def test_schema_12_rejects_unknown_legend_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "layout_blueprint.json",
                lambda value: value["panels"][0].update(legend_owner="absent"),
            )
            self.assert_validation_error(project, "unknown legend owner absent")

    def test_schema_12_rejects_duplicate_composite_placement(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value["composite"]["placements"].append(
                    {"panel": "a", "x_mm": 0, "y_mm": 0}
                ),
            )
            self.assert_validation_error(project, "composite placements must contain every panel exactly once")

    def test_schema_12_rejects_out_of_bounds_placement(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value["composite"]["placements"][0].update(x_mm=1.0),
            )
            self.assert_validation_error(project, "placement a exceeds composite page")

    def test_schema_12_rejects_unknown_panel_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "content_ledger.json",
                lambda value: value["panels"][0].update(claim_ids=["missing"]),
            )
            self.assert_validation_error(project, "unknown claim missing")

    def test_schema_12_rejects_invalid_authority_checked_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(
                0,
                self.init_project(project, "nature-figure-guide-2026-09-double").returncode,
            )
            rewrite_json(
                project / "venue_contract.json",
                lambda value: value["authority"].update(checked_date="2026-13-99"),
            )
            self.assert_validation_error(project, "invalid authority checked date")

    def test_final_stage_rejects_unverified_journal_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project, "nature-double").returncode)
            self.assert_validation_error(project, "verified venue authority", stage="final")

    def test_venue_contract_rejects_composite_over_fixed_height(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(
                0,
                self.init_project(project, "nature-figure-guide-2026-09-double").returncode,
            )
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value["composite"].update(size_mm=[183.0, 1000.0]),
            )
            self.assert_validation_error(project, "exceeds venue maximum height 170")

    def test_final_artwork_contract_uses_caption_height_band(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(
                0,
                self.init_project(
                    project,
                    "nature-research-final-artwork-2026-09-double",
                ).returncode,
            )
            (project / "caption.txt").write_text(
                "Measured response across independent specimens.",
                encoding="utf-8",
            )
            rewrite_json(
                project / "venue_contract.json",
                lambda value: value.update(caption_file="caption.txt"),
            )

            def enlarge_to_226_mm(spec):
                spec["composite"]["size_mm"] = [180.0, 226.0]
                spec["panels"][0]["size_mm"] = [180.0, 226.0]

            rewrite_json(project / "figure_spec.json", enlarge_to_226_mm)
            self.assert_validation_error(project, "exceeds venue maximum height 225")

    def test_final_artwork_requires_caption_for_final_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(
                0,
                self.init_project(
                    project,
                    "nature-research-final-artwork-2026-09-double",
                ).returncode,
            )
            mark_project_ready(project)
            self.assert_validation_error(
                project,
                "caption_file is required for caption-dependent height validation",
                stage="final",
            )

    def test_custom_non_journal_contract_passes_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = run_script(
                INIT,
                str(project),
                "--figure-id",
                "fig1",
                "--layout-profile",
                "custom",
                "--page-width-mm",
                "175",
            )
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def flowchart_project(self, root: Path) -> Path:
        project = root / "figure"
        created = self.init_project(project, mode="flowchart")
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        make_two_stage_flowchart(project)
        return project

    def test_initialized_flowchart_mode_has_valid_semantic_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, mode="flowchart")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            self.assertEqual("flowchart", read_json(project / "figure_spec.json")["panels"][0]["panel_kind"])
            flowchart = read_json(project / "flowchart_spec.json")["flowcharts"][0]
            self.assertTrue(flowchart["stages"])
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_flowchart_rejects_unknown_edge_endpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["edges"][0].update(to="absent"),
            )
            self.assert_validation_error(project, "unknown endpoint absent")

    def test_flowchart_rejects_missing_claim_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["stages"][0].update(content_anchor="absent"),
            )
            self.assert_validation_error(project, "unknown claim absent")

    def test_flowchart_rejects_unknown_formula_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["stages"][0].update(formula_refs=["absent"]),
            )
            self.assert_validation_error(project, "unknown formula absent")

    def test_flowchart_rejects_uncovered_visible_arrow(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0].update(edges=[]),
            )
            self.assert_validation_error(project, "visible arrow a-route is not covered")

    def test_flowchart_rejects_one_arrow_covered_by_two_edges(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))

            def duplicate_edge(value):
                edge = json.loads(json.dumps(value["flowcharts"][0]["edges"][0]))
                edge["id"] = "route-duplicate"
                value["flowcharts"][0]["edges"].append(edge)

            rewrite_json(project / "flowchart_spec.json", duplicate_edge)
            self.assert_validation_error(project, "visible arrow a-route is covered 2 times")

    def test_flowchart_rejects_claiming_edge_with_wrong_line_style(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["edges"][0].update(
                    role="prospective", line_style="solid"
                ),
            )
            self.assert_validation_error(project, "prospective edge must be dashed")

    def test_flowchart_requires_non_colour_redundancy(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["edges"][0].update(redundancy=[]),
            )
            self.assert_validation_error(project, "requires non-colour redundancy")

    def test_flowchart_rejects_pictogram_stronger_than_inferred_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.flowchart_project(Path(tmp))
            rewrite_json(
                project / "flowchart_spec.json",
                lambda value: value["flowcharts"][0]["stages"][1]["pictogram"].update(
                    evidence_status="measured"
                ),
            )
            self.assert_validation_error(project, "incompatible with anchored claim")

    def numeric_project(self, root: Path) -> Path:
        project = root / "figure"
        created = self.init_project(project, "nature-figure-guide-2026-09-double")
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        make_numeric_source_project(project)
        return project

    def test_numeric_panel_without_source_data_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value.update(datasets=[], panels=[]),
            )
            self.assert_validation_error(project, "panel a requires source-data coverage")

    def test_complete_coverage_rejects_not_applicable_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            (project / "source-data" / "files" / "panel-a.csv").unlink()
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value.update(
                    datasets=[
                        {
                            "id": "panel-a-data",
                            "title": "Unavailable numeric source",
                            "description": "No source dataset is available.",
                            "kind": "numeric",
                            "availability": "not_applicable",
                            "reason": "Fixture for an invalid complete-coverage declaration.",
                            "audiences": ["author", "reviewer"],
                        }
                    ]
                ),
            )
            self.assert_validation_error(project, "cannot use not_applicable dataset")

    def test_shareable_claim_asset_rejects_controlled_source_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            image_path = project / "assets" / "processed" / "panel-a.png"
            Image.new("RGB", (700, 700), "white").save(image_path)

            def add_asset(spec):
                spec["assets"]["panel-a-image"] = {
                    "kind": "reference_image",
                    "evidence_role": "claim_supporting",
                    "path": "assets/processed/panel-a.png",
                }
                spec["panels"][0]["elements"].append(
                    {
                        "type": "image",
                        "id": "a-image",
                        "x": 0.1,
                        "y": 0.2,
                        "w": 0.8,
                        "h": 0.7,
                        "asset": "panel-a-image",
                    }
                )

            rewrite_json(project / "figure_spec.json", add_asset)
            rewrite_json(
                project / "asset_manifest.json",
                lambda value: value["assets"].update(
                    {
                        "panel-a-image": {
                            "path": "assets/processed/panel-a.png",
                            "evidence_role": "claim_supporting",
                            "distribution": "shareable",
                            "audiences": ["reviewer", "public"],
                            "source_dataset_ids": ["controlled-images"],
                        }
                    }
                ),
            )
            controlled = {
                "id": "controlled-images",
                "title": "Controlled microscopy images",
                "description": "Source images require approved access.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Institutional approval is required.",
                "access_route": "https://example.org/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(controlled),
            )
            self.assert_validation_error(
                project,
                "controlled source cannot be externally distributed",
            )

    def test_claim_supporting_image_cannot_be_not_applicable(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            image_path = project / "assets" / "processed" / "panel-a.png"
            image_path.write_bytes(b"claim-supporting-image")

            def add_image(spec):
                spec["assets"]["panel-a-image"] = {
                    "kind": "reference_image",
                    "evidence_role": "claim_supporting",
                    "path": "assets/processed/panel-a.png",
                }
                spec["panels"][0]["elements"].append(
                    {
                        "type": "image",
                        "id": "a-image",
                        "x": 0.15,
                        "y": 0.22,
                        "w": 0.7,
                        "h": 0.6,
                        "asset": "panel-a-image",
                    }
                )

            rewrite_json(project / "figure_spec.json", add_image)
            rewrite_json(
                project / "asset_manifest.json",
                lambda value: value["assets"].update(
                    {
                        "panel-a-image": {
                            "evidence_role": "claim_supporting",
                            "distribution": "controlled_access",
                        }
                    }
                ),
            )
            self.assert_validation_error(project, "claim-supporting image panel a cannot be not_applicable")

    def test_schematic_panel_with_reasoned_not_applicable_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_source_data_rejects_absolute_and_parent_paths(self):
        for unsafe in ("/tmp/data.csv", "../data.csv"):
            with self.subTest(path=unsafe), tempfile.TemporaryDirectory() as tmp:
                project = self.numeric_project(Path(tmp))
                rewrite_json(
                    project / "source_data_manifest.json",
                    lambda value: value["datasets"][0].update(path=unsafe),
                )
                self.assert_validation_error(project, "unsafe project-relative path")

    def test_source_data_rejects_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            (project / "source-data" / "files" / "panel-a.csv").unlink()
            self.assert_validation_error(project, "dataset panel-a-data: missing file")

    def test_source_data_rejects_orphan_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            (project / "source-data" / "files" / "orphan.tsv").write_text("x\n1\n", encoding="utf-8")
            self.assert_validation_error(project, "undeclared source-data file")

    def test_source_manifest_rejects_private_locator_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"][0].update(
                    private_locator="/" + "Users" + "/example/restricted/panel-a.csv"
                ),
            )
            self.assert_validation_error(project, "prohibited private locator")

    def test_controlled_access_requires_conditions_and_route(self):
        for missing, expected in (
            ("access_conditions", "access_conditions"),
            ("access_route", "access_route"),
        ):
            with self.subTest(field=missing), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / "figure"
                self.assertEqual(0, self.init_project(project).returncode)
                controlled = {
                    "id": "image-source",
                    "title": "Controlled source image",
                    "description": "Source image available by approved request.",
                    "kind": "repository_object",
                    "availability": "controlled_access",
                    "repository_or_accession": "Controlled imaging repository",
                    "access_conditions": "Institutional approval is required.",
                    "access_route": "https://example.org/request",
                    "audiences": ["author", "reviewer"],
                }
                del controlled[missing]
                rewrite_json(
                    project / "source_data_manifest.json",
                    lambda value: value.update(datasets=[controlled]),
                )
                self.assert_validation_error(project, expected)

    def test_controlled_access_rejects_private_file_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            controlled = {
                "id": "image-source",
                "title": "Controlled source image",
                "description": "Source image available by approved request.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Institutional approval is required.",
                "access_route": "file:///Volumes/ControlledStudy/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value.update(datasets=[controlled]),
            )
            self.assert_validation_error(project, "access_route must be a public HTTPS URL")

    def test_asset_manifest_rejects_private_locator_in_unreferenced_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            self.assertEqual(0, self.init_project(project).returncode)
            rewrite_json(
                project / "asset_manifest.json",
                lambda value: value["assets"].update(
                    {
                        "unreferenced-controlled": {
                            "distribution": "controlled_access",
                            "private_locator": "file:///Volumes/ControlledStudy/raw.tif",
                        }
                    }
                ),
            )
            self.assert_validation_error(project, "asset_manifest.json: prohibited private locator")

    def test_image_dataset_requires_acquisition_channels_and_processing(self):
        required = ("acquisition", "channels", "lut", "crop", "registration", "segmentation", "processing")
        for missing in required:
            with self.subTest(field=missing), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / "figure"
                self.assertEqual(0, self.init_project(project).returncode)
                image = {
                    "id": "image-source",
                    "title": "Controlled source image",
                    "description": "Source image metadata fixture.",
                    "kind": "image",
                    "availability": "controlled_access",
                    "repository_or_accession": "Imaging repository record",
                    "access_conditions": "Approved request required.",
                    "access_route": "https://example.org/request",
                    "audiences": ["author", "reviewer"],
                    "render_entrypoint_not_applicable_reason": "Image is rendered by the registered imaging workflow.",
                    "acquisition": "multiplex fluorescence microscopy",
                    "channels": ["protein-A"],
                    "lut": "linear grayscale",
                    "crop": "full field; no crop",
                    "registration": "not_applied",
                    "segmentation": "not_applied",
                    "processing": "global linear rescaling only",
                }
                del image[missing]
                rewrite_json(
                    project / "source_data_manifest.json",
                    lambda value: value.update(datasets=[image]),
                )
                self.assert_validation_error(project, f"image-source: {missing}")

    def test_reviewer_package_includes_only_declared_reviewer_source_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            private_path = project / "source-data" / "files" / "author-only.csv"
            private_path.write_text("specimen_id,value\ns3,3.0\n", encoding="utf-8")
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(
                    numeric_dataset(
                        "author-only-data",
                        "source-data/files/author-only.csv",
                        audiences=["author"],
                    )
                ),
            )
            mark_project_ready(project)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((output / "source-data" / "files" / "panel-a.csv").is_file())
            self.assertTrue((output / "scripts" / "plot_panel_a.py").is_file())
            self.assertFalse((output / "source-data" / "files" / "author-only.csv").exists())

    def test_reviewer_package_excludes_private_locator_and_restricted_raw_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            raw = project / "assets" / "processed" / "controlled-image.png"
            Image.new("RGB", (700, 700), "white").save(raw)
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value["assets"].update(
                    {
                        "controlled-image": {
                            "kind": "reference_image",
                            "evidence_role": "claim_supporting",
                            "path": "assets/processed/controlled-image.png",
                        }
                    }
                ),
            )
            rewrite_json(
                project / "asset_manifest.json",
                lambda value: value["assets"].update(
                    {
                        "controlled-image": {
                            "path": "assets/processed/controlled-image.png",
                            "evidence_role": "claim_supporting",
                            "distribution": "controlled_access",
                            "source_dataset_ids": ["controlled-image-source"],
                        }
                    }
                ),
            )
            controlled = {
                "id": "controlled-image-source",
                "title": "Controlled image source",
                "description": "Raw image is not distributed.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Approved request required.",
                "access_route": "https://example.org/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(controlled),
            )
            private = project / "qa" / "private" / "source_data_local_map.json"
            private.write_text(json.dumps({"controlled-image-source": "/private/raw/image.tif"}), encoding="utf-8")
            mark_project_ready(project)

            def authorize_quantitative_only(value: dict) -> None:
                for record in value["delivery_outputs"]:
                    if record["content_scope"] == "complete_figure":
                        record["content_scope"] = "quantitative_only"
                        record["dataset_ids"] = ["panel-a-data"]
                    elif record["content_scope"] == "layout_proof":
                        record["audiences"] = ["author"]

            rewrite_json(project / "source_data_manifest.json", authorize_quantitative_only)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse((output / "qa" / "private" / "source_data_local_map.json").exists())
            self.assertFalse((output / "assets" / "processed" / "controlled-image.png").exists())
            self.assertNotIn("path", read_json(output / "figure_spec.json")["assets"]["controlled-image"])
            self.assertNotIn("path", read_json(output / "asset_manifest.json")["assets"]["controlled-image"])
            public_manifest = read_json(output / "source_data_manifest.json")
            controlled_copy = next(
                item for item in public_manifest["datasets"] if item["id"] == "controlled-image-source"
            )
            self.assertEqual("controlled_access", controlled_copy["availability"])

    def test_reviewer_package_includes_only_explicitly_authorized_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            mark_project_ready(project)
            figure_id = read_json(project / "figure_spec.json")["figure_id"]
            summary = project / "outputs" / "summary"
            reviewer_pdf = summary / f"{figure_id}_reviewer-quantitative.pdf"
            reviewer_svg = summary / f"{figure_id}_reviewer-quantitative.svg"
            write_blank_pdf(reviewer_pdf, 180.0, 60.0)
            reviewer_svg.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L1 1"/></svg>\n',
                encoding="utf-8",
            )

            def restrict_outputs(value: dict) -> None:
                for record in value["delivery_outputs"]:
                    if record["content_scope"] == "complete_figure":
                        record["audiences"] = ["author"]
                        record["contains_controlled_visual_content"] = True
                value["delivery_outputs"].extend(
                    [
                        {
                            "path": reviewer_pdf.relative_to(project).as_posix(),
                            "audiences": ["reviewer"],
                            "content_scope": "quantitative_only",
                            "contains_controlled_visual_content": False,
                            "dataset_ids": ["panel-a-data"],
                        },
                        {
                            "path": reviewer_svg.relative_to(project).as_posix(),
                            "audiences": ["reviewer"],
                            "content_scope": "quantitative_only",
                            "contains_controlled_visual_content": False,
                            "dataset_ids": ["panel-a-data"],
                        },
                    ]
                )

            rewrite_json(project / "source_data_manifest.json", restrict_outputs)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse((output / "outputs" / "summary" / f"{figure_id}_complete.pdf").exists())
            self.assertFalse((output / "outputs" / "summary" / f"{figure_id}_complete.svg").exists())
            self.assertTrue(
                (output / "outputs" / "summary" / f"{figure_id}_reviewer-quantitative.pdf").is_file()
            )
            self.assertTrue(
                (output / "outputs" / "summary" / f"{figure_id}_reviewer-quantitative.svg").is_file()
            )

    def test_reviewer_package_rejects_source_file_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            source = project / "source-data" / "files" / "panel-a.csv"
            outside = Path(tmp) / "controlled-outside-project.csv"
            outside.write_text("specimen_id,value\nprivate,99\n", encoding="utf-8")
            source.unlink()
            source.symlink_to(outside)
            mark_project_ready(project)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("regular non-symlink file within the project", result.stderr)
            self.assertFalse((output / "source-data" / "files" / "panel-a.csv").exists())

    def test_reviewer_package_rejects_private_locator_in_copied_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            (project / "source-data" / "files" / "panel-a.csv").write_text(
                "specimen_id,value,raw_reference\ns1,1.0,file:///Volumes/ControlledStudy/raw.tif\n",
                encoding="utf-8",
            )
            mark_project_ready(project)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("private locator", result.stderr)

    def test_reviewer_package_allows_non_locator_profile_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            (project / "source-data" / "files" / "panel-a.csv").write_text(
                "specimen_id,value,note\ns1,1.0,profile: baseline\n",
                encoding="utf-8",
            )
            mark_project_ready(project)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reviewer_package_rejects_private_locator_in_pdf_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            mark_project_ready(project)
            spec = read_json(project / "figure_spec.json")
            pdf = project / "outputs" / "summary" / f"{spec['figure_id']}_complete.pdf"
            writer = PdfWriter()
            writer.add_blank_page(
                width=spec["composite"]["size_mm"][0] * MM_TO_PT,
                height=spec["composite"]["size_mm"][1] * MM_TO_PT,
            )
            writer.add_metadata({"/Title": "file:///Volumes/ControlledStudy/raw.tif"})
            with pdf.open("wb") as handle:
                writer.write(handle)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("private locator", result.stderr)

    def test_mixed_access_reviewer_output_requires_numeric_only_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            controlled = {
                "id": "controlled-images",
                "title": "Controlled source images",
                "description": "Images available by approved request.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Institutional approval is required.",
                "access_route": "https://example.org/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(controlled),
            )
            mark_project_ready(project)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("mixed-access reviewer output", result.stderr)

    def test_mixed_access_quantitative_svg_rejects_embedded_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            controlled = {
                "id": "controlled-images",
                "title": "Controlled source images",
                "description": "Images available by approved request.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Institutional approval is required.",
                "access_route": "https://example.org/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(controlled),
            )
            mark_project_ready(project)

            def authorize_quantitative(value: dict) -> None:
                for record in value["delivery_outputs"]:
                    if record["content_scope"] == "complete_figure":
                        record["content_scope"] = "quantitative_only"
                        record["dataset_ids"] = ["panel-a-data"]
                    elif record["content_scope"] == "layout_proof":
                        record["audiences"] = ["author"]

            rewrite_json(project / "source_data_manifest.json", authorize_quantitative)
            spec = read_json(project / "figure_spec.json")
            svg = project / "outputs" / "summary" / f"{spec['figure_id']}_complete.svg"
            svg.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/>'
                '<image href="data:image/png;base64,AA=="/></svg>\n',
                encoding="utf-8",
            )
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("quantitative-only SVG must not contain image elements", result.stderr)

    def test_mixed_access_reviewer_package_rejects_layout_proof_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            controlled = {
                "id": "controlled-images",
                "title": "Controlled source images",
                "description": "Images available by approved request.",
                "kind": "repository_object",
                "availability": "controlled_access",
                "repository_or_accession": "Controlled imaging repository",
                "access_conditions": "Institutional approval is required.",
                "access_route": "https://example.org/request",
                "audiences": ["author", "reviewer"],
            }
            rewrite_json(
                project / "source_data_manifest.json",
                lambda value: value["datasets"].append(controlled),
            )
            mark_project_ready(project)

            def authorize_quantitative(value: dict) -> None:
                for record in value["delivery_outputs"]:
                    if record["content_scope"] == "complete_figure":
                        record["content_scope"] = "quantitative_only"
                        record["dataset_ids"] = ["panel-a-data"]

            rewrite_json(project / "source_data_manifest.json", authorize_quantitative)
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("mixed-access reviewer output", result.stderr)
            self.assertFalse(output.exists())

    def test_public_package_uses_public_data_and_output_allowlists(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            mark_project_ready(project)

            def authorize_public(value: dict) -> None:
                value["datasets"][0]["audiences"].append("public")
                for record in value["delivery_outputs"]:
                    record["audiences"].append("public")

            rewrite_json(project / "source_data_manifest.json", authorize_public)
            output = Path(tmp) / "public"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "public",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((output / "source-data" / "files" / "panel-a.csv").is_file())

    def test_layout_proof_renders_without_scientific_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(LAYOUT_PROOF, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((project / "outputs" / "layout" / "fig1_layout-proof.svg").is_file())
            self.assertTrue((project / "outputs" / "layout" / "fig1_layout-proof.png").is_file())

    def test_layout_proof_encodes_reading_path_inside_panels_without_footer_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(LAYOUT_PROOF, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            svg = (project / "outputs" / "layout" / "fig1_layout-proof.svg").read_text(
                encoding="utf-8"
            )
            self.assertIn("<!-- path 1: primary-evidence -->", svg)
            self.assertNotIn("primary-evidence: design  &gt;", svg)

    def test_layout_proof_records_reviewed_geometry(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(LAYOUT_PROOF, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            receipt_path = project / "qa" / "layout_proof.json"
            self.assertTrue(receipt_path.is_file())
            self.assertEqual(
                geometry_receipt(
                    read_json(project / "figure_spec.json"),
                    read_json(project / "layout_blueprint.json"),
                ),
                read_json(receipt_path),
            )

    def test_final_stage_rejects_revise_or_stale_layout_review(self):
        mutations = (
            ("revise", lambda review, blueprint: review.update(status="REVISE"), "layout review must be PASS"),
            (
                "stale",
                lambda review, blueprint: review.update(
                    status="PASS",
                    reviewed_blueprint_revision=blueprint["blueprint_revision"] - 1,
                ),
                "stale layout review",
            ),
        )
        for name, mutation, expected in mutations:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / "figure"
                created = self.init_project(project, "nature-figure-guide-2026-09-double")
                self.assertEqual(0, created.returncode, created.stdout + created.stderr)
                blueprint = read_json(project / "layout_blueprint.json")
                rewrite_json(
                    project / "qa" / "layout_review.json",
                    lambda review: mutation(review, blueprint),
                )
                self.assert_validation_error(project, expected, stage="final")

    def test_final_stage_rejects_incomplete_layout_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            blueprint = read_json(project / "layout_blueprint.json")
            venue = read_json(project / "venue_contract.json")
            rewrite_json(
                project / "qa" / "layout_review.json",
                lambda review: review.update(
                    status="PASS",
                    reviewed_blueprint_revision=blueprint["blueprint_revision"],
                    ordered_panel_ids=["a"],
                    selected_width_mm=venue["geometry"]["selected_width_mm"],
                ),
            )
            self.assert_validation_error(project, "layout review check", stage="final")

    def test_final_stage_rejects_stale_layout_geometry(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            mark_project_ready(project)
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value["composite"]["placements"][0].update(w_mm=170.0),
            )
            self.assert_validation_error(project, "stale layout proof geometry", stage="final")

    def test_packaging_rejects_missing_layout_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            mark_project_ready(project)
            (project / "outputs" / "layout" / "fig1_layout-proof.svg").unlink()
            (project / "outputs" / "layout" / "fig1_layout-proof.png").unlink()
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(Path(tmp) / "reviewer"),
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("layout proof is required before packaging", result.stderr)

    def test_packaging_rejects_duplicate_composite_placement(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            mark_project_ready(project)

            def duplicate_placement(spec):
                spec["composite"]["placements"].append(
                    json.loads(json.dumps(spec["composite"]["placements"][0]))
                )

            rewrite_json(project / "figure_spec.json", duplicate_placement)
            spec = read_json(project / "figure_spec.json")
            blueprint = read_json(project / "layout_blueprint.json")
            (project / "qa" / "layout_proof.json").write_text(
                json.dumps(geometry_receipt(spec, blueprint), indent=2) + "\n",
                encoding="utf-8",
            )
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("composite placements must contain every panel exactly once", result.stderr)
            self.assertFalse(output.exists())

    def test_packaging_rechecks_qa_after_layout_proof_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.numeric_project(Path(tmp))
            mark_project_ready(project)
            Image.new("RGB", (100, 100), "white").save(
                project / "outputs" / "layout" / "fig1_layout-proof.png"
            )
            output = Path(tmp) / "reviewer"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("layout proof PNG aspect ratio", result.stderr)
            self.assertFalse(output.exists())

    def test_final_stage_rejects_missing_layout_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            mark_project_ready(project)
            (project / "outputs" / "layout" / "fig1_layout-proof.svg").unlink()
            (project / "outputs" / "layout" / "fig1_layout-proof.png").unlink()
            self.assert_validation_error(project, "layout proof is required", stage="final")

    def test_layout_workflow_stops_after_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(WORKFLOW, str(project), "--phase", "layout")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((project / "outputs" / "layout" / "fig1_layout-proof.svg").is_file())
            self.assertFalse((project / "outputs" / "summary" / "fig1_complete.pdf").exists())

    def test_final_workflow_renders_after_passed_layout_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            layout = run_script(WORKFLOW, str(project), "--phase", "layout")
            self.assertEqual(0, layout.returncode, layout.stdout + layout.stderr)
            blueprint = read_json(project / "layout_blueprint.json")
            venue = read_json(project / "venue_contract.json")

            def pass_review(review):
                review.update(
                    status="PASS",
                    reviewed_blueprint_revision=blueprint["blueprint_revision"],
                    ordered_panel_ids=[panel["id"] for panel in blueprint["panels"]],
                    selected_width_mm=venue["geometry"]["selected_width_mm"],
                )
                review["checks"] = {key: "PASS" for key in review["checks"]}

            rewrite_json(project / "qa" / "layout_review.json", pass_review)
            final = run_script(WORKFLOW, str(project), "--phase", "final")
            self.assertEqual(0, final.returncode, final.stdout + final.stderr)
            self.assertTrue((project / "outputs" / "summary" / "fig1_complete.pdf").is_file())
            self.assertTrue((project / "outputs" / "summary" / "fig1_complete.svg").is_file())

    def test_standalone_final_validation_requires_rendered_declared_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            layout = run_script(WORKFLOW, str(project), "--phase", "layout")
            self.assertEqual(0, layout.returncode, layout.stdout + layout.stderr)
            blueprint = read_json(project / "layout_blueprint.json")
            venue = read_json(project / "venue_contract.json")

            def pass_review(review):
                review.update(
                    status="PASS",
                    reviewed_blueprint_revision=blueprint["blueprint_revision"],
                    ordered_panel_ids=[panel["id"] for panel in blueprint["panels"]],
                    selected_width_mm=venue["geometry"]["selected_width_mm"],
                )
                review["checks"] = {key: "PASS" for key in review["checks"]}

            rewrite_json(project / "qa" / "layout_review.json", pass_review)
            self.assert_validation_error(
                project,
                "missing output file outputs/summary/fig1_complete.pdf",
                stage="final",
            )

    def test_legacy_schema_11_layout_workflow_is_validation_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            rewrite_json(
                project / "figure_spec.json",
                lambda value: value.update(schema_version="1.1"),
            )
            for name in ("venue_contract.json", "layout_blueprint.json", "source_data_manifest.json"):
                (project / name).unlink()
            result = run_script(WORKFLOW, str(project), "--phase", "layout")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("validation-only", result.stdout)
            self.assertFalse((project / "outputs" / "layout" / "fig1_layout-proof.svg").exists())

    def test_qa_report_records_layout_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            mark_project_ready(project)
            result = run_script(QA, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            layout = read_json(project / "qa" / "qa_report.json")["checks"]["layout"]
            self.assertEqual(1, layout["blueprint_revision"])
            self.assertEqual(1, layout["reviewed_blueprint_revision"])
            self.assertEqual(["a"], layout["ordered_panel_ids"])
            self.assertEqual(183.0, layout["selected_width_mm"])

    def test_qa_rejects_invalid_layout_proof_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            mark_project_ready(project)
            (project / "outputs" / "layout" / "fig1_layout-proof.png").write_bytes(b"not-a-png")
            result = run_script(QA, str(project))
            self.assertEqual(1, result.returncode)
            report = read_json(project / "qa" / "qa_report.json")
            self.assertTrue(
                any("layout proof PNG" in error for error in report["errors"]),
                report["errors"],
            )

    def test_qa_reports_invalid_layout_contract_json(self):
        for filename in ("layout_proof.json", "layout_review.json"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / "figure"
                created = self.init_project(project, "nature-figure-guide-2026-09-double")
                self.assertEqual(0, created.returncode, created.stdout + created.stderr)
                mark_project_ready(project)
                (project / "qa" / filename).write_text("not-json\n", encoding="utf-8")
                result = run_script(QA, str(project))
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                report = read_json(project / "qa" / "qa_report.json")
                self.assertTrue(
                    any(filename in error for error in report["errors"]),
                    report["errors"],
                )

    def test_qa_allows_opaque_rgb_reference_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            image_path = project / "assets" / "processed" / "micrograph.png"
            Image.new("RGB", (700, 700), (110, 120, 130)).save(image_path)

            def add_image(spec):
                spec["assets"]["micrograph"] = {
                    "kind": "reference_image",
                    "evidence_role": "decorative",
                    "path": "assets/processed/micrograph.png",
                }
                spec["panels"][0]["elements"].append(
                    {
                        "type": "image",
                        "id": "a-micrograph",
                        "x": 0.1,
                        "y": 0.2,
                        "w": 0.8,
                        "h": 0.7,
                        "asset": "micrograph",
                    }
                )

            rewrite_json(project / "figure_spec.json", add_image)
            rewrite_json(
                project / "asset_manifest.json",
                lambda value: value["assets"].update(
                    {
                        "micrograph": {
                            "path": "assets/processed/micrograph.png",
                            "evidence_role": "decorative",
                            "distribution": "author",
                            "audiences": ["author"],
                        }
                    }
                ),
            )
            mark_project_ready(project)
            result = run_script(QA, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = read_json(project / "qa" / "qa_report.json")
            self.assertFalse(
                any("no alpha channel" in error or "opaque border pixels" in error for error in report["errors"]),
                report["errors"],
            )

    def test_named_nature_profiles_initialize_exact_widths(self):
        cases = {
            "nature-single": 88.0,
            "nature-protocols": 135.0,
            "nature-double": 180.0,
        }
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for profile, expected_width in cases.items():
                with self.subTest(profile=profile):
                    project = base / profile
                    result = self.init_project(project, profile)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    spec = json.loads((project / "figure_spec.json").read_text(encoding="utf-8"))
                    self.assertEqual(expected_width, spec["journal_profile"]["page_width_mm"])
                    self.assertEqual(expected_width, spec["panels"][0]["size_mm"][0])
                    self.assertEqual(expected_width, spec["composite"]["size_mm"][0])

    def test_initialized_project_passes_schema_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project)
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            result = run_script(VALIDATE, str(project))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_renderer_sets_writable_cache_before_importing_matplotlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_package = root / "matplotlib"
            fake_package.mkdir()
            (fake_package / "__init__.py").write_text(
                "import os\n"
                "if not os.environ.get('MPLCONFIGDIR'):\n"
                "    raise RuntimeError('MPLCONFIGDIR was not set before import')\n"
                "if not os.environ.get('XDG_CACHE_HOME'):\n"
                "    raise RuntimeError('XDG_CACHE_HOME was not set before import')\n"
                "def use(*args, **kwargs):\n"
                "    return None\n",
                encoding="utf-8",
            )
            (fake_package / "pyplot.py").write_text("", encoding="utf-8")
            (fake_package / "text.py").write_text("Text = object\n", encoding="utf-8")
            (fake_package / "transforms.py").write_text("Bbox = object\n", encoding="utf-8")
            (fake_package / "patches.py").write_text(
                "Ellipse = FancyArrowPatch = FancyBboxPatch = Rectangle = object\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.pop("MPLCONFIGDIR", None)
            environment.pop("XDG_CACHE_HOME", None)
            environment["PYTHONPATH"] = str(root)
            result = subprocess.run(
                [sys.executable, "-B", str(RENDER), "--help"],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_named_profile_rejects_spec_width_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project)
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            spec_path = project / "figure_spec.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["journal_profile"]["page_width_mm"] = 179.0
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            result = run_script(VALIDATE, str(project))
            self.assertEqual(1, result.returncode)
            self.assertIn("expects 180 mm", result.stderr)

    def test_flowchart_conditioning_arrow_must_be_dashed(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project)
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            spec_path = project / "figure_spec.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["panels"][0]["panel_kind"] = "flowchart"
            spec["panels"][0]["elements"].append(
                {
                    "type": "arrow",
                    "id": "conditioning-arrow",
                    "x1": 0.1,
                    "y1": 0.5,
                    "x2": 0.9,
                    "y2": 0.5,
                    "role": "conditioning",
                    "line_style": "solid",
                    "redundancy": ["label"],
                }
            )
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            result = run_script(VALIDATE, str(project))
            self.assertEqual(1, result.returncode)
            self.assertIn("conditioning arrow must be dashed", result.stderr)

    def test_journal_pdf_validator_catches_width_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            caption = root / "caption.txt"
            caption.write_text(" ".join(["word"] * 100), encoding="utf-8")
            correct = root / "correct.pdf"
            wrong = root / "wrong.pdf"
            write_blank_pdf(correct, 180.0, 210.0)
            write_blank_pdf(wrong, 179.0, 210.0)

            passed = run_script(
                JOURNAL,
                str(correct),
                "--profile",
                "nature-research-double",
                "--caption-file",
                str(caption),
                "--json",
            )
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            self.assertEqual("PASS", json.loads(passed.stdout)["status"])

            failed = run_script(
                JOURNAL,
                str(wrong),
                "--profile",
                "nature-research-double",
                "--caption-file",
                str(caption),
                "--json",
            )
            self.assertEqual(1, failed.returncode)
            self.assertIn("width", " ".join(json.loads(failed.stdout)["errors"]).lower())

    def test_reviewer_packaging_removes_internal_prompt_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "figure"
            created = self.init_project(project, "nature-figure-guide-2026-09-double")
            self.assertEqual(0, created.returncode, created.stdout + created.stderr)
            spec_path = project / "figure_spec.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["prompt_record"] = {"text": "internal drafting instruction"}
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            mark_project_ready(project)
            output = project / "public"
            result = run_script(
                PACKAGE_DELIVERABLES,
                str(project),
                "--audience",
                "reviewer",
                "--output",
                str(output),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            public_spec = json.loads((output / "figure_spec.json").read_text(encoding="utf-8"))
            self.assertNotIn("prompt_record", public_spec)
            self.assertTrue((output / "delivery_index.json").is_file())


if __name__ == "__main__":
    unittest.main()
