#!/usr/bin/env python3
"""Generate original artificial measurements; no human, animal or repository data."""

import argparse
import csv
from pathlib import Path

import numpy as np


def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate(destination):
    destination.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(184)
    cells, assays, molecules = [], [], []
    features = ["Phosphatidylcholine feature", "Hexosylceramide feature",
                "Sialylated glycopeptide feature", "Amino-acid feature"]
    for index in range(8):
        donor = f"D{index + 1:02d}"
        offset = rng.normal(0, 0.2)
        for condition, shift in [("control", 0), ("perturbed", 1)]:
            for cell_index in range(80):
                x, y = rng.uniform(0, 800), rng.uniform(0, 500)
                state = int(rng.choice(3, p=[0.46 - 0.12 * shift, 0.32 + 0.10 * shift, 0.22 + 0.02 * shift]))
                rna_a = max(0, rng.normal(0.7 + 0.45 * state + 0.3 * shift + offset, 0.35))
                rna_b = max(0, rng.normal(1.8 - 0.6 * state + offset, 0.35))
                cells.append(dict(cell_id=f"{donor}-{condition}-{cell_index:03d}",
                    donor=donor, condition=condition, state=f"S{state + 1}",
                    x_um=round(x, 3), y_um=round(y, 3), rna_a=round(rna_a, 4),
                    rna_b=round(rna_b, 4),
                    embed_x=round(state * 2.1 + rng.normal(0, 0.5), 4),
                    embed_y=round((state == 1) * 2 + rng.normal(0, 0.6), 4)))
            # Linked assay summaries are generated separately, not inferred from cells.
            rna = 1 + offset + shift * (0.35 + rng.normal(0, 0.12))
            atac = 0.7 + offset * 0.5 + shift * (0.25 + rng.normal(0, 0.13))
            assays.append(dict(donor=donor, condition=condition, rna=round(rna, 4),
                atac=round(atac, 4), protein=round(2 + offset + shift * rng.normal(0.2, 0.25), 4),
                glyco_fraction=round(0.3 + offset * 0.08 + shift * rng.normal(0.06, 0.03), 4),
                metabolite_available=int(not (index in [2, 6] and shift == 1))))
            for fi, feature in enumerate(features):
                value = 3 + offset + fi * 0.3 + shift * [0.45, -0.32, 0.1, 0.02][fi] + rng.normal(0, 0.17)
                detected = not (index in [2, 6] and shift == 1 and fi == 0)
                molecules.append(dict(donor=donor, condition=condition, feature=feature,
                    log2_abundance=round(value, 4) if detected else "", detected=int(detected)))
    tracks = [dict(position_bp=x, control=round(0.1 + np.exp(-((x - 400) / 80) ** 2), 5),
        perturbed=round(0.1 + 1.6 * np.exp(-((x - 410) / 80) ** 2), 5)) for x in range(0, 1001, 10)]
    spectrum = [dict(mz=round(float(x), 3), relative_intensity=round(float(y), 4))
        for x, y in zip(np.sort(rng.uniform(150, 850, 34)), rng.uniform(0.03, 1, 34))]
    dose = [dict(donor=f"D{i + 1:02d}", concentration_uM=d,
        response=round(float(1 / (1 + d / (2 + i * 0.2)) + rng.normal(0, 0.035)), 4))
        for i in range(8) for d in [0, 0.1, 1, 10, 100]]
    for name, rows in [("cells", cells), ("assays", assays), ("molecules", molecules),
                       ("tracks", tracks), ("spectrum", spectrum), ("dose", dose)]:
        write(destination / f"{name}.csv", rows)
    print(f"Generated SYNTHETIC tables: {len(cells)} cells; 8 paired units; 6 CSV files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    generate(parser.parse_args().destination)
