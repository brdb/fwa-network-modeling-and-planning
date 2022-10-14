#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_preparation import graph_preparation

def print_capacity_info(scen):

    t = 300 # CPE requirement in Mbps

    total_capacity_60GHz_sunny = []
    total_capacity_60GHz_rain1 = []
    total_capacity_60GHz_rain2 = []
    total_capacity_60GHz_veg = []

    total_capacity_140GHz_sunny = []
    total_capacity_140GHz_rain1 = []
    total_capacity_140GHz_rain2 = []
    total_capacity_140GHz_veg = []

    total_throughput_60GHz_sunny = []
    total_throughput_60GHz_rain1 = []
    total_throughput_60GHz_rain2 = []
    total_throughput_60GHz_veg = []

    for i in range(0,50):

        filename = "../data/" + scen + "/links_" + str(i) + ".csv"
        g = graph_creation(filename, print_stats=False)

        g_sunny = graph_preparation(g, t, f=60e9, print_stats=False)
        total_capacity_60GHz_sunny.append(sum(g_sunny.es['cap']) / 1000)
        total_throughput_60GHz_sunny.append(sum(g_sunny.es['tp']) / 1000)

        g_rain1 = graph_preparation(g, t, f=60e9, pr=15, print_stats=False)
        total_capacity_60GHz_rain1.append(sum(g_rain1.es['cap']) / 1000)
        total_throughput_60GHz_rain1.append(sum(g_rain1.es['tp']) / 1000)

        g_rain2 = graph_preparation(g, t, f=60e9, pr=25, print_stats=False)
        total_capacity_60GHz_rain2.append(sum(g_rain2.es['cap']) / 1000)
        total_throughput_60GHz_rain2.append(sum(g_rain2.es['tp']) / 1000)

        g_veg = graph_preparation(g, t, f=60e9, vd=0.1, print_stats=False)
        total_capacity_60GHz_veg.append(sum(g_veg.es['cap']) / 1000)
        total_throughput_60GHz_veg.append(sum(g_veg.es['tp']) / 1000)

        g_sunny = graph_preparation(g, t, f=140e9, print_stats=False)
        total_capacity_140GHz_sunny.append(sum(g_sunny.es['cap']) / 1000)
        g_rain1 = graph_preparation(g, t, f=140e9, pr=15, print_stats=False)
        total_capacity_140GHz_rain1.append(sum(g_rain1.es['cap']) / 1000) 
        g_rain2 = graph_preparation(g, t, f=140e9, pr=25, print_stats=False)
        total_capacity_140GHz_rain2.append(sum(g_rain2.es['cap']) / 1000) 
        g_veg = graph_preparation(g, t, f=140e9, vd=0.1, print_stats=False)
        total_capacity_140GHz_veg.append(sum(g_veg.es['cap']) / 1000) 
     
    # Print average total network capacity
    print("----------------------------------------------------------------------")
    print(scen)
    print("----------------------------------------------------------------------")
    print(f"Average total network capacity sunny day  @ 60 GHz: {np.mean(total_capacity_60GHz_sunny)}")
    print(f"Average total network capacity light rain @ 60 GHz: {np.mean(total_capacity_60GHz_rain1)}")
    print(f"Average total network capacity heavy rain @ 60 GHz: {np.mean(total_capacity_60GHz_rain2)}")
    print(f"Average total network capacity vegetation @ 60 GHz: {np.mean(total_capacity_60GHz_veg)}")
    print(f"\n")
    print(f"Average total network capacity sunny day  @ 140 GHz: {np.mean(total_capacity_140GHz_sunny)}")
    print(f"Average total network capacity light rain @ 140 GHz: {np.mean(total_capacity_140GHz_rain1)}")
    print(f"Average total network capacity heavy rain @ 140 GHz: {np.mean(total_capacity_140GHz_rain2)}")
    print(f"Average total network capacity vegetation @ 140 GHz: {np.mean(total_capacity_140GHz_veg)}")
    print(f"\n")
    print(f"Average total throughput sunny day  @ 60 GHz: {np.mean(total_throughput_60GHz_sunny)}")
    print(f"Average total throughput light rain @ 60 GHz: {np.mean(total_throughput_60GHz_rain1)}")
    print(f"Average total throughput heavy rain @ 60 GHz: {np.mean(total_throughput_60GHz_rain2)}")
    print(f"Average total throughput vegetation @ 60 GHz: {np.mean(total_throughput_60GHz_veg)}")
    print("----------------------------------------------------------------------")
    print("\n")

if __name__ == '__main__':

    print_capacity_info("UC1_50CPE_UrbanVillage")
    print_capacity_info("UC1_100CPE_UrbanVillage")
    print_capacity_info("UC1_300CPE_UrbanVillage")
    print_capacity_info("UC1_600CPE_UrbanVillage")

    print_capacity_info("UC2_10CPE_Rural")
    print_capacity_info("UC2_50CPE_Rural")

    # print_capacity_info("UC3_50CPE_UrbanCity")
    # print_capacity_info("UC3_100CPE_UrbanCity")
    print_capacity_info("UC3_300CPE_UrbanCity")
    print_capacity_info("UC3_600CPE_UrbanCity")    
