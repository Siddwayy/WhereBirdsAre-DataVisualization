#!/usr/bin/env python3
"""Geographic hotspot map -> viz1_map.png (standalone; same logic as notebook viz1 cell)."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import re
import seaborn as sns
import warnings
from matplotlib.colors import Normalize

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
df["OBS_COUNT_NUM"] = pd.to_numeric(df["OBSERVATION COUNT"], errors="coerce")
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

loc = (
    df.groupby(["LOCALITY", "LATITUDE", "LONGITUDE"])
    .agg(
        obs=("GLOBAL UNIQUE IDENTIFIER", "count"),
        spp=("COMMON NAME", "nunique"),
        county=("COUNTY", "first"),
    )
    .reset_index()
)

try:
    import geopandas as gpd
except ImportError:
    gpd = None

FIG_BG = "#f9f7f0"
# ocean blue
OCEAN = "#9ecae1"
# land colors
LAND_FILL = "#1b4d2e"
# outline color
LAND_EDGE = "#1f1f1f"

fig, ax = plt.subplots(figsize=(11.2, 7.6), facecolor=FIG_BG)
ax.set_facecolor(OCEAN)

pad_lon, pad_lat = 0.65, 0.55
lon0 = max(loc["LONGITUDE"].min() - pad_lon, -67.85)
lon1 = min(loc["LONGITUDE"].max() + pad_lon, -51.85)
lat0 = max(loc["LATITUDE"].min() - pad_lat, 46.35)
lat1 = min(loc["LATITUDE"].max() + pad_lat, 60.9)

if gpd is not None:
    try:
        local_land = DATA_DIR / "NL_Land_Bound_4792812732831105689.geojson"
        if local_land.exists():
            land = gpd.read_file(local_land)
        else:
            raise FileNotFoundError(str(local_land))

        # clip to extent
        land = land.set_crs(4326) if land.crs is None else land.to_crs(4326)
        land = land.cx[lon0:lon1, lat0:lat1]

        land.plot(
            ax=ax,
            color=LAND_FILL,
            edgecolor=LAND_EDGE,
            linewidth=0.28,
            # solid land
            alpha=0.65,
            zorder=1,
            aspect=None,
        )
    except Exception as _e:
        print(f"Basemap skipped (local geojson failed): {_e}")

ax.set_xlim(lon0, lon1)
ax.set_ylim(lat0, lat1)
ax.set_aspect("equal", adjustable="box")

# map border
from matplotlib.patches import Rectangle
BORDER_COLOR = "#000000"
BORDER_LW = 2.2
ax.add_patch(
    Rectangle(
        (lon0, lat0),
        lon1 - lon0,
        lat1 - lat0,
        transform=ax.transData,
        fill=False,
        edgecolor=BORDER_COLOR,
        linewidth=BORDER_LW,
        zorder=20,
    )
)


def obs_to_size(obs):
    x = np.asarray(obs, dtype=float)
    return np.clip(np.log1p(x) * 3.2, 4, 72)


sizes = obs_to_size(loc["obs"])
norm = Normalize(vmin=loc["spp"].min(), vmax=loc["spp"].max())
# color gradient
cmap = plt.get_cmap("magma")

sc = ax.scatter(
    loc["LONGITUDE"],
    loc["LATITUDE"],
    s=sizes,
    c=loc["spp"],
    cmap=cmap,
    norm=norm,
    alpha=0.44,
    edgecolors="white",
    linewidths=0.14,
    zorder=5,
)

cb = plt.colorbar(sc, ax=ax, shrink=0.6, pad=0.018)
cb.set_label("Unique species per locality", fontsize=10, labelpad=8)
cb.ax.tick_params(labelsize=9)
cb.outline.set_visible(False)
cb.ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True, min_n_ticks=4))

avalon_county = "Avalon Peninsula-St. John's"
avalon_pct = 100 * (df["COUNTY"] == avalon_county).sum() / len(df)
ax.text(
    0.02,
    0.98,
    f"Avalon Peninsula (St. John's region)\n{avalon_pct:.1f}% of all observations",
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="top",
    color="#333",
    bbox=dict(
        boxstyle="round,pad=0.42",
        facecolor="white",
        edgecolor="#c8c5c0",
        linewidth=0.75,
        alpha=0.94,
    ),
)

regions = [
    # position labels away from land
    ("Northern\nPeninsula", "Northern Peninsula-St. Anthony", (-55, 8)),
    # lift south coast label
    ("South coast", "South Coast-Channel-Port aux Basques", (-18, -15)),
    # adjust labrador label
    ("Labrador", "Labrador-Happy Valley-Goose Bay", (55, 35)),
]
for label, county_key, xyoff in regions:
    sub = loc.loc[loc["county"] == county_key]
    if sub.empty:
        continue
    rlon = sub["LONGITUDE"].median()
    rlat = sub["LATITUDE"].median()
    ax.annotate(
        label,
        (rlon, rlat),
        xytext=xyoff,
        textcoords="offset points",
        fontsize=8,
        color="#111111",
        ha="center",
        zorder=7,
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor=(1, 1, 1, 0.9),
            edgecolor="#111111",
            linewidth=0.85,
        ),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#111111",
            lw=0.95,
            mutation_scale=11,
            shrinkA=0,
            shrinkB=0,
        ),
    )

ap = loc.loc[loc["county"] == avalon_county]
if not ap.empty:
    ax.annotate(
        "Avalon",
        (ap["LONGITUDE"].median(), ap["LATITUDE"].median()),
        xytext=(42, -48),
        textcoords="offset points",
        fontsize=8.5,
        color="#111111",
        style="italic",
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor=(1, 1, 1, 0.9),
            edgecolor="#111111",
            linewidth=0.85,
        ),
        zorder=7,
        ha="left",
        arrowprops=dict(
            arrowstyle="-|>",
            color="#111111",
            lw=0.95,
            mutation_scale=11,
            shrinkA=0,
            shrinkB=0,
        ),
    )

for spine in ax.spines.values():
    spine.set_visible(False)

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{abs(x):.0f}\u00b0W")
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0f}\u00b0N"))
# bold axes
ax.tick_params(axis="both", labelsize=9, colors="#000000", length=4, width=1.2)
for _t in ax.get_xticklabels() + ax.get_yticklabels():
    _t.set_color("#000000")
    _t.set_fontweight("bold")

# grid in ocean
ax.set_axisbelow(True)
ax.grid(True, which="major", color="#bdbdbd", linewidth=0.25, alpha=0.22, zorder=0)

TITLE_GREEN = "#0c2e21"
SUBHEAD_GRAY = "#4a4a4a"
fig.subplots_adjust(left=0.07, right=0.98, top=0.70, bottom=0.08)
ax.text(
    0.5,
    1.20,
    "01 Geographic Hotspots Map",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=17,
    fontweight="bold",
    color=TITLE_GREEN,
    clip_on=False,
)
ax.text(
    0.5,
    1.125,
    "This map plots every unique birding locality across NL in 2025.\n"
    'It identifies where activity is densest and where biodiversity "hotspots" '
    "actually occur across the province.",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=9,
    fontweight="normal",
    color=SUBHEAD_GRAY,
    linespacing=1.22,
    clip_on=False,
)

for v, lab in [(10, "~10 obs"), (100, "~100 obs"), (1000, "1 000+ obs")]:
    ax.scatter(
        [],
        [],
        s=float(obs_to_size([v])[0]),
        c="#4a3d5c",
        alpha=0.48,
        edgecolors="white",
        linewidths=0.14,
        label=lab,
    )
handles, labels = ax.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    title="Observation count\n(scaled for overlap)",
    loc="upper right",
    bbox_to_anchor=(0.99, 0.848),
    bbox_transform=fig.transFigure,
    fontsize=8,
    title_fontsize=8.5,
    framealpha=0.96,
    edgecolor="#dcdcdc",
    fancybox=False,
    borderpad=0.55,
)

out = ASSETS_DIR / "viz1_map.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor=FIG_BG, edgecolor="none")
plt.close()
print(f"Saved {out}")
