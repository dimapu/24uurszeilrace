from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from coordinates import convert_coordinate, get_direction
from speed import get_speed

LON_FACTOR = 0.6088

plt.close("all")

# %% Read data
raw_data_fn = Path(__file__).parent / "_data/raw.xlsx"
df_bouys: pd.DataFrame = pd.read_excel(raw_data_fn, "buoys")
df_stretches: pd.DataFrame = pd.read_excel(raw_data_fn, "stretches")

# %% Normalize data
df_bouys["name"] = (
    df_bouys["Name"].str.replace(" ", "").str.replace("-", "").str.upper()
)
df_bouys["lat"] = df_bouys["Lat"].apply(convert_coordinate)
df_bouys["lon"] = df_bouys["Lon"].apply(convert_coordinate)
df_bouys.set_index("name", inplace=True)
df_bouys = df_bouys[["Zone", "lat", "lon"]]

df_stretches["start"] = df_stretches["Start"].str.replace("-", "").str.upper()
df_stretches["end"] = df_stretches["Eind"].str.replace("-", "").str.upper()
df_stretches["Afstand"] = (
    df_stretches["Afstand"].str.replace(",", ".").astype(float)
)
df_stretches = df_stretches[["Afstand", "Max Aantal", "type", "start", "end"]]


# %% Get edge coordinates and distances, start and end
df_stretches = pd.merge(
    df_stretches,
    df_bouys,
    left_on="start",
    right_on="name",
    how="left",
)
df_stretches = pd.merge(
    df_stretches,
    df_bouys,
    left_on="end",
    right_on="name",
    suffixes=["_start", "_end"],
    how="left",
)
df_stretches["dx"] = (df_stretches["lon_end"] - df_stretches["lon_start"]) * 60
df_stretches["dy"] = (df_stretches["lat_end"] - df_stretches["lat_start"]) * 60
df_stretches["dx_nm"] = df_stretches["dx"] * LON_FACTOR
df_stretches["dy_nm"] = df_stretches["dy"]
df_stretches["dist"] = np.sqrt(
    df_stretches["dx_nm"] ** 2 + df_stretches["dy"] ** 2
)
df_stretches["distance_diff"] = df_stretches["Afstand"] - df_stretches["dist"]
df_stretches["heading"] = get_direction(
    df_stretches["dx_nm"], df_stretches["dy_nm"]
)
df_stretches["reverse_heading"] = get_direction(
    -df_stretches["dx_nm"], -df_stretches["dy_nm"]
)


# Limit to Ijsselmeer
df = df_stretches.query("Zone_start == 'Ijsselmeer' | Zone_end == 'Ijsselmeer'")

# %% Plots
df_plot = df.dropna(axis="index")
n_total = len(df)
n_found = len(df_plot)

print(f"{n_total=}, {n_found=}, n_not_found={n_total-n_found}")

# Plot points and edges
ax = sns.scatterplot(
    data=df_bouys.query("Zone == 'Ijsselmeer'"),
    x="lon",
    y="lat",
    style="Zone",
    hue="Zone",
)
ax.set_aspect(1 / LON_FACTOR)

for i, r in df_plot.iterrows():
    sx, sy = r["lon_start"], r["lat_start"]
    ex, ey = r["lon_end"], r["lat_end"]
    ax.plot([sx, ex], [sy, ey])

# Plot difference between calculated and official distance
plt.figure()
ax = sns.scatterplot(
    data=df_plot,
    x=df_plot.index,
    y="distance_diff",
    style="Zone_start",
    hue="Zone_end",
)
