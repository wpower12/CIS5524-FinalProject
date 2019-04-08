# Script for calculating some simple charateristics of the data sets.
# Want, for each thing: 
# - Number Nodes
# - Number Edges
# - Size of the bi-partite sets.
# - Number of Connected Components
# - For each CC
# 	- Size of bi-partite sets

import pickle
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms import bipartite as bp

LOG_FN = "initial_dataset_2019_04_08.txt"

FILES = [ # All are the top 300 posts in r/politics
		"pol_300_year_00_20_new.p", # Users comments > 0,  20 most recent comments
		"pol_300_year_10_20_new.p", # Users comments > 10, 20 most recent comments 
		"pol_300_year_00_50_new.p"] # Users comments > 0,  50 most recent comments

log  = open("results/{}".format(LOG_FN), "w")
for data_fn in FILES:
	print("Processing: {}".format(data_fn))
	edge_list = pickle.load(open("data/{}".format(data_fn), "rb"))
	log.write("File: {}\n".format(data_fn))
	user_cnt = 0
	graph = nx.Graph()
	for user in edge_list:
		user_cnt += 1
		for sub in user[1]:
			# Hacky way to avoid issues with a user 
			# sharing a name with a subreddit.
			graph.add_edge("U-"+user[0], "S-"+sub)

	log.write("\tnodes: {}\n".format(graph.order()))
	log.write("\tusers: {}, subrs: {}".format(user_cnt, graph.order()-user_cnt))
	log.write("\tedges: {}\n".format(graph.size()))
	log.write("\tbi-partite?: {}\n".format(bp.is_bipartite(graph)))
	log.write("\tnum CCs: {}\n".format(nx.number_connected_components(graph)))
	log.write("\tCC's:\n")
	n_cc = 0
	for c in nx.connected_components(graph):
		subg = graph.subgraph(c)
		n_nodes = subg.order()
		n_edges = subg.size()
		a, b = bp.sets(subg)

		# Hacky way to see which set is users/subrs
		for A in a:
			if A[0] == "S":
				user_cnt = len(b)
				subr_cnt = len(a)
			else:
				user_cnt = len(a)
				subr_cnt = len(b)
			break

		log.write("\t{}-th CC:\n".format(n_cc))
		log.write("\t\tnodes: {}, edges: {}\n".format(n_nodes, n_edges))
		log.write("\t\tusers: {}, subrs {}\n".format(user_cnt, subr_cnt))
		n_cc += 1

log.close()