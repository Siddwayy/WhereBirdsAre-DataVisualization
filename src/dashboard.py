"""
Where the Birds Are — NL Bird Dashboard (2025)
Interactive Dash dashboard for COMP-4304 Project
North Atlantic Theme — Newfoundland & Labrador
"""

import base64
import pandas as pd
import numpy as np
import re
from dash import Dash, dcc, html, Input, Output, State, callback_context, clientside_callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# CSS styles

EMBEDDED_CSS = """
*, *::before, *::after { box-sizing: border-box; }
html, body {
    margin: 0; padding: 0; height: 100vh; overflow: hidden;
    -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}
.theme-dark {
    --bg-page: #080E1A; --bg-card: rgba(13,27,46,0.75); --bg-card-solid: #0D1B2E;
    --accent: #00D4B4; --accent-orange: #FF6B35; --accent-gold: #FFD166;
    --accent-electric: #4ECDC4; --text-heading: #E8F4F8; --text-primary: #C8D8E8;
    --text-muted: #5A7A8A; --text-on-dark: #E8F4F8;
    --border: rgba(0,212,180,0.12); --border-hover: rgba(0,212,180,0.35);
    --glow: rgba(0,212,180,0.08); --input-bg: rgba(8,14,26,0.8);
    --input-border: rgba(0,212,180,0.2); --input-text: #C8D8E8;
    --slider-rail: rgba(0,212,180,0.15); --slider-track: #00D4B4;
    --mark-text: #5A7A8A; --shadow-1: rgba(0,0,0,0.4); --shadow-2: rgba(0,0,0,0.3);
    --scrollbar-track: #080E1A; --scrollbar-thumb: rgba(0,212,180,0.3);
}
.theme-light {
    --bg-page: #F0F4F8; --bg-card: rgba(255,255,255,0.72); --bg-card-solid: #FFFFFF;
    --accent: #2A9D8F; --accent-orange: #E76F51; --accent-gold: #D4880F;
    --accent-electric: #2A9D8F; --text-heading: #1A202C; --text-primary: #2D3748;
    --text-muted: #718096; --text-on-dark: #FAFAF8;
    --border: rgba(42,157,143,0.18); --border-hover: rgba(42,157,143,0.45);
    --glow: rgba(42,157,143,0.08); --input-bg: rgba(255,255,255,0.9);
    --input-border: rgba(42,157,143,0.25); --input-text: #2D3748;
    --slider-rail: rgba(42,157,143,0.15); --slider-track: #2A9D8F;
    --mark-text: #718096; --shadow-1: rgba(11,29,58,0.08); --shadow-2: rgba(11,29,58,0.05);
    --scrollbar-track: #F0F4F8; --scrollbar-thumb: rgba(42,157,143,0.3);
}
#app-root {
    height: 100vh; overflow: hidden; display: flex; flex-direction: column;
    background-color: var(--bg-page); transition: background-color 0.4s ease;
}
.theme-dark #app-root, .theme-dark {
    background-color: #080E1A;
    background-image: radial-gradient(ellipse 80% 50% at 50% 0%, rgba(0,212,180,0.04) 0%, transparent 60%);
}
#app-header {
    height: 60px; min-height: 60px; flex-shrink: 0; display: flex; align-items: center;
    padding: 0 24px; gap: 14px; position: relative; z-index: 10;
    background: radial-gradient(ellipse 60% 100% at 0% 50%, rgba(0,212,180,0.12) 0%, transparent 50%),
                radial-gradient(ellipse 40% 100% at 100% 50%, rgba(255,107,53,0.08) 0%, transparent 45%),
                linear-gradient(135deg, #050B14 0%, #0D1B2E 100%);
    border-bottom: 2px solid #00D4B4;
    box-shadow: 0 2px 0 rgba(0,212,180,0.15), 0 4px 24px rgba(0,0,0,0.4);
}
#header-title h1 {
    margin: 0; font-size: 20px; font-weight: 700; font-style: italic;
    font-family: 'Playfair Display', Georgia, serif; letter-spacing: -0.3px; line-height: 1.15;
    background: linear-gradient(90deg, #E8F4F8 0%, #E8F4F8 35%, #00D4B4 50%, #E8F4F8 65%, #E8F4F8 100%);
    background-size: 200% auto; -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; animation: shimmer 6s linear infinite;
}
@keyframes shimmer { from { background-position: 200% center; } to { background-position: -200% center; } }
#header-title span { color: #5A7A8A; font-size: 10.5px; font-family: 'DM Sans', system-ui, sans-serif; letter-spacing: 0.5px; }
#header-spacer { flex: 1; }
#theme-toggle {
    width: 34px; height: 34px; border-radius: 50%; border: 1px solid rgba(0,212,180,0.25);
    background: rgba(0,212,180,0.08); color: #E8F4F8; font-size: 16px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; padding: 0;
}
#theme-toggle:hover { background: rgba(0,212,180,0.18); box-shadow: 0 0 12px rgba(0,212,180,0.2); transform: scale(1.08); }
#reset-btn {
    font-size: 10px; padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(0,212,180,0.25);
    background: rgba(0,212,180,0.08); color: #E8F4F8; cursor: pointer;
    font-family: 'DM Sans', system-ui, sans-serif; font-weight: 500;
    transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}
#reset-btn:hover { background: rgba(0,212,180,0.2); box-shadow: 0 0 12px rgba(0,212,180,0.15); transform: scale(1.03); }
#reset-btn:active { transform: scale(0.97); }
.stat-badges-row { display: flex; gap: 10px; align-items: center; }
.stat-badge {
    display: flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 8px;
    background: rgba(255,209,102,0.06); border: 1px solid rgba(255,209,102,0.15);
    border-top: 1px solid rgba(255,209,102,0.25);
    transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    position: relative; overflow: hidden;
}
.stat-badge::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,209,102,0.04) 0%, transparent 60%); pointer-events: none;
}
.stat-badge:hover { background: rgba(255,209,102,0.10); border-color: rgba(255,209,102,0.35); box-shadow: 0 0 16px rgba(255,209,102,0.10); }
.stat-badge .stat-icon { font-size: 13px; }
.stat-badge .stat-value {
    font-family: 'DM Sans', system-ui, sans-serif; font-size: 16px; font-weight: 600;
    font-variant-numeric: tabular-nums; color: #FFD166; line-height: 1.1;
}
.stat-badge .stat-label {
    font-size: 8px; letter-spacing: 1.2px; text-transform: uppercase; color: #5A7A8A;
    font-family: 'DM Sans', system-ui, sans-serif; font-weight: 500;
}
#app-body {
    flex: 1; min-height: 0; display: grid; grid-template-columns: 60% 40%;
    grid-template-rows: 1fr 1fr; gap: 10px; padding: 10px;
}
#map-panel      { grid-column: 1; grid-row: 1 / 3; }
#bar-panel      { grid-column: 2; grid-row: 1; }
#seasonal-panel { grid-column: 2; grid-row: 2; }
.panel {
    background: var(--bg-card); backdrop-filter: blur(16px) saturate(150%);
    -webkit-backdrop-filter: blur(16px) saturate(150%); border-radius: 14px;
    border: 1px solid var(--border);
    box-shadow: 0 0 0 1px var(--glow), 0 4px 24px var(--shadow-1), 0 1px 4px var(--shadow-2),
                inset 0 1px 0 rgba(255,255,255,0.04);
    display: flex; flex-direction: column; overflow: hidden; padding: 12px 14px 6px 14px;
    position: relative; animation: fadeSlideIn 0.5s ease-out both;
}
#map-panel      { animation-delay: 0.05s; }
#bar-panel      { animation-delay: 0.15s; }
#seasonal-panel { animation-delay: 0.25s; }
.panel-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-shrink: 0; margin-bottom: 4px; }
.panel-title {
    margin: 0; color: var(--text-heading); font-size: 14px; font-weight: 800;
    font-family: 'Playfair Display', Georgia, serif; letter-spacing: 0.2px;
    white-space: nowrap; padding-left: 12px; position: relative;
}
.panel-title::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--accent), var(--accent-electric, var(--accent)));
    border-radius: 0 2px 2px 0; box-shadow: 0 0 8px var(--glow);
}
.panel-caption {
    margin: 0; font-size: 10px; color: var(--text-muted); font-family: 'DM Sans', system-ui, sans-serif;
    font-weight: 400; letter-spacing: 0.4px; text-transform: uppercase; padding-left: 12px; margin-top: 2px;
}
.panel-controls { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.map-controls-row { display: flex; align-items: center; gap: 14px; flex-shrink: 0; margin-bottom: 4px; padding: 4px 0; }
.map-controls-row .slider-wrap { flex: 1; min-width: 200px; }
.control-group { display: flex; align-items: center; gap: 6px; }
.control-label {
    font-size: 9px; font-weight: 600; color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 0.5px; white-space: nowrap; font-family: 'DM Sans', system-ui, sans-serif;
}
.graph-wrapper { flex: 1; min-height: 0; position: relative; }
.graph-wrapper > div, .graph-wrapper > div > div, .graph-wrapper > div > div > div { height: 100% !important; width: 100% !important; }
.graph-wrapper .js-plotly-plot, .graph-wrapper .plot-container, .graph-wrapper .svg-container { height: 100% !important; width: 100% !important; }
.graph-wrapper .main-svg { height: 100% !important; width: 100% !important; }
.bird-watermark { position: absolute; bottom: 12px; right: 16px; opacity: 0.06; pointer-events: none; z-index: 0; }
.Select-control { border: 1px solid var(--input-border) !important; border-radius: 8px !important; min-height: 30px !important; background-color: var(--input-bg) !important; font-size: 12px !important; transition: border-color 0.2s ease, box-shadow 0.2s ease !important; }
.Select-control:hover { border-color: var(--accent) !important; }
.is-focused > .Select-control { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--glow) !important; }
.Select-menu-outer { border: 1px solid var(--input-border) !important; border-radius: 8px !important; box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important; margin-top: 2px !important; background-color: var(--bg-card-solid) !important; }
.Select-option { color: var(--text-primary) !important; }
.Select-option.is-focused { background-color: rgba(0,212,180,0.15) !important; color: var(--text-heading) !important; }
.Select-option.is-selected { background-color: var(--accent) !important; color: #FAFAF8 !important; }
.Select-value-label { color: var(--input-text) !important; font-size: 12px !important; }
.Select-placeholder { color: var(--text-muted) !important; font-size: 12px !important; }
.Select-arrow-zone { color: var(--text-muted) !important; }
.rc-slider-track { background: linear-gradient(90deg, var(--accent), var(--accent-electric, var(--accent))) !important; box-shadow: 0 0 8px var(--glow) !important; height: 4px !important; }
.rc-slider-rail { background-color: var(--slider-rail) !important; height: 4px !important; }
.rc-slider-handle { border-color: var(--accent) !important; background-color: var(--bg-card-solid) !important; box-shadow: 0 1px 6px rgba(0,0,0,0.3) !important; width: 14px !important; height: 14px !important; margin-top: -5px !important; transition: border-color 0.2s, box-shadow 0.2s !important; }
.rc-slider-handle:hover, .rc-slider-handle:active { border-color: var(--accent) !important; box-shadow: 0 0 0 4px var(--glow), 0 0 12px var(--glow) !important; }
.rc-slider-dot-active { border-color: var(--accent) !important; }
.rc-slider-mark-text { font-size: 9px !important; color: var(--mark-text) !important; }
.rc-slider-tooltip-inner { background-color: var(--bg-card-solid) !important; color: var(--text-heading) !important; border-radius: 6px !important; font-size: 11px !important; font-family: 'DM Sans', system-ui, sans-serif !important; padding: 3px 8px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important; }
#app-footer { height: 24px; min-height: 24px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: #050B14; color: #5A7A8A; font-size: 9px; font-family: 'DM Sans', system-ui, sans-serif; letter-spacing: 0.5px; border-top: 1px solid rgba(0,212,180,0.08); }
.modebar { display: none !important; }
@keyframes fadeSlideIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
@media (hover: hover) {
    .panel { transition: box-shadow 0.3s ease, border-color 0.3s ease, transform 0.25s ease; }
    .panel:hover { border-color: var(--border-hover); box-shadow: 0 0 0 1px var(--glow), 0 0 24px var(--glow), 0 8px 40px var(--shadow-1); transform: translateY(-2px); }
}
.panel:focus-within { border-color: var(--border-hover); box-shadow: 0 0 0 2px var(--glow), 0 4px 24px var(--shadow-1); }
._dash-loading { color: var(--accent) !important; }
.dash-spinner { border-color: rgba(0,212,180,0.15) !important; border-top-color: var(--accent) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
@media (max-width: 960px) {
    #app-root, .theme-dark, .theme-light { height: auto; overflow: auto; }
    #app-body { grid-template-columns: 1fr; grid-template-rows: auto auto auto; height: auto; }
    #map-panel      { grid-column: 1; grid-row: 1; min-height: 500px; }
    #bar-panel      { grid-column: 1; grid-row: 2; min-height: 350px; }
    #seasonal-panel { grid-column: 1; grid-row: 3; min-height: 350px; }
    .stat-badges-row { display: none; }
}
"""

# load and prepare data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
df = pd.read_csv(DATA_DIR / 'birds.csv')
df['OBS_COUNT_NUM'] = pd.to_numeric(df['OBSERVATION COUNT'], errors='coerce')
df['OBSERVATION DATE'] = pd.to_datetime(df['OBSERVATION DATE'])
df['MONTH'] = df['OBSERVATION DATE'].dt.month

MONTH_NAMES = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

# categorize bird species
def categorize_bird(name):
    n = name.lower()
    def w(k): return bool(re.search(r'\b' + re.escape(k) + r'\b', n))
    def any_w(ks): return any(w(k) for k in ks)

    if any_w(['puffin','murre','gannet','petrel','shearwater','fulmar',
              'razorbill','guillemot','dovekie','cormorant','skua','auk']):
        return 'Seabirds'
    if any_w(['duck','goose','swan','teal','merganser','eider','scoter','scaup',
              'goldeneye','bufflehead','wigeon','pintail','shoveler','gadwall',
              'mallard','canvasback','redhead','loon','grebe','brant']):
        return 'Waterfowl'
    if any_w(['sandpiper','plover','turnstone','yellowlegs','whimbrel','dowitcher',
              'dunlin','sanderling','phalarope','snipe','woodcock','killdeer',
              'oystercatcher','curlew','godwit','knot','stilt']):
        return 'Shorebirds'
    if any_w(['hawk','eagle','falcon','owl','harrier','osprey','merlin',
              'kestrel','goshawk','vulture','kite']):
        return 'Raptors'
    if any_w(['gull','tern','jaeger','kittiwake']):
        return 'Gulls & Terns'
    return 'Songbirds & Other'

df['CATEGORY'] = df['COMMON NAME'].apply(categorize_bird)

# short names for counties
county_short = {
    "Avalon Peninsula-St. John's":       "Avalon Peninsula",
    "St. George's-Stephenville":         "St. George's",
    "Northern Peninsula-St. Anthony":    "Northern Peninsula",
    "Bonavista/Trinity-Clarenville":     "Bonavista / Trinity",
    "Labrador-Happy Valley-Goose Bay":   "Labrador (HVGB)",
    "Central Newfoundland-Grand Falls-Windsor": "Central NL",
    "Burin Peninsula-Marystown":         "Burin Peninsula",
    "Humber District-Corner Brook":      "Humber District",
    "Notre Dame Bay-Lewisporte":         "Notre Dame Bay",
    "South Coast-Channel-Port aux Basques": "South Coast",
    "Nunatsiavut-Nain":                  "Nunatsiavut",
}
df['COUNTY_SHORT'] = df['COUNTY'].map(county_short).fillna(df['COUNTY'])

# pre-compute data
loc_agg = (df.groupby(['LOCALITY', 'LATITUDE', 'LONGITUDE', 'CATEGORY', 'MONTH', 'COUNTY_SHORT'])
             .agg(obs=('GLOBAL UNIQUE IDENTIFIER', 'count'),
                  spp=('COMMON NAME', 'nunique'))
             .reset_index())

cty_agg = (df.groupby(['COUNTY_SHORT', 'CATEGORY'])
             .agg(spp=('COMMON NAME', 'nunique'))
             .reset_index())

seasonal_agg = (df.groupby(['COUNTY_SHORT', 'CATEGORY', 'MONTH'])
                  .agg(obs=('GLOBAL UNIQUE IDENTIFIER', 'count'))
                  .reset_index())

# summary stats
TOTAL_OBS = f"{len(df):,}"
TOTAL_SPP = str(df['COMMON NAME'].nunique())
TOTAL_REGIONS = str(df['COUNTY_SHORT'].nunique())

# form options
CAT_ORDER = ['All Categories', 'Seabirds', 'Waterfowl', 'Shorebirds',
             'Raptors', 'Gulls & Terns', 'Songbirds & Other']
COUNTY_OPTIONS = ['All Counties'] + sorted(df['COUNTY_SHORT'].unique().tolist())

# setup themes

DARK = {
    'bg_page':        '#080E1A',
    'bg_card':        'rgba(13,27,46,0.75)',
    'accent_teal':    '#00D4B4',
    'accent_orange':  '#FF6B35',
    'accent_gold':    '#FFD166',
    'accent_electric':'#4ECDC4',
    'accent_iceberg': '#7FDBDA',
    'text_primary':   '#C8D8E8',
    'text_heading':   '#E8F4F8',
    'text_muted':     '#5A7A8A',
    'text_light':     '#E8F4F8',
    'border':         'rgba(0,212,180,0.15)',
    'chart_bg':       'rgba(0,0,0,0)',
    'chart_grid':     'rgba(0,212,180,0.08)',
    'chart_font':     '#9BBCCC',
    'bar_scale':      ['#0D2E3D','#0A6E6A','#00D4B4','#4ECDC4'],
    'map_scale':      [[0,'#0A3040'],[0.3,'#00D4B4'],[0.65,'#FFD166'],[1.0,'#FF6B35']],
    'map_style':      'carto-darkmatter',
    'colorbar_bg':    'rgba(5,11,20,0.85)',
    'colorbar_border':'rgba(0,212,180,0.25)',
    'hover_bg':       'rgba(8,14,26,0.95)',
    'hover_border':   '#00D4B4',
}

LIGHT = {
    'bg_page':        '#F0F4F8',
    'bg_card':        'rgba(255,255,255,0.72)',
    'accent_teal':    '#2A9D8F',
    'accent_orange':  '#E76F51',
    'accent_gold':    '#D4A017',
    'accent_electric':'#2A9D8F',
    'accent_iceberg': '#A8DADC',
    'text_primary':   '#2D3748',
    'text_heading':   '#1A202C',
    'text_muted':     '#718096',
    'text_light':     '#FAFAF8',
    'border':         'rgba(42,157,143,0.2)',
    'chart_bg':       'rgba(0,0,0,0)',
    'chart_grid':     'rgba(42,157,143,0.12)',
    'chart_font':     '#4A5568',
    'bar_scale':      ['#A8DADC','#2A9D8F','#1B4332','#0B1D3A'],
    'map_scale':      [[0,'#A8DADC'],[0.3,'#2A9D8F'],[0.65,'#E76F51'],[1.0,'#C4391D']],
    'map_style':      'carto-positron',
    'colorbar_bg':    'rgba(255,255,255,0.9)',
    'colorbar_border':'rgba(42,157,143,0.3)',
    'hover_bg':       'rgba(11,29,58,0.95)',
    'hover_border':   '#2A9D8F',
}

def get_theme(theme_name):
    return DARK if theme_name == 'dark' else LIGHT

# Category colors for line chart (work on both themes)
CAT_COLORS = {
    'Seabirds':          '#00D4B4',
    'Waterfowl':         '#4ECDC4',
    'Shorebirds':        '#FF6B35',
    'Raptors':           '#FFD166',
    'Gulls & Terns':     '#7FDBDA',
    'Songbirds & Other': '#E8A0BF',
}
CAT_COLORS_LIGHT = {
    'Seabirds':          '#0A8E7A',
    'Waterfowl':         '#2A9D8F',
    'Shorebirds':        '#E76F51',
    'Raptors':           '#D4880F',
    'Gulls & Terns':     '#1B7A7A',
    'Songbirds & Other': '#7C3A8F',
}

FONT_HEADING = "'Playfair Display', Georgia, serif"
FONT_BODY = "'DM Sans', 'Inter', system-ui, sans-serif"

def chart_layout(T):
    return dict(
        paper_bgcolor=T['chart_bg'],
        plot_bgcolor=T['chart_bg'],
        font=dict(family=FONT_BODY, size=11, color=T['chart_font']),
        margin=dict(l=8, r=8, t=4, b=8),
        hoverlabel=dict(
            bgcolor=T['hover_bg'],
            bordercolor=T['hover_border'],
            font=dict(color='#FAFAF8', size=12, family=FONT_BODY),
            namelength=-1,
        ),
    )

# inline svg icons

PUFFIN_SVG = '''<svg viewBox="0 0 80 80" width="36" height="36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="32" rx="16" ry="18" fill="#FAFAF8"/>
  <ellipse cx="40" cy="30" rx="13" ry="15" fill="#0B1D3A"/>
  <circle cx="45" cy="25" r="3.5" fill="#FAFAF8"/>
  <circle cx="45" cy="25" r="1.8" fill="#0B1D3A"/>
  <path d="M50 30 L66 26 L62 33 L50 32Z" fill="#E76F51"/>
  <path d="M50 32 L62 33 L58 37 L50 34Z" fill="#CC5A3E"/>
  <path d="M30 48 L26 70 L32 70 L34 50Z" fill="#E76F51"/>
  <path d="M50 48 L48 70 L54 70 L52 50Z" fill="#E76F51"/>
  <ellipse cx="40" cy="50" rx="14" ry="12" fill="#0B1D3A"/>
  <ellipse cx="40" cy="48" rx="10" ry="9" fill="#FAFAF8"/>
  <path d="M26 42 L18 52 L24 48Z" fill="#0B1D3A" opacity="0.7"/>
  <path d="M54 42 L62 52 L56 48Z" fill="#0B1D3A" opacity="0.7"/>
</svg>'''

BIRD_WATERMARK_SVG = '''<svg viewBox="0 0 200 120" width="140" height="84" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 80 Q40 20 80 40 Q100 48 110 35 Q120 22 140 30 Q160 38 170 25
           L175 28 Q165 42 145 38 Q125 34 115 48 Q105 60 85 52 Q55 38 40 85Z"
        fill="#00D4B4" opacity="0.06"/>
  <path d="M170 25 L195 15 L185 30 Z" fill="#FF6B35" opacity="0.08"/>
  <circle cx="172" cy="24" r="2" fill="#FAFAF8" opacity="0.06"/>
</svg>'''

puffin_b64 = base64.b64encode(PUFFIN_SVG.encode()).decode()
watermark_b64 = base64.b64encode(BIRD_WATERMARK_SVG.encode()).decode()

# helpers

def stat_badge(badge_id, value, label, icon):
    return html.Div(className='stat-badge', children=[
        html.Span(icon, className='stat-icon'),
        html.Div([
            html.Div(value, id=badge_id, className='stat-value'),
            html.Div(label, className='stat-label'),
        ]),
    ])

# app layout

app = Dash(
    __name__,
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=DM+Sans:wght@300;400;500;600&display=swap'
    ]
)
app.title = "Where the Birds Are — NL Bird Dashboard"

# Inject CSS directly into the HTML template (no external assets/ folder needed)
app.index_string = '''<!DOCTYPE html>
<html><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}
<style>''' + EMBEDDED_CSS + '''</style>
</head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>'''

app.layout = html.Div(id='app-root', className='theme-dark', children=[

    # store selected theme
    dcc.Store(id='theme-store', data='dark'),

    # layout header
    html.Header(id='app-header', children=[
        html.Img(src=f'data:image/svg+xml;base64,{puffin_b64}',
                 style={'height': '36px', 'width': '36px'}),
        html.Div(id='header-title', children=[
            html.H1("Where the Birds Are"),
            html.Span("Newfoundland & Labrador  \u00b7  2025"),
        ]),
        html.Div(id='header-spacer'),
        html.Button("\u263E", id='theme-toggle', n_clicks=0,
                    title='Toggle dark/light theme'),
        html.Button("\u21BA Reset", id='reset-btn', n_clicks=0),
        html.Div(className='stat-badges-row', children=[
            stat_badge('stat-obs', TOTAL_OBS, "Observations", "\U0001F4CD"),
            stat_badge('stat-spp', TOTAL_SPP, "Species", "\U0001FABF"),
            stat_badge('stat-regions', TOTAL_REGIONS, "Regions", "\U0001F5FA"),
        ]),
    ]),

    # main content grid
    html.Main(id='app-body', children=[

        # map widget
        html.Div(id='map-panel', className='panel', children=[
            html.Div(className='panel-header', children=[
                html.Div([
                    html.H2("Observation Hotspots", className='panel-title'),
                    html.P("Bubble size = observations  \u00b7  Color = species richness",
                           className='panel-caption'),
                ]),
            ]),
            html.Div(className='map-controls-row', children=[
                html.Div(className='control-group', children=[
                    html.Span("Category", className='control-label'),
                    dcc.Dropdown(id='map-category', options=CAT_ORDER,
                                 value='All Categories', clearable=False,
                                 style={'width': '160px', 'fontSize': '12px'}),
                ]),
                html.Div(className='slider-wrap', children=[
                    html.Span("Month Range", className='control-label',
                              style={'marginBottom': '2px', 'display': 'block'}),
                    dcc.RangeSlider(id='map-month', min=1, max=12, step=1,
                                    value=[1, 12],
                                    marks={m: {'label': MONTH_NAMES[m],
                                               'style': {'fontSize': '9px'}}
                                           for m in range(1, 13)},
                                    tooltip={'placement': 'bottom'}),
                ]),
            ]),
            html.Div(className='graph-wrapper', children=[
                dcc.Loading(type='circle', color='#00D4B4', children=[
                    dcc.Graph(id='map-graph',
                              style={'height': '100%', 'width': '100%'},
                              config={'displayModeBar': False, 'responsive': True}),
                ]),
            ]),
            html.Img(src=f'data:image/svg+xml;base64,{watermark_b64}',
                     className='bird-watermark'),
        ]),

        # bar chart widget
        html.Div(id='bar-panel', className='panel', children=[
            html.Div(className='panel-header', children=[
                html.Div([
                    html.H2("Species Richness by County", className='panel-title'),
                    html.P("Unique species per region", className='panel-caption'),
                ]),
                html.Div(className='panel-controls', children=[
                    dcc.Dropdown(id='bar-category', options=CAT_ORDER,
                                 value='All Categories', clearable=False,
                                 style={'width': '155px', 'fontSize': '12px'}),
                ]),
            ]),
            html.Div(className='graph-wrapper', children=[
                dcc.Loading(type='circle', color='#00D4B4', children=[
                    dcc.Graph(id='bar-graph',
                              style={'height': '100%', 'width': '100%'},
                              config={'displayModeBar': False, 'responsive': True}),
                ]),
            ]),
        ]),

        # line chart widget
        html.Div(id='seasonal-panel', className='panel', children=[
            html.Div(className='panel-header', children=[
                html.Div([
                    html.H2("Seasonal Activity", className='panel-title'),
                    html.P("Observation trends by category & month",
                           className='panel-caption'),
                ]),
                html.Div(className='panel-controls', children=[
                    dcc.Dropdown(id='seasonal-county', options=COUNTY_OPTIONS,
                                 value='All Counties', clearable=False,
                                 style={'width': '170px', 'fontSize': '12px'}),
                ]),
            ]),
            html.Div(className='graph-wrapper', children=[
                dcc.Loading(type='circle', color='#00D4B4', children=[
                    dcc.Graph(id='seasonal-graph',
                              style={'height': '100%', 'width': '100%'},
                              config={'displayModeBar': False, 'responsive': True}),
                ]),
            ]),
        ]),
    ]),

    # layout footer
    html.Footer(id='app-footer', children=[
        html.Span("Data: eBird 2025  \u00b7  COMP-4304  \u00b7  Memorial University of Newfoundland"),
    ]),
])

# app logic callbacks

# theme toggle callback
clientside_callback(
    """
    function(n_clicks, current_theme) {
        if (n_clicks === 0) return window.dash_clientside.no_update;
        var new_theme = current_theme === 'dark' ? 'light' : 'dark';
        return new_theme;
    }
    """,
    Output('theme-store', 'data'),
    Input('theme-toggle', 'n_clicks'),
    State('theme-store', 'data'),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(theme) {
        var root = document.getElementById('app-root');
        root.className = 'theme-' + theme;
        return theme === 'dark' ? '\u263E' : '\u2600';
    }
    """,
    Output('theme-toggle', 'children'),
    Input('theme-store', 'data'),
)


# map update logic
@app.callback(Output('map-graph', 'figure'),
              Input('map-category', 'value'),
              Input('map-month', 'value'),
              Input('theme-store', 'data'))
def update_map(category, month_range, theme):
    T = get_theme(theme)
    data = loc_agg.copy()

    if category != 'All Categories':
        data = data[data['CATEGORY'] == category]

    data = data[(data['MONTH'] >= month_range[0]) & (data['MONTH'] <= month_range[1])]

    data = (data.groupby(['LOCALITY', 'LATITUDE', 'LONGITUDE', 'COUNTY_SHORT'])
                .agg(obs=('obs', 'sum'), spp=('spp', 'max'))
                .reset_index())

    if data.empty:
        raise PreventUpdate

    fig = px.scatter_mapbox(
        data, lat='LATITUDE', lon='LONGITUDE',
        color='spp', size='obs',
        color_continuous_scale=T['map_scale'],
        size_max=22, opacity=0.88,
        hover_name='LOCALITY',
        hover_data={'COUNTY_SHORT': True, 'spp': True, 'obs': True,
                    'LATITUDE': False, 'LONGITUDE': False},
        labels={'spp': 'Species', 'obs': 'Observations', 'COUNTY_SHORT': 'County'},
        mapbox_style=T['map_style'],
        zoom=4.5,
        center={'lat': 51, 'lon': -56},
    )
    CL = chart_layout(T)
    fig.update_layout(
        **{k: v for k, v in CL.items() if k != 'margin'},
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=dict(text='Species<br>Richness',
                       font=dict(size=9, color=T['text_muted'], family=FONT_BODY),
                       side='right'),
            tickfont=dict(size=9, color=T['text_muted'], family=FONT_BODY),
            len=0.55, thickness=12, x=1.01,
            bgcolor=T['colorbar_bg'],
            outlinecolor=T['colorbar_border'], outlinewidth=1,
            borderwidth=0, nticks=5,
        ),
    )
    fig.update_traces(
        hovertemplate=(
            '<b style="font-size:13px">%{hovertext}</b><br>'
            '<span style="color:#00D4B4">County:</span> %{customdata[0]}<br>'
            '<span style="color:#00D4B4">Species:</span> %{customdata[1]}<br>'
            '<span style="color:#00D4B4">Observations:</span> %{customdata[2]}<br>'
            '<extra></extra>'
        )
    )
    return fig


# bar chart logic
@app.callback(Output('bar-graph', 'figure'),
              Input('bar-category', 'value'),
              Input('theme-store', 'data'))
def update_bar(category, theme):
    T = get_theme(theme)
    if category != 'All Categories':
        data = cty_agg[cty_agg['CATEGORY'] == category].copy()
    else:
        data = (df.groupby('COUNTY_SHORT')
                  .agg(spp=('COMMON NAME', 'nunique'))
                  .reset_index())

    data = data.sort_values('spp', ascending=True)

    if data.empty:
        raise PreventUpdate

    fig = px.bar(data, x='spp', y='COUNTY_SHORT', orientation='h',
                 text='spp',
                 color='spp', color_continuous_scale=T['bar_scale'],
                 labels={'spp': 'Unique Species', 'COUNTY_SHORT': ''})

    fig.update_traces(
        textfont=dict(size=10, color=T['text_primary'], family=FONT_BODY),
        textposition='outside', cliponaxis=False,
        marker=dict(line_width=0, cornerradius=4),
        hovertemplate='<b>%{y}</b><br>%{x} unique species<extra></extra>',
    )
    CL = chart_layout(T)
    fig.update_layout(
        **{k: v for k, v in CL.items() if k != 'margin'},
        margin=dict(l=0, r=36, t=4, b=30),
        showlegend=False, coloraxis_showscale=False,
        clickmode='event+select',
        xaxis=dict(
            title=dict(text='Unique Species',
                       font=dict(size=10, color=T['text_muted'], family=FONT_BODY),
                       standoff=6),
            tickfont=dict(size=10, color=T['chart_font'], family=FONT_BODY),
            gridcolor=T['chart_grid'], gridwidth=1, griddash='dot',
            zeroline=False, showline=False,
        ),
        yaxis=dict(
            tickfont=dict(size=10, color=T['chart_font'], family=FONT_BODY),
            gridcolor='rgba(0,0,0,0)',
            showline=False, automargin=True,
        ),
        bargap=0.32,
        transition={'duration': 300, 'easing': 'cubic-in-out'},
    )

    # Subtle median reference line (below bars, annotation on x-axis)
    median_spp = int(data['spp'].median())
    fig.add_vline(
        x=median_spp,
        line_width=1, line_dash='dash',
        line_color=T['accent_gold'], opacity=0.3,
    )
    fig.add_annotation(
        x=median_spp, y=-0.08, yref='paper',
        text=f"median {median_spp}",
        showarrow=False,
        font=dict(size=8, color=T['accent_gold'], family=FONT_BODY),
        opacity=0.7,
    )
    return fig


# seasonal chart logic
@app.callback(Output('seasonal-graph', 'figure'),
              Output('seasonal-county', 'value'),
              Input('seasonal-county', 'value'),
              Input('bar-graph', 'clickData'),
              Input('theme-store', 'data'))
def update_seasonal(county, click_data, theme):
    T = get_theme(theme)
    colors = CAT_COLORS if theme == 'dark' else CAT_COLORS_LIGHT

    triggered = callback_context.triggered[0]['prop_id'] if callback_context.triggered else ''
    if 'bar-graph' in triggered and click_data and click_data.get('points'):
        county = click_data['points'][0].get('y', county)

    if county != 'All Counties':
        data = seasonal_agg[seasonal_agg['COUNTY_SHORT'] == county]
    else:
        data = seasonal_agg

    monthly = (data.groupby(['CATEGORY', 'MONTH'])['obs']
                   .sum().reset_index())

    cat_order = ['Seabirds', 'Waterfowl', 'Shorebirds',
                 'Raptors', 'Gulls & Terns', 'Songbirds & Other']
    month_labels = [MONTH_NAMES[m] for m in range(1, 13)]

    fig = go.Figure()

    for cat in cat_order:
        cat_data = monthly[monthly['CATEGORY'] == cat]
        y_vals = []
        for m in range(1, 13):
            row = cat_data[cat_data['MONTH'] == m]
            y_vals.append(int(row['obs'].iloc[0]) if len(row) > 0 else 0)

        fig.add_trace(go.Scatter(
            x=month_labels,
            y=y_vals,
            name=cat,
            mode='lines+markers',
            line=dict(
                color=colors.get(cat, '#718096'),
                width=2.5,
                shape='spline',
                smoothing=0.8,
            ),
            marker=dict(
                size=5,
                color=colors.get(cat, '#718096'),
                line=dict(width=1, color='rgba(255,255,255,0.4)'),
            ),
            hovertemplate='%{y:,.0f}<extra></extra>',
        ))

    CL = chart_layout(T)
    fig.update_layout(
        **{k: v for k, v in CL.items() if k != 'margin'},
        margin=dict(l=0, r=8, t=4, b=30),
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='left', x=0,
            font=dict(size=9, color=T['chart_font'], family=FONT_BODY),
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0,
            traceorder='normal',
        ),
        xaxis=dict(
            tickfont=dict(size=10, color=T['chart_font'], family=FONT_BODY),
            gridcolor=T['chart_grid'], gridwidth=1,
            showline=False, zeroline=False, fixedrange=True,
        ),
        yaxis=dict(
            tickfont=dict(size=9, color=T['text_muted'], family=FONT_BODY),
            gridcolor=T['chart_grid'], gridwidth=1,
            showline=False, zeroline=False, automargin=True,
            tickformat=',.0f',
            title=dict(text='Observations',
                       font=dict(size=9, color=T['text_muted'], family=FONT_BODY),
                       standoff=4),
            fixedrange=True,
        ),
        hovermode='x unified',
        transition={'duration': 300, 'easing': 'cubic-in-out'},
    )
    return fig, county


# ── Dynamic stat badges ───────────────────────────────────────
@app.callback(
    Output('stat-obs', 'children'),
    Output('stat-spp', 'children'),
    Output('stat-regions', 'children'),
    Input('map-category', 'value'),
    Input('map-month', 'value'))
def update_stats(category, month_range):
    data = loc_agg.copy()
    if category != 'All Categories':
        data = data[data['CATEGORY'] == category]
    data = data[(data['MONTH'] >= month_range[0]) & (data['MONTH'] <= month_range[1])]
    obs = f"{int(data['obs'].sum()):,}"
    spp = str(int(data['spp'].sum()))
    regions = str(data['COUNTY_SHORT'].nunique())
    return obs, spp, regions


# ── Reset all filters ────────────────────────────────────────
@app.callback(
    Output('map-category', 'value'),
    Output('map-month', 'value'),
    Output('bar-category', 'value'),
    Output('seasonal-county', 'value', allow_duplicate=True),
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True)
def reset_filters(n):
    return 'All Categories', [1, 12], 'All Categories', 'All Counties'


# ═══════════════════════════════════════════════════════════════
# Run
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print(f"\n  Where the Birds Are — NL Bird Dashboard")
    print(f"  Loaded {len(df):,} observations | {df['COMMON NAME'].nunique()} species | {df['COUNTY_SHORT'].nunique()} regions")
    print(f"  Starting server...\n")
    app.run(debug=False)
