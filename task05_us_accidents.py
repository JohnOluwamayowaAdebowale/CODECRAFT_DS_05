import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_PATH = "US_Accidents.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    # Basic time features
    for col in ["Start_Time","End_Time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "Start_Time" in df.columns:
        df["Hour"] = df["Start_Time"].dt.hour
        df["Weekday"] = df["Start_Time"].dt.day_name()
        df["Month"] = df["Start_Time"].dt.month

    # Core columns (robust to schema variants)
    severity_col = "Severity" if "Severity" in df.columns else None
    weather_col = None
    for c in df.columns:
        if c.lower() in {"weather_condition","weather"}:
            weather_col = c
            break
    road_col = None
    for c in df.columns:
        if c.lower() in {"amenity","bump","crossing","give_way","junction","no_exit","railway","roundabout","station","stop","traffic_calming","traffic_signal","turning_loop"}:
            road_col = c  # just mark any road infra flag
            break

    # Plots
    if severity_col:
        plt.figure()
        df[severity_col].value_counts().sort_index().plot(kind="bar")
        plt.title("Severity Distribution")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "severity_distribution.png"))
        plt.close()

    if "Hour" in df.columns:
        plt.figure()
        df["Hour"].dropna().astype(int).plot(kind="hist", bins=24)
        plt.title("Accidents by Hour of Day")
        plt.xlabel("Hour")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "accidents_by_hour.png"))
        plt.close()

    if weather_col:
        top_weather = df[weather_col].value_counts().head(15)
        plt.figure()
        top_weather.plot(kind="bar")
        plt.title("Top Weather Conditions (Accidents)")
        plt.xlabel("Weather Condition")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "top_weather_conditions.png"))
        plt.close()

    # Hotspots map (sample 20k points for performance)
    lat_col, lon_col = None, None
    for cand in ["Start_Lat","Latitude","lat","Lat"]:
        if cand in df.columns:
            lat_col = cand; break
    for cand in ["Start_Lng","Longitude","lon","Lng","Long"]:
        if cand in df.columns:
            lon_col = cand; break

    if lat_col and lon_col:
        df_map = df[[lat_col, lon_col]].dropna().sample(min(20000, len(df)), random_state=42)
        center = [df_map[lat_col].median(), df_map[lon_col].median()]
        m = folium.Map(location=center, zoom_start=5)
        # HeatMap without external plugin: simple marker clusters for performance-friendly alternative
        for _, row in df_map.iterrows():
            folium.CircleMarker(location=[row[lat_col], row[lon_col]], radius=1).add_to(m)
        m.save(os.path.join(OUTPUT_DIR, "accident_hotspots.html"))

    # Pairwise: Hour vs Severity (if available)
    if severity_col and "Hour" in df.columns:
        grp = df.groupby(["Hour", severity_col]).size().unstack(fill_value=0)
        grp.to_csv(os.path.join(OUTPUT_DIR, "hour_by_severity.csv"))
        plt.figure()
        grp.plot(kind="line")
        plt.title("Accident Counts by Hour and Severity")
        plt.xlabel("Hour")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "hour_by_severity.png"))
        plt.close()

    print("Analysis complete. See outputs/.")

if __name__ == "__main__":
    main()
