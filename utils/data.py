from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from utils.coordinates import convert_coordinate, get_direction

LON_FACTOR = 0.6088


def read_data():
    """Read bouys and legs data from the file."""
    raw_data_fn = Path(__file__).parent.parent / "_data/raw.xlsx"
    bouys: pd.DataFrame = pd.read_excel(raw_data_fn, "buoys")
    stretches: pd.DataFrame = pd.read_excel(raw_data_fn, "stretches")
    return bouys, stretches


def normalize_data(bouys, stretches):
    """Normalize data."""
    bouys["name"] = (
        bouys["Name"].str.replace(" ", "").str.replace("-", "").str.upper()
    )
    bouys["lat"] = bouys["Lat"].apply(convert_coordinate)
    bouys["lon"] = bouys["Lon"].apply(convert_coordinate)
    # bouys.set_index("name", inplace=True)
    
    bouys["ID"]= bouys.index
    bouys = bouys[["ID", "name", "Zone", "lon", "lat"]]

    stretches["start"] = stretches["Start"].str.replace("-", "").str.upper()
    stretches["end"] = stretches["Eind"].str.replace("-", "").str.upper()
    stretches = stretches[["Afstand", "Max Aantal", "type", "start", "end"]]
    return bouys, stretches


def calculate_distances(bouys, stretches):
    """Get edge coordinates and distances, start and end.
    """
    stretches = pd.merge(
        stretches,
        bouys,
        left_on="start",
        right_on="name",
        how="left",
    )
    stretches = pd.merge(
        stretches,
        bouys,
        left_on="end",
        right_on="name",
        suffixes=["_start", "_end"],
        how="left",
    )
    stretches["dx"] = (stretches["lon_end"] - stretches["lon_start"]) * 60
    stretches["dy"] = (stretches["lat_end"] - stretches["lat_start"]) * 60
    stretches["dx_nm"] = stretches["dx"] * LON_FACTOR
    stretches["dy_nm"] = stretches["dy"]
    stretches["dist"] = np.sqrt(stretches["dx_nm"] ** 2 + stretches["dy"] ** 2)
    stretches["distance_diff"] = stretches["Afstand"] - stretches["dist"]
    stretches["heading"] = get_direction(stretches["dx_nm"], stretches["dy_nm"])
    stretches["reverse_heading"] = get_direction(
        -stretches["dx_nm"], -stretches["dy_nm"]
    )
    return stretches


def filter_location(bouys, stretches, location="Ijsselmeer"):
    """Limit data to a location."""
    bs = bouys.query(f"Zone == '{location}'")
    legs = stretches.query(
        f"Zone_start == '{location}' & Zone_end == '{location}'"
    )

    return bs, legs


def parse_alex_output(route: str):

    path_legs = route.splitlines()
    data = [leg.split() for leg in path_legs ]
    df = pd.DataFrame(data).drop([1, 2, 4, 5, 7], axis='columns').rename({0:"end", 3: "coarse", 6: "arrival", 8:"cum_dist"}, axis='columns')
    df["end"] = df["end"].str.replace(",", "").str.replace("-", "")
    df["start"] = df["end"].shift(1)
    df["cum_dist"] = df["cum_dist"].astype(float)

    return df


def plot_all_bouys(bouys, stretches):
    plt.close()
    # %% Plots
    df_plot = stretches.dropna(axis="index")
    n_total = len(stretches)
    n_found = len(df_plot)

    print(f"{n_total=}, {n_found=}, n_not_found={n_total-n_found}")

    # Plot points and edges
    ax = sns.scatterplot(
        data=bouys.query("Zone == 'Ijsselmeer'"),
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
        style="type",
        hue="Zone_end",
    )
    
    
def get_data():
    bouys, legs = read_data()
    bouys, legs = normalize_data(bouys, legs)
    legs = calculate_distances(bouys, legs)
    bouys, legs = filter_location(bouys, legs)    
    return bouys, legs


def main():
    data = read_data()
    bouys, legs = normalize_data(*data)
    legs = calculate_distances(bouys, legs)
    bouys, legs = filter_location(bouys, legs)

    plot_all_bouys(bouys, legs)


if __name__ == "__main__":
    main()
