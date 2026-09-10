import json
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
SKILL = PACKAGE / "skills" / "prepare-conference-manuscripts"
EXPECTED_SKILLS = {"prepare-conference-manuscripts"}
EXPECTED_MODES = {
    "recon",
    "draft",
    "audit",
    "polish",
    "rebuttal",
    "camera-ready",
    "package",
}
FORMAL_VENUES = ("aaai", "iclr", "acl", "cvpr", "icml", "neurips", "iccv")
FORMAL_VENUE_SCOPES = (
    ("AAAI", "AAAI-27 Main Technical Track"),
    ("ICLR", "ICLR 2027 Conference"),
    ("ACL", "ACL 2026 Main Conference through ARR"),
    ("CVPR", "CVPR 2026 Main Conference"),
    ("ICML", "ICML 2026 Main Track"),
    ("NeurIPS", "NeurIPS 2026 Main Track"),
    ("ICCV", "ICCV 2025 Main Conference"),
)
FORMAL_ADAPTER_PROFILES = {
    "aaai": {
        "routing_label": "AAAI",
        "routing_scope": "AAAI-27 Main Technical Track",
        "venue": "AAAI-27",
        "year": 2027,
        "track": "Main Technical Track",
        "checked_on": "2026-09-04",
    },
    "iclr": {
        "routing_label": "ICLR",
        "routing_scope": "ICLR 2027 Conference",
        "venue": "ICLR 2027",
        "year": 2027,
        "track": "Conference",
        "checked_on": "2026-09-04",
    },
    "acl": {
        "routing_label": "ACL",
        "routing_scope": "ACL 2026 Main Conference through ARR",
        "venue": "ACL 2026",
        "year": 2026,
        "track": "Main Conference through ACL Rolling Review",
        "checked_on": "2026-09-04",
    },
    "cvpr": {
        "routing_label": "CVPR",
        "routing_scope": "CVPR 2026 Main Conference",
        "venue": "CVPR 2026",
        "year": 2026,
        "track": "Main Conference",
        "checked_on": "2026-09-04",
    },
    "icml": {
        "routing_label": "ICML",
        "routing_scope": "ICML 2026 Main Track",
        "venue": "ICML 2026",
        "year": 2026,
        "track": "Main Track",
        "checked_on": "2026-09-04",
    },
    "neurips": {
        "routing_label": "NeurIPS",
        "routing_scope": "NeurIPS 2026 Main Track",
        "venue": "NeurIPS 2026",
        "year": 2026,
        "track": "Main Track",
        "checked_on": "2026-09-04",
    },
    # ICCV is biennial. The dated scope is the most recent completed cycle, because the
    # 2027 author-guideline page returned HTTP 404 when this adapter was written.
    "iccv": {
        "routing_label": "ICCV",
        "routing_scope": "ICCV 2025 Main Conference",
        "venue": "ICCV 2025",
        "year": 2025,
        "track": "Main Conference",
        "checked_on": "2026-09-10",
    },
}
VENUE_CONTRACT_FILES = (
    "guide.md",
    "references/official-sources.md",
    "references/stage-matrix.md",
    "references/venue-profile.json",
    "references/published-paper-observations.md",
)


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def source_statuses(path: Path) -> dict[str, str]:
    statuses = {}
    status_index = None
    in_registry = False
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not in_registry:
            if cells and cells[0] == "ID" and "Status" in cells:
                status_index = cells.index("Status")
                in_registry = True
            continue
        if not line.strip() or not line.lstrip().startswith("|") or len(cells) <= status_index:
            break
        if cells[0].startswith("`") and cells[0].endswith("`"):
            statuses[cells[0].strip("`")] = cells[status_index].strip("`")
    return statuses


class ConferencePackageContractTest(unittest.TestCase):
    def test_package_exposes_one_skill(self):
        observed = {
            path.parent.name for path in SKILL.rglob("SKILL.md")
        }
        self.assertEqual(EXPECTED_SKILLS, observed)

    def test_entrypoint_routes_lifecycle_modes(self):
        skill = SKILL / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        for mode in EXPECTED_MODES:
            self.assertIn(f"`{mode}`", text)

    def test_entrypoint_description_includes_conference_statistics_or_evaluation_report(self):
        """Break caught: conference statistical reporting does not select this skill."""
        first_line = (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()[2]
        self.assertIn("statistical", first_line.casefold())
        self.assertIn("evaluation report", first_line.casefold())
        self.assertIn("rebuttal", first_line.casefold())

    def test_entrypoint_routes_all_formal_adapters_by_venue_year_and_track(self):
        """Break caught: a first-class adapter is omitted or generic becomes its default."""
        text = normalized_text(SKILL / "SKILL.md")
        for venue in FORMAL_VENUES:
            with self.subTest(venue=venue):
                self.assertIn(f"](components/venues/{venue}/guide.md)", text)
        for venue, scope in FORMAL_VENUE_SCOPES:
            with self.subTest(venue=venue, scope=scope):
                self.assertIn(f"| {venue} | {scope} |", text)
        self.assertIn("venue/year/track", text)
        self.assertIn(
            "If the requested venue/year/track differs from the dated scope, if a profile is stale, "
            "or if its current authority is uncertain, run `recon` before drafting, auditing, or "
            "packaging.",
            text,
        )
        self.assertIn(
            "Use [generic venue-profile](components/venues/generic/guide.md) only when no current "
            "first-class profile matches; create a dated task-local profile from current official "
            "sources and do not mutate a bundled profile to impersonate another venue.",
            text,
        )
        self.assertIn(
            "The linked paper observations are optional empirical drafting evidence. They can inform "
            "writing choices after official authority is resolved, but they never define venue rules, "
            "mandatory section order, or a replacement for current first-party instructions.",
            text,
        )

    def test_formal_adapter_profiles_match_their_exact_routing_scopes(self):
        """Break caught: a routed adapter profile can silently identify a different venue scope."""
        routing_table = normalized_text(SKILL / "SKILL.md")
        for adapter, expected in FORMAL_ADAPTER_PROFILES.items():
            with self.subTest(adapter=adapter):
                profile = json.loads(
                    (
                        SKILL
                        / "components"
                        / "venues"
                        / adapter
                        / "references"
                        / "venue-profile.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(
                    {
                        "venue": expected["venue"],
                        "year": expected["year"],
                        "track": expected["track"],
                        "checked_on": expected["checked_on"],
                    },
                    {
                        key: profile[key]
                        for key in ("venue", "year", "track", "checked_on")
                    },
                )
                self.assertIn(
                    f"| {expected['routing_label']} | {expected['routing_scope']} |",
                    routing_table,
                )

    def test_package_readme_links_all_formal_adapters_and_their_currency_boundary(self):
        """Break caught: an installed package leaves a formal venue undiscoverable or stale."""
        text = normalized_text(PACKAGE / "docs" / "conference-manuscripts.md")
        prefix = "../skills/prepare-conference-manuscripts/components/venues"
        for venue in FORMAL_VENUES:
            with self.subTest(venue=venue):
                self.assertIn(f"]({prefix}/{venue}/guide.md)", text)
        self.assertIn(
            "按准确的 `venue/year/track` 选择适配器。每份 profile 都是有日期的工程辅助； "
            "若范围过时、不匹配目标投稿或当前权威性不确定，先依据当前第一方来源运行 `recon`。",
            text,
        )
        self.assertIn(
            "只有没有匹配的当前正式 profile 时才使用 generic；创建任务内 profile，不修改捆绑 profile 来冒充其他范围。",
            text,
        )
        self.assertIn(
            "各正式适配器链接的已发表论文观察只是可选的经验性写作证据，不是会议规则，也不是强制章节顺序。",
            text,
        )

    def test_formal_venue_components_include_the_required_local_contract(self):
        """Break caught: a formal venue adapter ships without a required local artifact."""
        for venue in FORMAL_VENUES:
            component = SKILL / "components" / "venues" / venue
            for relative_path in VENUE_CONTRACT_FILES:
                with self.subTest(venue=venue, artifact=relative_path):
                    self.assertTrue((component / relative_path).is_file(), venue)
            with self.subTest(venue=venue, artifact="nested SKILL.md"):
                self.assertEqual([], list(component.rglob("SKILL.md")), venue)

    def test_round_one_venue_component_directories_match_the_supported_adapter_set(self):
        """Break caught: a stale or undeclared adapter leaks into venue routing."""
        venues = SKILL / "components" / "venues"
        observed = {path.name for path in venues.iterdir() if path.is_dir()}
        self.assertEqual(
            {"aaai", "iclr", "acl", "cvpr", "icml", "neurips", "iccv", "generic"}, observed
        )

    def test_formal_venue_rule_sources_are_documented_locally(self):
        """Break caught: an emitted venue rule points to an undocumented source ID."""
        for venue in FORMAL_VENUES:
            component = SKILL / "components" / "venues" / venue
            profile = json.loads(
                (component / "references" / "venue-profile.json").read_text(encoding="utf-8")
            )
            documented_sources = (component / "references" / "official-sources.md").read_text(encoding="utf-8")
            for rule_id, source_ids in profile["rule_sources"].items():
                for source_id in source_ids:
                    with self.subTest(venue=venue, rule_id=rule_id, source_id=source_id):
                        self.assertIn(f"`{source_id}`", documented_sources)

    def test_formal_profile_rule_sources_are_verified(self):
        """Break caught: a formal profile binds a rule to unavailable authority."""
        for venue in FORMAL_VENUES:
            component = SKILL / "components" / "venues" / venue
            profile = json.loads(
                (component / "references" / "venue-profile.json").read_text(encoding="utf-8")
            )
            statuses = source_statuses(component / "references" / "official-sources.md")
            for rule_id, source_ids in profile["rule_sources"].items():
                for source_id in source_ids:
                    with self.subTest(venue=venue, rule_id=rule_id, source_id=source_id):
                        self.assertIn(source_id, statuses)
                        self.assertEqual("VERIFIED", statuses[source_id])

    def test_source_statuses_ignores_later_code_id_tables(self):
        """Break caught: a later Markdown table can inject a source-registry status."""
        with tempfile.TemporaryDirectory() as tmp:
            sources = Path(tmp) / "official-sources.md"
            sources.write_text(
                "\n".join(
                    (
                        "# Synthetic official sources",
                        "",
                        "| ID | Status | Official source | Scope |",
                        "|---|---|---|---|",
                        "| `REGISTRY_SOURCE` | `VERIFIED` | <https://example.org/rules> | scope |",
                        "",
                        "The following table is unrelated to the source registry.",
                        "",
                        "| Code ID | Status | Meaning |",
                        "|---|---|---|",
                        "| `INJECTED_SOURCE` | `VERIFIED` | unrelated code |",
                        "",
                    )
                ),
                encoding="utf-8",
            )

            statuses = source_statuses(sources)

        self.assertEqual({"REGISTRY_SOURCE": "VERIFIED"}, statuses)

    def test_aaai_and_iclr_source_statuses_bound_their_authority(self):
        """Break caught: unavailable or unobserved source evidence looks rule-bearing."""
        aaai_sources = SKILL / "components" / "venues" / "aaai" / "references" / "official-sources.md"
        iclr_sources = SKILL / "components" / "venues" / "iclr" / "references" / "official-sources.md"
        aaai_text = normalized_text(aaai_sources)
        iclr_text = normalized_text(iclr_sources)

        self.assertIn("| ID | Official source | Status | Scope at the checked date |", aaai_text)
        self.assertEqual(
            {
                "AAAI27_SUBMISSION": "VERIFIED",
                "AAAI27_MAIN_CALL": "VERIFIED",
                "AAAI27_AUTHOR_POLICY": "COULD_NOT_OPEN",
                "AAAI_PUBLICATION_POLICY": "VERIFIED",
            },
            {
                source_id: source_statuses(aaai_sources).get(source_id)
                for source_id in (
                    "AAAI27_SUBMISSION",
                    "AAAI27_MAIN_CALL",
                    "AAAI27_AUTHOR_POLICY",
                    "AAAI_PUBLICATION_POLICY",
                )
            },
        )
        self.assertIn(
            "`AAAI27_AUTHOR_POLICY` is `COULD_NOT_OPEN`; it does not support any hard rule in this profile.",
            aaai_text,
        )

        self.assertIn("| ID | Official source | Status | Scope at the checked date |", iclr_text)
        self.assertEqual(
            {
                "ICLR27_AUTHOR_GUIDE": "VERIFIED",
                "ICLR27_AI_POLICY": "VERIFIED",
                "ICLR27_REVIEWER_GUIDE": "VERIFIED",
                "ICLR27_CALL": "VERIFIED",
            },
            {
                source_id: source_statuses(iclr_sources).get(source_id)
                for source_id in (
                    "ICLR27_AUTHOR_GUIDE",
                    "ICLR27_AI_POLICY",
                    "ICLR27_REVIEWER_GUIDE",
                    "ICLR27_CALL",
                )
            },
        )
        self.assertIn(
            "Current portal fields and enabled actions remain `UNVERIFIED` until directly observed.",
            iclr_text,
        )

    def test_local_components_are_not_extra_trigger_skills(self):
        for component in ("abstract", "manuscript-core", "statistics-reporting"):
            with self.subTest(component=component):
                root = SKILL / "components" / component
                self.assertTrue(root.is_dir())
                self.assertFalse((root / "SKILL.md").exists())

    def test_skill_declares_the_pdf_auditor_dependency(self):
        """Break caught: a fresh install cannot import the bundled PDF auditor."""
        requirements = SKILL / "requirements.txt"
        self.assertTrue(requirements.is_file(), requirements)
        declared = {
            line.strip().casefold()
            for line in requirements.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("pypdf==6.10.2", declared)

    def test_package_contains_no_symlinks(self):
        links = [str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob("*") if path.is_symlink()]
        self.assertEqual([], links)


if __name__ == "__main__":
    unittest.main()
