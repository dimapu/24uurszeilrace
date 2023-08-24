import datetime as dd
from collections import Counter
from itertools import pairwise
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Read graph
# plt.close("all")
# raw_data_fn = Path(__file__).parent / "_data/raw.xlsx"
# df_edges: pd.DataFrame = pd.read_excel(raw_data_fn, "example")


# # Reverse paths
# df_inverted = pd.DataFrame()
# df_inverted["start"] = df_edges["end"]
# df_inverted["end"] = df_edges["start"]
# df_all = pd.concat([df_edges, df_inverted])


# Create and draw graph
# G = nx.DiGraph()
# for i, r in df_edges.iterrows():
#     G.add_edge(r["start"], r["end"], weight=i)
# print("nodes", G.number_of_nodes())
# print("edges", G.number_of_edges())

# plt.figure()
# nx.draw(G, with_labels=True, font_weight="bold")


# Calculate paths



def add_leg(start, legs, n=1):
    """Add all possible legs to a given list of legs."""
    
    START_POINT = "start"
    END_POINT = "end"
    MAX_LEG_REP = 2

    _SFX = "_last"

    # Check the data
    assert END_POINT in start.columns, f"start must contain {END_POINT} column with the last point of the route" 
    assert START_POINT in legs.columns, f"legs must contain {START_POINT} column with the first point of the leg" 
    assert END_POINT in legs.columns, f"legs must contain {END_POINT} column with the last point of the leg" 

    if START_POINT not in start.columns:
        start.insert(loc=0, column=START_POINT, value=start[END_POINT])
    # print(start)

    # Add leg by join, remove and rename columns
    df = (
        pd.merge(
            start,
            legs,
            left_on=END_POINT,
            right_on=START_POINT,
            suffixes=("", _SFX),
        )
        .drop(START_POINT + _SFX, axis="columns")
        .rename(
            {END_POINT: f"{n}", END_POINT + _SFX: END_POINT}, axis="columns"
        )
    )

    # Check and remove repeated legs in each path
    idx_to_delete = []
    for i, r in df.iterrows():
        n = Counter("{}{}".format(*sorted([s, e])) for s, e in pairwise(r))

        if n.most_common(1)[0][1] > MAX_LEG_REP:
            idx_to_delete.append(i)

    df.drop(idx_to_delete, inplace=True)
    print(len(idx_to_delete))

    return df


def make_paths(start, legs, n_legs):
    """
    start contains list of starting points in the "end" column.
    legs contains pairs of viable edges in the "start", "end" columns.
    """
    n_paths = [n := len(start)]
    print(f"No. starting points: {n}")

    df = start
    t_start = dd.datetime.now()

    for i in range(n_legs):
        df = add_leg(df, legs, i)
        n_paths += [n := len(df)]
        print(f"Added leg {i+1}, total {n} paths.")
        print("Elapsed time: {}".format(dd.datetime.now() - t_start))

    df.drop("0", axis="columns", inplace=True)

    return df


def create_graph(bouys, legs):
    G = nx.DiGraph()
    
    for i, r in bouys.iterrows():
        G.add_node(r["name"])
    
    for i, r in legs.iterrows():
        if r["start"] is None or r["end"] is None: 
            continue
        G.add_edge(r["start"], r["end"])
        print("added", r["start"], r["end"])
    
    print("n nodes", G.number_of_nodes())
    print("n edges", G.number_of_edges())
    print("edges", G.edges)
       
    # nx.draw(G, with_labels=True, font_weight='bold')
   
    pos = {r["name"]: [r["lon"], r["lat"]] for i, r in bouys.iterrows()}
    return G, pos


def plot_n_paths(n_paths):
    # n = [1, 5, 34, 209, 1421, 9078, 59260, 378508, 2426287, 15393429, 97451347]
    plt.figure()
    plt.semilogy(n_paths, ".-")


def main():
    df_start = pd.DataFrame({"end": ["A", "D"]})
    res = make_paths(df_start, df_all, 12)
    return res


if __name__ == "__main__":
    res = main()


# plt.figure()
# plt.plot(n_paths)
