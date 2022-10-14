#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_preparation import graph_preparation

if __name__ == '__main__':

    t = 300 # CPE requirement in Mbps

    g0 = graph_creation('../data/UC1_100CPE_UrbanVillage/links_0.csv', print_stats=False)
    print("----------------------------------------------------------------------")
    print("Urban village, 100 CPEs, simulation 1")
    print("----------------------------------------------------------------------")
    g0_sunny = graph_preparation(g0, t, f=60e9, sa=0, print_stats=False)
    print("Total network capacity sunny day @ 60 GHz: " + str(sum(g0_sunny.es['tp']) / 1000) + "Gbps")
    g0_rainy = graph_preparation(g0, t, f=60e9, sa=10, print_stats=False)
    print("Total network capacity rainy day @ 60 GHz: " + str(sum(g0_rainy.es['tp']) / 1000) + "Gbps")
    g0_sunny = graph_preparation(g0, t, f=28e9, sa=0, print_stats=False)
    print("Total network capacity sunny day @ 28 GHz: " + str(sum(g0_sunny.es['tp']) / 1000) + "Gbps")
    g0_rainy = graph_preparation(g0, t, f=28e9, sa=10, print_stats=False)
    print("Total network capacity sunny day @ 28 GHz: " + str(sum(g0_sunny.es['tp']) / 1000) + "Gbps")
    print("----------------------------------------------------------------------")
    print("\n")

    # Get average simulation metrics of 50 simulations

    total_capacity_28GHz_sunny = []
    total_capacity_28GHz_rainy = []
    total_capacity_60GHz_sunny = []
    total_capacity_60GHz_rainy = []

    for i in range(0,50):

        filename = "../data/UC1_100CPE_UrbanVillage/links_" + str(i) + ".csv"
        g = graph_creation(filename, print_stats=False)
        g_sunny = graph_preparation(g, t, f=28e9, sa=0, print_stats=False)
        total_capacity_28GHz_sunny.append(sum(g_sunny.es['tp']) / 1000)
        g_rainy = graph_preparation(g, t, f=28e9, sa=10, print_stats=False)
        total_capacity_28GHz_rainy.append(sum(g_rainy.es['tp']) / 1000)
        g_sunny = graph_preparation(g, t, f=60e9, sa=0, print_stats=False)
        total_capacity_60GHz_sunny.append(sum(g_sunny.es['tp']) / 1000)
        g_rainy = graph_preparation(g, t, f=60e9, sa=10, print_stats=False)
        total_capacity_60GHz_rainy.append(sum(g_rainy.es['tp']) / 1000)
     
    # Print average total network capacity
    print("----------------------------------------------------------------------")
    print("Urban village, 100 CPEs, averaged")
    print("----------------------------------------------------------------------")
    print(f"Average total network capacity sunny day @ 28 GHz: {np.mean(total_capacity_28GHz_sunny)}")
    print(f"Average total network capacity rainy day @ 28 GHz: {np.mean(total_capacity_28GHz_rainy)}")
    print(f"Average total network capacity sunny day @ 60 GHz: {np.mean(total_capacity_60GHz_sunny)}")
    print(f"Average total network capacity rainy day @ 60 GHz: {np.mean(total_capacity_60GHz_rainy)}")
    print("----------------------------------------------------------------------")
   