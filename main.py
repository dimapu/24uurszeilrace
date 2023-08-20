from pathlib import Path

import pandas as pd
import seaborn as sns

# Read data
raw_data_fn = Path(__file__).parent / "_data/raw.xlsx"
df_bouys: pd.DataFrame = pd.read_excel(raw_data_fn, "buoys")
df_stretches = pd.read_excel(raw_data_fn, "stretches")


def convert_coordinate(c: str) -> float:
    """Convert coordinate string to float.

    Input format: "52°30,0000' N"
    """
    new = (
        c.replace("°", " ")
        .replace("'", " ")
        .replace('"', " ")
        .replace(",", ".")
    )
    deg, minutes, direction = new.split()
    return int(deg) + float(minutes) / 60.0


# Normalize data
df_bouys["name"] = (
    df_bouys["Name"].str.replace(" ", "").str.replace("-", "").str.upper()
)
df_bouys["lat"] = df_bouys["Lat"].apply(convert_coordinate)
df_bouys["lon"] = df_bouys["Lon"].apply(convert_coordinate)
df_bouys.set_index("name", inplace=True)
df_bouys = df_bouys[["Zone", "lat", "lon"]]

df_stretches["start"] = df_stretches["Start"].str.replace("-", "").str.upper()
df_stretches["end"] = df_stretches["Eind"].str.replace("-", "").str.upper()
df_stretches = df_stretches[["Afstand", "Max Aantal", "type", "start", "end"]]


# Plot points
ax = sns.scatterplot(data=df_bouys, x="lon", y="lat", style="Zone", hue="Zone")
ax.set_aspect(1 / 0.6)

# Plot edges
n_found, n_not_found = 0, 0
for i, edge in df_stretches.iterrows():
    start = edge["start"]
    end = edge["end"]
    if start not in df_bouys.index:
        print(f"missing start {start}")
        n_not_found += 1
        continue

    if end not in df_bouys.index:
        print(f"missing end {end}")
        n_not_found += 1
        continue

    n_found += 1

    sx, sy = df_bouys.loc[start]["lon"], df_bouys.loc[start]["lat"]
    ex, ey = df_bouys.loc[end]["lon"], df_bouys.loc[end]["lat"]

    ax.plot([sx, ex], [sy, ey])

print(f"{n_found=}, {n_not_found=}")
