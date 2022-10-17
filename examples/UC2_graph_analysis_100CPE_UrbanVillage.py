#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_analysis import graph_analysis, get_distance_metrics

if __name__ == '__main__':

    # Get metrics for simulation 1

    g0 = graph_creation('../data/UC1_100CPE_UrbanVillage/links_0.csv', print_stats=False)
    print("----------------------------------------------------------------------")
    print("Urban village, 100 CPEs, simulation 1")
    print("----------------------------------------------------------------------")
    _ = graph_analysis(g0, print_stats=True)
    print("----------------------------------------------------------------------")
    print("\n")

    # Get average simulation metrics of 50 simulations

    degr_avg = []
    dist_med = []
    graph_radius = []
    popeccentricity = []
    pophopcount = []
    for i in range(0,50):
        filename = "../data/UC1_100CPE_UrbanVillage/links_" + str(i) + ".csv"
        g = graph_creation(filename, print_stats=False)
        (_, ecc, radius, _, avg_path_length, _, avg_hop, _, deg) = graph_analysis(g, print_stats=False, weighted_stats=False, return_stats=True)
        degr_avg.append(np.mean(deg))
        dist_med.append(np.median(g.es["weight"]))
        graph_radius.append(radius)
        popeccentricity.append(ecc[0])
        pophopcount.append(avg_hop[0])

    # Print average vertex degree, median link distance, graph radius
    print("----------------------------------------------------------------------")
    print("Urban village, 100 CPEs, averaged")
    print("----------------------------------------------------------------------")
    print(f"Average vertex degree:                          {np.mean(degr_avg)}")
    print(f"Average link distance:                          {np.mean(dist_med)}")
    print(f"Average graph radius:                           {np.mean(graph_radius)}")
    print(f"Average PoP eccentricity:                       {np.mean(popeccentricity)}")
    print(f"Average hop count on shortest path towards PoP: {np.mean(pophopcount)}")
    print("----------------------------------------------------------------------")
