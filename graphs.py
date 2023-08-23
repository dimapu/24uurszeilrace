from pathlib import Path

import matplotlib.pyplot as plt

import networkx as nx
import pandas as pd

plt.close("all")
raw_data_fn = Path(__file__).parent / "_data/raw.xlsx"
df_edges: pd.DataFrame = pd.read_excel(raw_data_fn, "example")

G = nx.DiGraph()

for i, r in df_edges.iterrows():
    G.add_edge(r["start"], r["end"], weight=i)

print("nodes", G.number_of_nodes())
print("edges", G.number_of_edges())

plt.figure()
nx.draw(G, with_labels=True, font_weight='bold')
