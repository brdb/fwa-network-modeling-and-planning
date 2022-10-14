import sys
import os

import itertools
import collections

import igraph as ig
import numpy as np
import matplotlib.pyplot as plt

import logging

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_planning.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)


def network_planning(g, t, debug=False):
    """
    Function to perform the network planning towards the PoP.

    Params
    ------
    g : iGraph
        Input graph with CPE and edge nodes as vertices, and edges representing
        a Line-of-Sight link.
    t : integer
        CPE throughput requirement in Mbps
    debug : bool
        Plot the graph for debugging purposes
    """

    # Sanity checks before running planning algorithm
    if g is None:
        logging.error(
            "Input graph is None. Check if the input graph is succesfully prepared"
        )
        return None

    edge_list = g.get_edgelist()
    tp = []
    for idx, edge in enumerate(edge_list):
        # Check if each edge has attribute tp
        try:
            tp.append(g.es[idx]['tp'])
        except:
            logging.error("Attribute `tp` not available.")
            return None

    # Run planning algorithm
    g = planning_algorithm(g, t, w='weight')

    logging.debug("Node throughputs")
    logging.debug(g.vs["t"])

    if debug:
        layout = g.layout(layout='auto')

        visual_style = {}
        visual_style["vertex_size"] = 20
        visual_style["vertex_label"] = g.vs["id"]
        visual_style["layout"] = layout
        ig.plot(g, **visual_style)
    
        layout = g.layout(layout='auto')

        visual_style = {}
        visual_style["vertex_size"] = 20
        visual_style["vertex_label"] = g.vs["id"]
        visual_style["layout"] = layout
        ig.plot(g, **visual_style)

    return g

def planning_algorithm(g, t, w = None):

    # Get sorted vertex list depending on number of shortest paths 
    # and number of edges on the shortest path
    nd = [] # vertex list
    tp_req = [] # list with throughput requirements of all vertices
    nb_paths = [] # list with number of shortest paths for each vertex
    pathlen = [] # list with length of shortest path for each vertex
    for v in g.vs:
        results = g.get_all_shortest_paths(v, to=0, weights=None)
        nd.append(v)
        tp_req.append(-v["t"])
        nb_paths.append(len(results))
        pathlen.append(-len(results[0]))

    # sort list based on 
    # 1. throughput (highest throughput first) 
    # 2. number of shortest paths (lowest number of shortest paths first)
    # 3. path length (highest path length first)
    zipped_list = list(enumerate(zip(tp_req, nb_paths, pathlen)))
    sorted_list = sorted(zipped_list, key=lambda x: x[1])
    logging.debug(zipped_list)
    logging.debug(sorted_list)
    sorted_idx = sorted_list

    logging.debug(sorted_idx)
    logging.debug(tp_req)
    logging.debug(nb_paths)
    logging.debug(pathlen)
    # Make a copy of the graph that we can modify on the go
    g_work = g

    logging.debug(sorted_idx[0])
    for i in sorted_idx:
        # Get shortest path for node nd[i], using weighted graph
        v = nd[i[0]]
        logging.debug(f"Get shortest path for {v}")
        path = g_work.get_shortest_paths(v, to=0, weights=None, output="epath")
        logging.debug(path)
        edge_list = g_work.get_edgelist()
        distances = g_work.es["weight"]
        throughput = g_work.es["tp"]
        required_throughput = v["t"]
        vertex_path = []
        v1 = -1
        v2 = v
        for j in path: 
            for k in j: 
                v1_prev = v1
                v2_prev = v2
                edge = edge_list[k]
                logging.debug(f"considering edge: {edge}, v={v}, edge0={edge[0]}, {edge[0] == v.index}")
                if(edge[0] == v2_prev) or (edge[0] == v.index):
                    v1 = edge[0]
                    v2 = edge[1]
                else:
                    v1 = edge[1]
                    v2 = edge[0]
                logging.debug(f"Edge ({g_work.vs[v1]['id']},{g_work.vs[v2]['id']}) with distance {distances[k]} m has throughput {throughput[k]} Mbps, required {required_throughput}")
                if throughput[k] >  required_throughput:
                    throughput[k] = throughput[k] - required_throughput
                    logging.debug(f"Throughput is now {throughput[k]} Mbps")
                else:
                    print(f"Link ({v1},{v2}) has not enough bandwidth ({throughput[k]} Mbps)")
                    assert False 
                if throughput[k] < required_throughput:
                    # remove edge
                    logging.info(f"Edge {edge} ({g_work.vs[v1]['id']},{g_work.vs[v2]['id']}) with distance {distances[k]} is removed")
                    g_work.delete_edges(edge)
                g_work.es["tp"] = throughput
                vertex_path.append(v1)
                vertex_path.append(v2)

        # Add path as attribute to vertex
        v["eroute"] = path
        v["vroute"] = vertex_path

    logging.info(nd)
    return g_work

if __name__ == '__main__':
    print("Running from main currently not supported")
