import itertools
import pickle
import numpy as np
# import networkx as nx
# from networkx.algorithms.community import *
import igraph as ig

EDGELIST_FN = "pol_300_year_00_50_new_weighted"
COUNT          = 2000 
MIN_EDGE_VALUE = 4
IGNORE_SUBS_LISTS = [["politics"],
	    ["politics", "AskReddit", "worldnews", "news", "funny", "pics"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF", "mildlyinteresting", "trashy", "unpopularopinion", "BlackPeopleTwitter", "technology"]]

el = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
print("opened edgelist from: data/{}.p".format(EDGELIST_FN))

#### Building The Projection Graph
### These steps are the same for each iteration
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
	for sub_name in subs:
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1

# Bi-Adj Matrix for each set of ignored sups
for IGNORE_SUBS in IGNORE_SUBS_LISTS:
	print("Ignore top {} subs:".format(len(IGNORE_SUBS)-1))

	B = np.zeros((len(user_map), len(subs_map)), dtype=np.int16)
	i = 0
	for user in el:
		un = user[0]
		user_id = user_map[un]
		subs = user[1]
		for sub_name in subs:
			sub_id = subs_map[sub_name]
			if sub_name not in IGNORE_SUBS:
				B[user_id][sub_id] = 1.0
		i += 1
		if i >= COUNT:
			break

	print("\tbuilding projection")
	
	# Actual User-User Projection
	padj = np.matmul(B, B.transpose()) 
	np.fill_diagonal(padj, 0)
	clip_padj = np.where( padj > MIN_EDGE_VALUE, 1, 0)

	uuproj_graph = ig.Graph.Adjacency(clip_padj.tolist(), mode=ig.ADJ_MAX)
	print("\tfinding largest comp")
	components = uuproj_graph.components()

	# print("\t{} nodes, {} edges".format(uuproj_graph.vcount(),uuproj_graph.ecount()))
	print("\t{}".format(components.summary()))

	large_cc = components.giant()
	print("\t{} nodes, {} edges:".format(large_cc.vcount(),large_cc.ecount()))
	print("\t{} ave degree".format(ig.mean(large_cc.degree())))

