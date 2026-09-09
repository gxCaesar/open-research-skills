import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "build-scientific-visualizations": (
        "scientific-visualizations",
        ("scientific figure", "flowchart", "method schematic"),
        ("layout-sketch", "conference-figure-set", "journal-figure-set"),
    ),
    "prepare-conference-manuscripts": (
        "conference-manuscripts",
        ("conference manuscript", "AAAI", "ICLR", "rebuttal"),
        ("camera-ready", "venue profile", "locked scientific contract"),
    ),
    "prepare-journal-manuscripts": (
        "journal-manuscripts",
        ("journal manuscript", "cover letter", "data availability", "revise and resubmit"),
        ("editor-pack", "revision-response", "locked scientific contract"),
    ),
    "writing-funding-proposals": (
        "research-funding-proposals",
        ("funding proposal", "NSFC", "Guangdong"),
        ("deliverable mainline", "cautious exploration", "boundary confirmation"),
    ),
    "research-publication-pipeline": (
        "research-publication-workflow",
        ("research route", "data feasibility", "scoop", "headroom"),
        ("survey", "pilot", "freeze", "public-release"),
    ),
    "develop-method-to-sota": (
        "method-development",
        ("baseline", "state of the art", "headroom", "ablation control"),
        ("headroom-measure", "error-slices", "single-component", "exit-decision"),
    ),
    "survey-and-audit-novelty": (
        "survey-and-novelty",
        ("literature survey", "novelty audit", "prior art", "scoop"),
        ("contribution-lane", "joint-variable-audit", "search-angles", "kill-layer"),
    ),
    "run-cold-review-panel": (
        "cold-review-panel",
        ("mock review", "simulated reviewer", "pre-submission review", "red-team"),
        ("isolation-manifest", "lens-assignment", "artifact-execution", "meta-review"),
    ),
    "review-others-manuscripts": (
        "peer-review",
        ("invited referee", "referee report", "reviewer comments", "editorial prescreen"),
        ("initial-review", "revision-round", "editorial-prescreen", "confidentiality"),
    ),
    "release-research-artifacts": (
        "artifact-release",
        ("anonymized repository", "double-blind", "DOI", "artifact evaluation"),
        ("anonymized-submission", "named-archive", "data-card", "manifest-verification"),
    ),
}
LEGACY_ENTRYPOINTS = {
    "flowchart",
    "build-nature-style-scientific-figures",
    "research-figs-journal",
    "prepare-aaai-manuscripts",
    "prepare-iclr-manuscripts",
    "research-abstract-craft",
    "research-paper-card",
    "research-statistics",
    "research-data-availability",
}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    current = ""
    for line in match.group(1).splitlines():
        if line.startswith("  ") and current:
            fields[current] = f"{fields[current]} {line.strip()}".strip()
            continue
        key, separator, value = line.partition(":")
        if separator:
            current = key.strip()
            fields[current] = value.strip().lstrip(">-").strip()
    return fields


class TriggerBoundaryTest(unittest.TestCase):
    def test_frontmatter_descriptions_and_body_modes_are_discoverable(self):
        for skill, (package, triggers, modes) in SKILLS.items():
            path = ROOT / "skills" / skill / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            metadata = frontmatter(text)
            self.assertEqual(skill, metadata.get("name"), path)
            self.assertTrue(metadata.get("description", "").startswith("Use when"), path)
            description = metadata["description"].casefold()
            for phrase in triggers:
                self.assertIn(phrase.casefold(), description, f"{path}: {phrase}")
            body = text.casefold()
            for mode in modes:
                self.assertIn(mode.casefold(), body, f"{path}: {mode}")

    def test_declared_trigger_cases_have_one_existing_owner(self):
        cases = json.loads((ROOT / "tests" / "trigger-cases.json").read_text(encoding="utf-8"))
        owners = set(SKILLS)
        observed_ids = set()
        for case in cases["cases"]:
            self.assertNotIn(case["id"], observed_ids)
            observed_ids.add(case["id"])
            self.assertIn(case["owner"], owners)
            handoff = case.get("handoff")
            if handoff is not None:
                self.assertIn(handoff, owners)
                self.assertNotEqual(case["owner"], handoff)
            self.assertTrue(case["request"].strip())
            self.assertTrue(case["reason"].strip())

    def test_index_exposes_no_legacy_entrypoint(self):
        data = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
        names = {skill["name"] for skill in data["skills"]}
        self.assertTrue(LEGACY_ENTRYPOINTS.isdisjoint(names), names & LEGACY_ENTRYPOINTS)


if __name__ == "__main__":
    unittest.main()
