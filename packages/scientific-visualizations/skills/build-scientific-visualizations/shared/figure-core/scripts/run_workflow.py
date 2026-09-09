#!/usr/bin/env python3
"""Run validation, vector rendering, composition and QA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


SCRIPTS = Path(__file__).resolve().parent


def run(name: str, project: Path, *extra: str) -> None:
    subprocess.run([sys.executable, str(SCRIPTS / name), str(project), *extra], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--package", action="store_true")
    parser.add_argument("--phase", choices=["layout", "final"], default="final")
    parser.add_argument(
        "--direct-composite",
        action="store_true",
        help="validate and QA a natively rendered composite already present in outputs/summary",
    )
    args = parser.parse_args()
    project = args.project.resolve()
    if args.phase == "layout":
        run("validate_figure_project.py", project, "--stage", "layout")
        spec = json.loads((project / "figure_spec.json").read_text(encoding="utf-8"))
        if spec.get("schema_version") != "1.2":
            print(
                json.dumps(
                    {
                        "status": "PASS",
                        "phase": "layout",
                        "mode": "validation-only",
                        "schema_version": spec.get("schema_version"),
                    },
                    sort_keys=True,
                )
            )
            return
        run("render_layout_proof.py", project)
        return

    run(
        "validate_figure_project.py",
        project,
        "--stage",
        "final",
        "--allow-missing-outputs",
    )
    if args.direct_composite:
        spec = json.loads((project / "figure_spec.json").read_text(encoding="utf-8"))
        if spec.get("delivery_mode", "panel_set") != "composite":
            raise SystemExit("--direct-composite requires delivery_mode: composite")
        stem = project / "outputs" / "summary" / f"{spec['figure_id']}_complete"
        missing = [str(stem.with_suffix(extension)) for extension in [".pdf", ".svg"] if not stem.with_suffix(extension).exists()]
        if missing:
            raise SystemExit(f"direct composite outputs are missing: {missing}")
    else:
        for script in ["render_matplotlib.py", "compose_vector_pdf.py"]:
            run(script, project)
    run("validate_figure_project.py", project, "--stage", "final")
    run("qa_figure.py", project)
    if args.package: run("package_deliverables.py", project)


if __name__ == "__main__":
    main()
