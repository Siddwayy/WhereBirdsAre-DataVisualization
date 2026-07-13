<div align="center">

# 🐦 Where the Birds Are

A data portrait of birding across Newfoundland & Labrador · 2025 Field Season

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Dash-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=flat-square)
![GeoPandas](https://img.shields.io/badge/GeoPandas-Spatial_Data-139C5A?style=flat-square)
![eBird](https://img.shields.io/badge/Data-eBird-F2A900?style=flat-square)

Built for the **[Johnson Geo Centre](https://www.geocentre.ca/)** in St. John's, NL.

</div>

---

## Overview

**Where the Birds Are** transforms citizen-science eBird records into a cohesive set of visual outputs: a print-ready infographic poster, standalone charts, and an interactive Plotly Dash dashboard.

The project explores **where birders watch**, **which regions show the highest species diversity**, and **how species composition varies across Important Bird Areas (IBAs)** in Newfoundland and Labrador.

## Visualizations

### Infographic Poster
<p align="center">
  <img width="900" alt="Where the Birds Are infographic poster" src="https://github.com/user-attachments/assets/992d2db3-ec29-47da-9aed-96a3fe5c541f" />
</p>

### Interactive Dashboard
<p align="center">
  <img width="1100" alt="Where the Birds Are dashboard" src="https://github.com/user-attachments/assets/65d9227f-3fe1-4f2d-a1ab-0447392552be" />
</p>

## Key Metrics

| Metric | Value |
|---|---|
| 🔭 **Observations** | 27,000+ |
| 🪶 **Unique species** | 280+ |
| 📍 **Birding localities** | 1,400+ |
| 🗺️ **Counties / regions** | 11 |
| 🦅 **Important Bird Areas** | 8 |

## Deliverables

### 1. Infographic Poster
- Print-ready **36 × 24 in** landscape layout at **200 DPI**
- Built programmatically with **Python** and **Matplotlib**
- Combines the project’s main visual findings into a single narrative poster

### 2. Interactive Dashboard
- Built with **Plotly Dash** using a dark interface
- Supports cross-filtering by **category**, **month range**, and **county**
- Includes:
  - **Observation Hotspots** — bubble map where size represents observations and color represents species richness
  - **Species Richness by County** — horizontal bar chart ranking all 11 counties with a median reference line
  - **Seasonal Activity** — multi-line chart showing bird activity trends by category

### 3. Standalone Charts

| Chart | Description |
|---|---|
| **Geographic Hotspots** | Scatter map of NL localities; marker size = observations, color = diversity |
| **County Species Richness** | Horizontal bar chart ranking all 11 counties |
| **IBA Species Composition** | Stacked bar chart of the top 8 IBAs organized by bird group |

## Key Findings

- Around **65% of observations** come from the **Avalon Peninsula**, likely influenced by accessibility and birder density
- All **11 counties** show variation in species richness, with the **Avalon** leading overall
- The **8 IBAs** show distinct ecological profiles, from coastal seabird colonies to inland songbird habitats
- **Songbirds** dominate most IBAs, while **seabirds** lead in major coastal areas

## Why This Project Matters

- Turns raw citizen-science data into accessible public-facing visuals
- Combines **data analysis**, **geospatial storytelling**, **infographic design**, and **dashboard development**
- Supports science communication for a local institution in Newfoundland and Labrador
- Demonstrates the full workflow from raw dataset to print and interactive deliverables

## Project Structure

```text
.
├── assets/
│   └── images/              # Generated visualizations and charts
├── data/                    # Add birds.csv here to run locally
├── src/
│   ├── dashboard.py         # Plotly Dash interactive web app
│   ├── infographic.py       # Main script for the 36x24" poster
│   ├── viz1_map.py          # Standalone geographic hotspot map
│   ├── viz2_bar.py          # Standalone county species richness chart
│   └── viz3_iba.py          # Standalone IBA species composition chart
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/WhereBirdsAre-DataVisualization.git
cd WhereBirdsAre-DataVisualization
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib plotly dash geopandas Pillow
```

### 3. Add the data

Place `birds.csv` inside the `data/` directory.

This should be a filtered **eBird Basic Dataset** for Newfoundland & Labrador.

### 4. Run the visualizations

```bash
# Generate standalone charts
python src/viz1_map.py
python src/viz2_bar.py
python src/viz3_iba.py

# Generate full infographic poster
python src/infographic.py

# Launch the interactive dashboard
python src/dashboard.py
```

## Tech Stack

| Area | Tools |
|---|---|
| **Data Processing** | Python, Pandas, NumPy, GeoPandas |
| **Static Visualization** | Matplotlib, Pillow |
| **Interactive Dashboard** | Plotly Dash |
| **Data Source** | [eBird Basic Dataset](https://ebird.org/science/use-ebird-data) |

## Future Improvements

- Add more seasonal filtering and migration-focused views
- Include species-level drilldowns in the dashboard
- Publish the dashboard online for public access
- Add automated data cleaning and preprocessing scripts
- Expand infographic variants for education and outreach use

## Acknowledgment

Created for the **[Johnson Geo Centre](https://www.geocentre.ca/)** in St. John's, Newfoundland and Labrador.
