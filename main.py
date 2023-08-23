from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx

from data import LON_FACTOR

from data import read_data, normalize_data, calculate_distances, filter_location
from speed import get_speed

bouys, legs = read_data()
bouys, legs = normalize_data(bouys, legs)
legs = calculate_distances(bouys, legs)
bouys, legs  = filter_location(bouys, legs)
    

WIND = 90

legs["speed"] = get_speed(legs.heading.values, WIND)
legs["reverse_speed"] = get_speed(legs.reverse_heading.values, WIND)

legs.info()

# a = legs["lat_start"] < legs["lat_end"]

# b = legs["lon_start"] < legs["lon_end"]


G = nx.DiGraph()

for i, r in legs.iterrows():
    G.add_edge(r["start"], r["end"])

print("nodes", G.number_of_nodes())
print("edges", G.number_of_edges())

plt.figure()

# nx.draw(G, with_labels=True, font_weight='bold')

pos = {i: [r["lon"], r["lat"]] for i, r in bouys.iterrows()}

nx.draw_networkx_nodes(G, pos, node_color="green", node_size=100)
nx.draw_networkx_labels(G, pos)
plt.gca().set_aspect(1 / LON_FACTOR)

edge_colors = legs["speed"].values
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
cmap = plt.cm.Reds

edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=100,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=1,
)


pc = mpl.collections.PatchCollection(edges, cmap=cmap)
ax = plt.gca()
plt.colorbar(pc, ax=ax)