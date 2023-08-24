from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from utils.data import (LON_FACTOR, calculate_distances, filter_location,
                  normalize_data, read_data)
from utils.speed import get_speed

bouys, legs = read_data()
bouys, legs = normalize_data(bouys, legs)
legs = calculate_distances(bouys, legs)
bouys, legs = filter_location(bouys, legs)

legs_inverted = pd.DataFrame()
legs_inverted["start"] = legs["end"]
legs_inverted["end"] = legs["start"]
legs_inverted["Afstand"] = legs["Afstand"]
legs_inverted = calculate_distances(bouys, legs_inverted)

legs_all = pd.concat([legs, legs_inverted])

paths: pd.DataFrame = pd.read_hdf(r"C:\Users\dimap\ten_legs.h5", key="ten")


paths = paths.reset_index().rename(  # .loc[0:10]
    {"index": "path", "start": "0", "end": "100"}, axis="columns"
)


r = (
    paths.melt(id_vars="path", var_name="bouy_id", value_name="bouy_name")
    .astype({"bouy_id": "int16"})
    .sort_values(["path", "bouy_id"])
)

gr = r.groupby("path")

r["end"] = gr["bouy_name"].shift(-1)


r1 = pd.merge(
    r,
    legs_all,
    left_on=["bouy_name", "end"],
    right_on=["start", "end"],
    how="left",
).sort_values(["path", "bouy_id"])

dist = r1.groupby("path")["Afstand"].sum()
