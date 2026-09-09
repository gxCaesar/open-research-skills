import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "scientific-visualizations": ["build-scientific-visualizations"],
    "conference-manuscripts": ["prepare-conference-manuscripts"],
    "journal-manuscripts": ["prepare-journal-manuscripts"],
    "research-funding-proposals": ["writing-funding-proposals"],
    "research-publication-workflow": ["research-publication-pipeline"],
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


class PackageLayoutTest(unittest.TestCase):
    def test_index_matches_approved_packages(self):
        data = json.loads((ROOT / "package-index.json").read_text(encoding="utf-8"))
        observed = {item["name"]: item["skills"] for item in data["packages"]}
        self.assertEqual(EXPECTED, observed)

    def test_every_indexed_package_has_readme(self):
        for package in EXPECTED:
            self.assertTrue((ROOT / "packages" / package / "README.md").is_file(), package)

    def test_exactly_five_public_entrypoints(self):
        expected = {
            ROOT / "packages" / package / "skills" / skill / "SKILL.md"
            for package, skills in EXPECTED.items()
            for skill in skills
        }
        observed = set(ROOT.glob("packages/*/skills/*/SKILL.md"))
        self.assertEqual(expected, observed)
        self.assertEqual(5, len(list(ROOT.rglob("SKILL.md"))))

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
                    source = ROOT / "packages" / package / "skills" / skill_name
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

    def test_packages_do_not_keep_runtime_components_above_the_skill(self):
        """A package-level runtime directory would be absent from an exact skill install."""
        for package in EXPECTED:
            package_root = ROOT / "packages" / package
            with self.subTest(package=package):
                self.assertFalse((package_root / "components").exists())
                self.assertFalse((package_root / "shared").exists())

    def test_third_party_python_dependencies_are_skill_local_and_machine_readable(self):
        """Removing a declared runtime dependency file must break installed setup."""
        for package, expected_dependencies in REQUIRED_PYTHON_DEPENDENCIES.items():
            skill_name = EXPECTED[package][0]
            requirements = (
                ROOT / "packages" / package / "skills" / skill_name / "requirements.txt"
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
        """Component relocation must not leave documentation pointing at the old tree."""
        link_pattern = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
        observed = 0
        for package, skills in EXPECTED.items():
            package_root = ROOT / "packages" / package
            documents = [package_root / "README.md"]
            for skill in skills:
                documents.extend(sorted((package_root / "skills" / skill).rglob("*.md")))
            for document in documents:
                for raw_target in link_pattern.findall(document.read_text(encoding="utf-8")):
                    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
                    parsed = urlparse(target)
                    if parsed.scheme or target.startswith("#") or not parsed.path:
                        continue
                    observed += 1
                    resolved = document.parent / unquote(parsed.path)
                    with self.subTest(document=document, target=target):
                        self.assertTrue(resolved.is_file(), resolved)
        self.assertGreater(observed, 0)

    def test_skill_dir_command_targets_exist_inside_each_install_unit(self):
        """Command examples must not depend on an omitted package-level sibling."""
        target_pattern = re.compile(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)")
        forbidden_placeholders = ("<component-dir>", "<skill-dir>", "<figure-core>")
        observed = 0
        for package, skills in EXPECTED.items():
            for skill in skills:
                skill_root = ROOT / "packages" / package / "skills" / skill
                for document in sorted(skill_root.rglob("*.md")):
                    text = document.read_text(encoding="utf-8")
                    for placeholder in forbidden_placeholders:
                        self.assertNotIn(placeholder, text, document)
                    for relative in target_pattern.findall(text):
                        observed += 1
                        with self.subTest(document=document, target=relative):
                            self.assertTrue((skill_root / relative).exists(), relative)
        self.assertGreater(observed, 0)


if __name__ == "__main__":
    unittest.main()
