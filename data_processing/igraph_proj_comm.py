import itertools
import pickle
import numpy as np
# import networkx as nx
# from networkx.algorithms.community import *
import igraph as ig

EDGELIST_FN = "pol_300_year_00_50_new_weighted"
COUNT          = 5000 
MIN_EDGE_VALUE = 4
IGNORE_SUBS    = [
				  ["politics"],
				  ["politics", "AskReddit", "worldnews", "news"],]

el = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
print("opened edgelist from: data/{}.p".format(EDGELIST_FN))

#### Building The Projection Graph
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
# Second pass builds the sub map
s_id = 0
for user in el:
	un = user[0]
	subs = user[1]
	for sub in subs:
		sub_name = sub[0]
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1

# Bi-Adj Matrix
B = np.zeros((len(user_map), len(subs_map)), dtype=np.int16)
i = 0
for user in el:
	un = user[0]
	user_id = user_map[un]
	subs = user[1]
	for sub in subs:
		sub_name = sub[0]
		sub_id = subs_map[sub_name]
		if sub_name not in IGNORE_SUBS:
			B[user_id][sub_id] = 1.0
	i += 1
	if i >= COUNT:
		break

# Actual User-User Projection
padj = np.matmul(B, B.transpose()) 
np.fill_diagonal(padj, 0)
clip_padj = np.where( padj > MIN_EDGE_VALUE, 1, 0)

uuproj_graph = ig.Graph.Adjacency(clip_padj.tolist(), mode=ig.ADJ_MAX)
components = uuproj_graph.components()

print("full UU Proj graph:")
print("\t{} nodes, {} edges".format(uuproj_graph.vcount(),uuproj_graph.ecount()))
print("\t{}".format(components.summary()))

large_cc = components.giant()
print("Giant CC:")
print("\t{} nodes, {} edges:".format(large_cc.vcount(),large_cc.ecount()))

### Community Detection Algorithms
## Fast Greedy
fg_vdendr = large_cc.community_fastgreedy()
print("CD - fast greedy dendrogram:")
print("\topt cut: {}".format(fg_vdendr.optimal_count))
cut_oi = fg_vdendr.as_clustering(n=fg_vdendr.optimal_count)
print("\topt cut q: {}".format(cut_oi.q))

## Leading Eigenvector
print("CD - Leading Eigenvector:")
for i in range(2, 6):
	le_vclust = large_cc.community_leading_eigenvector(clusters=i)
	print("\t{} clusters: {}".format(i, le_vclust.q))

## Label Propogation
print("CD - Label Propogation:")
lp_vclust = large_cc.community_label_propagation()
print("\tmod: {}".format(lp_vclust.q))

## InfoMAP
# im_vclust = large_cc.community_infomap(trials=30)
# print("CD - infoMAP:\n\tmod: {}".format(im_vclust.q))
# # TODO - Why is this 0?

