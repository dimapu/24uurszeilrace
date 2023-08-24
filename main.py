from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from utils.data import LON_FACTOR, get_data
from utils.graphs import create_graph
from utils.speed import get_speed

bouys, legs = get_data()


WIND = 90

legs["speed"] = get_speed(legs.heading.values, WIND)
legs["reverse_speed"] = get_speed(legs.reverse_heading.values, WIND)

legs.info()

# a = legs["lat_start"] < legs["lat_end"]

# b = legs["lon_start"] < legs["lon_end"]


G, pos = create_graph(bouys, legs)

plt.figure()
nx.draw_networkx_nodes(G, pos, node_color="green", node_size=100)
nx.draw_networkx_labels(G, pos)
plt.gca().set_aspect(1 / LON_FACTOR)

edge_colors = legs["speed"].values
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
cmap = plt.cm.YlGnBu

edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=100,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=2,
)


pc = mpl.collections.PatchCollection(edges, cmap=cmap)
ax = plt.gca()
plt.colorbar(pc, ax=ax)


start = pd.DataFrame(
    # {"end": ["ENKN", "HIND", "LELYN", "MED", "OEVE", "STAV", "LEMMER"]}
    {"end": ["MED"]}
)
legs = legs[["start", "end"]]

# Reverse paths
legs_inverted = pd.DataFrame()
legs_inverted["start"] = legs["end"]
legs_inverted["end"] = legs["start"]
legs_all = pd.concat([legs, legs_inverted])


from lib.graphs import make_paths

res = make_paths(start, legs_all, 5)
