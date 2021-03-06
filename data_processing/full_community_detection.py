import itertools
import pickle
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite as bp
from networkx.algorithms.community import *

### Parameters
GRAPH_FN   = "50_new_weighted_SMALL_first2k_nxg_pp2" # Original Bipartite NX Graph
UU_PROJ_FN = "UUPROJ_F2K_t4_gexf"  # FN for saving the UU projection as an GEXF Graph
GNC_OBJ_FN = "GN_F2K_t4_Comms" # FN for saving the first community object/list

MIN_EDGE_VALUE = 4 # Weight threshold for the projection graph
				   # Minimum number of common subreddits for users to be
				   # represented in the projection as an edge.

### Finding the Bi-Partite Projection ###
graph = pickle.load(open("data/{}.p".format(GRAPH_FN), "rb"))
print("opened NX Graph from: data/{}.p".format(GRAPH_FN))

a, b = bp.sets(graph)
for A in a:
	if A[0] == "S":
		user_set = b
		subs_set = a
	else:
		user_set = a
		subs_set = b
	break

user_cnt = len(user_set)
subs_cnt = len(subs_set)

# These maps will let me recover the user/sub names 
subs_dict = dict()
user_dict = dict()
i = 0
for user in user_set:
	user_dict[user] = i
	i += 1
i = 0
for sub in subs_set:
	subs_dict[sub] = i
	i += 1

# Building the bi-adjaceny matrix
B = np.zeros((user_cnt, subs_cnt), dtype=np.int16)
for edge in graph.edges():
	# Hacky way to figure out which is which
	if edge[0][0] == "U":
		un = edge[0]
		sn = edge[1]
	else:
		un = edge[1]
		sn = edge[0]

	un_idx = user_dict[un]
	sn_idx = subs_dict[sn]
	B[un_idx][sn_idx] = 1

# Calculating the projection and thresholding it.
proj_adj = np.matmul(B, B.transpose()) 
np.fill_diagonal(proj_adj, 0)
clipped_proj = np.where( proj_adj > MIN_EDGE_VALUE, proj_adj, 0)

# Build a nx graph  
proj_graph = nx.from_numpy_array(clipped_proj)
cc = max(nx.connected_components(proj_graph))
g  = proj_graph.subgraph(cc)

nx.write_gexf(g, "results/{}.gexf".format(UU_PROJ_FN))
print("Saved UU projection graph to: results/{}.gexf".format(UU_PROJ_FN))

### Community Detection - Girvan-Newman 

# Running this for 2000 nodes should be interesting. 
comms = girvan_newman(proj_graph)
# Right now, printing them all to see what the size of them are. 
# limited = itertools.takewhile(lambda c: len(c) <= 6, comms)
partitions = []
for part in comms:
	perf = performance(proj_graph, part)
	print("len: {} perf: {}".format(len(part), perf))
	partitions.append([part, perf])

pickle.dump(partitions, open("results/{}.p".format(GNC_OBJ_FN), "wb"))
print("wrote partitions to: results/{}.p".format(GNC_OBJ_FN))