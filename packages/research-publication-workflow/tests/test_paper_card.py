import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
COMPONENT = PACKAGE / "skills" / "research-publication-pipeline" / "components" / "paper-card"
PREPARE = COMPONENT / "scripts" / "prepare_paper.py"
AUDIT = COMPONENT / "scripts" / "audit_paper_card.py"
LONG_TEXT = (
    "This synthetic source block is deliberately long enough for source validation "
    "and contains no real manuscript content."
)


def run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def card(pointer: str = "S001", locator_mode: str = "structure-grounded", figure: bool = False) -> str:
    header = "\n".join(
        [
            "> Source coverage: Partial paper",
            "> Extraction confidence: Mixed",
            f"> Locator mode: {locator_mode}",
            "> Primary analytical lens: methods",
            "> Secondary analytical lens: None",
            "> Context verification: Paper-only",
            "> Card completeness: Partial",
        ]
    )
    sections = []
    for number in range(1, 17):
        body = f"Grounded synthetic statement [Paper: {pointer}]"
        if number == 10 and figure:
            body += "\nFigure 1 is inventoried."
        if number == 16:
            body += (
                "\nInnovation status: unverified"
                "\nValidation: matched synthetic test"
                "\nFailure modes: no signal; confounding"
            )
        sections.append(f"## {number:02d} Section\n{body}")
    return header + "\n\n" + "\n\n".join(sections)


class PaperCardTest(unittest.TestCase):
    def test_source_map_preserves_verified_missing_and_invalid_locators(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.json"
            output = root / "bundle.json"
            source.write_text(
                json.dumps(
                    {
                        "metadata": {"title": "Synthetic paper"},
                        "blocks": [
                            {"id": "S001", "page": 1, "section": "Methods", "text": LONG_TEXT},
                            {"id": "S002", "text": "Missing locator. " + LONG_TEXT},
                            {"id": "S003", "page": "bad", "text": "Invalid locator. " + LONG_TEXT},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = run(PREPARE, str(source), "--output", str(output))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            bundle = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual([1], [page["pdf_page"] for page in bundle["pages"]])
            self.assertEqual(["missing", "invalid"], [item["locator_status"] for item in bundle["unlocated_blocks"]])
            self.assertEqual("mixed", bundle["locator_summary"]["page_locator_reliability"])
            self.assertEqual("structure-grounded", bundle["validation"]["recommended_locator_mode"])

    def test_extension_only_pdf_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "login.pdf"
            output = root / "bundle.json"
            source.write_text("<html>sign in</html>", encoding="utf-8")
            result = run(PREPARE, str(source), "--output", str(output))
            self.assertEqual(2, result.returncode)
            self.assertIn("PDF header", result.stderr)
            self.assertFalse(output.exists())

    def test_card_audit_validates_structure_blocks_and_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            card_path = root / "card.md"
            bundle_path = root / "bundle.json"
            report_path = root / "report.json"
            card_path.write_text(card(figure=True), encoding="utf-8")
            bundle_path.write_text(
                json.dumps(
                    {
                        "evidence_inventory": {
                            "figures": [{"id": "Figure 1"}],
                            "tables": [],
                            "equations": [],
                        },
                        "located_blocks": [{"id": "S001", "pdf_page": 1}],
                        "unlocated_blocks": [],
                    }
                ),
                encoding="utf-8",
            )
            result = run(
                AUDIT,
                "--card",
                str(card_path),
                "--bundle",
                str(bundle_path),
                "--locator-mode",
                "structure-grounded",
                "--report",
                str(report_path),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(0, json.loads(report_path.read_text(encoding="utf-8"))["summary"]["errors"])

    def test_card_audit_rejects_unknown_block_and_page_pointer_in_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            card_path = root / "card.md"
            bundle_path = root / "bundle.json"
            card_path.write_text(card("PDF p. 1, S999"), encoding="utf-8")
            bundle_path.write_text(
                json.dumps(
                    {
                        "evidence_inventory": {"figures": [], "tables": [], "equations": []},
                        "located_blocks": [{"id": "S001", "pdf_page": 1}],
                        "unlocated_blocks": [],
                    }
                ),
                encoding="utf-8",
            )
            result = run(
                AUDIT,
                "--card",
                str(card_path),
                "--bundle",
                str(bundle_path),
                "--locator-mode",
                "structure-grounded",
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("UNKNOWN_SOURCE_BLOCK", result.stdout)
            self.assertIn("PAGE_POINTER_FORBIDDEN", result.stdout)

    def test_page_grounded_pointer_must_exist_in_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            card_path = root / "card.md"
            bundle_path = root / "bundle.json"
            card_path.write_text(card("PDF p. 4", "page-grounded"), encoding="utf-8")
            bundle_path.write_text(
                json.dumps(
                    {
                        "page_count": 2,
                        "pages": [{"pdf_page": 1}, {"pdf_page": 2}],
                        "evidence_inventory": {"figures": [], "tables": [], "equations": []},
                        "located_blocks": [],
                        "unlocated_blocks": [],
                    }
                ),
                encoding="utf-8",
            )
            result = run(
                AUDIT,
                "--card",
                str(card_path),
                "--bundle",
                str(bundle_path),
                "--locator-mode",
                "page-grounded",
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("PAGE_POINTER_RANGE", result.stdout)


if __name__ == "__main__":
    unittest.main()
