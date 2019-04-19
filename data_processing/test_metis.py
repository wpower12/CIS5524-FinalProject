import itertools
import pickle
import metis
import numpy as np
import networkx as nx
from networkx.algorithms.community import *

GRAPH_FN = "full_NotWeighted_50"
# GRAPH_FN = "50_new_weighted_SMALL_first2k_nxg"

graph = pickle.load(open("data/{}.p".format(GRAPH_FN), "rb"))
print("opened NX Graph from: data/{}.p".format(GRAPH_FN))
nodes = list(graph.nodes())	

for num_parts in [2,3,4]:
	partitions = []
	for i in range(num_parts):
		partitions.append([])

	(edgecuts, parts) = metis.part_graph(graph)
	for i, p in enumerate(parts):
		partitions[p].append(nodes[i])

	perf = performance(graph, partitions)
	print("{} parts: {}".format(num_parts, perf))		

