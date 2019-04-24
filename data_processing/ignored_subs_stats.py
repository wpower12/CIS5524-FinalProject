import itertools
import pickle
import numpy as np
import random
import sys
# import networkx as nx
# from networkx.algorithms.community import *
import igraph as ig

if len(sys.argv) > 1:
	COUNT = int(sys.argv[1])
	MIN_EDGE_VALUE = int(sys.argv[2])
else:
	COUNT          = 5000 
	MIN_EDGE_VALUE = 4
EDGELIST_FN = "pol_300_year_00_50_new_weighted"
IGNORE_SUBS_LISTS = [
	    ["politics"],
	    ["politics", "AskReddit", "worldnews", "news", "funny", "pics"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF", "mildlyinteresting", "trashy", "unpopularopinion", "BlackPeopleTwitter", "technology"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF", "mildlyinteresting", "trashy", "unpopularopinion", "BlackPeopleTwitter", "technology", "science", "PublicFreakout", "OldSchoolCool", "AmItheAsshole", "nottheonion", "relationship_advice", "MurderedByWords", "RoastMe", "WhitePeopleTwitter", "oddlysatisfying", "atheism", "AdviceAnimals", "insanepeoplefacebook", "memes", "television", "nba", "AskMen", "nfl", "Futurology", "Damnthatsinteresting"]]
edge_list = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
print("opened edgelist from: data/{}.p".format(EDGELIST_FN))
print("random draw of {}, threshold {}".format(COUNT, MIN_EDGE_VALUE))

el = random.sample(edge_list, COUNT)

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
	# if u_id >= COUNT:
	# 	break

# Second pass builds the sub map
u_id = 0
s_id = 0
for user in el:
	un = user[0]
	subs = user[1]
	for sub_name in subs:
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1
	u_id += 1
	# if u_id >= COUNT:
	# 	break 

# Bi-Adj Matrix for each set of ignored sups
for IGNORE_SUBS in IGNORE_SUBS_LISTS:
	print("Ignore top {} subs:".format(len(IGNORE_SUBS)-1))

	B = np.zeros((len(user_map), len(subs_map)), dtype=np.int16)
	
	i = 0
	for user in el:
		# TODO - Resouvoir Sampling. 
		#        Roll a die, decide to add or not.
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

	print("\tbuilding projection: {}".format(np.count_nonzero(B)))

	# Actual User-User Projection
	padj = np.matmul(B, B.transpose()) 
	np.fill_diagonal(padj, 0)
	clip_padj = np.where( padj > MIN_EDGE_VALUE, 1, 0)

	uuproj_graph = ig.Graph.Adjacency(clip_padj.tolist(), mode=ig.ADJ_MAX) 
	components = uuproj_graph.components()

	# print("\t{} nodes, {} edges".format(uuproj_graph.vcount(),uuproj_graph.ecount()))
	print("\t{}".format(components.summary()))

	large_cc = components.giant()
	print("\t{} nodes, {} edges:".format(large_cc.vcount(),large_cc.ecount()))
	print("\t{} ave degree".format(ig.mean(large_cc.degree())))

	### Community Detection Algorithms
	## Fast Greedy
	fg_vdendr = large_cc.community_fastgreedy()
	print("\tCD - fast greedy dendrogram:")
	print("\t opt cut: {}".format(fg_vdendr.optimal_count))
	cut_oi = fg_vdendr.as_clustering(n=fg_vdendr.optimal_count)
	print("\t opt cut q: {}".format(cut_oi.q))

	## Leading Eigenvector
	print("\tCD - Leading Eigenvector:")
	for i in range(2, 5):
		le_vclust = large_cc.community_leading_eigenvector(clusters=i)
		print("\t  {} clusters: {}".format(i, le_vclust.q))

	## Label Propogation
	print("\tCD - Label Propogation:")
	lp_vclust = large_cc.community_label_propagation()
	print("\t mod: {}".format(lp_vclust.q))   