import pickle
# import math
import networkx as nx
from networkx.algorithms import bipartite as bp
import numpy as np

GRAPH_FN = "UUPROJ_50_new_weighted_SMALL_first2k_nxg"

graph = pickle.load(open("results/{}.p".format(GRAPH_FN), "rb"))


# This is a np array adjacency matrix.

# The bins should be 0-50? I think? Maybe I should do this in a notebook. 

hist_1 = np.histogram(graph, range(1, 50))
sum_1 = sum(hist_1[0])

for i in range(2, 10):
	hist_i = np.histogram(graph, range(i, 50))
	s = sum(hist_i[0])
	print("hist over {}: {}, ~{}%".format(i, s, (s/sum_1)*100))