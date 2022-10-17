#!/usr/bin/python

import logging

import logging

from graph_creation import graph_creation
from graph_preparation import graph_preparation
from graph_analysis import graph_analysis
from graph_planning import graph_planning
from graph_extension import graph_extension
from util_graph import get_connected_clusters

# Logging definitions
log_level = logging.INFO
log_format = "[%(asctime)s] - {%(module)s:%(lineno)d} - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_preparation.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)

if __name__ == '__main__':

    g_raw = graph_creation('../Data/Leest_100BS_1U/links.csv', print_stats=False)

    #_ = graph_analysis(g_raw, print_stats=False)
    #g = graph_extension(g_raw, '../Data/Leest_100BS_1U/edge_nodes.csv', '../Data/Leest_100BS_1U/basestations.csv')

    connected_clusters = get_connected_clusters(g_raw)  # type list[Graph]
    g = connected_clusters[0]

    t = 300 # CPE requirement in Mbps
    g_input = graph_preparation(g_raw, t, print_stats=True, datapath='../Data/Leest_100BS_1U')

    route = graph_planning(g_input, t, min_clique=3, max_clique=3)
    
    print("done")
    