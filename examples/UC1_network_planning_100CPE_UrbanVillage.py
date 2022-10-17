#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from graph_analysis import graph_analysis, get_distance_metrics
from util_graph import util_plot_graph, plot_physical_locations, plot_graph, plot_graph_with_locations
from graph_preparation import graph_preparation
from network_planning import network_planning
from util_graph import parse_unconnected_graph
from graph_extension import graph_extension

def print_graph_analysis(g):
    print("----------------------------------------------------------------------")
    print("Rural, 50 CPEs, simulation 1")
    print("----------------------------------------------------------------------")
    _ = graph_analysis(g, print_stats=True)
    med_dist = np.median(g.es["weight"])
    print(f"Median link distance: {med_dist}")
    print("----------------------------------------------------------------------")
    print("\n")

if __name__ == '__main__':

    datapath = '../data/UC1_100CPE_UrbanVillage'
    t=300

    # Create graph
    g0 = graph_creation(datapath + '/links_0.csv', print_stats=False)
    # Perform graph analysis
    print_graph_analysis(g0)
    # Visualize input graph
    # plot_graph(g0)
    unconnected_clusters = parse_unconnected_graph(g0)
    #plot_physical_locations(datapath,unconnected_clusters=unconnected_clusters,edge_nodes=False,savefig=True,show=True)

    g_ext = graph_extension(g0, datapath+'/edge_nodes_0.csv', datapath+'/basestations_0.csv')

    plot_graph(g_ext)

    # unconnected_clusters = parse_unconnected_graph(g_ext)
    # plot_physical_locations(datapath,unconnected_clusters=unconnected_clusters,edge_nodes=True,savefig=True,show=True)
    # g_prep = graph_preparation(g_ext, t, f=60e9, datapath=datapath, plot=False,print_stats=True)
    # print(f"Nb. of connected CPEs: {g_prep.vcount()}")

    # # Calculate capacity of links towards POP

    # g = graph_planning(g_prep,t)
    # print(g.vs["eroute"])

    # plot_graph_with_locations(datapath, g, edges=g.vs["eroute"] ,edge_nodes=False, show=True, savefig=True)




