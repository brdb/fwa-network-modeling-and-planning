#!/usr/bin/python

import sys
import os
import logging

import igraph as ig
import numpy as np
import csv

sys.path.append('../utils/')

from fileinput import filename
from graph_creation import graph_creation
from util_graph import get_connected_clusters

# Change to logging.DEBUG, .INFO, .WARNING, .ERROR, .CRITICAL
log_level = logging.INFO
log_format = "[%(asctime)s] - {%(module)s:%(lineno)d} - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_analysis.log'
logging.basicConfig(filename=log_fn, level=log_level,
                    format=log_format, datefmt=datefmt)


def graph_analysis(g, print_stats=True, weighted_stats=True, return_stats=False):
    """
    Analyses an input graph and returns certain graph properties.

    Params
    ------
    dataset : graph
        a graph object created via create_graph.
    print_stats : bool
        Prints statistics of the graph. Default is `True`.
    weighted_stats : bool
        When `True`, return properties calculated with a weighted graph. If 
        `False`, hop count is used as weight. Properties with different values
        for (un-)weighted graph:
            * eccentricity
            * radius
            * diameter
    return_stats: bool
        When `True`, return graph properties. Default is `False`.

    Returns
    -------
    g : graph object
        Input graph
    eccentricity : np.ndarray
        Eccentricity, found with the formula from Ch6, slide 17
    radius : float
        Radius, found with the formula from Ch6, slide 17
    diameter : float
        Diameter, found with the formula from Ch6, slide 17
    avg_path_length : list
        Average path length, found with the formula from Ch6, slide 18
    characteristic_path_length : float
        Characteristic path length, found with the formula from Ch6, slide 18
    avg_path_length_hop : list
        Average hop count for each node
    avg_hop_count : int
        Average hop count of full graph
    degree : list
        Node degree.
    """

    # Verify that the input parameter is a graph
    if not isinstance(g, ig.Graph):
        print(f"Parameter `g` must be a Graph object")
        assert False 

    # Split total graph into connected parts
    connected_clusters = get_connected_clusters(g)
    if connected_clusters:
        # Take largest connected part
        g = connected_clusters[np.argmax([len(i.vs) for i in connected_clusters])]

    try:
        edge_weights = g.es["weight"]
    except:
        edge_weights = None
        logging.error("No weights are assigned.")

    # Get some graph statistics
    (_, _, weighted_ecc, radius, diameter, 
        avg_path_length, char_path_length, 
        avg_hop, avg_hop_count) = get_distance_metrics(g, edge_weights)
    deg = g.degree()
    betweenness = g.betweenness(weights=edge_weights)
    ecc = g.eccentricity()

    # Try accessing eccentricity
    try:
        tmp = ecc.index(0)
    except ValueError:
        logging.info("No vertex has eccentricity 0")

    if print_stats:
        logging.info(f"Graph degree: {deg}")
        logging.info(f"Graph eccentricity (hop count): {ecc}")
        logging.info(f"Vertex betweenness: {betweenness}")
        logging.info(f"Edge betweenness: {g.edge_betweenness()}") 
        print(f"Average graph degree: {np.mean(deg)}")
        print(f"Average vertex betweenness: {np.mean(betweenness)}")
        print(f"Graph diameter (hop count): {g.diameter()}")
        
        print(f"Average graph eccentricity (hop count): {np.mean(ecc)}")
        try:
            print(f"Non-connected element with zero ecc: {ecc.index(0)}")
        except ValueError:
            print("No vertex has eccentricity 0")
        print(f"Graph radius (hop count): {g.radius()}")
        print(f"Graph diameter (incl. weights): {diameter}")
        logging.info(f"Graph eccentricity (incl. weights): {weighted_ecc}")
        print(f"Average graph eccentricity (incl. weights): {np.mean(weighted_ecc)}")
        try:
            print(f"Non-connected element with zero ecc: {list(weighted_ecc).index(0)}")
        except ValueError:
            print("No vertex has eccentricity 0")
        print(f"Graph radius (incl. weights): {radius}")
        logging.info(f"Average path length: {avg_path_length}")
        print(f"Average path length: {np.mean(avg_path_length)}")
        print(f"Characteristic path length: {char_path_length}")
        logging.info(f"Average hop count per node: {avg_hop}")
        print(f"Average hop count of graph: {np.mean(avg_hop)}")
        print(f"Characteristic hop count of graph: {np.median(avg_hop)}")
        print("\n")
        print(f"PoP degree: {deg[0]}")
        print(f"PoP vertex betweenness: {betweenness[0]}")
        print(f"PoP eccentricity: {ecc[0]}")
        print(f"PoP eccentricity: {weighted_ecc[0]}")
        print(f"PoP avg. path length: {avg_path_length[0]}")
        print(f"PoP avg. hop: {avg_hop[0]}")

        format_edges(g, slice(len(g.get_edgelist())))

    if weighted_stats:
        ecc = weighted_ecc
        radius = radius
        diameter = diameter
    else:
        ecc = ecc
        radius = g.radius()
        diameter = g.diameter()

    if return_stats:
        return (g, ecc, radius, diameter, 
            avg_path_length, char_path_length, 
            avg_hop, avg_hop_count, deg)
    else:
        return g


def format_edges(g, index_slice):
    """
    Helper function which formats edges and prints them.

    Params
    ------
    g : Graph
        Graph for which the edges need to be printed.
    index_slice : slice
        Indices which need to be printed. The order of the edges is the order of
        how the csv is read.
    """
    edge_list = g.get_edgelist()[index_slice]
    weights = g.es["weight"][index_slice]
    edgeA, typeA = [], []
    edgeB, typeB = [], []
    for idx, edge in enumerate(edge_list):
        edgeA.append(g.vs["id"][edge[0]])
        typeA.append(g.vs["type"][edge[0]])
        edgeB.append(g.vs["id"][edge[1]])
        typeB.append(g.vs["type"][edge[1]])

    sorted_idx = np.argsort(np.array(edgeA))
    for i in sorted_idx:
        logging.info(
            f"Edge {edgeA[i]} ({typeA[i]}) -> {edgeB[i]} ({typeB[i]}): weight {weights[i]}")


def get_distance_metrics(g, edge_weights=None, print_stats=False):
    """
    Calculates distance metrics seen in the course notes. This function exists
    as igraph does not support distance measures (e.g. eccentricity) that take
    the edge weights into account. Only hop-count is used.

    Params
    ------
    g : Graph
        Graph for which distance metrics need to be calculated
    edge_weights: list
        Weights of all edges in g

    Returns
    -------
    adj : np.ndarray
        Adjacency matrix
    dist_matrix : np.ndarray
        Distance matrix: M[i, j] = distance(i, j)
    eccentricity : np.ndarray
        Eccentricity, found with the formula from Ch6, slide 17
    radius : float
        Radius, found with the formula from Ch6, slide 17
    diameter : float
        Diameter, found with the formula from Ch6, slide 17
    avg_path_length : list
        Average path length, found with the formula from Ch6, slide 18
    characteristic_path_length : float
        Characteristic path length, found with the formula from Ch6, slide 18
    avg_path_length_hop : list
        Average hop count for each node
    avg_hop_count : int
        Average hop count of full graph
    """

    adj = np.array(g.get_adjacency(attribute='weight').data)
    dist_matrix = np.array(g.shortest_paths(weights=edge_weights))

    eccentricity = np.array([np.max(row) for row in dist_matrix])
    radius = np.min(eccentricity)
    diameter = np.max(dist_matrix)
    avg_path_length = np.sum(dist_matrix, axis=0)/(dist_matrix.shape[0] - 1)
    characteristic_path_length = np.median(avg_path_length)

    dist_matrix_hop = np.array(g.shortest_paths())
    avg_path_length_hop = np.sum(dist_matrix_hop, axis=0) / (dist_matrix_hop.shape[0] - 1)
    avg_hop_count = np.mean(avg_path_length_hop)

    if print_stats:
        print(f"Eccentricity: {eccentricity}")
        print(f"Radius: {radius}")
        print(f"Diameter: {diameter}")
        print(f"Average path length: {avg_path_length}")
        print(f"Characteristic path length: {characteristic_path_length}")
        print(f"Average hop count: {avg_path_length_hop}")
        print(f"Average hop count of graph: {avg_hop_count}")

    return (adj, dist_matrix, eccentricity, radius, diameter, 
           avg_path_length, characteristic_path_length,
           avg_path_length_hop, avg_hop_count)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        g = graph_creation(sys.argv[1])
        graph_analysis(g)
    else:
        print("Missing input data")
        print("Usage: graph_analysis.py graph_data_file")
