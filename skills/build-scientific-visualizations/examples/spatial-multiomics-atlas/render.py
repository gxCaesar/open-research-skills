#!/usr/bin/env python3
"""Render an asymmetric 14-panel, source-table-derived synthetic spatial atlas."""

import argparse
import csv
import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "spatial-atlas-mpl"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "spatial-atlas-cache"))
import matplotlib as mpl
mpl.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import ConnectionPatch, Rectangle
from matplotlib.text import Text
import numpy as np


EXAMPLE = Path(__file__).resolve().parent
W, H = 183, 170
INK, GREY = "#283440", "#78858E"
BLUE, TEAL, CORAL, GOLD, PURPLE = "#3F7C9B", "#69A28F", "#BF7B6C", "#B59A57", "#867AAB"
STATE_STYLE = {"Epithelial-like": (BLUE,"o"), "Stromal-like": (TEAL,"s"), "Immune-like": (GOLD,"^")}
DIVERGING = mpl.colors.LinearSegmentedColormap.from_list("assay_difference", [BLUE,"#FAFBFC",CORAL])
SEQUENTIAL = mpl.colors.LinearSegmentedColormap.from_list("boundary_abundance", ["#F0F5F7",BLUE,INK])


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def read_data(directory):
    cells, assays, tracks, regions = [read_csv(directory / f"{name}.csv") for name in ("cells","assays","tracks","regions")]
    lookup = {}
    for row in assays:
        key = (row["donor"], row["condition"], row["feature"])
        if key in lookup:
            raise ValueError(f"duplicate assay unit: {key}")
        value = float(row["value"]) if row["value"] else np.nan
        if not np.isfinite(value):
            raise ValueError(f"missing assay value: {key}")
        lookup[key] = value
    donors = sorted({row["donor"] for row in cells})
    features = list(dict.fromkeys(row["feature"] for row in assays))
    expected = {(donor,condition,feature) for donor in donors for condition in ("C","P") for feature in features}
    if set(lookup) != expected:
        raise ValueError("missing or unmatched donor-condition-feature values; cross-assay pairs must share explicit donor IDs")
    cell_groups = {(row["donor"],row["condition"]) for row in cells}
    if cell_groups != {(donor,condition) for donor in donors for condition in ("C","P")}:
        raise ValueError("missing cell population for a paired donor-condition")
    return cells, lookup, tracks, regions, donors, features


def interval(values):
    values = np.asarray(values, dtype=float)
    resampled = np.random.default_rng(700).choice(values, size=(2000,len(values))).mean(axis=1)
    return float(values.mean()), np.quantile(resampled,[0.025,0.975])


def panel(fig, letter, title, x, y, width, height, left=6, bottom=5, top=5):
    fig.text(x/W, 1-y/H, letter, fontsize=8, weight="bold", va="top")
    fig.text((x+4)/W, 1-(y+0.25)/H, title, fontsize=6.2, va="top")
    ax = fig.add_axes([(x+left)/W,1-(y+height-bottom)/H,(width-left-1)/W,(height-top-bottom)/H])
    ax.spines[["right","top"]].set_visible(False)
    ax.tick_params(length=1.5,width=0.45,pad=1)
    return ax


def colorbar(fig, ax, artist, label, ticks=None):
    bar = fig.colorbar(artist,ax=ax,fraction=0.045,pad=0.035,ticks=ticks)
    bar.solids.set_rasterized(False)
    bar.set_label(label,fontsize=5,labelpad=1.5)
    bar.ax.tick_params(labelsize=5,length=1,pad=1)
    bar.outline.set_linewidth(0.3)


def render(directory, output):
    font = "Arial" if any(item.name == "Arial" for item in font_manager.fontManager.ttflist) else "DejaVu Sans"
    mpl.rcParams.update({"font.family":font,"font.size":5.5,"axes.labelsize":5.5,
        "xtick.labelsize":5,"ytick.labelsize":5,"axes.linewidth":0.45,
        "axes.labelcolor":INK,"text.color":INK,"xtick.color":INK,"ytick.color":INK,
        "axes.edgecolor":GREY,"pdf.fonttype":42,"svg.fonttype":"none",
        "savefig.bbox":None,"savefig.pad_inches":0})
    cells, values, tracks, regions, donors, features = read_data(directory)
    delta = {feature:np.array([values[donor,"P",feature]-values[donor,"C",feature] for donor in donors]) for feature in features}
    groups = {(donor,condition):[row for row in cells if row["donor"]==donor and row["condition"]==condition]
              for donor in donors for condition in ("C","P")}
    fig = plt.figure(figsize=(W/25.4,H/25.4),dpi=180)
    fig.text(5/W,1-3/H,"Spatial architecture across molecular layers",fontsize=8,weight="bold",va="top")
    fig.text(178/W,1-3.5/H,"SYNTHETIC DATA  ·  editorial demonstration",fontsize=5.5,ha="right",va="top",color=INK)

    # A broad spatial anchor is paired with two exact linked views and a matrix.
    region = regions[0]
    focal = groups[region["donor"],region["condition"]]
    rx,ry,rw,rh = [float(region[key]) for key in ("x_um","y_um","width_um","height_um")]
    roi = [row for row in focal if rx<=float(row["x_um"])<=rx+rw and ry<=float(row["y_um"])<=ry+rh]
    a = panel(fig,"a","Spatial compartments",5,12,84,47,left=0,bottom=5,top=5)
    b = panel(fig,"b","Same-field ROI",95,12,39,21,left=0,bottom=0,top=4)
    c = panel(fig,"c","Boundary RNA",139,12,39,21,left=0,bottom=0,top=4)
    for ax,table,size in [(a,focal,3.4),(b,roi,6.5)]:
        for state,(color,marker) in STATE_STYLE.items():
            subset = [row for row in table if row["state"]==state]
            ax.scatter([float(row["x_um"]) for row in subset],[float(row["y_um"]) for row in subset],
                       color=color,marker=marker,s=size,linewidths=0)
        ax.set_aspect("equal"); ax.axis("off")
    theta=np.linspace(0,2*np.pi,240)
    a.plot(850+730*0.61*np.cos(theta),510+440*0.61*np.sin(theta),color=INK,lw=0.5,ls=(0,(3,3)),alpha=0.7)
    a.set(xlim=(0,1700),ylim=(0,1080))
    a.add_patch(Rectangle((rx,ry),rw,rh,fill=False,ec=INK,lw=0.7))
    a.plot([70,270],[70,70],color=INK,lw=1.2); a.text(170,105,"200 µm",ha="center",fontsize=5)
    a.text(1680,1040,f"{region['donor']} / {region['condition']}\n{len(focal)} cells",ha="right",va="top",fontsize=5.2)
    a.legend(handles=[Line2D([],[],color=color,marker=marker,ls="none",ms=3,label=state)
                      for state,(color,marker) in STATE_STYLE.items()],loc="upper left",bbox_to_anchor=(0.02,-0.01),
             frameon=False,ncol=3,fontsize=5,columnspacing=0.7,handletextpad=0.25,borderaxespad=0)
    b.set(xlim=(rx,rx+rw),ylim=(ry,ry+rh))
    b.plot([rx+15,rx+115],[ry-12,ry-12],color=INK,lw=1,clip_on=False)
    b.text(rx+65,ry-33,"100 µm",ha="center",va="top",fontsize=5)
    fig.add_artist(ConnectionPatch((rx+rw,ry+rh),(rx,ry+rh),"data","data",axesA=a,axesB=b,color=GREY,lw=0.45))
    marker=c.scatter([float(row["x_um"]) for row in roi],[float(row["y_um"]) for row in roi],
                     c=[float(row["rna_boundary"]) for row in roi],s=7,cmap=SEQUENTIAL,linewidths=0)
    c.set(xlim=(rx,rx+rw),ylim=(ry,ry+rh)); c.set_aspect("equal"); c.axis("off")
    colorbar(fig,c,marker,"RNA (a.u.)")
    d=panel(fig,"d","State-resolved molecular profiles",95,37,83,22,left=17,bottom=4,top=4)
    markers=["rna_epithelial","rna_stromal","rna_boundary","atac","protein","invariant"]
    states=list(STATE_STYLE)
    matrix=np.array([[np.mean([float(row[feature]) for row in cells if row["state"]==state]) for state in states] for feature in markers])
    # Scale by actual cell-level variation, not by tiny between-state differences.
    # This keeps the invariant control near neutral instead of amplifying its noise.
    feature_mean=np.array([np.mean([float(row[feature]) for row in cells]) for feature in markers])
    feature_sd=np.array([np.std([float(row[feature]) for row in cells]) for feature in markers])
    matrix=(matrix-feature_mean[:,None])/feature_sd[:,None]
    marker_bound=max(1.5,float(np.ceil(np.max(np.abs(matrix))*2)/2))
    art=d.pcolormesh(matrix,cmap=DIVERGING,vmin=-marker_bound,vmax=marker_bound,edgecolor="white",linewidth=0.5)
    d.set(xticks=np.arange(3)+0.5,xticklabels=["Epithelial","Stromal","Immune"],yticks=np.arange(6)+0.5,
          yticklabels=["RNA epithelial","RNA stromal","RNA boundary","ATAC","Protein","Invariant"],ylim=(6,0))
    d.tick_params(length=0)
    colorbar(fig,d,art,"Cell-scale z",[-marker_bound,0,marker_bound])

    # Tall, richly annotated multiomic matrix versus compact paired and spatial views.
    e=panel(fig,"e","Paired multiomic changes",5,65,84,45,left=24,bottom=5,top=5)
    standardized=np.array([delta[feature]/np.std([values[donor,"C",feature] for donor in donors],ddof=1) for feature in features])
    bound=max(1,float(np.ceil(np.max(np.abs(standardized))*2)/2))
    art=e.pcolormesh(standardized,cmap=DIVERGING,vmin=-bound,vmax=bound,edgecolor="white",linewidth=0.3)
    e.set(xticks=np.arange(len(donors))+0.5,xticklabels=[donor[1:] for donor in donors],
          yticks=np.arange(len(features))+0.5,yticklabels=features,ylim=(len(features),0))
    e.tick_params(length=0)
    colorbar(fig,e,art,"Δ / control SD",[-bound,0,bound])
    e.set_xlabel("Paired donor",labelpad=1)
    for letter,feature,x in [("f","RNA boundary",95),("g","Protein surface",139)]:
        ax=panel(fig,letter,feature,x,65,39,21,left=7,bottom=4,top=4)
        for donor in donors:
            pair=[values[donor,condition,feature] for condition in ("C","P")]
            ax.plot([0,1],pair,color="#BFC9CE",lw=0.45,zorder=1)
            ax.scatter([0,1],pair,color=[BLUE,CORAL],s=5,zorder=2,linewidths=0)
        ax.set(xticks=[0,1],xticklabels=["Control","Perturbed"],xlim=(-0.15,1.15),ylabel="a.u.")
        ax.set_yticks([round(min(values[d,c,feature] for d in donors for c in ("C","P")),1),
                       round(max(values[d,c,feature] for d in donors for c in ("C","P")),1)])
    h=panel(fig,"h","Boundary profile",95,90,83,20,left=8,bottom=5,top=4)
    bins=np.array([-260,-180,-100,-20,60,140,220,300])
    for condition,color,linestyle in [("C",BLUE,"-"),("P",CORAL,"--")]:
        samples=[]
        for lo,hi in zip(bins[:-1],bins[1:]):
            unit_means=[np.mean([float(row["rna_boundary"]) for row in groups[donor,condition]
                                 if lo<=float(row["radial_offset_um"])<hi]) for donor in donors]
            samples.append(interval(unit_means))
        centre=(bins[:-1]+bins[1:])/2
        h.fill_between(centre,[item[1][0] for item in samples],[item[1][1] for item in samples],color=color,alpha=0.15,lw=0)
        h.plot(centre,[item[0] for item in samples],color=color,ls=linestyle,lw=0.85)
    h.axvline(0,color=GREY,ls=":",lw=0.45)
    h.set(xlabel="Radial offset from boundary (µm)",ylabel="RNA (a.u.)",xticks=[-200,0,200],yticks=[0.5,1.5])
    h.legend(handles=[Line2D([],[],color=BLUE,lw=0.85,label="Control"),
                      Line2D([],[],color=CORAL,lw=0.85,ls="--",label="Perturbed")],
             loc="upper right",frameon=False,ncol=2,fontsize=5,handlelength=1.2,
             handletextpad=0.3,columnspacing=0.7,borderpad=0)

    # A wide locus stack shares a coordinate axis; the small views are paired by identity.
    i=panel(fig,"i","Illustrative locus tracks",5,116,84,22,left=12,bottom=5,top=4)
    for index,assay in enumerate(["RNA","ATAC","Protein"]):
        amplitude=max(float(row["signal"]) for row in tracks if row["assay"]==assay)
        for condition,color,linestyle in [("C",BLUE,"-"),("P",CORAL,"--")]:
            subset=[row for row in tracks if row["assay"]==assay and row["condition"]==condition]
            x=[float(row["position_kb"]) for row in subset]
            y=[float(row["signal"])/amplitude+1.2*(2-index) for row in subset]
            i.fill_between(x,1.2*(2-index),y,color=color,alpha=0.13,lw=0)
            i.plot(x,y,color=color,ls=linestyle,lw=0.55)
    i.set(xlim=(0,60),ylim=(0,3.6),yticks=[0.4,1.6,2.8],yticklabels=["Protein","ATAC","RNA"],
          xticks=[0,20,40,60],xlabel="Artificial position (kb)")
    i.spines["left"].set_visible(False); i.tick_params(axis="y",length=0)
    j=panel(fig,"j","Cross-assay pairing",95,116,39,22,left=7,bottom=5,top=4)
    j.scatter(delta["RNA boundary"],delta["ATAC boundary"],s=10,color=BLUE,edgecolors="white",lw=0.3)
    j.set(xlabel="Δ RNA (a.u.)",ylabel="Δ ATAC",xticks=[0,0.4],yticks=[0,0.2])
    k=panel(fig,"k","State composition",139,116,39,22,left=6,bottom=5,top=4)
    for index,(state,(color,marker)) in enumerate(STATE_STYLE.items()):
        proportions=np.array([sum(row["state"]==state for row in groups[donor,"C"])/len(groups[donor,"C"]) for donor in donors])
        k.scatter(index+np.linspace(-0.18,0.18,len(donors)),proportions,s=7,color=color,marker=marker,lw=0)
        k.plot([index-0.26,index+0.26],[proportions.mean()]*2,color=INK,lw=0.6)
    k.set(xticks=[0,1,2],xticklabels=["Epi.","Stroma","Immune"],ylabel="Fraction",ylim=(0,0.65),yticks=[0,0.5])

    # Negative/specificity evidence retains equal visual weight at the bottom.
    l=panel(fig,"l","Specificity and direction",5,144,84,22,left=25,bottom=4,top=4)
    selected=["RNA boundary","Protein surface","Lipid module","Invariant control"]
    for index,feature in enumerate(selected):
        sample=delta[feature]/np.std([values[donor,"C",feature] for donor in donors],ddof=1)
        mean,ci=interval(sample)
        l.scatter(sample,index+np.linspace(-0.1,0.1,len(sample)),s=4,color="#B2BEC5",lw=0)
        l.errorbar(mean,index,xerr=[[mean-ci[0]],[ci[1]-mean]],color=INK,marker="o",ms=2,capsize=1.5,lw=0.8)
    l.axvline(0,color=GREY,ls=":",lw=0.5)
    l.set(yticks=range(4),yticklabels=selected,ylim=(3.5,-0.5),xlabel="Paired change / control SD")
    m=panel(fig,"m","Paired sign-flip null",95,144,39,22,left=7,bottom=4,top=4)
    target=delta["RNA boundary"]
    null=(np.random.default_rng(842).choice([-1,1],(2000,len(target)))*target).mean(axis=1)
    m.hist(null,bins=20,color="#D8E1E6",edgecolor="white",lw=0.3)
    m.axvline(target.mean(),color=CORAL,lw=1)
    m.annotate("Observed",(target.mean(),m.get_ylim()[1]*0.96),xytext=(-1,0),textcoords="offset points",
               ha="right",va="top",fontsize=5,color=INK)
    m.set(xlabel="Mean Δ RNA",ylabel="Draws",yticks=[0,200])
    n=panel(fig,"n","Boundary-width sensitivity",139,144,39,22,left=7,bottom=4,top=4)
    radii=[40,80,120,180]
    for radius in radii:
        differences=[]
        for donor in donors:
            means=[np.mean([float(row["rna_boundary"]) for row in groups[donor,condition]
                            if abs(float(row["radial_offset_um"]))<=radius]) for condition in ("C","P")]
            differences.append(means[1]-means[0])
        mean,ci=interval(differences)
        n.errorbar(radius,mean,yerr=[[mean-ci[0]],[ci[1]-mean]],color=BLUE,marker="o",ms=2,capsize=1,lw=0.6)
    n.set(xlabel="Half-width (µm)",ylabel="Δ RNA",xticks=[40,120,180],yticks=[0,0.4])
    fig.text(5/W,1-168.5/H,f"All values synthetic · {len(donors)} paired units · intervals: donor bootstrap 95% · no experimental or significance claims",fontsize=5,va="center",color=GREY)

    helper=EXAMPLE.parents[1]/"shared/figure-core/scripts/render_matplotlib.py"
    spec=importlib.util.spec_from_file_location("atlas_text_bounds",helper)
    bounds=importlib.util.module_from_spec(spec); spec.loader.exec_module(bounds)
    fig.canvas.draw()
    undrawn=set()
    for ax in fig.axes:
        for axis,limits in [(ax.xaxis,ax.get_xlim()),(ax.yaxis,ax.get_ylim())]:
            for tick in axis.get_major_ticks()+axis.get_minor_ticks():
                if not min(limits)<=tick.get_loc()<=max(limits): undrawn.update([tick.label1,tick.label2])
    overflow=[artist.get_text() for artist in fig.findobj(Text)
              if artist not in undrawn and bounds.text_overflow_pt(artist,fig.bbox,fig.canvas.get_renderer())]
    if overflow:
        plt.close(fig)
        raise ValueError(f"Text extends outside page: {overflow}")
    output.mkdir(parents=True,exist_ok=True)
    for extension in ("pdf","svg","png"):
        metadata={"pdf":{"Creator":None,"Producer":None,"CreationDate":None,"ModDate":None},
                  "svg":{"Creator":None,"Date":None},"png":{"Software":None}}[extension]
        fig.savefig(output/f"spatial-multiomics-atlas.{extension}",dpi=300,metadata=metadata,bbox_inches=None)
    plt.close(fig)
    result=dict(panels=14,donors=len(donors),cells=len(cells),width_mm=W,height_mm=H,font=font,text_overflows=len(overflow))
    print(json.dumps(result,sort_keys=True))
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data",type=Path,default=EXAMPLE/"data")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    render(args.data,args.output)
