import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "skills" / "research-publication-pipeline"


class PublicReleaseDemoTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "installed skill"
        self.output = self.root / "demo output"
        shutil.copytree(SKILL, self.skill)

    def run_demo(self):
        return subprocess.run(
            [sys.executable, "-B", str(self.skill / "examples" / "run_demo.py"),
             str(self.output), "--with-public-release"],
            cwd=self.root, text=True, capture_output=True, check=False,
        )

    def replace_example(self, source):
        """Mutate the real bundled example in this test's isolated installed copy."""
        builder = self.skill / "examples" / "synthetic_workspace.py"
        builder.write_text(
            builder.read_text(encoding="utf-8")
            + "\nPUBLIC_RELEASE_FILES['src/example.py'] = " + repr(source) + "\n",
            encoding="utf-8",
        )

    def release_record(self):
        return json.loads(
            (self.output / "handoff" / "handoff.json").read_text(encoding="utf-8")
        )["public_release"]

    def test_copied_skill_rehearses_the_release_outside_the_source_tree(self):
        """Catch skipped execution, an in-place run, or outputs leaked into the release."""
        builder = self.skill / "examples" / "synthetic_workspace.py"
        guard = (
            "from pathlib import Path\n"
            f"assert Path.cwd() != Path({str(self.output / 'public-release')!r})\n"
        )
        builder.write_text(
            builder.read_text(encoding="utf-8")
            + "\nPUBLIC_RELEASE_FILES['tests/test_example.py'] = " + repr(guard)
            + " + PUBLIC_RELEASE_FILES['tests/test_example.py']\n",
            encoding="utf-8",
        )

        result = self.run_demo()

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("public-release: PASS", result.stdout)
        release = self.release_record()
        self.assertEqual("AUDITED", release["status"])
        self.assertEqual("PASS", release["rehearsal"]["status"])
        self.assertNotIn("public-release validator", release["rehearsal"]["not_run"])
        commands = release["rehearsal"]["commands"]
        self.assertEqual(2, len(commands))
        for command in commands:
            self.assertEqual(0, command["exit_code"])
            self.assertTrue(command["observed_outputs"])
        observed = json.loads(
            (self.output / "results" / "public-release-example.json").read_text(encoding="utf-8")
        )
        self.assertEqual({"count": 3, "total": 6}, observed)
        actual_files = {
            path.relative_to(self.output / "public-release").as_posix()
            for path in (self.output / "public-release").rglob("*") if path.is_file()
        }
        self.assertEqual({
            "README.md", "requirements.txt", "src/example.py", "examples/input.json",
            "docs/data.md", "docs/expected-output.md", "tests/test_example.py",
            "LICENSE", "CITATION.cff", "LIMITATIONS.md",
        }, actual_files)

    def test_nonzero_example_exit_cannot_be_recorded_as_a_passing_rehearsal(self):
        self.replace_example("raise SystemExit(7)\n")

        result = self.run_demo()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        release = self.release_record()
        self.assertEqual("FAILED", release["status"])
        self.assertEqual("FAILED", release["rehearsal"]["status"])
        self.assertEqual(7, release["rehearsal"]["commands"][0]["exit_code"])
        self.assertIn("tests/test_example.py", " ".join(release["rehearsal"]["not_run"]))
        self.assertIn("public-release validator", release["rehearsal"]["not_run"])
        self.assertNotIn("public-release: PASS", result.stdout)

    def test_zero_exit_with_wrong_result_cannot_pass_rehearsal(self):
        self.replace_example(
            "import sys\nfrom pathlib import Path\n"
            "Path(sys.argv[2]).write_text('{\"count\": 3, \"total\": 999}')\n"
            "print('completed')\n"
        )

        result = self.run_demo()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        release = self.release_record()
        self.assertEqual("FAILED", release["rehearsal"]["status"])
        self.assertEqual(0, release["rehearsal"]["commands"][0]["exit_code"])
        self.assertNotIn("public-release: PASS", result.stdout)

    def test_correct_file_with_wrong_stdout_cannot_pass_rehearsal(self):
        self.replace_example(
            "from pathlib import Path\n"
            "def summarize(values):\n"
            "    return {\"count\": len(values), \"total\": sum(values)}\n"
            "if __name__ == '__main__':\n"
            "    import sys\n"
            "    Path(sys.argv[2]).write_text('{\"count\": 3, \"total\": 6}')\n"
            "    print('{\"count\": 3, \"total\": 999}')\n"
        )

        result = self.run_demo()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        release = self.release_record()
        self.assertEqual("FAILED", release["rehearsal"]["status"])
        self.assertEqual(1, len(release["rehearsal"]["commands"]))
        self.assertEqual(0, release["rehearsal"]["commands"][0]["exit_code"])
        self.assertNotIn("public-release: PASS", result.stdout)

    def test_example_matching_the_demo_input_must_still_pass_its_tests(self):
        """Catch skipping tests when a hard-coded answer happens to fit the sample."""
        builder = self.skill / "examples" / "synthetic_workspace.py"
        builder.write_text(
            builder.read_text(encoding="utf-8")
            + "\nPUBLIC_RELEASE_FILES['src/example.py'] = "
            "PUBLIC_RELEASE_FILES['src/example.py'].replace('sum(values)', '6')\n",
            encoding="utf-8",
        )

        result = self.run_demo()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        release = self.release_record()
        self.assertEqual("FAILED", release["rehearsal"]["status"])
        commands = release["rehearsal"]["commands"]
        self.assertEqual(0, commands[0]["exit_code"])
        self.assertEqual(1, commands[1]["exit_code"])
        self.assertIn("public-release validator", release["rehearsal"]["not_run"])
        self.assertNotIn("tests/test_example.py", " ".join(release["rehearsal"]["not_run"]))
        self.assertNotIn("public-release: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
