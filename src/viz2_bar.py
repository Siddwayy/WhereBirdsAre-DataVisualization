#!/usr/bin/env python3
"""County species richness bar chart -> viz2_bar.png (standalone)."""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
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

cty = (
    df.groupby("COUNTY")
    .agg(spp=("COMMON NAME", "nunique"), obs=("GLOBAL UNIQUE IDENTIFIER", "count"))
    .sort_values("spp", ascending=True)
    .reset_index()
)

county_short = {
    "Avalon Peninsula-St. John's": "Avalon Peninsula",
    "St. George's-Stephenville": "St. George's",
    "Northern Peninsula-St. Anthony": "Northern Peninsula",
    "Bonavista/Trinity-Clarenville": "Bonavista / Trinity",
    "Labrador-Happy Valley-Goose Bay": "Labrador (HVGB)",
    "Central Newfoundland-Grand Falls-Windsor": "Central NL",
    "Burin Peninsula-Marystown": "Burin Peninsula",
    "Humber District-Corner Brook": "Humber District",
    "Notre Dame Bay-Lewisporte": "Notre Dame Bay",
    "South Coast-Channel-Port aux Basques": "South Coast",
    "Nunatsiavut-Nain": "Nunatsiavut",
}
cty["label"] = cty["COUNTY"].map(county_short)

FIG_BG = "#f9f7f0"
TITLE_GREEN = "#0c2e21"
SUBHEAD_GRAY = "#4a4a4a"

# get prepared data
vals = cty["spp"].astype(float).values
labels = cty["label"].values
n = len(cty)
y = np.arange(n)

avalon_county = "Avalon Peninsula-St. John's"
avalon_mask = cty["COUNTY"].values == avalon_county
avalon_i = int(np.where(avalon_mask)[0][0]) if avalon_mask.any() else None
avalon_val = int(vals[avalon_i]) if avalon_i is not None else None

vals_int = vals.astype(int)
median_val = float(np.median(vals))

# get color tiers
order_desc = np.argsort(vals)[::-1]
leader_i = int(order_desc[0]) if n > 0 else None
high_set = set(order_desc[1:4].tolist())
mid_set = set(order_desc[4:7].tolist())
low_set = set(order_desc[7:].tolist())

LEADER_COLOR = "#0b3a63"
HIGH_COLOR = "#2c7fb8"
MID_COLOR = "#9bbdd3"
LOW_COLOR = "#d6dde6"

bar_colors = []
for i in range(n):
    if i == leader_i:
        bar_colors.append(LEADER_COLOR)
    elif i in high_set:
        bar_colors.append(HIGH_COLOR)
    elif i in mid_set:
        bar_colors.append(MID_COLOR)
    else:
        bar_colors.append(LOW_COLOR)

# setup layout grids
fig = plt.figure(figsize=(12.8, 7.0), facecolor=FIG_BG)
gs = fig.add_gridspec(2, 1, height_ratios=[0.95, 4.9], hspace=0.18)

ax_card = fig.add_subplot(gs[0])
ax_card.axis("off")

ax = fig.add_subplot(gs[1])
ax.set_facecolor("white")

fig.patch.set_facecolor(FIG_BG)

# add title and subtitle
fig.text(
    0.5,
    0.965,
    "Avalon Peninsula Leads Bird Species Richness in 2025",
    ha="center",
    va="top",
    fontsize=18,
    fontweight="bold",
    color=TITLE_GREEN,
)
fig.text(
    0.5,
    0.905,
    "Horizontal ranking of unique species counts per county (2025 field season).",
    ha="center",
    va="top",
    fontsize=10.5,
    fontweight="normal",
    color=SUBHEAD_GRAY,
)

# add background bands
def _band(i0, i1, color, alpha):
    y0 = min(i0, i1) - 0.5
    y1 = max(i0, i1) + 0.5
    ax.axhspan(y0, y1, color=color, alpha=alpha, zorder=0)

if leader_i is not None:
    _band(leader_i, leader_i, LEADER_COLOR, 0.08)
for i in high_set:
    pass
if len(high_set) > 0:
    _band(min(high_set), max(high_set), HIGH_COLOR, 0.05)
if len(mid_set) > 0:
    _band(min(mid_set), max(mid_set), MID_COLOR, 0.04)
if len(low_set) > 0:
    _band(min(low_set), max(low_set), LOW_COLOR, 0.02)

bars = ax.barh(
    y,
    vals,
    color=bar_colors,
    edgecolor="#000000",
    linewidth=0.6,
    height=0.72,
    zorder=2,
)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10)

ax.set_xlim(0, float(vals.max()) * 1.18)
ax.set_xlabel("Unique species richness", fontsize=12)

# draw median line
ax.axvline(median_val, color="#9ca3af", linewidth=1.2, linestyle="--", alpha=0.8, zorder=1)
ax.annotate(
    f"Provincial median: {int(median_val)}",
    xy=(median_val, 1.01),
    xycoords=("data", "axes fraction"),
    ha="left",
    va="bottom",
    fontsize=10,
    fontweight="bold",
    color="#111111",
    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9),
    annotation_clip=False,
)

# clean gridlines
ax.grid(axis="x", color="#e5e7eb", linewidth=0.9)
ax.grid(axis="y", visible=False)

for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#d1d5db")

# format axes
ax.tick_params(axis="x", colors="#000000", width=1.2, length=5)
ax.tick_params(axis="y", colors="#000000", length=0)
for _t in ax.get_xticklabels() + ax.get_yticklabels():
    _t.set_color("#000000")
    _t.set_fontweight("bold")

# add chart border
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

# draw value labels
for b, v, i in zip(bars, vals, range(n)):
    yy = b.get_y() + b.get_height() / 2
    is_leader = (i == leader_i)
    color = LEADER_COLOR if is_leader else "#374151"
    x_text = v + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
    ax.annotate(
        f"{int(v)}",
        (v, yy),
        xytext=(8 if not is_leader else 10, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=10,
        fontweight=("bold" if is_leader else "semibold"),
        color=color,
        bbox=dict(
            boxstyle="round,pad=0.18",
            fc="white",
            ec="none",
            alpha=0.72 if is_leader else 0.0,
        ),
        clip_on=False,
        zorder=3,
    )

# draw top card
if avalon_i is not None:
    diff = avalon_val - median_val
    ax_card.set_xlim(0, 1)
    ax_card.set_ylim(0, 1)
    ax_card.text(
        0.03,
        0.75,
        "Insight",
        fontsize=10,
        fontweight="bold",
        color=TITLE_GREEN,
    )
    ax_card.text(
        0.03,
        0.48,
        f"Avalon Peninsula",
        fontsize=14,
        fontweight="bold",
        color=LEADER_COLOR,
    )
    ax_card.text(
        0.03,
        0.28,
        f"Unique species: {avalon_val}",
        fontsize=11.5,
        fontweight="normal",
        color="#111827",
    )
    ax_card.text(
        0.03,
        0.10,
        f"{'+' if diff >= 0 else ''}{int(diff)} above provincial median",
        fontsize=10,
        fontweight="normal",
        color=SUBHEAD_GRAY,
    )
    # divider line
    ax_card.plot([0.03, 0.97], [0.63, 0.63], color="#e5e7eb", linewidth=1.0)

out = ASSETS_DIR / "viz2_bar.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor=FIG_BG)
plt.close()
print(f"Saved {out}")
