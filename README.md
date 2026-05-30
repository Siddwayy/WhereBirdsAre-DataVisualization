# Where the Birds Are

**A data portrait of birding across Newfoundland & Labrador · 2025 field season**

Built for the [Johnson Geo Centre](https://www.geocentre.ca/) (St. John's, NL). This project turns citizen-science eBird records into a print-ready infographic, three standalone charts, and an interactive Plotly Dash dashboard.

<img width="4800" height="7200" alt="infographic(36)" src="https://github.com/user-attachments/assets/49e693c9-ded1-41f3-bbaa-65f1c546dc2e" />

<img width="2550" height="1263" alt="Dashboard" src="https://github.com/user-attachments/assets/b7ae4fa4-312d-4349-a640-c3999e79541e" />

---

## Overview

Where the Birds Are explores **where birders watch**, **which regions have the highest species diversity**, and **how species composition varies across Important Bird Areas (IBAs)** in Newfoundland and Labrador.

| Metric | Value |
|--------|-------|
| Observations | 27,000+ |
| Unique species | 280+ |
| Birding localities | 1,400+ |
| Counties / regions | 11 |
| Important Bird Areas | 8 |

---

## Deliverables

### 1. Infographic poster
- **36×24 in** landscape, **200 DPI**, print-ready
- Built with **Python** and **Matplotlib**
- Combines all three core visualizations into one narrative layout

### 2. Interactive dashboard
- **Plotly Dash** web app with dark UI
- Linked filters across map and charts (category, month range, county)
- **Panels:**
  - **Observation Hotspots** — bubble map (size = observations, color = species richness)
  - **Species Richness by County** — horizontal bar chart with median reference
  - **Seasonal Activity** — multi-line trends by bird group

### 3. Standalone charts

| Chart | Description |
|-------|-------------|
| **Geographic Hotspots** | Scatter map of NL localities; marker size = observations, color = diversity |
| **County Species Richness** | Horizontal bar chart ranking all 11 counties |
| **IBA Species Composition** | Stacked bars for top 8 IBAs by bird group |

---

## Key findings

- **~65%** of observations come from the **Avalon Peninsula** (access + birder density).
- **11 counties** show significant variation in species richness; **Avalon leads**.
- **8 IBAs** have distinct ecological profiles (coastal vs inland).
- **Songbirds** dominate most IBAs; **seabirds** lead in key coastal zones.

---

## Tech stack

- **Python** · **Matplotlib** · **Pandas** · **NumPy** · **GeoPandas** · **PIL**
- **Plotly Dash** · **Jupyter Notebook**
- **Data:** [eBird Basic Dataset](https://ebird.org/science/use-ebird-data) (2025), filtered to Newfoundland & Labrador

---
