import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
COMPONENTS = PACKAGE / "skills" / "prepare-journal-manuscripts" / "components"
VALIDATOR = COMPONENTS / "data-availability" / "scripts" / "validate_data_inventory.py"
EXAMPLE = COMPONENTS / "data-availability" / "examples" / "data-inventory.example.json"


def public_inventory() -> dict:
    return {
        "schema_version": 1,
        "journal": "Synthetic journal",
        "article_type": "Original research",
        "policy_checked_on": "2026-09-04",
        "datasets": [
            {
                "dataset_id": "D1",
                "description": "Synthetic data supporting the primary comparison.",
                "origin": "generated",
                "access_route": "public_repository",
                "supports": ["Figure 1", "Table 1"],
                "repository": "Synthetic Repository",
                "identifier": "https://doi.org/10.0000/synthetic.1",
                "version_or_access_date": "version 1",
                "licence": "Synthetic open-data licence",
                "files": [
                    {"name": "source-data.csv", "role": "Figure 1 source data", "format": "CSV"}
                ],
                "citation": "Synthetic Creator (2026). Synthetic dataset. Synthetic Repository. https://doi.org/10.0000/synthetic.1",
                "restrictions": {}
            }
        ]
    }


def run(payload: dict, mode: str = "final") -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "inventory.json"
        target.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(target), "--mode", mode, "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )


class DataAvailabilityValidatorTest(unittest.TestCase):
    def test_bundled_example_passes_final_mode(self):
        result = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(EXAMPLE), "--mode", "final", "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_public_repository_route_passes(self):
        result = run(public_inventory())
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_controlled_route_requires_durable_access_procedure(self):
        payload = public_inventory()
        dataset = payload["datasets"][0]
        dataset.update(
            {
                "access_route": "controlled_access",
                "licence": "not applicable: controlled data",
                "restrictions": {"reason": "participant privacy"},
            }
        )
        result = run(payload)
        self.assertEqual(1, result.returncode)
        self.assertIn("CONTROLLED_ACCESS", result.stdout)

    def test_controlled_route_allows_no_public_record_when_reason_is_explicit(self):
        payload = public_inventory()
        dataset = payload["datasets"][0]
        dataset.update(
            {
                "access_route": "controlled_access",
                "repository": "Institutional controlled archive",
                "identifier": "",
                "licence": "not applicable: controlled data",
                "restrictions": {
                    "reason": "participant consent prohibits a public record",
                    "controller": "institutional data access committee",
                    "request_route": "institutional application form",
                    "conditions": "ethics approval and data-use agreement",
                    "metadata_public": False,
                    "metadata_unavailable_reason": "the consent restriction covers record-level discovery metadata"
                },
            }
        )
        result = run(payload)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_embedded_route_requires_exact_files_and_claim_mapping(self):
        payload = public_inventory()
        dataset = payload["datasets"][0]
        dataset.update(
            {
                "access_route": "within_paper_or_supplement",
                "repository": "",
                "identifier": "",
                "licence": "not applicable: journal-hosted source data",
                "files": [],
                "citation": "not applicable: data distributed with the article",
            }
        )
        result = run(payload)
        self.assertEqual(1, result.returncode)
        self.assertIn("EMBEDDED_FILES", result.stdout)

    def test_final_mode_rejects_unresolved_identifiers(self):
        payload = public_inventory()
        payload["datasets"][0]["identifier"] = "AUTHOR_INPUT_NEEDED"
        working = run(payload, mode="working")
        final = run(payload, mode="final")
        self.assertEqual(0, working.returncode, working.stdout + working.stderr)
        self.assertEqual("PASS_WITH_WARNINGS", json.loads(working.stdout)["status"])
        self.assertEqual(1, final.returncode)
        self.assertIn("UNRESOLVED_FIELD", final.stdout)


if __name__ == "__main__":
    unittest.main()
