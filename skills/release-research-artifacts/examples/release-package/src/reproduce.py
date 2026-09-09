#!/usr/bin/env python3
"""Recompute the one number this synthetic package reports."""

import csv
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = list(csv.DictReader((HERE.parent / "data" / "scores.csv").open(encoding="utf-8")))
    values = [float(row["score"]) for row in rows]
    print(f"units={len(values)} mean={statistics.fmean(values):.4f}")


if __name__ == "__main__":
    main()
