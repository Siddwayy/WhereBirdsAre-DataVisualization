# 🐦 Where the Birds Are

**A data portrait of birding across Newfoundland & Labrador · 2025 Field Season**

Built for the **[Johnson Geo Centre](https://www.geocentre.ca/)** in St. John's, NL, this project transforms citizen-science eBird records into a cohesive set of visual outputs: a print-ready infographic poster, standalone charts, and an interactive Plotly Dash dashboard.

---

## 🖼️ Visualizations

### Infographic Poster
<img width="4800" height="7200" alt="Where the Birds Are infographic poster" src="https://github.com/user-attachments/assets/4557d3e9-b45f-41fa-8c9a-cc32e72a7a5b" />

### Interactive Dashboard
<img width="1417" height="697" alt="Where the Birds Are interactive dashboard" src="https://github.com/user-attachments/assets/68fae6a0-a190-4a8b-a673-bee18672781d" />

---

## 📊 Project Overview

*Where the Birds Are* explores **where birders watch**, **which regions show the highest species diversity**, and **how species composition varies across Important Bird Areas (IBAs)** in Newfoundland and Labrador.

### Key Metrics

| Metric | Value |
|--------|-------|
| 🔭 **Observations** | 27,000+ |
| 🪶 **Unique species** | 280+ |
| 📍 **Birding localities** | 1,400+ |
| 🗺️ **Counties / regions** | 11 |
| 🦅 **Important Bird Areas** | 8 |

---

## 🎨 Deliverables

### 1. Infographic Poster
- Print-ready **36 × 24 in** landscape layout at **200 DPI**.
- Built programmatically with **Python** and **Matplotlib**.
- Combines the project’s core visualizations into a single narrative poster.

### 2. Interactive Dashboard
- Built with **Plotly Dash** and designed with a dark UI.
- Supports linked cross-filtering across the map and charts by **category**, **month range**, and **county**.
- Includes:
  - **Observation Hotspots:** Bubble map where marker size represents observations and color represents species richness.
  - **Species Richness by County:** Horizontal bar chart ranking all 11 counties with a median reference line.
  - **Seasonal Activity:** Multi-line chart showing bird activity trends by category.

### 3. Standalone Charts

| Chart | Description |
|-------|-------------|
| **Geographic Hotspots** | Scatter map of NL localities; marker size = observations, color = diversity. |
| **County Species Richness** | Horizontal bar chart ranking all 11 counties. |
| **IBA Species Composition** | Stacked bar chart of the top 8 IBAs organized by bird group. |

---

## 💡 Key Findings

- Around **65% of observations** come from the **Avalon Peninsula**, likely influenced by accessibility and birder density.
- All **11 counties** show notable variation in species richness, with the **Avalon** leading overall.
- The **8 IBAs** display distinct ecological profiles, from coastal seabird colonies to inland songbird habitats.
- **Songbirds** dominate most IBAs, while **seabirds** lead in major coastal areas.

---

## 🏗️ Project Structure

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

---

## 🚀 How to Run Locally

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
Place `birds.csv` in the `data/` directory.  
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

---

## 💻 Tech Stack

- **Data Processing:** Python, Pandas, NumPy, GeoPandas
- **Static Visualization:** Matplotlib, Pillow
- **Interactive Web App:** Plotly Dash
- **Data Source:** [eBird Basic Dataset](https://ebird.org/science/use-ebird-data), filtered to Newfoundland & Labrador
