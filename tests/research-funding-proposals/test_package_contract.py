import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILLS = PACKAGE / "skills"


class FundingPackageContractTest(unittest.TestCase):
    def test_package_exposes_one_funding_skill(self):
        observed = {
            path.parent.name
            for path in (SKILLS / "writing-funding-proposals").rglob("SKILL.md")
        }
        self.assertEqual({"writing-funding-proposals"}, observed)

    def test_skill_has_portable_tools_and_profiles(self):
        skill = SKILLS / "writing-funding-proposals"
        required = [
            "scripts/init_proposal_workspace.py",
            "scripts/validate_proposal_workspace.py",
            "scripts/audit_chinese_prose.py",
            "references/profiles/nsfc-2026.md",
            "references/profiles/guangdong-2026.md",
            "references/commitment-calibration.md",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((skill / relative).is_file())

    def test_skill_calibrates_scientific_commitments(self):
        skill = SKILLS / "writing-funding-proposals"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        for commitment in (
            "deliverable mainline",
            "cautious exploration",
            "boundary confirmation",
        ):
            self.assertIn(commitment, text)

    def test_package_contains_no_symlinks_or_private_profiles(self):
        links = [str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)
        private_prefix = "c" + "gx"
        forbidden_names = {
            f"{private_prefix}-corpus-register.csv",
            f"{private_prefix}-writing-patterns.md",
        }
        observed = {path.name for path in PACKAGE.rglob("*")}
        self.assertTrue(forbidden_names.isdisjoint(observed))


if __name__ == "__main__":
    unittest.main()
