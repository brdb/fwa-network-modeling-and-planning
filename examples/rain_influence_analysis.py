#!/usr/bin/python

import sys
import os
import logging

import igraph as ig
import numpy as np
import csv
import matplotlib.pyplot as plt

sys.path.append('../core/')
sys.path.append('../utils/')

from fileinput import filename

from graph_creation import graph_creation
from graph_preparation import graph_preparation

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - {%(module)s:%(lineno)d} - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'graph_preparation.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)


if __name__ == '__main__':

    t = 300 # CPE requirement in Mbps

    g1 = graph_creation('../data/UC1_100CPE_UrbanVillage/links_0.csv', print_stats=False)
    g1_sunny = graph_preparation(g1, t, sa=0, print_stats=False, datapath='../Data/Leest_100BS_1U')
    g1_rainy = graph_preparation(g1, t, sa=10, print_stats=False, datapath='../Data/Leest_100BS_1U')
    
    print(g1_rainy)
    print("For the graph with 100 CPEs in Leest: ")
    print(f"  total throughput sunny day: {np.sum(g1_sunny.es['tp'])}")
    print(f"  total throughput rainy day: {np.sum(g1_rainy.es['tp'])}")
    print(f"  average edge throughput sunny day: {np.mean(g1_sunny.es['tp'])}")
    print(f"  average edge throughput rainy day: {np.mean(g1_rainy.es['tp'])}")

    g2 = graph_creation('../Data/Leest_600BS_1U/links.csv', print_stats=False)
    g2_sunny = graph_preparation(g2, t, sa=0, print_stats=False, datapath='../Data/Leest_600BS_1U')
    g2_rainy = graph_preparation(g2, t, sa=10, print_stats=False, datapath='../Data/Leest_600BS_1U')

    print("For the graph with 600 CPEs in Leest: ")
    print(f"  total throughput sunny day: {np.sum(g2_sunny.es['tp'])}")
    print(f"  total throughput rainy day: {np.sum(g2_rainy.es['tp'])}")
    print(f"  average edge throughput sunny day: {np.mean(g2_sunny.es['tp'])}")
    print(f"  average edge throughput rainy day: {np.mean(g2_rainy.es['tp'])}")    
