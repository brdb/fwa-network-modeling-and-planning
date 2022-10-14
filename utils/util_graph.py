#!/usr/bin/python

import os
import logging

import igraph as ig
import numpy as np
import csv
import matplotlib as plt

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'util_graph.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)


def print_vertices(g):
    """
    Helper function to print vertices with attribute values.

    Params
    ------
    g : Graph
        Graph for which the vertices need to be printed.
    """
    for v in ig.VertexSeq(g):
        print(v)


def get_connected_clusters(g):
    """
    Helper function that extracts the connected clusters. Logs the vertices of 
    each cluster with flag DEBUG.

    Params
    ------
    g : Graph
        Graph for which the connected clusters should be extracted.

    Returns
    -------
    connected_clusters : list[Graph]
        List of connected components. Each entry is a Graph object. If `g` is
        connected, `None` is returned.
    """

    if g.is_connected():
        logging.info("Input graph is connected")
        return None
    else:
        logging.info("Input graph is not connected")

    tmp = g.clusters()  # type VertexClustering
    tmp2 = tmp.subgraphs()  # list[Graph]
    for i in range(len(tmp2)):
        logging.debug(f"Cluster {i}, size {len(tmp2[i].vs)}")

    return tmp2


def plot_physical_locations(data_path, unconnected_clusters=None, edge_nodes=True, savefig=False, show=False):
    """
    Plots the physical locations of the nodes and the graph itself from the csv
    file directly. If `unconnected_clusters` is not `None`, the unconnected
    clusters are plotted in another colour.

    Params
    ------
    data_path : str
        Path to certain configuration. E.g. -/Data/Leest_300BS_1U
    unconnected_clusters : list of lists
        List of lists, representing the unconnected clusters. Each entry of the
        list represents a single unconnected cluster. Each entry of the cluster
        is a node-ID. If not provided, nothing extra will be plotted.
        E.g. [[44], [32,34,35]]
    savefig : bool
        Saves fig. Default `False`
    show : bool
        Shows fig. Default `False`

    Returns
    -------
    x, y: list
        Lists of (x, y)-coordinates of each node
    """
    config = data_path.split('/')[-1]
    dataset = f"{data_path}/basestations_0.csv"

    # Read (x, y)-coordinates
    x = []
    y = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it = 1
                continue
            x.append(float(row[1])/1000)
            y.append(float(row[2])/1000)

    if edge_nodes:
        dataset = f"{data_path}/edge_nodes_0.csv"

        if not os.path.isfile(dataset):
            print("No valid EDGE node data file")
            assert False

        edge_id = []
        edge_x = []
        edge_y = []
        edge_links = []
        with open(dataset, 'r') as csvFile:
            reader = csv.reader(csvFile)
            it = 0
            for row in reader:
                if it == 0:
                    it = 1
                    continue
                edge_links.append((int(row[0]), int(row[1])))
                if int(row[1]) not in edge_id:
                    edge_id.append(int(row[1]))
                    edge_x.append(float(row[2])/1000)
                    edge_y.append(float(row[3])/1000)

    dataset = f"{data_path}/links_0.csv"

    # Read CPE links: (A[i], B[i]) represents an edge connecting two CPEs
    A = []
    B = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it = 1
                continue
            A.append(int(row[0]))
            B.append(int(row[2]))

    s_area = 1**2*np.pi

    plt.figure()
    # Loop over each edge
    # Draw a line from A -> B
    legend = True
    for i in range(len(A)):
        x_tmp1 = x[A[i]]
        x_tmp2 = x[B[i]]
        y_tmp1 = y[A[i]]
        y_tmp2 = y[B[i]]
        if legend:
            plt.plot([x_tmp1, x_tmp2], [y_tmp1, y_tmp2], 'r-o',
                     linewidth=0.05, markersize=s_area/2, zorder=1, label="Connected CPEs")
            legend = False
        else:
            plt.plot([x_tmp1, x_tmp2], [y_tmp1, y_tmp2], 'r-o',
                     linewidth=0.05, markersize=s_area/2, zorder=1)
    plt.scatter(x[0], y[0], c='b', marker='x', label="POP", zorder=2)
    legend=True

    s_area = 2**2*np.pi
    if unconnected_clusters:
        for cluster in unconnected_clusters:
            for node in cluster:
                if legend:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area, label="Unconnected CPEs", zorder=2)
                    legend = False
                else:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area, zorder=2)
    if edge_nodes:
        legend = True
        for i in range(len(edge_x)):
            if legend:
                plt.scatter(edge_x[i], edge_y[i], c='g', marker='D', s=s_area, label="EDGE node")
                legend = False
            else:
                plt.scatter(edge_x[i], edge_y[i], c='g', marker='D', s=s_area)
        for i in range(len(edge_links)):
            cpe_x = x[edge_links[i][0]]
            cpe_y = y[edge_links[i][0]]
            plt.plot([cpe_x, edge_x[edge_links[i][1]]], [cpe_y, edge_y[edge_links[i][1]]], 'g-',
                     linewidth=0.1, zorder=1)

    plt.xlabel("x [km]")
    plt.legend()
    if savefig:
        plt.savefig(f"{data_path}/figures/{config}_graph_from_csv.png", dpi=600)

    plt.figure()
    plt.scatter(x[0], y[0], c='b', marker='x', label="POP")
    plt.scatter(x[1:], y[1:], c='r', s=s_area, label='Connected CPEs')
    legend = True
    if unconnected_clusters:
        for cluster in unconnected_clusters:
            for node in cluster:
                if legend:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area*1.5, zorder=2, label='Unconnected CPEs')
                    legend = False
                else:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area*1.5, zorder=2)
    plt.xlabel("x [km]")
    plt.ylabel("y [km]")
    plt.title("Physical node locations")
    plt.legend()
    if savefig:
        plt.savefig(f"{data_path}/figures/{config}_graph_physical_locations.png", dpi=600)

    if show: 
        plt.show()
    return x, y


def plot_graph_with_locations(data_path, simulation_id=None, g=None, unconnected_clusters=None, edges=None, edge_nodes=True, savefig=False, show=False):
    """
    Plots the physical locations of the nodes and the graph itself from the csv
    file directly. If `unconnected_clusters` is not `None`, the unconnected
    clusters are plotted in another colour.

    Params
    ------
    data_path : str
        Path to certain configuration. E.g. -/Data/Leest_300BS_1U
    simulation_id : int
        Simulation number that needs to be visualized, cf. provided data directory
    unconnected_clusters : list of lists
        List of lists, representing the unconnected clusters. Each entry of the
        list represents a single unconnected cluster. Each entry of the cluster
        is a node-ID. If not provided, nothing extra will be plotted.
        E.g. [[44], [32,34,35]]
    savefig : bool
        Saves fig. Default `False`
    show : bool
        Shows fig. Default `False`

    Returns
    -------
    x, y: list
        Lists of (x, y)-coordinates of each node
    """
    config = data_path.split('/')[-1]
    if simulation_id is not None:
        dataset = f"{data_path}/basestations_{simulation_id}.csv"
    else:
        dataset = f"{data_path}/basestations.csv"

    # Read (x, y)-coordinates
    x = []
    y = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it = 1
                continue
            x.append(float(row[1])/1000)
            y.append(float(row[2])/1000)

    if edge_nodes:
        if simulation_id is not None:
            dataset = f"{data_path}/edge_nodes_{simulation_id}.csv"
        else:
            dataset = f"{data_path}/edge_nodes.csv"

        if not os.path.isfile(dataset):
            print("No valid EDGE node data file")
            assert False

        edge_id = []
        edge_x = []
        edge_y = []
        edge_links = []
        with open(dataset, 'r') as csvFile:
            reader = csv.reader(csvFile)
            it = 0
            for row in reader:
                if it == 0:
                    it = 1
                    continue
                edge_links.append((int(row[0]), int(row[1])))
                if int(row[1]) not in edge_id:
                    edge_id.append(int(row[1]))
                    edge_x.append(float(row[2])/1000)
                    edge_y.append(float(row[3])/1000)

    if simulation_id is not None:
        dataset = f"{data_path}/links_{simulation_id}.csv"
    else:
        dataset = f"{data_path}/links.csv"

    # Read CPE links: (A[i], B[i]) represents an edge connecting two CPEs
    A = []
    B = []
    with open(dataset, 'r') as csvFile:
        reader = csv.reader(csvFile)
        it = 0
        for row in reader:
            if it == 0:
                it = 1
                continue
            A.append(int(row[0]))
            B.append(int(row[2]))

    s_area = 1**2*np.pi

    plt.figure()
    # Loop over each edge
    # Draw a line from A -> B
    legend = True
    for i in range(len(A)):
        x_tmp1 = x[A[i]]
        x_tmp2 = x[B[i]]
        y_tmp1 = y[A[i]]
        y_tmp2 = y[B[i]]
        if legend:
            plt.plot([x_tmp1, x_tmp2], [y_tmp1, y_tmp2], 'r-o',
                     linewidth=0.05, markersize=s_area/2, zorder=1, label="Connected CPEs")
            legend = False
        else:
            plt.plot([x_tmp1, x_tmp2], [y_tmp1, y_tmp2], 'r-o',
                     linewidth=0.05, markersize=s_area/2, zorder=1)
    plt.scatter(x[0], y[0], c='b', marker='x', label="POP", zorder=2)
    legend=True

    s_area = 2**2*np.pi
    if unconnected_clusters:
        for cluster in unconnected_clusters:
            for node in cluster:
                if legend:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area*1.5, label="Unconnected CPEs", zorder=2)
                    legend = False
                else:
                    plt.scatter(x[node], y[node], c='k', marker='s', s=s_area*1.5, zorder=2)
    if edge_nodes:
        for i in range(len(edge_x)):
            plt.scatter(edge_x[i], edge_y[i], c='g', marker='D', s=s_area, label="EDGE node")
        for i in range(len(edge_links)):
            cpe_x = x[edge_links[i][0]]
            cpe_y = y[edge_links[i][0]]
            plt.plot([cpe_x, edge_x[edge_links[i][1]]], [cpe_y, edge_y[edge_links[i][1]]], 'g-',
                     linewidth=0.05, zorder=1)
    plt.xlabel("x [km]")
    plt.ylabel("y [km]")
    plt.legend()
    
    if savefig:
        plt.savefig(f"{data_path}/figures/{config}_graph_from_csv.png", dpi=600)

    if show: 
        plt.show()

    return x, y


def plot_graph(g, weights=None):
    """
    Plot the graph via igraph plotting functionality, using kk layout. 
    PoP devices are colored in blue, whereas CPE devices are colored in red 
    and EDGE devices are colored in green. If `weights` is not `None`, 
    the weight attribute of all edges is printed.

    Params
    ------
    g : Graph
        Graph that needs to be visualized.

    weights : str
        Edge attribute that needs to be printed

    """

    device_types = g.vs['type']
    colors = [dev.replace('PoP', 'blue') for dev in device_types]
    colors = [color.replace('CPE', 'red') for color in colors]
    colors = [color.replace('EDGE', 'green') for color in colors]

    layout = g.layout('kk')

    if weights:
        edge_weights = g.es[weights]
        g.es['label'] = edge_weights
        g.es["curved"] = False # else plotting the weights doesnt work

    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_label"] = g.vs["id"]
    visual_style["layout"] = layout
    visual_style["vertex_color"] = colors
    ig.plot(g, **visual_style)

    plt.show()


def parse_unconnected_graph(g):
    """
    Determine unconnected subgraphs from an input graph and return the unconnected vertices.

    Params
    ------
    g : Graph
        Graph that needs to be visualized.


    Returns
    -------
    l: list
        Lists of unconnected vertices
    """

    tmp = g.clusters()  # type VertexClustering
    tmp2 = tmp.subgraphs()  # list[Graph]
    logging.info(f"Graph consist of {len(tmp2)} connected subgraphs:")

    l = []
    for i in range(len(tmp2)):
        logging.debug(f"Cluster {i}, size {len(tmp2[i].vs)}")
        if len(tmp2[i].vs) < max([len(tmp2[j].vs) for j in range(len(tmp2))]):
            l.append(tmp2[i].vs["id"])
    if l:
        logging.info(f"Connections from largest connected subgraph must be made "
                     f"to subgraphs with nodes {l}"
        )
    
    return l
