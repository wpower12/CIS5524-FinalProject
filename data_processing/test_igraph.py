import itertools
import pickle
import numpy as np
# import networkx as nx
# from networkx.algorithms.community import *
import igraph as ig

COUNT = 1000
# GRAPH_FN = "full_NotWeighted_50"
EDGELIST_FN = "pol_300_year_00_50_new_weighted"

el = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
print("opened edgelist from: data/{}.p".format(EDGELIST_FN))

ig_graph = ig.Graph()

user_map = dict()
subs_map = dict()

# First pass builds the user map
u_id = 0
s_id = 0
for user in el:
	un = user[0]
	user_map[un] = u_id
	u_id += 1
	if u_id >= COUNT:
		break

print("built user map.")

# Second pass builds the sub map
s_id = u_id
for user in el:
	un = user[0]
	subs = user[1]
	for sub in subs:
		sub_name = sub[0]
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1


print("built sub map.")

ig_graph.add_vertices(s_id-1)

print("added vertices.")

# Third pass actually builds the graph. WOW im inefficient.
i = 0
for user in el:
	un = user[0]
	user_id = user_map[un]
	subs = user[1]
	for sub in subs:
		sub_name = sub[0]
		sub_id = subs_map[sub_name]
		ig_graph.add_edges([(user_id, sub_id)])
	i += 1
	if i >= COUNT:
		break

print(ig_graph)
 