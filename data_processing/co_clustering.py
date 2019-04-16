# Numpy ops to get the co-clustering. 
# This is ignoring the weights in the data for now,
# But can easily change it to not do that?

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


##### Everything above here is copy/pasted from the other
#     scripts. Everything below is the attempt to build the
#     correct kind of matricies for the Bi-Clustering Algo.

# once you have the B, you can use numpy to build the actual 
# A matrix, then build the An, Then scale with D  

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

# With the bi-adjacecny in place, we can build the full adjacency
# A = np.zeros((user_cnt+subs_cnt, user_cnt+subs_cnt), dtype=np.int16)

# Only need the off-diagonals filled in.
# Before I move to this, need to update the sn indexs to refer
# to their new location? Or rather, when I index into A, I have
# to go to sn_idx+len(user_dict)-1 because im concactentating them.

u_zeros = np.zeros((user_cnt, user_cnt), dtype=np.int16)
s_zeros = np.zeros((subs_cnt, subs_cnt), dtype=np.int16)
Bt = np.transpose(B)

A = np.block([[u_zeros, B], [Bt, s_zeros]])

# Now I find the lapcian of this. Need a degree matrix.
D = np.zeros((user_cnt+subs_cnt,user_cnt+subs_cnt), dtype=np.int16)
sums = np.sum(A, axis=0)

for i in range(len(sums)):
	D[i][i] = sums[i]

# The Laplacian
L = D - A
print(A)
print(D)
print(L)

