#!/usr/bin/env python3
"""Summarize paired synthetic task scores using only the Python standard library."""

import argparse
import csv
import json
import math
from pathlib import Path


def analyze(scores):
    rows = []
    seen = set()
    with scores.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["task", "baseline", "candidate"]:
            raise ValueError("expected columns: task,baseline,candidate")
        for line, row in enumerate(reader, start=2):
            task = (row.get("task") or "").strip()
            if not task:
                raise ValueError(f"line {line}: task must not be empty")
            if task in seen:
                raise ValueError(f"line {line}: duplicate task {task}")
            if None in row or None in row.values():
                raise ValueError(f"line {line}: expected exactly three fields")
            baseline, candidate = float(row["baseline"]), float(row["candidate"])
            difference = candidate - baseline
            if not all(math.isfinite(value) for value in (baseline, candidate, difference)):
                raise ValueError(f"line {line}: nonfinite score or difference")
            seen.add(task)
            rows.append({"task": task, "baseline": baseline, "candidate": candidate,
                         "difference": difference})
    if not rows:
        raise ValueError("scores must contain at least one task")
    differences = [row["difference"] for row in rows]
    summary = {
        "data_kind": "synthetic teaching scores",
        "score_direction": "higher is better",
        "tasks": len(rows),
        "wins": sum(value > 0 for value in differences),
        "losses": sum(value < 0 for value in differences),
        "ties": sum(value == 0 for value in differences),
        "mean_difference": round(math.fsum(value / len(rows) for value in differences), 12),
    }
    for row in rows:
        row["difference"] = round(row["difference"], 12)
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, required=True, help="CSV with task,baseline,candidate")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    args = parser.parse_args()
    try:
        if args.output.exists() or args.output.is_symlink():
            raise ValueError("output already exists; choose a new directory")
        rows, summary = analyze(args.scores)
        args.output.mkdir(parents=True, exist_ok=False)
        with (args.output / "differences.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["task", "baseline", "candidate", "difference"])
            writer.writeheader()
            writer.writerows(rows)
        (args.output / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
        if summary["wins"] == summary["tasks"]:
            interpretation = "本表每项候选分数均高于基线。"
        elif summary["ties"] == summary["tasks"]:
            interpretation = "本表所有任务分数均相等。"
        elif summary["losses"] == summary["tasks"]:
            interpretation = "本表每项候选分数均低于基线。"
        elif summary["wins"] and summary["losses"]:
            interpretation = "混合方向不支持每项任务均改善的说法。"
        else:
            interpretation = "本表包含相等分数，不支持每项任务均改善的说法。"
        brief = (
            "# 合成任务配对比较（synthetic）\n\n"
            f"在 {summary['tasks']} 个合成教学任务中，候选得分高于基线 {summary['wins']} 次，"
            f"低于基线 {summary['losses']} 次，相等 {summary['ties']} 次。"
            f"候选减基线的等权平均差为 {summary['mean_difference']:+.6f} 个任意分数单位。\n\n"
            f"这些数值不是细胞扰动实验或模型训练结果。{interpretation}"
            "下一步应检查真实任务定义、配对关系与失败条件；本分析不提供统计推断、机制或泛化结论。\n"
        )
        (args.output / "summary.md").write_text(brief, encoding="utf-8")
    except (OSError, ValueError, OverflowError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(brief)
    print(f"Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
