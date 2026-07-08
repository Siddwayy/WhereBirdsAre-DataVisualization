#!/usr/bin/env python3
"""IBA species composition stacked bars -> viz3_iba.png (standalone)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.family": "sans-serif",
    }
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets" / "images"

df = pd.read_csv(DATA_DIR / "birds.csv")
df["OBSERVATION DATE"] = pd.to_datetime(df["OBSERVATION DATE"])
df["MONTH"] = df["OBSERVATION DATE"].dt.month


def categorize_bird(name):
    n = name.lower()

    def w(k):
        return bool(re.search(r"\b" + re.escape(k) + r"\b", n))

    def any_w(ks):
        return any(w(k) for k in ks)

    if any_w(
        [
            "puffin",
            "murre",
            "gannet",
            "petrel",
            "shearwater",
            "fulmar",
            "razorbill",
            "guillemot",
            "dovekie",
            "cormorant",
            "skua",
            "auk",
        ]
    ):
        return "Seabirds"
    if any_w(
        [
            "duck",
            "goose",
            "swan",
            "teal",
            "merganser",
            "eider",
            "scoter",
            "scaup",
            "goldeneye",
            "bufflehead",
            "wigeon",
            "pintail",
            "shoveler",
            "gadwall",
            "mallard",
            "canvasback",
            "redhead",
            "loon",
            "grebe",
            "brant",
        ]
    ):
        return "Waterfowl"
    if any_w(
        [
            "sandpiper",
            "plover",
            "turnstone",
            "yellowlegs",
            "whimbrel",
            "dowitcher",
            "dunlin",
            "sanderling",
            "phalarope",
            "snipe",
            "woodcock",
            "killdeer",
            "oystercatcher",
            "curlew",
            "godwit",
            "knot",
            "stilt",
        ]
    ):
        return "Shorebirds"
    if any_w(
        [
            "hawk",
            "eagle",
            "falcon",
            "owl",
            "harrier",
            "osprey",
            "merlin",
            "kestrel",
            "goshawk",
            "vulture",
            "kite",
        ]
    ):
        return "Raptors"
    if any_w(["gull", "tern", "jaeger", "kittiwake"]):
        return "Gulls & Terns"
    return "Songbirds & Other"


df["CATEGORY"] = df["COMMON NAME"].apply(categorize_bird)

iba = df.dropna(subset=["IBA NAME"]).copy()
iba = iba.assign(IBA_SINGLE=iba["IBA NAME"].str.split("|")).explode("IBA_SINGLE")
iba["IBA_SINGLE"] = iba["IBA_SINGLE"].str.strip()

iba_names = {
    "BIRDLIFE_11191": "Cape St. Mary's",
    "BIRDLIFE_11192": "Witless Bay Islands",
    "BIRDLIFE_11193": "Baccalieu Island",
    "BIRDLIFE_11204": "Quidi Vidi Lake",
    "BIRDLIFE_11206": "Cape Freels",
    "BIRDLIFE_11207": "Placentia Bay",
    "US-AK_4545": "Northern Peninsula IBA",
    "CA-NF_022": "Quidi Vidi Lake",
}
iba["IBA_LABEL"] = iba["IBA_SINGLE"].map(lambda x: iba_names.get(x, x))

iba_top = (
    iba.groupby("IBA_LABEL")
    .agg(spp=("COMMON NAME", "nunique"), obs=("GLOBAL UNIQUE IDENTIFIER", "count"))
    .sort_values("spp", ascending=False)
    .head(8)
)

iba_cat = (
    iba[iba["IBA_LABEL"].isin(iba_top.index)]
    .groupby(["IBA_LABEL", "CATEGORY"])["COMMON NAME"]
    .nunique()
    .reset_index(name="spp")
)

CAT_ORDER = [
    "Seabirds",
    "Waterfowl",
    "Shorebirds",
    "Raptors",
    "Gulls & Terns",
    "Songbirds & Other",
]
CAT_COLORS = {
    # category colors
    "Seabirds": "#4c78a8",
    "Waterfowl": "#72b7b2",
    "Shorebirds": "#f2cf5b",
    "Raptors": "#b279a2",
    "Gulls & Terns": "#e45756",
    "Songbirds & Other": "#6f5f58",
}

piv = iba_cat.pivot_table(index="IBA_LABEL", columns="CATEGORY", values="spp", fill_value=0)
piv["_t"] = piv.sum(axis=1)
piv = piv.sort_values("_t", ascending=True).drop("_t", axis=1)

# helper to wrap text
def wrap_label(s):
    if len(s) <= 22:
        return s
    cut = s.rfind(" ", 0, 22)
    if cut == -1:
        cut = 22
    return s[:cut] + "\n" + s[cut + 1 :]


labels = [wrap_label(x) for x in piv.index.tolist()]
totals = piv.sum(axis=1).astype(int).values
y = np.arange(len(piv))

FIG_BG = "#f9f7f0"
fig, ax = plt.subplots(figsize=(12.2, 6.6), facecolor=FIG_BG)
ax.set_facecolor("white")

# alternate row backgrounds
for i in range(len(y)):
    if i % 2 == 0:
        ax.axhspan(i - 0.43, i + 0.43, color="#f7f7f7", alpha=0.55, zorder=0)

left = np.zeros(len(piv))
for cat in CAT_ORDER:
    if cat in piv.columns:
        v = piv[cat].values
        ax.barh(
            y,
            v,
            left=left,
            label=cat,
            color=CAT_COLORS[cat],
            edgecolor="#000000",
            linewidth=0.5,
            height=0.74,
            zorder=2,
        )
        left += v

# draw totals on the right
for yi, t in zip(y, totals):
    ax.text(
        t + 1.4,
        yi,
        f"{t}",
        va="center",
        ha="left",
        fontsize=9.6,
        fontweight="bold",
        color="#1f2937",
    )

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9.5)
ax.set_xlim(0, totals.max() * 1.12)
ax.set_xlabel("Total unique species richness", fontsize=12, color="#111827")

# median line
median_total = float(np.median(totals))
ax.axvline(median_total, color="#9ca3af", linestyle="--", linewidth=1.2, alpha=0.9, zorder=1)
ax.text(
    median_total,
    len(y) - 0.22,
    f"Median total: {int(median_total)}",
    ha="left",
    va="bottom",
    fontsize=9,
    fontweight="bold",
    color="#374151",
    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.9),
)

# custom legend position
handles, lg_labels = ax.get_legend_handles_labels()
fig.legend(
    handles,
    lg_labels,
    ncol=3,
    frameon=True,
    bbox_to_anchor=(0.5, 0.885),
    loc="upper center",
    fontsize=9,
    handlelength=1.9,
    columnspacing=1.4,
    facecolor=FIG_BG,
    edgecolor="none",
)

# add title and subtitle
fig.text(
    0.5,
    0.965,
    "Northern Peninsula IBA Shows the Broadest Species Richness in 2025",
    ha="center",
    va="top",
    fontsize=17,
    fontweight="bold",
    color="#0c2e21",
)
fig.text(
    0.5,
    0.922,
    "Stacked segments show composition by bird group; total bar length = unique species richness.",
    ha="center",
    va="top",
    fontsize=10,
    color="#4a4a4a",
)

# highlight top location
top_i = int(np.argmax(totals))
ax.annotate(
    "Highest total richness\nwith broad composition",
    xy=(totals[top_i], top_i),
    xytext=(56, 34),
    textcoords="offset points",
    ha="left",
    va="bottom",
    fontsize=9.5,
    fontweight="bold",
    color="#0b3a63",
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#0b3a63", linewidth=1.0, alpha=1.0),
    arrowprops=dict(
        arrowstyle="->",
        color="#0b3a63",
        lw=1.2,
        shrinkA=0,
        shrinkB=0,
        connectionstyle="arc3,rad=-0.12",
    ),
    clip_on=False,
    zorder=30,
)

# clean axes
ax.grid(axis="x", color="#e5e7eb", linewidth=0.8)
ax.grid(axis="y", visible=False)
ax.tick_params(axis="x", colors="#000000", width=1.2, length=5)
ax.tick_params(axis="y", colors="#000000", length=0)
for _t in ax.get_xticklabels() + ax.get_yticklabels():
    _t.set_color("#000000")
    _t.set_fontweight("bold")
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#d1d5db")

# chart border
from matplotlib.patches import Rectangle
BORDER_LW = 2.2
x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
ax.add_patch(
    Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        transform=ax.transData,
        fill=False,
        edgecolor="#000000",
        linewidth=BORDER_LW,
        zorder=20,
    )
)

fig.subplots_adjust(left=0.28, right=0.97, top=0.74, bottom=0.12)
out = ASSETS_DIR / "viz3_iba.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor=FIG_BG)
plt.close()
print(f"Saved {out}")
