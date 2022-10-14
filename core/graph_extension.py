#!/usr/bin/python

import os
import logging

import igraph as ig
import numpy as np
import csv

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_extension.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)


def graph_extension(g, dataset, cpe_loc, print_stats=True):
    """ 
    Extend an existing graph by adding EDGE devices that are listed in a separate data set

    Params
    ------
    g : iGraph
        Input graph with CPE and POP devices
    dataset : str
        Relative path towards data set with EDGE devices and links
    cpe_loc : str
        Relative path towards data file with the locations of CPE devices
    print_stats : bool
        Print graph statistics to terminal console
 

    Return
    ------
    g : iGraph
        Graph with POP, CPE, and EDGE devices (represented by vertices)
    """

    if os.path.isfile(dataset) and os.path.isfile(cpe_loc):
        print("Using EDGE data set: " + dataset + " and CPE location file: " + cpe_loc )
    else:
        print("CRITICAL: Input file does not exist")
        return -1

    # Parse input CSV data of EDGE links
    cpe_id = []
    edge_id = []
    edge_x_loc = []
    edge_y_loc = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it += 1
                assert row[0] == "CPE_id"
                assert row[1] == "Edge_id"
                assert row[2] == "Edge_loc_x"
                assert row[3] == "Edge_loc_y"
                continue
            try:
                cpe_id.append(int(row[0]))
                edge_id.append(int(row[1]))
                edge_x_loc.append(float(row[2]))
                edge_y_loc.append(float(row[3]))
            except:
                print("Error parsing graph data")
                return -1

    # Parse input CSV data with CPE locations
    cpe_x = []
    cpe_y = []
    with open(cpe_loc, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it = 1
                continue
            cpe_x.append(float(row[1]))
            cpe_y.append(float(row[2]))

    # Add all EDGE nodes
    nb_cpe_pop_nodes = g.vcount()
    nb_edge_nodes = len(set(edge_id))
    max_cpe_id = max(g.vs["id"])
    edge_node_id = range(max_cpe_id+1, max_cpe_id+1+nb_edge_nodes)
    g.add_vertices(nb_edge_nodes)
    g.vs[nb_cpe_pop_nodes:]["id"] = edge_node_id
    g.vs[nb_cpe_pop_nodes:]["type"] = 'EDGE'

    # Get links between EDGE nodes according to input graph data
    cpe_node_id = g.vs["id"]
    edges = []
    edge_weights = []
    for i in range(len(cpe_id)):
        # Calculate LOS distance between EDGE and CPE
        dist = np.sqrt(np.power(cpe_x[cpe_id[i]]-edge_x_loc[i],2)+np.power(cpe_y[cpe_id[i]]-edge_y_loc[i],2))
        # Find vertex ID of CPE node
        cpe_node = cpe_node_id.index(cpe_id[i])
        # Find vertex ID of EDGE node
        edge_node = edge_id[i] + max_cpe_id + 1
        edge = (cpe_node, edge_node)
        edges.append(edge)
        edge_weights.append(dist)
        logging.info(f"Add link ({cpe_id[i]}:{cpe_node}, {edge_id[i]}:{edge_node}) to graph with distance {dist} m")

    # Add edges to graph
    nb_edges_orig = g.ecount()
    g.add_edges(edges)
    g.es[nb_edges_orig:]["weight"] = edge_weights  

    # Visualize graph
    if print_stats:
        print(g)
        ig.summary(g)

    return g

