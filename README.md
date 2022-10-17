# fwa-network-modeling-and-planning
Framework for network modeling and planning of fixed wireless access (FWA) networks

## Introduction

The goal is to characterize FWA networks via network analysis and to create a network planning algorithm. 
The planning algorithm defines to which nodes the CPE devices have to connect, and routes traffic from a CPE device towards the POP device.

## Installation requirements

This framework is written in Python 3.
The following Python packages are required to run the tool
These can easily be installed using `pip install`, or using a package manager like Anaconda. 

- numpy package
- igraph package for graph modeling (https://igraph.org/python/)
- matplotlib package
- pycairo package for graph plotting

Installation instructions for the `cairo` package are platform dependent, and can be found in https://igraph.org/python/tutorial/latest/install.html#installing-igraph.

## File structure

An overview of the most important files and folders:

```
├───core
│   ├───graph_analysis.py           # methods to analyse a given graph
│   ├───graph_creation.py           # methods to construct a graph, given a csv file
│   ├───graph_extension.py          # allows manual addition of EDGE nodes
│   ├───network_planning.py         # contains a wrapper function to plan the graph, and methods to construct a graph with cliques replaced
│   ├───graph_preparation.py        # method that implements the preparation algorithm
│   utils
│   ├───utiil_graph.py              # helper functions for graph operations
│   └───util_linkbudget.py          # contains link budget calculations
└───data
    ├───environments                # Shape files for different environments
    │    ├─── uc1-LeestUrban        # Urban village environment (Leest, Belgium)
    │    ├─── uc2-LeestRural        # Rural environment (near Leest, Belgium)
    │    └─── uc3-GhentUrban        # Urban city environment (Ghent, Belgium)
    ├───UC1_50CPE_UrbanVillage      # Urban village with 50 CPEs
    ├───UC1_100CPE_UrbanVillage     # Urban village with 100 CPEs
    ├───UC1_300CPE_UrbanVillage     # Urban village with 300 CPEs
    ├───UC1_600CPE_UrbanVillage     # Urban village with 600 CPEs
    ├───UC2_10CPE_Rural             # Urban village with 10 CPEs
    ├───UC2_50CPE_Rural             # Urban village with 50 CPEs
    ├───UC3_50CPE_UrbanCity         # Urban city with 50 CPEs
    ├───UC3_100CPE_UrbanCity        # Urban city with 100 CPEs
    ├───UC3_200CPE_UrbanCity        # Urban city with 300 CPEs
    └───UC3_600CPE_UrbanCity        # Urban city with 600 CPEs
```

The `examples` directory contains example scripts for network planning and characterization of different environments and number of subscribers.
More information on the code structure can be found in the appendix of the report in the docs directory. 

