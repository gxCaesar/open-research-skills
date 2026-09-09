#!/usr/bin/env python3
"""Create a portable, human-facing research publication workspace."""

import argparse
import json
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "assets" / "templates"

JSON_TARGETS = {
    "project.json": Path("project.json"),
    "source-register.json": Path("evidence/source-register.json"),
    "intake.json": Path("intake/intake.json"),
    "protocol.json": Path("protocol/protocol.json"),
    "headroom.json": Path("development/headroom.json"),
    "iteration-ledger.json": Path("development/iteration-ledger.json"),
    "claim-register.json": Path("claims/claim-register.json"),
    "handoff.json": Path("handoff/handoff.json"),
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def ensure_empty_target(target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise ValueError(f"target exists and is not a directory: {target}")
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"refusing to overwrite non-empty directory: {target}")
    target.mkdir(parents=True, exist_ok=True)


def initialize(args: argparse.Namespace) -> Path:
    target = Path(args.project).expanduser().resolve()
    ensure_empty_target(target)

    for source_name, relative_target in JSON_TARGETS.items():
        payload = read_json(TEMPLATES / source_name)
        write_json(target / relative_target, payload)

    project = read_json(target / "project.json")
    project.update(
        {
            "project_id": args.project_id,
            "title": args.title,
            "domain": args.domain,
            "contribution_lane": args.contribution_lane,
        }
    )
    write_json(target / "project.json", project)

    intake = read_json(target / "intake" / "intake.json")
    intake["scoop"]["contribution_lane"] = args.contribution_lane
    write_json(target / "intake" / "intake.json", intake)

    protocol = read_json(target / "protocol" / "protocol.json")
    protocol["contribution_lane"] = args.contribution_lane
    write_json(target / "protocol" / "protocol.json", protocol)

    shutil.copyfile(TEMPLATES / "START_HERE.md", target / "START_HERE.md")
    (target / "public-release").mkdir()
    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="new publication workspace directory")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument(
        "--contribution-lane",
        required=True,
        choices=("sota-method", "discovery", "benchmark"),
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        target = initialize(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"created publication workspace: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
