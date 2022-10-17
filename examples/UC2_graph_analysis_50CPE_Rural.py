#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_analysis import graph_analysis, get_distance_metrics

if __name__ == '__main__':

    # Get metrics for simulation 1

    g0 = graph_creation('../data/UC2_50CPE_Rural/links_0.csv', print_stats=False)
    print("----------------------------------------------------------------------")
    print("Rural, 50 CPEs, simulation 1")
    print("----------------------------------------------------------------------")
    _ = graph_analysis(g0, print_stats=True)
    med_dist = np.median(g0.es["weight"])
    print(f"Median link distance: {med_dist}")
    print("----------------------------------------------------------------------")
    print("\n")
