#!/usr/bin/python

import logging

import igraph as ig
import numpy as np

from util_graph import parse_unconnected_graph
from util_linkbudget import get_pathloss, get_throughput, get_capacity
from util_graph import get_connected_clusters, plot_physical_locations

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_preparation.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)


def graph_preparation(g, t, f=60e9, sa=0, pr=0, vd=0, print_stats=True, datapath=None, plot=False):
    """ 
    Graph preparation algorithm, transforming weight of edges from distance to throughput,
    using link budget calculations, as well as a verification whether a solution can exist

    Params
    ------
    g : iGraph
        Input graph with CPE and edge nodes as vertices, and edges representing a Line-of-Sight
        link.
    t : integer
        CPE throughput requirement in Mbps
    f : integer
        Carrier frequency in Hz
    sa : float
        Specific attenuation in dB / km
    pr : float
        Precipitation rate in mm / h
 

    Return
    ------
    g : iGraph
        Graph with throughput attribute attached to the edges
    """

    # Verify whether graph is connected
    if not g.is_connected():
        logging.error(f"Input graph is not connected")
        unconnected_clusters = parse_unconnected_graph(g)
        if datapath and plot:
            plot_physical_locations(datapath, unconnected_clusters, edge_nodes=False, show=True, savefig=True)

        connected_clusters = get_connected_clusters(g)  # type list[Graph]
        g = connected_clusters[0]
        if 0 not in [i for i in g.vs['id']]:
            logging.error("PoP is not present in largest subgraph")
            return None

    # Get throughput for each link
    distances = g.es["weight"]
    edge_list = g.get_edgelist()
    PoP_edge_ind = []
    PoP_edge_tp = []
    PoP_edge_cap = []
    logging.debug(connected_clusters)
    logging.debug(g)
    for idx, edge in enumerate(edge_list):
        pl = get_pathloss(distances[idx],f,sa,vd,pr)
        tp = get_throughput(pl, f)
        cap = get_capacity(pl, f)
        logging.info(
            f"Edge {edge} with distance {distances[idx]} m has path loss {pl} dB and throughput {tp} Mbps")

        # Add throughput as attribute to edge in g
        g.es[idx]['tp'] = tp
        # Add capacity as attribute to edge in g
        g.es[idx]['cap'] = cap

        if edge[0] == 0 or edge[1] == 0:
            PoP_edge_ind.append(idx)
            PoP_edge_tp.append(tp)
            PoP_edge_cap.append(cap)

    for idx in range(g.vcount()):
        g.vs[idx]['t'] = t

    # Get edges connected to PoP
    # Sum throughputs of edges connected to PoP
    T = np.sum(PoP_edge_tp)

    number_CPE = len(ig.VertexSeq(g)) # when adding edge nodes, take only CPE
    network_throughput = number_CPE * t
    if T < network_throughput:
        logging.error(f"The PoP links do not have enough bandwidth ({T}) for the full network throughput ({network_throughput})")
        #return None
    else:
        logging.info(f"Network supports total throughput ({T} > {network_throughput})")

    return g

