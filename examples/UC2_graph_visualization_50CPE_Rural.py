#!/usr/bin/python

import sys
import igraph as ig
import numpy as np

sys.path.append('../core/')

from graph_creation import graph_creation
from util_graph import plot_graph, plot_graph_with_locations

if __name__ == '__main__':

    datapath = '../data/UC2_50CPE_Rural'

    g0 = graph_creation(datapath+'/links_0.csv', print_stats=False)

    plot_graph(g0)
    plot_graph_with_locations(datapath, simulation_id=0, edge_nodes=False, savefig=True, show=True)

    # Do something with unconnected clusters also! 
    # Do something with edge nodes also