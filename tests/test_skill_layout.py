import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "scientific-visualizations": ["build-scientific-visualizations"],
    "conference-manuscripts": ["prepare-conference-manuscripts"],
    "journal-manuscripts": ["prepare-journal-manuscripts"],
    "research-funding-proposals": ["writing-funding-proposals"],
    "research-publication-workflow": ["research-publication-pipeline"],
    "method-development": ["develop-method-to-sota"],
    "survey-and-novelty": ["survey-and-audit-novelty"],
    "cold-review-panel": ["run-cold-review-panel"],
    "peer-review": ["review-others-manuscripts"],
    "artifact-release": ["release-research-artifacts"],
}
RUNTIME_PROBES = {
    "scientific-visualizations": (
        "build-scientific-visualizations",
        (
            "components/flowchart/guide.md",
            "components/compound-figure/guide.md",
            "components/journal-figure-set/guide.md",
            "shared/figure-core/scripts/init_figure_project.py",
        ),
        ("shared/figure-core/scripts/init_figure_project.py", "--help"),
    ),
    "conference-manuscripts": (
        "prepare-conference-manuscripts",
        (
            "components/venues/aaai/guide.md",
            "components/venues/aaai/references/venue-profile.json",
            "components/venues/iclr/guide.md",
            "components/venues/iclr/references/venue-profile.json",
            "components/venues/acl/guide.md",
            "components/venues/acl/references/venue-profile.json",
            "components/venues/cvpr/guide.md",
            "components/venues/cvpr/references/venue-profile.json",
            "components/venues/icml/guide.md",
            "components/venues/icml/references/venue-profile.json",
            "components/venues/neurips/guide.md",
            "components/venues/neurips/references/venue-profile.json",
            "components/venues/generic/guide.md",
            "components/venues/generic/references/venue-profile.template.json",
            "components/abstract/scripts/check_abstract.py",
            "components/statistics-reporting/scripts/validate_analysis_register.py",
            "components/manuscript-core/scripts/audit_tex.py",
        ),
        ("components/manuscript-core/scripts/audit_tex.py", "--help"),
    ),
    "journal-manuscripts": (
        "prepare-journal-manuscripts",
        (
            "components/abstract/guide.md",
            "components/statistics-reporting/guide.md",
            "components/data-availability/guide.md",
        ),
        ("components/abstract/scripts/check_abstract.py", "--help"),
    ),
    "research-funding-proposals": (
        "writing-funding-proposals",
        (
            "scripts/init_proposal_workspace.py",
            "scripts/validate_proposal_workspace.py",
            "references/authority-and-policy.md",
        ),
        ("scripts/validate_proposal_workspace.py", "--help"),
    ),
    "research-publication-workflow": (
        "research-publication-pipeline",
        (
            "components/paper-card/guide.md",
            "components/paper-card/scripts/prepare_paper.py",
            "scripts/init_publication_project.py",
        ),
        ("components/paper-card/scripts/prepare_paper.py", "--help"),
    ),
    "method-development": (
        "develop-method-to-sota",
        (
            "scripts/check_iteration_ledger.py",
            "examples/iteration-ledger/clean.json",
            "references/component-iteration.md",
        ),
        ("scripts/check_iteration_ledger.py", "examples/iteration-ledger/clean.json"),
    ),
    "survey-and-novelty": (
        "survey-and-audit-novelty",
        (
            "scripts/check_survey_ledger.py",
            "examples/survey-ledger/clean.json",
            "references/kill-layers.md",
        ),
        ("scripts/check_survey_ledger.py", "examples/survey-ledger/clean.json"),
    ),
}
REQUIRED_PYTHON_DEPENDENCIES = {
    "scientific-visualizations": {
        "matplotlib",
        "pillow",
        "pypdf",
    },
    "conference-manuscripts": {"pypdf"},
    "research-publication-workflow": {"pypdf"},
}


def local_markdown_findings(document, boundary):
    """Inspect actual inline links and images without leaving an install boundary."""
    findings = []
    text = document.read_text(encoding="utf-8")
    for raw in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", text):
        target = raw.strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlparse(target)
        if parsed.scheme or not parsed.path:
            continue
        resolved = (document.parent / unquote(parsed.path)).resolve()
        if not resolved.is_relative_to(boundary.resolve()):
            findings.append((target, "link leaves its installation boundary"))
        elif not resolved.exists():
            findings.append((target, "linked resource is missing"))
    return findings


DECLARED_SKILLS = tuple(skill for skills in EXPECTED.values() for skill in skills)


def entrypoint_findings(root: Path, declared: Sequence[str]) -> list[str]:
    """SKILL.md files the release does not declare, and declared ones it lacks."""
    expected = {root / "skills" / name / "SKILL.md" for name in declared}
    observed = set(root.rglob("SKILL.md"))
    return sorted(str(path.relative_to(root)) for path in observed ^ expected)


class SkillLayoutTest(unittest.TestCase):
    def test_index_matches_the_flat_install_units(self):
        data = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        self.assertEqual(1, data["schema_version"])
        expected = {
            skill: {
                "name": skill,
                "entrypoint": f"skills/{skill}/SKILL.md",
                "guide": f"docs/{slug}.md",
            }
            for slug, skills in EXPECTED.items() for skill in skills
        }
        observed = {item["name"]: item for item in data["skills"]}
        self.assertEqual(len(expected), len(data["skills"]))
        self.assertEqual(expected, observed)
        self.assertFalse((ROOT / "package-index.json").exists())

    def test_every_indexed_skill_has_a_guide_and_test_suite(self):
        for slug in EXPECTED:
            self.assertTrue((ROOT / "docs" / f"{slug}.md").is_file(), slug)
            self.assertTrue(list((ROOT / "tests" / slug).glob("test_*.py")), slug)
        for name in ("README.md", "CONTRIBUTING.md", "MAINTAINERS.md", "LICENSE", "NOTICE", "THIRD_PARTY.md"):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_exactly_the_declared_public_entrypoints(self):
        self.assertEqual([], entrypoint_findings(ROOT, DECLARED_SKILLS))

    def test_an_undeclared_entrypoint_is_rejected(self):
        """An extra SKILL.md anywhere in the tree must be reported, not absorbed."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in DECLARED_SKILLS:
                entry = root / "skills" / name / "SKILL.md"
                entry.parent.mkdir(parents=True)
                entry.write_text("stub\n", encoding="utf-8")
            self.assertEqual([], entrypoint_findings(root, DECLARED_SKILLS))
            stray = root / "skills" / "vendored" / "inner" / "SKILL.md"
            stray.parent.mkdir(parents=True)
            stray.write_text("stub\n", encoding="utf-8")
            self.assertEqual(
                ["skills/vendored/inner/SKILL.md"],
                entrypoint_findings(root, DECLARED_SKILLS),
            )

    def test_release_tree_contains_no_symlink(self):
        links = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)

    def test_no_skill_is_installed_at_release_root(self):
        self.assertFalse((ROOT / "SKILL.md").exists())
        for child in ROOT.iterdir():
            if child.is_dir():
                self.assertFalse((child / "SKILL.md").exists(), child.name)

    def test_each_exact_skill_directory_is_a_standalone_install(self):
        """Moving runtime resources above SKILL.md must break this test."""
        with tempfile.TemporaryDirectory() as tmp:
            install_root = Path(tmp)
            for package, (skill_name, resources, probe) in RUNTIME_PROBES.items():
                with self.subTest(package=package):
                    source = ROOT / "skills" / skill_name
                    installed = install_root / skill_name
                    shutil.copytree(source, installed)
                    for relative in resources:
                        self.assertTrue((installed / relative).is_file(), relative)
                    result = subprocess.run(
                        [sys.executable, "-B", str(installed / probe[0]), *probe[1:]],
                        cwd=installed,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_runtime_components_are_not_kept_above_the_install_units(self):
        """Root runtime siblings would be absent from an exact skill install."""
        self.assertFalse((ROOT / "packages").exists())
        for parent in (ROOT, ROOT / "skills"):
            self.assertFalse((parent / "components").exists())
            self.assertFalse((parent / "shared").exists())

    def test_third_party_python_dependencies_are_skill_local_and_machine_readable(self):
        """Removing a declared runtime dependency file must break installed setup."""
        for package, expected_dependencies in REQUIRED_PYTHON_DEPENDENCIES.items():
            skill_name = EXPECTED[package][0]
            requirements = (
                ROOT / "skills" / skill_name / "requirements.txt"
            )
            with self.subTest(package=package):
                self.assertTrue(requirements.is_file())
                observed = {
                    line.split("=", 1)[0].split("<", 1)[0].split(">", 1)[0].strip().casefold()
                    for line in requirements.read_text(encoding="utf-8").splitlines()
                    if line.strip() and not line.lstrip().startswith("#")
                }
                self.assertTrue(expected_dependencies.issubset(observed), observed)

    def test_local_markdown_links_survive_exact_skill_moves(self):
        """Guides may cross the repository; installed skills may not depend on siblings."""
        documents = {document: ROOT for document in ROOT.glob("*.md")}
        documents.update({document: ROOT for document in (ROOT / "docs").rglob("*.md")})
        for skills in EXPECTED.values():
            for skill in skills:
                boundary = ROOT / "skills" / skill
                documents.update({document: boundary for document in boundary.rglob("*.md")})
        self.assertTrue(documents)
        for document, boundary in documents.items():
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertEqual([], local_markdown_findings(document, boundary))

    def test_missing_or_sibling_link_mutation_is_rejected(self):
        """Mutating a real guide must reveal a missing file or an install escape."""
        source = ROOT / "skills" / "writing-funding-proposals" / "examples"
        with tempfile.TemporaryDirectory() as tmp:
            installed = Path(tmp) / "installed"
            shutil.copytree(source, installed / "examples")
            document = installed / "examples" / "README.md"
            original = document.read_text(encoding="utf-8")
            self.assertEqual([], local_markdown_findings(document, installed))
            target = "section-brief-walkthrough.md"
            self.assertIn(f"]({target})", original)
            document.write_text(original.replace(f"]({target})", "](missing-example.md)", 1), encoding="utf-8")
            self.assertEqual(
                [("missing-example.md", "linked resource is missing")],
                local_markdown_findings(document, installed),
            )
            shutil.copyfile(source / target, Path(tmp) / "outside-guide.md")
            document.write_text(original.replace(f"]({target})", "](../../outside-guide.md)", 1), encoding="utf-8")
            self.assertEqual(
                [("../../outside-guide.md", "link leaves its installation boundary")],
                local_markdown_findings(document, installed),
            )

    def test_skill_dir_command_targets_exist_inside_each_install_unit(self):
        """Command examples must not depend on an omitted package-level sibling."""
        target_pattern = re.compile(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)")
        forbidden_placeholders = ("<component-dir>", "<skill-dir>", "<figure-core>")
        observed = 0
        for package, skills in EXPECTED.items():
            for skill in skills:
                skill_root = ROOT / "skills" / skill
                for document in sorted(skill_root.rglob("*.md")):
                    text = document.read_text(encoding="utf-8")
                    for placeholder in forbidden_placeholders:
                        self.assertNotIn(placeholder, text, document)
                    for relative in target_pattern.findall(text):
                        observed += 1
                        with self.subTest(document=document, target=relative):
                            self.assertTrue((skill_root / relative).exists(), relative)
                            self.assertTrue((skill_root / relative).resolve().is_relative_to(skill_root.resolve()), relative)
        self.assertGreater(observed, 0)


if __name__ == "__main__":
    unittest.main()
