# CODECRAFT_DS_05 — Traffic Accident Pattern Analysis

**Goal:** Analyze traffic accident data to identify patterns related to road conditions, weather, and time of day. Visualize hotspots.  
**Sample dataset:** US Accidents (place the CSV as `US_Accidents.csv`)  
Example source: Kaggle "US Accidents (2016–2023)"

## Files
- `task05_us_accidents.py` — EDA + hotspot map (Folium).
- `requirements.txt`

## How to Use
1. Download the dataset CSV (e.g., `US_Accidents_March23.csv`) and rename it to `US_Accidents.csv` in this folder.
2. Create a virtual environment and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python task05_us_accidents.py
   ```
4. See summary charts in `./outputs/` and an interactive map `./outputs/accident_hotspots.html`.
