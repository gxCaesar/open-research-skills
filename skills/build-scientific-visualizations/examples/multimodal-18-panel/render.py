#!/usr/bin/env python3
"""Render 18 source-table-derived panels on an original synthetic demonstration page."""

import argparse
import csv
import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "multimodal-example-mpl"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "multimodal-example-cache"))
import matplotlib as mpl
mpl.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import ConnectionPatch, Rectangle
from matplotlib.text import Text
import numpy as np


EXAMPLE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 183, 235
INK, MUTED, BLUE, CORAL = "#28303F", "#78818B", "#367DA2", "#B96A57"
STATES = [("S1", BLUE, "o"), ("S2", CORAL, "^"), ("S3", "#8078A8", "s")]


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def paired_values(table, feature):
    """Join by independent unit; missing measurements remove pairs, not just rows."""
    paired = {}
    for row in table:
        donor, condition = row["donor"], row["condition"]
        values = paired.setdefault(donor, {})
        if condition in values:
            raise ValueError(f"duplicate unit-condition: {donor}, {condition}")
        values[condition] = float(row[feature]) if row[feature] != "" else np.nan
    complete = sorted(donor for donor, values in paired.items()
        if all(condition in values and np.isfinite(values[condition])
               for condition in ("control", "perturbed")))
    differences = np.array([paired[donor]["perturbed"] - paired[donor]["control"] for donor in complete])
    return complete, differences, len(paired) - len(complete)


def interval(values):
    """Descriptive unit bootstrap, not a confirmatory analysis template."""
    values = np.asarray(values, dtype=float)
    draws = np.random.default_rng(701).choice(values, (2000, len(values)), replace=True).mean(axis=1)
    return float(values.mean()), np.quantile(draws, [0.025, 0.975])


def panel(fig, letter, title, x, y, w, h, left=8, bottom=8):
    # Coordinates are mm from page top. Labels occupy reserved page space.
    fig.text(x / WIDTH, (HEIGHT - y) / HEIGHT, letter, fontsize=8, weight="bold", va="top")
    fig.text((x + 4) / WIDTH, (HEIGHT - y) / HEIGHT, title, fontsize=6.5, va="top")
    ax = fig.add_axes([(x + left) / WIDTH, (HEIGHT - y - h + bottom) / HEIGHT,
                       (w - left - 1) / WIDTH, (h - bottom - 7) / HEIGHT])
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=2, width=0.5, pad=1.5)
    return ax


def band(fig, y, text):
    fig.text(5 / WIDTH, (HEIGHT - y) / HEIGHT, text, fontsize=7, weight="bold", va="top", color=INK)
    fig.add_artist(Line2D([5 / WIDTH, 178 / WIDTH], [(HEIGHT - y - 3.6) / HEIGHT] * 2,
                          transform=fig.transFigure, lw=0.5, color="#D4DADF"))


def colorbar(fig, ax, artist, label, ticks=None):
    cb = fig.colorbar(artist, ax=ax, fraction=0.065, pad=0.07, ticks=ticks)
    cb.solids.set_rasterized(False)
    cb.set_label(label, fontsize=5.5, labelpad=2)
    cb.ax.tick_params(labelsize=5.5, length=1.5, pad=1)
    cb.outline.set_linewidth(0.4)


def render(data_dir, output, font=None):
    font = font or ("Arial" if any(f.name == "Arial" for f in font_manager.fontManager.ttflist) else "DejaVu Sans")
    mpl.rcParams.update({"font.family": font, "font.size": 6, "axes.labelsize": 6,
        "xtick.labelsize": 5.5, "ytick.labelsize": 5.5, "axes.linewidth": 0.5,
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": MUTED,
        "xtick.color": INK, "ytick.color": INK, "pdf.fonttype": 42, "svg.fonttype": "none",
        "savefig.bbox": None, "savefig.pad_inches": 0})
    cells, assays, molecules, tracks, spectrum, dose = [rows(data_dir / f"{name}.csv")
        for name in ("cells", "assays", "molecules", "tracks", "spectrum", "dose")]
    # This is a fixed teaching population, not a general missing-data processor.
    # Keep the declared n and cross-assay donor correspondence true before drawing.
    expected_donors = [f"D{i:02d}" for i in range(1, 9)]
    expected_pairs = {(donor, condition) for donor in expected_donors
                      for condition in ("control", "perturbed")}
    if len(assays) != 16 or {(row["donor"], row["condition"]) for row in assays} != expected_pairs:
        raise ValueError("fixed demonstration requires exactly D01–D08 control/perturbed pairs; missing or extra units are unsupported")
    for feature in ("rna", "atac", "protein", "glyco_fraction"):
        assay_donors, _, _ = paired_values(assays, feature)
        if assay_donors != expected_donors:
            raise ValueError(f"fixed demonstration requires complete {feature} pairs for D01–D08; missing assay values cannot be aligned by array position")
    for row in assays:
        expected_available = "0" if row["condition"] == "perturbed" and row["donor"] in {"D03", "D07"} else "1"
        if row["metabolite_available"] != expected_available:
            raise ValueError("fixed demonstration requires its declared six linked donors; altered metabolite availability is unsupported")
    donors, rna_change, missing = paired_values(assays, "rna")
    fig = plt.figure(figsize=(WIDTH / 25.4, HEIGHT / 25.4), dpi=150)
    fig.text(5 / WIDTH, 1 - 3 / HEIGHT, "SYNTHETIC MULTI-MODAL ATLAS", weight="bold", fontsize=8, va="top")
    fig.text(178 / WIDTH, 1 - 3.5 / HEIGHT, "Design demonstration · no biological findings", fontsize=6, ha="right", va="top")

    band(fig, 10, "01  Spatial context and cell identity")
    field = [r for r in cells if r["donor"] == "D01" and r["condition"] == "control"]
    a = panel(fig, "a", "D01 / control", 5, 17, 53, 39, left=7, bottom=7)
    b = panel(fig, "b", "Linked ROI", 61, 17, 28, 39, left=0, bottom=7)
    for ax, subset in [(a, field), (b, [r for r in field if 220 <= float(r["x_um"]) <= 520 and 100 <= float(r["y_um"]) <= 400])]:
        for state, color, marker in STATES:
            selection = [r for r in subset if r["state"] == state]
            ax.scatter([float(r["x_um"]) for r in selection], [float(r["y_um"]) for r in selection],
                       c=color, marker=marker, s=10 if ax is a else 18, lw=0)
        ax.set_aspect("equal")
    a.set(xlim=(0, 800), ylim=(0, 500), xlabel="x (µm)", ylabel="y (µm)")
    a.set_xticks([0, 400, 800]); a.set_yticks([0, 250, 500])
    a.add_patch(Rectangle((220, 100), 300, 300, fill=False, ec=INK, lw=0.7))
    b.set(xlim=(220, 520), ylim=(100, 400)); b.axis("off")
    b.plot([240, 340], [125, 125], color=INK, lw=1.3); b.text(290, 141, "100 µm", ha="center", fontsize=5.5)
    fig.add_artist(ConnectionPatch((520, 400), (220, 400), "data", "data", axesA=a, axesB=b, color=MUTED, lw=0.5))
    c = panel(fig, "c", "Latent coordinates", 92, 17, 39, 39, left=6, bottom=7)
    for state, color, marker in STATES:
        subset = [r for r in cells if r["state"] == state]
        c.scatter([float(r["embed_x"]) for r in subset], [float(r["embed_y"]) for r in subset], s=2, color=color, marker=marker, lw=0, alpha=0.5)
    c.set(xlabel="Latent 1", ylabel="Latent 2", xticks=[], yticks=[])
    c.legend(handles=[Line2D([], [], color=color, marker=marker, ls="none", ms=3, label=state) for state,color,marker in STATES],
             loc="upper left", frameon=False, fontsize=5.5, handletextpad=0.2, borderpad=0, labelspacing=0.2)
    d = panel(fig, "d", "Marker summary", 134, 17, 44, 39, left=5, bottom=12)
    for si, (state, _, _) in enumerate(STATES):
        subset = [r for r in cells if r["state"] == state]
        for fi, feature in enumerate(["rna_a", "rna_b"]):
            values = np.array([float(r[feature]) for r in subset])
            art = d.scatter(fi, si, s=55 * np.mean(values > 1), c=[values.mean()], cmap="viridis", vmin=0, vmax=2, edgecolors=INK, lw=0.25)
    d.set(xticks=[0, 1], xticklabels=["RNA-A", "RNA-B"], yticks=range(3), yticklabels=["S1", "S2", "S3"], xlim=(-0.6,1.6), ylim=(2.5,-0.5))
    colorbar(fig, d, art, "Mean (a.u.)", [0, 1, 2])
    d.legend(handles=[Line2D([],[],marker="o",ls="none",color=MUTED,ms=np.sqrt(55*fraction),label=label)
             for fraction,label in [(0.25,"25%"),(0.75,"75%")]], title="Fraction > 1", title_fontsize=5.5,
             frameon=False,fontsize=5.5,loc="upper left",bbox_to_anchor=(-0.10,-0.19),ncol=2,
             borderpad=0,handletextpad=0.2,columnspacing=0.6)

    band(fig, 58, "02  Quantification respects paired experimental units")
    e = panel(fig, "e", "RNA by donor", 5, 65, 48, 34, left=8)
    for donor in donors:
        pair = {r["condition"]: float(r["rna"]) for r in assays if r["donor"] == donor}
        e.plot([0, 1], [pair["control"], pair["perturbed"]], c="#C3C9CE", lw=0.6)
        e.scatter([0, 1], [pair["control"], pair["perturbed"]], c=[BLUE, CORAL], s=10, zorder=3)
    e.set(xticks=[0, 1], xticklabels=["Control", "Perturbed"], ylabel="RNA (a.u.)", xlim=(-0.25,1.25))
    f = panel(fig, "f", "Spatial profile / eight donors", 57, 65, 64, 34, left=8)
    bins = [0, 200, 400, 600, 800]
    for condition, color, linestyle, marker in [("control", BLUE, "-", "o"), ("perturbed", CORAL, "--", "s")]:
        summaries = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            unit_means = [np.mean([float(r["rna_a"]) for r in cells if r["donor"] == donor and r["condition"] == condition and lo <= float(r["x_um"]) < hi]) for donor in donors]
            summaries.append(interval(unit_means))
        means = [s[0] for s in summaries]
        errors = np.array([[s[0] - s[1][0], s[1][1] - s[0]] for s in summaries]).T
        f.errorbar([100, 300, 500, 700], means, yerr=errors, color=color, linestyle=linestyle, marker=marker, ms=2.5, lw=0.7, capsize=1.5, label=condition.title())
    f.set(xlabel="x bin centre (µm)", ylabel="Mean RNA-A (a.u.)")
    f.legend(frameon=False, fontsize=5.5, loc="lower left", bbox_to_anchor=(0,1),
             borderaxespad=0,ncol=2,columnspacing=1,handlelength=1.3)
    g = panel(fig, "g", "Paired assay changes", 125, 65, 53, 34, left=16)
    for yi, (feature, label) in enumerate([("rna", "RNA"), ("atac", "ATAC"), ("protein", "Protein")]):
        _, values, _ = paired_values(assays, feature)
        control_sd = np.std([float(row[feature]) for row in assays if row["condition"] == "control"], ddof=1)
        values = values / control_sd
        mean, ci = interval(values)
        g.scatter(values, yi + np.linspace(-0.12,0.12,len(values)), color=MUTED, s=7)
        g.errorbar(mean, yi, xerr=[[mean-ci[0]],[ci[1]-mean]], color=INK, marker="D", ms=3, capsize=2)
    g.axvline(0, color=MUTED, lw=0.6, ls=":")
    g.set(yticks=range(3), yticklabels=["RNA", "ATAC", "Protein"], xlabel="Δ / control SD", ylim=(2.6,-0.6))

    band(fig, 101, "03  Molecular signals, missingness and composition")
    h = panel(fig, "h", "Detection", 5, 108, 36, 35, left=6, bottom=9)
    features = list(dict.fromkeys(r["feature"] for r in molecules))
    detection = np.array([[int(next(r for r in molecules if r["donor"] == donor and r["condition"] == "perturbed" and r["feature"] == feature)["detected"]) for donor in donors] for feature in features])
    h.pcolormesh(detection, cmap=mpl.colors.ListedColormap(["#FFFFFF", "#667989"]), vmin=0,vmax=1, edgecolors="#D4DADF", lw=0.4)
    h.set(xticks=np.arange(8)+0.5, xticklabels=[str(i) for i in range(1,9)], yticks=np.arange(4)+0.5, yticklabels=["M1","M2","M3","M4"], xlabel="Donor (white: missing)", ylim=(4,0))
    i = panel(fig, "i", "Feature-level paired effects", 45, 108, 72, 35, left=34, bottom=9)
    labels = ["Phosphatidylcholine\nfeature (M1)", "Hexosylceramide\nfeature (M2)", "Sialylated glycopeptide\nfeature (M3)", "Amino-acid\nfeature (M4)"]
    for yi, feature in enumerate(features):
        ids, values, _ = paired_values([r for r in molecules if r["feature"] == feature], "log2_abundance")
        mean, ci = interval(values)
        i.errorbar(mean, yi, xerr=[[mean-ci[0]],[ci[1]-mean]], marker="o", ms=3, color=BLUE, capsize=2)
        i.text(0.96, yi, f"n={len(ids)}", transform=i.get_yaxis_transform(), fontsize=5.5, va="center", ha="right")
    i.axvline(0, color=MUTED, lw=0.6, ls=":")
    i.set(yticks=range(4), yticklabels=labels, ylim=(3.6,-0.6), xlabel="Δ log2 abundance", xlim=(-0.65,0.9))
    j = panel(fig, "j", "Glyco fraction", 121, 108, 27, 35, left=6, bottom=9)
    for donor in donors:
        pair = {r["condition"]:float(r["glyco_fraction"]) for r in assays if r["donor"]==donor}
        j.plot([0,1], [pair["control"],pair["perturbed"]], color=MUTED, marker="o", ms=2, lw=0.5)
    j.set(xticks=[0,1], xticklabels=["C","P"], ylim=(0,1), ylabel="Fraction", xlim=(-0.2,1.2))
    k = panel(fig, "k", "Spectrum", 152, 108, 26, 35, left=5, bottom=9)
    k.vlines([float(r["mz"]) for r in spectrum], 0, [float(r["relative_intensity"]) for r in spectrum], color=BLUE, lw=0.6)
    k.set(xlabel="m/z", ylabel="Relative intensity", xticks=[200,800], yticks=[0,1], ylim=(0,1.05))

    band(fig, 145, "04  Locus context and explicit null comparisons")
    l = panel(fig, "l", "Artificial locus", 5, 152, 48, 34, left=7)
    for condition, color, ls in [("control",BLUE,"-"),("perturbed",CORAL,"--")]:
        l.plot([float(r["position_bp"]) for r in tracks], [float(r[condition]) for r in tracks], color=color, ls=ls, lw=0.9, label=condition.title())
    l.set(xlabel="Artificial coordinate (bp)", ylabel="Signal (a.u.)", xticks=[0,500,1000], ylim=(0,2))
    l.legend(frameon=False, fontsize=5.5, handlelength=1.3)
    m = panel(fig, "m", "RNA–ATAC", 57, 152, 37, 34, left=8)
    _, atac_change, _ = paired_values(assays, "atac")
    m.scatter(rna_change, atac_change, color=BLUE, s=14)
    for donor, x, y in zip(donors, rna_change, atac_change):
        m.annotate(donor[-1], (x,y), xytext=(2,2), textcoords="offset points", fontsize=5)
    m.set(xlabel="Δ RNA (a.u.)", ylabel="Δ ATAC (a.u.)")
    n = panel(fig, "n", "Within-donor null", 98, 152, 40, 34, left=8)
    rng = np.random.default_rng(211)
    null = (rng.choice([-1,1], (2000,len(rna_change))) * rna_change).mean(axis=1)
    n.hist(null, bins=np.linspace(-0.6,0.6,22), color="#CED8DF", edgecolor="white", lw=0.3)
    n.axvline(rna_change.mean(), color=CORAL, lw=1, label="Observed")
    n.set(xlabel="Mean Δ RNA", ylabel="Sign-flip draws")
    n.legend(frameon=False, fontsize=5.5, loc="upper left", handlelength=1)
    o = panel(fig, "o", "Response series", 142, 152, 36, 34, left=7)
    for donor in donors:
        subset = [r for r in dose if r["donor"]==donor]
        o.plot([float(r["concentration_uM"]) for r in subset], [float(r["response"]) for r in subset], c=MUTED, alpha=0.5, lw=0.6)
    o.set_xscale("symlog", linthresh=0.1)
    o.set(xlabel="Concentration (µM)", ylabel="Response (a.u.)", xticks=[0,1,100], xticklabels=["0","1","100"])

    band(fig, 188, "05  Linkage and robustness remain visible")
    p = panel(fig, "p", "Linked units / perturbed", 5, 195, 50, 34, left=15)
    counts = [len(donors),len(donors),sum(int(r["metabolite_available"]) for r in assays if r["condition"]=="perturbed")]
    p.barh([0,1,2],counts,color="#D1DCE4",edgecolor=INK,lw=0.4,hatch="//")
    p.set(yticks=[0,1,2],yticklabels=["RNA","ATAC","Metab."],xlim=(0,9),xticks=[0,4,8],xlabel="Available donors",ylim=(2.6,-0.6))
    for yy,value in enumerate(counts): p.text(value+0.15,yy,str(value),va="center",fontsize=6)
    q = panel(fig, "q", "Complete-pair sensitivity", 59, 195, 57, 34, left=17)
    complete = {r["donor"] for r in assays if r["condition"]=="perturbed" and int(r["metabolite_available"])}
    for yy,selection in enumerate([rna_change,np.array([value for donor,value in zip(donors,rna_change) if donor in complete])]):
        mean,ci=interval(selection)
        q.errorbar(mean,yy,xerr=[[mean-ci[0]],[ci[1]-mean]],color=BLUE,marker="o",ms=3,capsize=2)
    q.set(yticks=[0,1],yticklabels=["All (n=8)","Linked (n=6)"],xlabel="Mean Δ RNA (a.u.)",ylim=(1.6,-0.6))
    q.axvline(0,color=MUTED,lw=0.6,ls=":")
    r = panel(fig, "r", "Cross-assay pairing control", 120, 195, 58, 34, left=9)
    observed = float(np.corrcoef(rna_change,atac_change)[0,1])
    shuffled = np.array([np.corrcoef(rna_change,rng.permutation(atac_change))[0,1] for _ in range(2000)])
    r.hist(shuffled,bins=np.linspace(-1,1,21),color="#CED8DF",edgecolor="white",lw=0.3)
    r.axvline(observed,color=CORAL,lw=1,label="Matched IDs")
    r.set(xlabel="Donor-level correlation",ylabel="Shuffled draws",xticks=[-1,0,1])
    r.legend(frameon=False,fontsize=5.5,handlelength=1,loc="upper right")
    fig.text(5/WIDTH, 2/HEIGHT, "C, control; P, perturbed · a.u., arbitrary units · intervals, donor bootstrap 95% · no significance claims", fontsize=5.5)

    # Reuse the installed helper's actual font-metric check, not a new validator.
    helper = EXAMPLE.parents[1] / "shared/figure-core/scripts/render_matplotlib.py"
    spec = importlib.util.spec_from_file_location("figure_text_bounds", helper)
    bounds = importlib.util.module_from_spec(spec); spec.loader.exec_module(bounds)
    fig.canvas.draw()
    # Matplotlib retains tick Text objects beyond the view limits but does not draw them.
    undrawn_ticks = set()
    for ax in fig.axes:
        for axis, limits in [(ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())]:
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not min(limits) <= tick.get_loc() <= max(limits):
                    undrawn_ticks.update([tick.label1, tick.label2])
    overflow = [artist.get_text() for artist in fig.findobj(Text)
        if artist not in undrawn_ticks and bounds.text_overflow_pt(artist, fig.bbox, fig.canvas.get_renderer())]
    if overflow:
        plt.close(fig)
        raise ValueError(f"text outside page: {overflow}")
    output.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "svg", "png"):
        metadata = {"pdf": {"Creator": None, "Producer": None, "CreationDate": None, "ModDate": None},
                    "svg": {"Creator": None, "Date": None}, "png": {"Software": None}}[extension]
        fig.savefig(output / f"multimodal-18-panel.{extension}", dpi=240, bbox_inches=None, metadata=metadata)
    plt.close(fig)
    report = dict(panels=18, paired_units=len(donors), incomplete_rna_pairs=missing,
                  text_overflows=len(overflow), font=font, width_mm=WIDTH, height_mm=HEIGHT)
    print(json.dumps(report, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=EXAMPLE / "data")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font", help="Installed font; defaults to Arial, or reported DejaVu Sans fallback")
    args = parser.parse_args()
    render(args.data, args.output, args.font)
