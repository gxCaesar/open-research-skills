#!/usr/bin/env python3
"""Create the original synthetic atlas tables. No experimental images or data are used."""

import argparse
import csv
from pathlib import Path

import numpy as np


def save(path, table):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(table[0]))
        writer.writeheader(); writer.writerows(table)


def generate(destination):
    destination.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(64121)
    cells, assays, tracks = [], [], []
    labels = ["RNA boundary", "RNA epithelial", "RNA stromal", "ATAC boundary",
              "ATAC lineage", "Protein surface", "Protein matrix", "Lipid module",
              "Amino-acid module", "Invariant control"]
    for unit in range(12):
        donor = f"D{unit + 1:02d}"
        donor_offset = rng.normal(0, 0.28)
        response = rng.normal(0.28, 0.24)
        for condition, intervention in [("C", 0), ("P", 1)]:
            sample = []
            for cell in range(720):
                angle = rng.uniform(0, 2 * np.pi)
                radius = np.sqrt(rng.uniform(0, 1)) * (1 + 0.08*np.sin(3*angle) + 0.06*np.cos(5*angle))
                x = 850 + 730 * radius * np.cos(angle)
                y = 510 + 440 * radius * np.sin(angle)
                offset = (radius - 0.61) * 500
                if radius < 0.52:
                    probabilities = [0.86, 0.08, 0.06]
                elif radius < 0.75:
                    probabilities = [0.18, 0.22, 0.60]
                else:
                    probabilities = [0.08, 0.81, 0.11]
                state = rng.choice(["Epithelial-like", "Stromal-like", "Immune-like"], p=probabilities)
                niche = np.exp(-0.5 * (offset / 75)**2)
                target = max(0.02, 0.6 + 0.65*niche + 0.45*(state == "Immune-like") +
                             donor_offset + intervention * response * (0.25 + niche) + rng.normal(0,0.25))
                values = dict(
                    rna_epithelial=max(0.02, 0.3 + 1.5*(state == "Epithelial-like") + donor_offset + rng.normal(0,0.22)),
                    rna_stromal=max(0.02, 0.3 + 1.5*(state == "Stromal-like") + donor_offset + rng.normal(0,0.22)),
                    rna_boundary=target,
                    atac=max(0.02, 0.2 + 0.6*target + intervention*rng.normal(0,0.12) + rng.normal(0,0.18)),
                    protein=max(0.02, 0.25 + 0.5*target + intervention*0.07 + rng.normal(0,0.2)),
                    invariant=max(0.02, 1 + donor_offset + rng.normal(0,0.26)))
                row = dict(donor=donor, condition=condition, cell_id=f"{donor}-{condition}-{cell:04d}",
                           state=state, x_um=round(x,3), y_um=round(y,3), radial_offset_um=round(offset,3))
                row.update({key: round(value,5) for key,value in values.items()})
                cells.append(row); sample.append(row)
            means = {key: np.mean([row[key] for row in sample]) for key in values}
            # Assay-specific offsets make these arbitrary abundance units, not calibrated concentrations.
            measurements = [means["rna_boundary"], means["rna_epithelial"], means["rna_stromal"],
                means["atac"], 0.4*means["rna_epithelial"] - intervention*0.08 + rng.normal(0,0.03),
                means["protein"], 0.5*means["rna_stromal"] - intervention*response*0.3 + rng.normal(0,0.02),
                1 + donor_offset - intervention*response*0.7 + rng.normal(0,0.09),
                1.2 + donor_offset + intervention*response*0.2 + rng.normal(0,0.05), means["invariant"]]
            assays.extend(dict(donor=donor,condition=condition,feature=feature,value=round(float(value),6))
                          for feature,value in zip(labels,measurements))
    for assay, peaks in [("RNA", [(12,1),(35,0.6),(49,0.5)]),
                         ("ATAC", [(11,0.9),(32,0.4),(48,0.6)]),
                         ("Protein", [(14,0.6),(37,0.7),(47,0.3)])]:
        for condition, scale in [("C",1), ("P",1.3)]:
            for position in np.linspace(0,60,181):
                signal = 0.02 + sum(amplitude*np.exp(-0.5*((position-centre)/(1.2 if assay=="ATAC" else 2.2))**2)
                                    for centre,amplitude in peaks)
                tracks.append(dict(assay=assay,condition=condition,position_kb=round(float(position),4),
                                   signal=round(float(signal*scale),5)))
    save(destination / "cells.csv", cells)
    save(destination / "assays.csv", assays)
    save(destination / "tracks.csv", tracks)
    save(destination / "regions.csv", [dict(region="ROI-1", donor="D01", condition="C", x_um=1080,
                                             y_um=240, width_um=360, height_um=360)])
    print(f"SYNTHETIC: {len(cells)} cells; {len(assays)} donor-condition-feature values; 12 paired units")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    generate(parser.parse_args().destination)
