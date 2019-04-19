import itertools
import pickle
import numpy as np
import networkx as nx
from networkx.algorithms.community import *
import igraph as ig

# GRAPH_FN = "full_NotWeighted_50"
GRAPH_FN = "50_new_weighted_SMALL_first2k_nxg"

graph = pickle.load(open("data/{}.p".format(GRAPH_FN), "rb"))
print("opened NX Graph from: data/{}.p".format(GRAPH_FN))

ig_graph = ig.Graph()

ig_graph.add_vertices(graph.nodes())
ig_graph.add_edges(graph.edges())
	