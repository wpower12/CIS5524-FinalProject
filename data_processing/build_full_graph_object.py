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

THRESH = 1000

data_fn = "pol_300_year_00_50_new_weighted.p"
out_fn  = "SMALL_weighted_attrs.gexf"

edge_list = pickle.load(open("data/{}".format(data_fn), "rb"))
user_cnt = 0
graph = nx.Graph()
for user in edge_list:
	graph.add_node("U-"+user[0], type="user")
	user_cnt += 1
	for sub in user[1]:
		graph.add_node("S-"+sub, type="sub")
		w = user[1][sub]
		# Hacky way to avoid issues with a user 
		# sharing a name with a subreddit.
		graph.add_edge("U-"+user[0], "S-"+sub, weight=w)

	if user_cnt > THRESH:
		break

nx.write_gexf(graph, out_fn)