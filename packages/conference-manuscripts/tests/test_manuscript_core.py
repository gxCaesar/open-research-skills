import json
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from pypdf import PdfWriter


PACKAGE = Path(__file__).resolve().parents[1]
SKILL = PACKAGE / "skills" / "prepare-conference-manuscripts"
CORE = SKILL / "components" / "manuscript-core" / "scripts"
AUDIT_TEX = CORE / "audit_tex.py"
AUDIT_PDF = CORE / "audit_pdf.py"
AUDIT_ARCHIVE = CORE / "audit_archive.py"
VALIDATE_REPORT = CORE / "validate_review_report.py"
AAAI_PROFILE = SKILL / "components" / "venues" / "aaai" / "references" / "venue-profile.json"
ICLR_PROFILE = SKILL / "components" / "venues" / "iclr" / "references" / "venue-profile.json"
ACL_PROFILE = SKILL / "components" / "venues" / "acl" / "references" / "venue-profile.json"
CVPR_PROFILE = SKILL / "components" / "venues" / "cvpr" / "references" / "venue-profile.json"
ICML_PROFILE = SKILL / "components" / "venues" / "icml" / "references" / "venue-profile.json"
NEURIPS_PROFILE = SKILL / "components" / "venues" / "neurips" / "references" / "venue-profile.json"
GENERIC_PROFILE = (
    SKILL
    / "components"
    / "venues"
    / "generic"
    / "references"
    / "venue-profile.template.json"
)


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def write_pdf(path: Path, width: float, height: float, author: str = "") -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=width, height=height)
    if author:
        writer.add_metadata({"/Author": author})
    with path.open("wb") as handle:
        writer.write(handle)


def synthetic_profile(*, allowed_stages=None) -> dict:
    profile = json.loads(GENERIC_PROFILE.read_text(encoding="utf-8"))
    profile.update(
        {
            "venue": "Synthetic Computing Conference",
            "year": 2027,
            "track": "Main track",
            "checked_on": "2026-09-04",
            "rule_sources": {
                "DOCUMENT_CLASS": ["SYNTHETIC_AUTHOR_GUIDE"],
                "SYNTHETIC_STYLE_CURRENT": ["SYNTHETIC_AUTHOR_GUIDE"],
                "PDF_PAGE_SIZE": ["SYNTHETIC_AUTHOR_GUIDE"],
            },
            "allowed_stages": allowed_stages or ["anonymous_submission", "camera_ready"],
        }
    )
    profile["tex_contract"].update(
        {
            "document_class": "article",
            "style_package": "synthetic2027",
            "style_rule_id": "SYNTHETIC_STYLE_CURRENT",
            "required_options": {},
            "anonymous_stages": [],
            "anonymous_source_author_mode": "render_hidden",
            "forbid_acknowledgments_in_anonymous": False,
            "final_copy_command": "",
            "required_headings": {},
            "forbidden_layout_packages": [],
            "require_abstract": [],
        }
    )
    profile["pdf_contract"].update(
        {
            "page_width_points": 612.0,
            "page_height_points": 792.0,
            "page_tolerance_points": 2.0,
            "anonymous_stages": [],
            "max_total_pages": {},
            "manual_content_page_limit": {},
        }
    )
    return profile


class ManuscriptCoreTest(unittest.TestCase):
    def assert_path_free_cli_error(
        self,
        result: subprocess.CompletedProcess,
        root: Path,
        expected_basename: str,
        expected_summary: str,
    ) -> None:
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(expected_basename, result.stderr)
        self.assertIn(expected_summary, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        for forbidden in (str(root), "/private/tmp", "/Users"):
            self.assertNotIn(forbidden, result.stderr)

    def test_top_level_audit_errors_redact_artifact_and_profile_paths(self):
        """Break caught: CLI error interpolation exposed temporary artifact/profile roots."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
            pdf = root / "paper.pdf"
            write_pdf(pdf, 612, 792)
            missing_profile = root / "missing-profile.json"
            malformed_profile = root / "malformed-profile.json"
            malformed_profile.write_text("{", encoding="utf-8")
            non_object_profile = root / "non-object-profile.json"
            non_object_profile.write_text("[]", encoding="utf-8")

            cases = (
                (
                    "missing TeX",
                    run_script(
                        AUDIT_TEX,
                        str(root / "missing-paper.tex"),
                        "--profile",
                        str(AAAI_PROFILE),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "missing-paper.tex",
                    "OSError",
                ),
                (
                    "missing PDF",
                    run_script(
                        AUDIT_PDF,
                        str(root / "missing-paper.pdf"),
                        "--profile",
                        str(AAAI_PROFILE),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "missing-paper.pdf",
                    "FileNotFoundError",
                ),
                (
                    "missing TeX profile",
                    run_script(
                        AUDIT_TEX,
                        str(tex),
                        "--profile",
                        str(missing_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "missing-profile.json",
                    "FileNotFoundError",
                ),
                (
                    "missing PDF profile",
                    run_script(
                        AUDIT_PDF,
                        str(pdf),
                        "--profile",
                        str(missing_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "missing-profile.json",
                    "FileNotFoundError",
                ),
                (
                    "malformed TeX profile",
                    run_script(
                        AUDIT_TEX,
                        str(tex),
                        "--profile",
                        str(malformed_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "malformed-profile.json",
                    "invalid JSON at line 1, column 2",
                ),
                (
                    "malformed PDF profile",
                    run_script(
                        AUDIT_PDF,
                        str(pdf),
                        "--profile",
                        str(malformed_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "malformed-profile.json",
                    "invalid JSON at line 1, column 2",
                ),
                (
                    "non-object TeX profile",
                    run_script(
                        AUDIT_TEX,
                        str(tex),
                        "--profile",
                        str(non_object_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "non-object-profile.json",
                    "expected a JSON object",
                ),
                (
                    "non-object PDF profile",
                    run_script(
                        AUDIT_PDF,
                        str(pdf),
                        "--profile",
                        str(non_object_profile),
                        "--stage",
                        "anonymous_submission",
                    ),
                    "non-object-profile.json",
                    "expected a JSON object",
                ),
            )

        for label, result, basename, summary in cases:
            with self.subTest(case=label):
                self.assert_path_free_cli_error(result, root, basename, summary)

    def test_generic_profile_without_rule_sources_cannot_certify_tex(self):
        """Break caught: a filled profile with no authority bindings used to pass."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = json.loads(GENERIC_PROFILE.read_text(encoding="utf-8"))
            profile.update(
                {
                    "venue": "Synthetic Computing Conference",
                    "year": 2027,
                    "track": "Main track",
                    "checked_on": "2026-09-04",
                    "rule_sources": {},
                }
            )
            profile["tex_contract"].update(
                {
                    "document_class": "article",
                    "style_package": "synthetic2027",
                    "style_rule_id": "SYNTHETIC_STYLE_CURRENT",
                    "required_options": {"anonymous_submission": []},
                    "anonymous_stages": [],
                    "require_abstract": ["anonymous_submission"],
                }
            )
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("incomplete profile", result.stderr)

    def test_incomplete_generic_profile_cannot_certify_tex_or_pdf(self):
        """Break caught: an untouched task-local template can look like usable authority."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "placeholder.tex"
            tex.write_text(
                r"""\documentclass{REPLACE_WITH_OFFICIAL_DOCUMENT_CLASS}
\usepackage{REPLACE_WITH_OFFICIAL_STYLE_PACKAGE}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            pdf = root / "placeholder.pdf"
            write_pdf(pdf, 612, 792)
            tex_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(GENERIC_PROFILE),
                "--stage",
                "anonymous_submission",
            )
            pdf_result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(GENERIC_PROFILE),
                "--stage",
                "anonymous_submission",
            )

        self.assertEqual(2, tex_result.returncode, tex_result.stdout + tex_result.stderr)
        self.assertIn("incomplete profile", tex_result.stderr)
        self.assertEqual(2, pdf_result.returncode, pdf_result.stdout + pdf_result.stderr)
        self.assertIn("incomplete profile", pdf_result.stderr)

    def test_tex_preprocessor_ignores_comments_and_literal_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass[letterpaper]{article}
\usepackage[submission]{aaai2027}
% \section{Acknowledgments}
\begin{verbatim}
\usepackage{geometry}
\end{verbatim}
\begin{document}
\title{Synthetic Paper}
\begin{abstract}A complete synthetic abstract.\end{abstract}
Synthetic body.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual([], json.loads(result.stdout)["findings"])

    def test_aaai_tex_audit_detects_style_acknowledgment_and_layout_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{geometry}
\begin{document}
\section*{Acknowledgments}
Thanks to the identifying institution.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(1, result.returncode)
            codes = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
            self.assertIn("AAAI_STYLE_SUBMISSION", codes)
            self.assertIn("ANON_ACKNOWLEDGMENTS", codes)
            self.assertIn("LAYOUT_OVERRIDE", codes)

    def test_iclr_source_author_is_allowed_until_finalcopy_is_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            base = r"""\documentclass{article}
\usepackage{iclr2027_conference}
\author{Synthetic Author}
\begin{document}
\title{Synthetic Paper}
\begin{abstract}A complete synthetic abstract.\end{abstract}
\section*{AI Use Statement}
No tools were used in this synthetic fixture.
\end{document}
"""
            tex.write_text(base, encoding="utf-8")
            passed = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ICLR_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)

            tex.write_text(base.replace("\\begin{document}", "\\iclrfinalcopy\n\\begin{document}"), encoding="utf-8")
            failed = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ICLR_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(1, failed.returncode)
            self.assertIn("ICLR_FINALCOPY_DISABLED", failed.stdout)

    def test_tex_audit_requires_configured_document_class_options(self):
        """Break caught: required document-class options were not audited."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["tex_contract"]["required_document_class_options"] = ["letterpaper"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        finding = json.loads(result.stdout)["findings"][0]
        self.assertEqual("DOCUMENT_CLASS", finding["rule_id"])
        self.assertIn("letterpaper", finding["expected"])

    def test_tex_audit_enforces_stage_scoped_required_and_forbidden_style_options(self):
        """Break caught: forbidden stage-specific style options were accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["tex_contract"].update(
                {
                    "required_options": {"anonymous_submission": ["review"]},
                    "forbidden_options": {"anonymous_submission": ["final"]},
                }
            )
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            good_tex = root / "good.tex"
            good_tex.write_text(
                r"""\documentclass{article}
\usepackage[review]{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            missing_tex = root / "missing.tex"
            missing_tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            forbidden_tex = root / "forbidden.tex"
            forbidden_tex.write_text(
                r"""\documentclass{article}
\usepackage[review,final]{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            good = run_script(
                AUDIT_TEX,
                str(good_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            missing = run_script(
                AUDIT_TEX,
                str(missing_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            forbidden = run_script(
                AUDIT_TEX,
                str(forbidden_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertEqual(1, missing.returncode, missing.stdout + missing.stderr)
        self.assertIn("SYNTHETIC_STYLE_CURRENT", missing.stdout)
        self.assertEqual(1, forbidden.returncode, forbidden.stdout + forbidden.stderr)
        self.assertIn("SYNTHETIC_STYLE_CURRENT", forbidden.stdout)

    def test_tex_audit_uses_configured_final_copy_rule_ids_for_all_stages(self):
        """Break caught: final-copy rules were hard-coded to ICLR and anonymous stages."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile(allowed_stages=["draft", "camera_ready"])
            profile["tex_contract"].update(
                {
                    "final_copy_command": "syntheticfinalcopy",
                    "final_copy_rule_ids": {
                        "disabled": "SYNTHETIC_FINALCOPY_DISABLED",
                        "enabled": "SYNTHETIC_FINALCOPY_ENABLED",
                    },
                    "final_copy_required_stages": ["camera_ready"],
                }
            )
            profile["rule_sources"].update(
                {
                    "SYNTHETIC_FINALCOPY_DISABLED": ["SYNTHETIC_AUTHOR_GUIDE"],
                    "SYNTHETIC_FINALCOPY_ENABLED": ["SYNTHETIC_AUTHOR_GUIDE"],
                }
            )
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            enabled_tex = root / "enabled.tex"
            enabled_tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\syntheticfinalcopy
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            disabled_tex = root / "disabled.tex"
            disabled_tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            draft = run_script(
                AUDIT_TEX,
                str(enabled_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "draft",
                "--format",
                "json",
            )
            camera_ready = run_script(
                AUDIT_TEX,
                str(disabled_tex),
                "--profile",
                str(profile_path),
                "--stage",
                "camera_ready",
                "--format",
                "json",
            )

        self.assertEqual(1, draft.returncode, draft.stdout + draft.stderr)
        self.assertIn("SYNTHETIC_FINALCOPY_DISABLED", draft.stdout)
        self.assertNotIn("ICLR_FINALCOPY_DISABLED", draft.stdout)
        self.assertEqual(1, camera_ready.returncode, camera_ready.stdout + camera_ready.stderr)
        self.assertIn("SYNTHETIC_FINALCOPY_ENABLED", camera_ready.stdout)
        self.assertNotIn("ICLR_FINALCOPY_ENABLED", camera_ready.stdout)

    def test_tex_audit_flags_configured_anonymous_identity_commands(self):
        """Break caught: flag mode only searched author and affiliation commands."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["tex_contract"].update(
                {
                    "anonymous_stages": ["anonymous_submission"],
                    "anonymous_source_author_mode": "flag",
                    "anonymous_source_identity_commands": ["institute"],
                }
            )
            profile["rule_sources"]["ANON_SOURCE_IDENTITY"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\institute{Synthetic Institute}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("ANON_SOURCE_IDENTITY", result.stdout)

    def test_profile_contract_rejects_invalid_anonymity_mode_and_unknown_stage_key(self):
        """Break caught: malformed configured profile fields used to be accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            invalid_mode = synthetic_profile()
            invalid_mode["tex_contract"]["anonymous_source_author_mode"] = "unknown_mode"
            invalid_mode_path = root / "invalid-mode.json"
            invalid_mode_path.write_text(json.dumps(invalid_mode), encoding="utf-8")
            invalid_mode_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(invalid_mode_path),
                "--stage",
                "anonymous_submission",
            )

            invalid_stage = synthetic_profile()
            invalid_stage["tex_contract"]["required_options"] = {"unlisted_stage": ["review"]}
            invalid_stage_path = root / "invalid-stage.json"
            invalid_stage_path.write_text(json.dumps(invalid_stage), encoding="utf-8")
            invalid_stage_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(invalid_stage_path),
                "--stage",
                "anonymous_submission",
            )

        self.assertEqual(2, invalid_mode_result.returncode, invalid_mode_result.stdout + invalid_mode_result.stderr)
        self.assertIn("anonymous_source_author_mode", invalid_mode_result.stderr)
        self.assertEqual(2, invalid_stage_result.returncode, invalid_stage_result.stdout + invalid_stage_result.stderr)
        self.assertIn("unlisted_stage", invalid_stage_result.stderr)

    def test_profile_contract_rejects_non_control_word_command_names(self):
        """Break caught: punctuation and leading slashes were accepted in TeX command names."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            profiles = []
            for command in (r"\finalcopy", "final-copy"):
                profile = synthetic_profile()
                profile["tex_contract"].update(
                    {
                        "final_copy_command": command,
                        "final_copy_rule_ids": {
                            "disabled": "SYNTHETIC_FINALCOPY_DISABLED",
                            "enabled": "SYNTHETIC_FINALCOPY_ENABLED",
                        },
                        "final_copy_required_stages": ["camera_ready"],
                    }
                )
                profile["rule_sources"].update(
                    {
                        "SYNTHETIC_FINALCOPY_DISABLED": ["SYNTHETIC_AUTHOR_GUIDE"],
                        "SYNTHETIC_FINALCOPY_ENABLED": ["SYNTHETIC_AUTHOR_GUIDE"],
                    }
                )
                profiles.append(("final_copy_command", profile))
            for command in (r"\institute", "institute!"):
                profile = synthetic_profile()
                profile["tex_contract"].update(
                    {
                        "anonymous_stages": ["anonymous_submission"],
                        "anonymous_source_author_mode": "flag",
                        "anonymous_source_identity_commands": ["author", command],
                    }
                )
                profile["rule_sources"]["ANON_SOURCE_IDENTITY"] = ["SYNTHETIC_AUTHOR_GUIDE"]
                profiles.append(("anonymous_source_identity_commands", profile))

            results = []
            for index, (field, profile) in enumerate(profiles):
                profile_path = root / f"invalid-command-{index}.json"
                profile_path.write_text(json.dumps(profile), encoding="utf-8")
                results.append(
                    (
                        field,
                        run_script(
                            AUDIT_TEX,
                            str(tex),
                            "--profile",
                            str(profile_path),
                            "--stage",
                            "anonymous_submission",
                        ),
                    )
                )

        for field, result in results:
            with self.subTest(field=field, stderr=result.stderr):
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(field, result.stderr)

    def test_tex_audit_reports_identity_findings_at_the_included_source_location(self):
        """Break caught: findings in included files pointed to the main source."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["tex_contract"].update(
                {
                    "anonymous_stages": ["anonymous_submission"],
                    "anonymous_source_author_mode": "flag",
                    "anonymous_source_identity_commands": ["author"],
                }
            )
            profile["rule_sources"]["ANON_SOURCE_IDENTITY"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\input{identity}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            identity = root / "identity.tex"
            identity.write_text("\\author{Synthetic Author}\n", encoding="utf-8")
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual("paper.tex", report["target"])
        findings = report["findings"]
        identity_finding = next(item for item in findings if item["rule_id"] == "ANON_SOURCE_IDENTITY")
        self.assertEqual("identity.tex:1", identity_finding["location"])

    def test_tex_audit_emits_relative_paths_for_nested_included_sources(self):
        """Break caught: runtime reports exposed absolute source paths."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["tex_contract"].update(
                {
                    "anonymous_stages": ["anonymous_submission"],
                    "anonymous_source_author_mode": "flag",
                    "anonymous_source_identity_commands": ["author"],
                }
            )
            profile["rule_sources"]["ANON_SOURCE_IDENTITY"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\input{sub/identity}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            identity = root / "sub" / "identity.tex"
            identity.parent.mkdir()
            identity.write_text("\\author{Synthetic Author}\n", encoding="utf-8")
            json_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            markdown_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "markdown",
            )

        self.assertEqual(1, json_result.returncode, json_result.stdout + json_result.stderr)
        self.assertEqual(1, markdown_result.returncode, markdown_result.stdout + markdown_result.stderr)
        report = json.loads(json_result.stdout)
        self.assertEqual("paper.tex", report["target"])
        finding = next(item for item in report["findings"] if item["rule_id"] == "ANON_SOURCE_IDENTITY")
        self.assertEqual("sub/identity.tex:1", finding["location"])
        self.assertNotIn(str(root), json_result.stdout)
        self.assertIn("- Location: `sub/identity.tex:1`", markdown_result.stdout)
        self.assertNotIn(str(root), markdown_result.stdout)

    def test_tex_audit_redacts_external_included_source_paths_and_limitations(self):
        """Break caught: external source paths leaked parent directories into reports."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manuscript = root / "manuscript"
            manuscript.mkdir()
            external = root / "private-parent"
            external.mkdir()
            profile = synthetic_profile()
            profile["tex_contract"].update(
                {
                    "anonymous_stages": ["anonymous_submission"],
                    "anonymous_source_author_mode": "flag",
                    "anonymous_source_identity_commands": ["author"],
                }
            )
            profile["rule_sources"]["ANON_SOURCE_IDENTITY"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            tex = manuscript / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{synthetic2027}
\input{../private-parent/identity}
\input{../private-parent/missing}
\begin{document}\end{document}
""",
                encoding="utf-8",
            )
            identity = external / "identity.tex"
            identity.write_text("\\author{Synthetic Author}\n", encoding="utf-8")
            json_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            markdown_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "markdown",
            )

        self.assertEqual(1, json_result.returncode, json_result.stdout + json_result.stderr)
        self.assertEqual(1, markdown_result.returncode, markdown_result.stdout + markdown_result.stderr)
        report = json.loads(json_result.stdout)
        finding = next(item for item in report["findings"] if item["rule_id"] == "ANON_SOURCE_IDENTITY")
        self.assertEqual("<external>/identity.tex:1", finding["location"])
        self.assertIn("Could not read <external>/missing.tex (FileNotFoundError).", report["limitations"])
        self.assertIn("- Location: `<external>/identity.tex:1`", markdown_result.stdout)
        for output in (json_result.stdout, markdown_result.stdout):
            self.assertNotIn("..", output)
            self.assertNotIn(str(root), output)
            self.assertNotIn("private-parent", output)

    def test_pdf_audit_reports_decimal_mb_file_size_without_bytes(self):
        """Break caught: configured PDF size limits were ignored or exposed raw bytes."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["pdf_contract"]["max_file_size_mb"] = {"anonymous_submission": 0.000001}
            profile["rule_sources"]["PDF_FILE_SIZE"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            pdf = root / "paper.pdf"
            write_pdf(pdf, 612, 792)
            result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        findings = json.loads(result.stdout)["findings"]
        size_finding = next(item for item in findings if item["rule_id"] == "PDF_FILE_SIZE")
        self.assertIn("MB", size_finding["observed"])
        self.assertNotIn("byte", size_finding["observed"].casefold())
        self.assertNotIn("byte", size_finding["expected"].casefold())

    def test_pdf_audit_preserves_tiny_decimal_mb_limits(self):
        """Break caught: a nonzero decimal-MB limit was rounded down to zero."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = synthetic_profile()
            profile["pdf_contract"]["max_file_size_mb"] = {"anonymous_submission": 0.0000001}
            profile["rule_sources"]["PDF_FILE_SIZE"] = ["SYNTHETIC_AUTHOR_GUIDE"]
            profile_path = root / "profile.json"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            pdf = root / "paper.pdf"
            write_pdf(pdf, 612, 792)
            result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(profile_path),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        findings = json.loads(result.stdout)["findings"]
        size_finding = next(item for item in findings if item["rule_id"] == "PDF_FILE_SIZE")
        self.assertEqual("The stage profile permits at most 1e-07 MB.", size_finding["expected"])

    def test_pdf_audit_emits_artifact_relative_paths(self):
        """Break caught: runtime PDF reports exposed absolute artifact paths."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pdf = root / "paper.pdf"
            write_pdf(pdf, 595.28, 841.89)
            json_result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            markdown_result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "markdown",
            )

        self.assertEqual(1, json_result.returncode, json_result.stdout + json_result.stderr)
        self.assertEqual(1, markdown_result.returncode, markdown_result.stdout + markdown_result.stderr)
        report = json.loads(json_result.stdout)
        self.assertEqual("paper.pdf", report["target"])
        finding = next(item for item in report["findings"] if item["rule_id"] == "PDF_PAGE_SIZE")
        self.assertEqual("paper.pdf:page 1", finding["location"])
        self.assertNotIn(str(root), json_result.stdout)
        self.assertNotIn(str(root), markdown_result.stdout)

    def test_pdf_audit_checks_page_geometry_and_anonymous_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            letter = root / "letter.pdf"
            a4 = root / "a4.pdf"
            named = root / "named.pdf"
            write_pdf(letter, 612, 792)
            write_pdf(a4, 595.28, 841.89)
            write_pdf(named, 612, 792, author="Synthetic Author")

            passed = run_script(
                AUDIT_PDF,
                str(letter),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            wrong_size = run_script(
                AUDIT_PDF,
                str(a4),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(1, wrong_size.returncode)
            self.assertIn("PDF_PAGE_SIZE", wrong_size.stdout)
            identity = run_script(
                AUDIT_PDF,
                str(named),
                "--profile",
                str(AAAI_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            self.assertEqual(1, identity.returncode)
            self.assertIn("PDF_AUTHOR_METADATA", identity.stdout)

    def test_acl_anonymous_submission_accepts_a4_review_source_with_limitations(self):
        """Break caught: ACL review artifacts lose A4, 11pt, review mode, or Limitations."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass[11pt]{article}
\usepackage[review]{acl}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section{Limitations}
Synthetic limitation.
\end{document}
""",
                encoding="utf-8",
            )
            source_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )
            pdf = root / "paper.pdf"
            write_pdf(pdf, 595.28, 841.89)
            pdf_result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(0, source_result.returncode, source_result.stdout + source_result.stderr)
        self.assertEqual(0, pdf_result.returncode, pdf_result.stdout + pdf_result.stderr)

    def test_acl_anonymous_submission_rejects_missing_11pt_or_review_mode(self):
        """Break caught: ACL's anonymous source contract accepts the unqualified final invocation."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{acl}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section{Limitations}
Synthetic limitation.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertEqual({"DOCUMENT_CLASS", "ACL26_STYLE_CURRENT"}, rule_ids)

    def test_round_one_acl_anonymous_submission_rejects_non_a4_pdf(self):
        """Break caught: ACL review PDFs accept US Letter instead of the required A4 page size."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "paper.pdf"
            write_pdf(pdf, 612, 792)
            result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("PDF_PAGE_SIZE", rule_ids)

    def test_round_one_acl_anonymous_submission_rejects_missing_limitations(self):
        """Break caught: ACL review sources omit the required Limitations section."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass[11pt]{article}
\usepackage[review]{acl}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("REQUIRED_HEADING", rule_ids)

    def test_round_one_acl_style_finding_cites_review_and_final_format_sources(self):
        """Break caught: ACL's stage-specific invocation emits only generic formatting evidence."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass[11pt]{article}
\usepackage{acl}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section{Limitations}
Synthetic limitation.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ACL_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        finding = next(
            item
            for item in json.loads(result.stdout)["findings"]
            if item["rule_id"] == "ACL26_STYLE_CURRENT"
        )
        self.assertEqual(
            ["ACL2026_FORMATTING", "ACL2026_REVIEW_VERSION", "ACL2026_FINAL_VERSION"],
            finding["sources"],
        )

    def test_acl_camera_ready_rejects_review_or_final_style_options(self):
        """Break caught: ACL camera-ready sources retain review-era style flags."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for option in ("review", "final"):
                tex = root / f"{option}.tex"
                tex.write_text(
                    rf"""\documentclass[11pt]{{article}}
\usepackage[{option}]{{acl}}
\begin{{document}}
\begin{{abstract}}Synthetic abstract.\end{{abstract}}
\section{{Limitations}}
Synthetic limitation.
\end{{document}}
""",
                    encoding="utf-8",
                )
                result = run_script(
                    AUDIT_TEX,
                    str(tex),
                    "--profile",
                    str(ACL_PROFILE),
                    "--stage",
                    "camera_ready",
                    "--format",
                    "json",
                )
                with self.subTest(option=option):
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("ACL26_STYLE_CURRENT", result.stdout)

    def test_cvpr_anonymous_submission_rejects_incomplete_document_class_options(self):
        """Break caught: a CVPR source may omit a required class option and still pass."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass[10pt,twocolumn]{article}
\usepackage[review]{cvpr}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("DOCUMENT_CLASS", result.stdout)

    def test_round_one_cvpr_anonymous_submission_rejects_missing_review_option(self):
        """Break caught: CVPR anonymous sources pass without the review style option."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("CVPR26_STYLE_CURRENT", rule_ids)

    def test_cvpr_camera_ready_accepts_no_option_and_rejects_review_options(self):
        """Break caught: CVPR camera-ready source retains review or rebuttal mode."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.tex"
            good.write_text(
                r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            passed = run_script(
                AUDIT_TEX,
                str(good),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "camera_ready",
                "--format",
                "json",
            )
            rejected = []
            for option in ("review", "rebuttal"):
                tex = root / f"{option}.tex"
                tex.write_text(
                    rf"""\documentclass[10pt,twocolumn,letterpaper]{{article}}
\usepackage[{option}]{{cvpr}}
\begin{{document}}
\begin{{abstract}}Synthetic abstract.\end{{abstract}}
\end{{document}}
""",
                    encoding="utf-8",
                )
                rejected.append(
                    run_script(
                        AUDIT_TEX,
                        str(tex),
                        "--profile",
                        str(CVPR_PROFILE),
                        "--stage",
                        "camera_ready",
                        "--format",
                        "json",
                    )
                )

        self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
        for result in rejected:
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("CVPR26_STYLE_CURRENT", result.stdout)

    def test_cvpr_rebuttal_requires_rebuttal_mode_and_one_page(self):
        """Break caught: CVPR rebuttals use the paper style or exceed the one-page limit."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "rebuttal.tex"
            tex.write_text(
                r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage[rebuttal]{cvpr}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            source_result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "rebuttal",
                "--format",
                "json",
            )
            pdf = root / "rebuttal.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)
            writer.add_blank_page(width=612, height=792)
            with pdf.open("wb") as handle:
                writer.write(handle)
            pdf_result = run_script(
                AUDIT_PDF,
                str(pdf),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "rebuttal",
                "--format",
                "json",
            )

        self.assertEqual(0, source_result.returncode, source_result.stdout + source_result.stderr)
        self.assertEqual(1, pdf_result.returncode, pdf_result.stdout + pdf_result.stderr)
        self.assertIn("PDF_TOTAL_PAGE_LIMIT", pdf_result.stdout)

    def test_round_one_cvpr_rebuttal_rejects_missing_rebuttal_option(self):
        """Break caught: CVPR rebuttal sources pass with the paper-style invocation."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "rebuttal.tex"
            tex.write_text(
                r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(CVPR_PROFILE),
                "--stage",
                "rebuttal",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("CVPR26_STYLE_CURRENT", rule_ids)

    def test_icml_anonymous_submission_rejects_accepted_style_option(self):
        """Break caught: ICML's accepted flag is allowed before anonymous review ends."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "paper.tex"
            tex.write_text(
                r"""\documentclass[letterpaper]{article}
\usepackage[accepted]{icml2026}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section{Impact Statement}
Synthetic impact.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ICML_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("ICML26_STYLE_CURRENT", result.stdout)

    def test_icml_camera_ready_requires_accepted_option_and_impact_statement(self):
        """Break caught: ICML final sources omit accepted mode or the required Impact Statement."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = r"""\documentclass[letterpaper]{article}
\usepackage%s{icml2026}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
%s
\end{document}
"""
            missing_option = root / "missing-option.tex"
            missing_option.write_text(base % ("", r"\section{Impact Statement}"), encoding="utf-8")
            missing_heading = root / "missing-heading.tex"
            missing_heading.write_text(base % ("[accepted]", ""), encoding="utf-8")
            good = root / "good.tex"
            good.write_text(base % ("[accepted]", r"\section{Impact Statement}"), encoding="utf-8")
            missing_option_result = run_script(
                AUDIT_TEX, str(missing_option), "--profile", str(ICML_PROFILE), "--stage", "camera_ready", "--format", "json"
            )
            missing_heading_result = run_script(
                AUDIT_TEX, str(missing_heading), "--profile", str(ICML_PROFILE), "--stage", "camera_ready", "--format", "json"
            )
            good_result = run_script(
                AUDIT_TEX, str(good), "--profile", str(ICML_PROFILE), "--stage", "camera_ready", "--format", "json"
            )

        self.assertEqual(1, missing_option_result.returncode, missing_option_result.stdout + missing_option_result.stderr)
        self.assertIn("ICML26_STYLE_CURRENT", missing_option_result.stdout)
        self.assertEqual(1, missing_heading_result.returncode, missing_heading_result.stdout + missing_heading_result.stderr)
        self.assertIn("REQUIRED_HEADING", missing_heading_result.stdout)
        self.assertEqual(0, good_result.returncode, good_result.stdout + good_result.stderr)

    def test_icml_profile_uses_current_submission_and_final_file_size_limits(self):
        """Break caught: stale ICML 10 MB guidance replaces the current stage-specific limits."""
        profile = json.loads(ICML_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            {"anonymous_submission": 50, "camera_ready": 20},
            profile["pdf_contract"]["max_file_size_mb"],
        )

    def test_neurips_anonymous_submission_allows_default_or_main_and_rejects_final_or_preprint(self):
        """Break caught: NeurIPS anonymous sources accept a final or preprint style option."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = r"""\documentclass[letterpaper]{article}
\usepackage%s{neurips_2026}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section*{NeurIPS Paper Checklist}
Synthetic checklist.
\end{document}
"""
            accepted = []
            for suffix, options in (("default", ""), ("main", "[main]")):
                tex = root / f"{suffix}.tex"
                tex.write_text(base % options, encoding="utf-8")
                accepted.append(
                    run_script(
                        AUDIT_TEX, str(tex), "--profile", str(NEURIPS_PROFILE), "--stage", "anonymous_submission", "--format", "json"
                    )
                )
            rejected = []
            for suffix, options in (("final", "[final]"), ("preprint", "[preprint]")):
                tex = root / f"{suffix}.tex"
                tex.write_text(base % options, encoding="utf-8")
                rejected.append(
                    run_script(
                        AUDIT_TEX, str(tex), "--profile", str(NEURIPS_PROFILE), "--stage", "anonymous_submission", "--format", "json"
                    )
                )

        for result in accepted:
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for result in rejected:
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("NEURIPS26_STYLE_CURRENT", result.stdout)

    def test_neurips_camera_ready_requires_main_final_and_paper_checklist(self):
        """Break caught: NeurIPS final copies omit main/final mode or the paper checklist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = r"""\documentclass[letterpaper]{article}
\usepackage%s{neurips_2026}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
%s
\end{document}
"""
            missing_main = root / "missing-main.tex"
            missing_main.write_text(base % ("[final]", r"\section*{NeurIPS Paper Checklist}"), encoding="utf-8")
            missing_checklist = root / "missing-checklist.tex"
            missing_checklist.write_text(base % ("[main,final]", ""), encoding="utf-8")
            good = root / "good.tex"
            good.write_text(base % ("[main,final]", r"\section*{NeurIPS Paper Checklist}"), encoding="utf-8")
            missing_main_result = run_script(
                AUDIT_TEX, str(missing_main), "--profile", str(NEURIPS_PROFILE), "--stage", "camera_ready", "--format", "json"
            )
            missing_checklist_result = run_script(
                AUDIT_TEX, str(missing_checklist), "--profile", str(NEURIPS_PROFILE), "--stage", "camera_ready", "--format", "json"
            )
            good_result = run_script(
                AUDIT_TEX, str(good), "--profile", str(NEURIPS_PROFILE), "--stage", "camera_ready", "--format", "json"
            )

        self.assertEqual(1, missing_main_result.returncode, missing_main_result.stdout + missing_main_result.stderr)
        self.assertIn("NEURIPS26_STYLE_CURRENT", missing_main_result.stdout)
        self.assertEqual(1, missing_checklist_result.returncode, missing_checklist_result.stdout + missing_checklist_result.stderr)
        self.assertIn("REQUIRED_HEADING", missing_checklist_result.stdout)
        self.assertEqual(0, good_result.returncode, good_result.stdout + good_result.stderr)

    def test_round_one_neurips_camera_ready_rejects_main_without_final(self):
        """Break caught: NeurIPS camera-ready sources pass with main but without final mode."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass[letterpaper]{article}
\usepackage[main]{neurips_2026}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section*{NeurIPS Paper Checklist}
Synthetic checklist.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(NEURIPS_PROFILE),
                "--stage",
                "camera_ready",
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        rule_ids = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
        self.assertIn("NEURIPS26_STYLE_CURRENT", rule_ids)

    def test_neurips_profile_uses_current_submission_file_size_limit(self):
        """Break caught: NeurIPS submission size is read from stale instructions."""
        profile = json.loads(NEURIPS_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual({"anonymous_submission": 50}, profile["pdf_contract"]["max_file_size_mb"])

    def test_iclr_ai_use_disclosure_is_not_gated_on_one_exact_heading(self):
        """Break caught: ICLR rejects a truthful AI-use section only for using another heading."""
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "paper.tex"
            tex.write_text(
                r"""\documentclass{article}
\usepackage{iclr2027_conference}
\begin{document}
\begin{abstract}Synthetic abstract.\end{abstract}
\section*{Disclosure of AI Assistance}
No tools were used in this synthetic fixture.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script(
                AUDIT_TEX,
                str(tex),
                "--profile",
                str(ICLR_PROFILE),
                "--stage",
                "anonymous_submission",
                "--format",
                "json",
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_archive_audit_rejects_unsafe_paths_repository_metadata_and_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "supplement.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("README.md", "Prepared by Synthetic Author")
                handle.writestr(".git/config", "repository metadata")
                handle.writestr("../escape.txt", "unsafe")
                info = zipfile.ZipInfo("linked-file")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                handle.writestr(info, "target")
            result = run_script(
                AUDIT_ARCHIVE,
                str(archive),
                "--identity",
                "Synthetic Author",
                "--format",
                "json",
            )
            self.assertEqual(1, result.returncode)
            codes = {item["rule_id"] for item in json.loads(result.stdout)["findings"]}
            self.assertEqual(
                {"ARCHIVE_IDENTITY", "ARCHIVE_REPOSITORY_METADATA", "ARCHIVE_SYMLINK", "ARCHIVE_UNSAFE_PATH"},
                codes,
            )

    def test_archive_audit_redacts_untrusted_member_paths_and_identity_needles(self):
        """Break caught: raw archive member paths and identity needles reached public output."""
        unsafe_identity = "/private/tmp/synthetic-author"
        unsafe_member = f"{unsafe_identity}/supplement.tex"
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "supplement.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr(unsafe_member, "Synthetic supplementary material.")
            results = (
                (
                    "json",
                    run_script(
                        AUDIT_ARCHIVE,
                        str(archive),
                        "--identity",
                        unsafe_identity,
                        "--format",
                        "json",
                    ),
                ),
                (
                    "markdown",
                    run_script(
                        AUDIT_ARCHIVE,
                        str(archive),
                        "--identity",
                        unsafe_identity,
                        "--format",
                        "markdown",
                    ),
                ),
            )

        for output_format, result in results:
            with self.subTest(output_format=output_format):
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                output = result.stdout + result.stderr
                for forbidden in ("/private/tmp", unsafe_member, unsafe_identity, "Traceback"):
                    self.assertNotIn(forbidden, output)
                self.assertIn("ARCHIVE_UNSAFE_PATH", output)
                self.assertIn("ARCHIVE_IDENTITY", output)

                if output_format == "json":
                    report = json.loads(result.stdout)
                    self.assertEqual(1, report["schema_version"])
                    self.assertEqual(1, report["member_count"])
                    findings = {item["rule_id"]: item for item in report["findings"]}
                    self.assertEqual({"ARCHIVE_UNSAFE_PATH", "ARCHIVE_IDENTITY"}, set(findings))
                    self.assertEqual("P0", findings["ARCHIVE_UNSAFE_PATH"]["priority"])
                    self.assertEqual("P0", findings["ARCHIVE_IDENTITY"]["priority"])
                    self.assertEqual(
                        "A supplied identity pattern matched.",
                        findings["ARCHIVE_IDENTITY"]["observed"],
                    )
                    for finding in findings.values():
                        self.assertNotIn("/", finding["location"])
                        self.assertNotIn("\\", finding["location"])

    def test_archive_and_review_cli_outputs_are_path_free(self):
        """Break caught: archive and review CLIs expose local paths in their outputs."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "supplement.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("README.md", "Portable supplementary material.")
            archive_success = run_script(AUDIT_ARCHIVE, str(archive), "--format", "json")
            archive_missing = run_script(
                AUDIT_ARCHIVE,
                str(root / "missing-supplement.zip"),
                "--format",
                "json",
            )
            malformed_archive = root / "malformed-supplement.zip"
            malformed_archive.write_bytes(b"not a ZIP archive")
            archive_malformed = run_script(AUDIT_ARCHIVE, str(malformed_archive), "--format", "json")

            report = {
                "schema_version": 1,
                "venue": "Synthetic venue",
                "year": 2027,
                "stage": "anonymous_submission",
                "mode": "diagnose",
                "artifacts": [{"path": "paper.tex", "status": "observed"}],
                "sources": [],
                "findings": [],
                "limitations": [],
            }
            report_path = root / "report.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")
            review_success = run_script(VALIDATE_REPORT, str(report_path), "--format", "json")
            review_missing = run_script(
                VALIDATE_REPORT,
                str(root / "missing-report.json"),
                "--format",
                "json",
            )
            malformed_report = root / "malformed-report.json"
            malformed_report.write_text("{", encoding="utf-8")
            review_malformed = run_script(VALIDATE_REPORT, str(malformed_report), "--format", "json")
            non_utf8_report = root / "non-utf8-report.json"
            non_utf8_report.write_bytes(b"\xff")
            review_non_utf8 = run_script(VALIDATE_REPORT, str(non_utf8_report), "--format", "json")

        for label, result, expected_target in (
            ("archive success", archive_success, "supplement.zip"),
            ("review success", review_success, "report.json"),
        ):
            with self.subTest(case=label):
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(
                    expected_target,
                    json.loads(result.stdout)["target"],
                    result.stdout + result.stderr,
                )

        for label, result, basename, summary in (
            (
                "missing archive",
                archive_missing,
                "missing-supplement.zip",
                "FileNotFoundError: No such file or directory",
            ),
            (
                "malformed archive",
                archive_malformed,
                "malformed-supplement.zip",
                "BadZipFile",
            ),
            (
                "missing review report",
                review_missing,
                "missing-report.json",
                "FileNotFoundError: No such file or directory",
            ),
            (
                "malformed review report",
                review_malformed,
                "malformed-report.json",
                "invalid JSON at line 1, column 2",
            ),
            (
                "non-UTF-8 review report",
                review_non_utf8,
                "non-utf8-report.json",
                "UnicodeDecodeError",
            ),
        ):
            with self.subTest(case=label):
                self.assert_path_free_cli_error(result, root, basename, summary)

    def test_review_report_validator_accepts_valid_and_rejects_p0_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "report.json"
            report = {
                "schema_version": 1,
                "venue": "Synthetic venue",
                "year": 2027,
                "stage": "anonymous_submission",
                "mode": "diagnose",
                "artifacts": [{"path": "paper.tex", "status": "observed"}],
                "sources": [{"source_id": "OFFICIAL", "url": "https://example.org/rules", "checked_on": "2026-09-04", "status": "VERIFIED"}],
                "findings": [{
                    "id": "F1",
                    "basis": "official_hard_rule",
                    "priority": "P0",
                    "status": "observed",
                    "location": "paper.tex:4",
                    "observed": "Anonymous mode is disabled.",
                    "expected": "Anonymous mode is active.",
                    "impact": "Identity may be visible.",
                    "minimal_action": "Enable anonymous mode.",
                    "verification": "Rebuild and inspect the PDF.",
                    "sources": ["OFFICIAL"],
                }],
                "limitations": [],
            }
            report_path.write_text(json.dumps(report), encoding="utf-8")
            passed = run_script(VALIDATE_REPORT, str(report_path), "--format", "json")
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)

            report["findings"][0]["basis"] = "inference"
            report_path.write_text(json.dumps(report), encoding="utf-8")
            failed = run_script(VALIDATE_REPORT, str(report_path), "--format", "json")
            self.assertEqual(1, failed.returncode)
            self.assertIn("P0", failed.stdout)


if __name__ == "__main__":
    unittest.main()
