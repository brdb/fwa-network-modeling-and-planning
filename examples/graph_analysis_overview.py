#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_analysis import graph_analysis, get_distance_metrics
from graph_preparation import graph_preparation

def print_uc_statistics(scen):

    degr_avg = []
    dist_med = []
    graph_radius = []
    popeccentricity = []
    pophopcount = []
    vertexcount = []

    for i in range(0,50):
        filename = "../data/" + scen + "/links_" + str(i) + ".csv"
        g = graph_creation(filename, print_stats=False)
        (_, ecc, radius, _, avg_path_length, _, avg_hop, _, deg) = graph_analysis(g, print_stats=False, weighted_stats=False, return_stats=True)
        g_prep = graph_preparation(g, 300, f=60e9, print_stats=False)
        vertexcount.append(g_prep.vcount())
        degr_avg.append(np.mean(deg))
        dist_med.append(np.median(g.es["weight"]))
        graph_radius.append(radius)
        popeccentricity.append(ecc[0])
        pophopcount.append(avg_hop[0])

    # Print average vertex degree, median link distance, graph radius
    print("----------------------------------------------------------------------")
    print(scen)
    print("----------------------------------------------------------------------")
    print(f"Average vertex degree:                          {np.mean(degr_avg)}")
    print(f"Average link distance:                          {np.mean(dist_med)}")
    print(f"Average graph radius:                           {np.mean(graph_radius)}")
    print(f"Average PoP eccentricity:                       {np.mean(popeccentricity)}")
    print(f"Average hop count on shortest path towards PoP: {np.mean(pophopcount)}")
    print(f"Average number of connected vertices:           {np.mean(vertexcount)}")
    print("----------------------------------------------------------------------")
    print("\n")

if __name__ == '__main__':

    print_uc_statistics("UC1_50CPE_UrbanVillage")
    print_uc_statistics("UC1_100CPE_UrbanVillage")
    print_uc_statistics("UC1_300CPE_UrbanVillage")
    print_uc_statistics("UC1_600CPE_UrbanVillage")

    print_uc_statistics("UC2_10CPE_Rural")
    print_uc_statistics("UC2_50CPE_Rural")

    print_uc_statistics("UC3_50CPE_UrbanCity")
    print_uc_statistics("UC3_100CPE_UrbanCity")
    print_uc_statistics("UC3_300CPE_UrbanCity")
    print_uc_statistics("UC3_600CPE_UrbanCity")    
