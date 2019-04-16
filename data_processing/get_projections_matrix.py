import pickle
import networkx as nx
from networkx.algorithms import bipartite as bp
import numpy as np

GRAPH_FN = "50_new_weighted_SMALL_first2k_nxg"

graph = pickle.load(open("data/{}.p".format(GRAPH_FN), "rb"))
a, b = bp.sets(graph)

# hacky way to see which is the user set. 
for A in a:
	if A[0] == "S":
		user_set = b
		subs_set = a
	else:
		user_set = a
		subs_set = b
	break

# Need a numpy array of size |users| x |subs|
user_cnt = len(user_set)
subs_cnt = len(subs_set)

print("{} users, {} subs".format(user_cnt, subs_cnt))
print("number edges in og nx graph: {}".format(graph.number_of_edges()))

# These maps will let me recover the user/sub names 
# after manipulating the matrices. 
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

## Building the bi-adjaceny matrix
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
print("number edges in bi-adjaceny: {}".format(np.count_nonzero(B)))

## Calculating the projection.

# M's suggestion - I think? Could only find one paper that explicitly describes this
# method, but it seems to be correct.
padj = np.matmul(B, B.transpose()) 
np.fill_diagonal(padj, 0)


# Here's where we threshold. If you are 
MIN_EDGE_VALUE = 3

clipped = np.where( padj > MIN_EDGE_VALUE, padj, 0)

# clipped = np.clip(projection_adj, MIN_EDGE_VALUE, 50)
# clipped = np.clip(clipped, 0, 1)

print("number edges in thresholded projection matrix: {}".format(np.count_nonzero(clipped)))
# pickle.dump(clipped, open("results/UUPROJ_thresh3_{}.p".format(GRAPH_FN), "wb"))

# Build a nx graph  
proj_graph = nx.from_numpy_array(clipped)

# Get the largest CC for first viz.
cc = max(nx.connected_components(proj_graph))
g  = proj_graph.subgraph(cc)

print("number edges in projection graph: {}".format(g.number_of_edges()))
nx.write_gexf(g, "results/02_thresh3_{}.gexf".format(GRAPH_FN))
