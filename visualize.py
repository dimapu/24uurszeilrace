from collections import Counter
from itertools import pairwise
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from utils.data import LON_FACTOR, get_data, parse_alex_output
from utils.graphs import create_graph
from utils.speed import get_speed, calculate_pointing_angle
from utils.validation import evaluate_correctness
from utils.data import calculate_distances

bouys, legs = get_data()

legs_inverted = pd.DataFrame()
legs_inverted["start"] = legs["end"]
legs_inverted["end"] = legs["start"]
legs_inverted["Afstand"] = legs["Afstand"]
legs_inverted = calculate_distances(bouys, legs_inverted)

legs_all = pd.concat([legs, legs_inverted])


route = """MED, Course to: N/A, Time at: 16:00, Distance: 0.00
SPORT-C, Course to: 39, Time at: 16:18, Distance: 1.55
KR-A, Course to: 61, Time at: 16:50, Distance: 4.70
LC11, Course to: 108, Time at: 18:09, Distance: 7.68
SPORT-D, Course to: 182, Time at: 19:05, Distance: 10.80
SB28, Course to: 59, Time at: 21:11, Distance: 19.06
EL-B, Course to: 153, Time at: 22:10, Distance: 22.65
EZ-C, Course to: 224, Time at: 23:05, Distance: 26.96
EL-A, Course to: 7, Time at: 23:31, Distance: 29.51
SB8, Course to: 322, Time at: 1:06, Distance: 34.82
EL-A, Course to: 142, Time at: 2:08, Distance: 40.12
SB8, Course to: 322, Time at: 3:02, Distance: 45.43
KR-A, Course to: 273, Time at: 4:10, Distance: 50.13
LC1, Course to: 58, Time at: 5:18, Distance: 53.57
VF-B, Course to: 5, Time at: 6:05, Distance: 56.55
SPORT-B, Course to: 316, Time at: 6:43, Distance: 60.31
SPORT-A, Course to: 290, Time at: 7:36, Distance: 63.21
SPORT-B, Course to: 110, Time at: 8:23, Distance: 66.11
VF-B, Course to: 136, Time at: 9:01, Distance: 69.87
SPORT-A, Course to: 305, Time at: 10:12, Distance: 76.37
LC1, Course to: 143, Time at: 12:13, Distance: 84.74
WV19, Course to: 277, Time at: 13:45, Distance: 90.50
TOCHT, Course to: 185, Time at: 15:43, Distance: 95.50
"""

df = parse_alex_output(route)






res = evaluate_correctness(df["end"])
print(res)

G, pos = create_graph(bouys, df)


plt.figure()
nx.draw_networkx_nodes(G, pos, node_color="green", node_size=100)
nx.draw_networkx_labels(G, pos)
plt.gca().set_aspect(1 / LON_FACTOR)


df_for_colors = df.set_index(["start", "end"])
edge_colors = [df_for_colors.loc[e]["cum_dist"].values[0] for e in G.edges]
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
cmap = plt.cm.YlGnBu

edges = nx.draw_networkx_edges(
    G,
    pos,
    style="--",
    node_size=100,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=3,
    edge_vmax=100,
    edge_vmin=0,
)
pc = mpl.collections.PatchCollection(edges, cmap=cmap)
pc.set_array(edge_colors)
ax = plt.gca()
plt.colorbar(pc, ax=ax)


df_r = df[["start", "end"]].dropna()
print(len(df_r))

# Add distances and directions

df_r = pd.merge(df_r, legs_all[["start", "end", "Afstand", "heading"]], left_on=["start", "end"], right_on=["start", "end"], how="left")
df_r["cum_dist"] = df_r["Afstand"].cumsum()
df_r["time"] = 0
df_r["ETA"] = 0


prev_ETA = 0
for i, r in df_r.iterrows():
    df_r.at[i, "pa"] = calculate_pointing_angle(r["heading"], 225)
    df_r.at[i, "speed"] = speed =  get_speed(r["heading"], 225)
    time = df_r.at[i, "time"] = r["Afstand"] / max(speed, 2)
    a = df_r.at[i, "ETA"] = prev_ETA + time
    prev_ETA = a
    print(a)
    
    


# df_r["pa"] = calculate_pointing_angle(df_r["heading"], 225)
# df_r["speed"] = get_speed(df_r["heading"], 225)




