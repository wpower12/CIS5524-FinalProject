# Will take the name of one of the 'processed' data sets, and return a 
# numpy array that is properly formatted to be converted to a networkx
# graph object. I want this so I can easily do matrix versions of the
# algorithms, will still having an easy method for pulling the graph
# into networkx, and subsequently convert it to a .gexf file for loading
# into gephi for visualization.

# Need to add a user defined data type for the numpy array version

# same format, each entry in the A matrix, instead of being a single value,
# will be a tuple, of the 'user defined' data type. 

# Our DT: [('label', string), ('type', string), ('weight', int)]
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

# Repurposing to build a fulle adjacency matrix. 
user_cnt = len(user_set)
subs_cnt = len(subs_set)
subs_dict = dict()
user_dict = dict()

i = 0
for user in user_set:
	user_dict[user] = i
	i += 1
# We keep counting. 
for sub in subs_set:
	subs_dict[sub] = i
	i += 1

## Building the adjaceny matrix
dt = [('label', string), ('type', string), ('weight', int)]
A = np.empty((graph.size(), graph.size()), dtype=dt)

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