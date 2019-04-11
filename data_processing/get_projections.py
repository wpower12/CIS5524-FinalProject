import pickle
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms import bipartite as bp

FILES = [ # All are the top 300 posts in r/politics
		"pol_300_year_00_20_new", # Users comments > 0,  20 most recent comments
		"pol_300_year_10_20_new", # Users comments > 10, 20 most recent comments 
		"pol_300_year_00_50_new"] # Users comments > 0,  50 most recent comments

for data_fn in FILES:
	print("Processing: {}".format(data_fn))
	edge_list = pickle.load(open("data/{}.p".format(data_fn), "rb"))

	graph = nx.Graph()
	for user in edge_list:
		for sub in user[1]:
			# Hacky way to avoid issues with a user 
			# sharing a name with a subreddit.
			graph.add_edge("U-"+user[0], "S-"+sub)


	# need to just get the largest CC. 
	cc = max(nx.connected_components(graph), key=len)
	g_mcc  = graph.subgraph(cc)
	a, b = bp.sets(g_mcc)

	# hacky way to see which is the user set. 
	for A in a:
		if A[0] == "S":
			user_set = b
		else:
			user_set = a
		break

	user_user_g = bp.projected_graph(g_mcc, user_set)

	pickle.dump(user_user_g, open("uup_{}.p".format(data_fn), "wb"))
