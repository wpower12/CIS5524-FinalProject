import pickle
import itertools
import numpy as np
import networkx as nx

GRAPH_FN   = "50_new_weighted_SMALL_first2k_nxg"
OUT_FN     = "50_new_weighted_SMALL_first2k_nxg_pp2"

graph = pickle.load(open("data/{}.p".format(GRAPH_FN), "rb"))
pickle.dump(graph, open("data/{}.p".format(OUT_FN), "wb"), protocol=2)