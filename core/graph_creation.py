#!/usr/bin/python

import sys
import os
import logging

import igraph as ig
import numpy as np
import csv

# Change to logging.DEBUG, .INFO, .WARNING, .ERROR, .CRITICAL
log_level = logging.DEBUG
log_format = "[%(asctime)s] - {%(module)s:%(lineno)d} - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_creation.log'
logging.basicConfig(filename=log_fn, level=log_level,
                    format=log_format, datefmt=datefmt)

def graph_creation(dataset, print_stats=True):
    """ 
    Graph creation function, transforming a data set generated via the GRAND tool into a graph. 

    Params
    ------
    dataset : str
        Relative path towards the data set
    print_stats : bool
        Print graph statistics to terminal console
 

    Return
    ------
    g : iGraph
        Graph with vertices representing CPE devices and edges representing wireless LOS links
    """

    if os.path.isfile(dataset):
        logging.info("Creating graph with data set: " + dataset)
    else:
        logging.critical("CRITICAL: Input file does not exist")
        return -1

    # Parse input CSV data
    nodeA_column = 0
    nodeAtype_column = 1
    nodeB_column = 2
    nodeBtype_column = 3
    distance_column = 4
    maxbitrate_column = 9
    maxpathloss_column = 7
    nodeA = []
    nodeA_type = []
    nodeB = []
    nodeB_type = []
    weights = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it += 1
                assert row[nodeA_column] == "NodeAid"
                assert row[nodeAtype_column] == "NodeAType"
                assert row[nodeB_column] == "NodeBid"
                assert row[nodeBtype_column] == "NodeBType"
                assert row[distance_column] == "distance"
                assert row[maxbitrate_column] == "maxbitrate"
                assert row[maxpathloss_column] == "maxPathLoss"
                continue
            try:
                nodeA.append(int(row[nodeA_column]))
                nodeA_type.append((row[nodeAtype_column]))
                nodeB.append(int(row[nodeB_column]))
                nodeB_type.append((row[nodeBtype_column]))
                weights.append(float(row[distance_column]))
            except:
                print("Error parsing graph data")
                return -1

    # Construct graph
    g = ig.Graph()

    # Add single PoP node
    g.add_vertices(1)
    g.vs["id"] = 0
    g.vs["type"] = 'PoP'

    # Add all CPE nodes: igraph ids 1 -> nb_cpe_nodes + 1
    nb_cpe_nodes = np.max(nodeA)
    cpe_node_id = range(1, nb_cpe_nodes+1)
    g.add_vertices(nb_cpe_nodes)
    g.vs[1:]["id"] = cpe_node_id
    g.vs[1:]["type"] = 'CPE'

    # Get links between EDGE nodes according to input graph data
    edge_links = [(nodeA[i], nodeB[i], weights[i]) for i in range(len(nodeA))]
    unique_edge_links = list(set(edge_links))
    edges = []
    edge_weights = []

    for x in unique_edge_links:
        # check if link (A, B) or link (B, A) is already in edges this avoids
        # adding a duplicate symmetric edge as the graph is undirected e.g. if
        # (0, 104) is already in edges, do not append (104, 0)
        edge1 = (x[0], x[1])
        edge2 = (x[1], x[0])
        if (edge1 not in edges) and (edge2 not in edges):
            edges.append(edge1)
            edge_weights.append(x[2])   # weights are symmetric

    # Add edges to graph
    g.add_edges(edges)
    g.es["weight"] = edge_weights  

    # Visualize graph
    if print_stats:
        print(g)
        ig.summary(g)

    return g

if __name__ == '__main__':

    if len(sys.argv) == 2:
        graph_creation(sys.argv[1])
    else:
        print("Missing input data")
        print("Usage: graph_analysis.py graph_data_file")
