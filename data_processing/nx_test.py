import pickle
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms import bipartite as bp

DATA_PFN = "pol_300_year_00_20_new.p"
DEBUG = ""

edge_list = pickle.load(open("data/{}".format(DATA_PFN), "rb"))
graph = nx.Graph()

for user in edge_list:
	# print(user)
	for sub in user[1]:
		a = user[0]
		b = sub
		# print(a, b)
		graph.add_edge("U-"+user[0], "S-"+sub)

DEBUG  = "num nodes: {}\n".format(graph.order())
DEBUG += "num cc's: {}\n".format(nx.number_connected_components(graph))
DEBUG += "connected?: {}\n".format(nx.is_connected(graph))
DEBUG += "bipartite?: {}\n".format(bp.is_bipartite(graph))

print(DEBUG)
DEBUG = ""

# for c in nx.connected_components(graph):
# 	subg = graph.subgraph(c)
# 	i += 1
# 	a, b = bp.sets(subg)

# sorted_ccs = sorted(nx.connected_components(graph), key=len)
# cc = sorted_ccs[-1]

cc = max(nx.connected_components(graph), key=len)
g  = graph.subgraph(cc)

DEBUG += "sub graph bipartite?: {}\n".format(bp.is_bipartite(g))

print(DEBUG)
DEBUG = ""

a, b = bp.sets(g)
DEBUG += "found bipartite set of largest CC\n"
print(DEBUG)
DEBUG = ""

# hacky way to see which is the user set. 
for A in a:
	if A[0] == "S":
		user_set = b
	else:
		user_set = a
	break

print(len(user_set))
# user_user_g = bp.projected_graph(g, user_set)

# DEBUG += "found user-user projection of largest CC"
# print(DEBUG)
# DEBUG = ""

# DEBUG += "size of user-user projection\n"
# DEBUG += "{} nodes, {} edges\n".format(user_user_g.order(), user_user_g.size())

# pickle.dump(user_user_g, open("user_user_graph.p", "wb"))

# # need to do it by parts. How many connected components? 

# # Might need a LOT more comments from the user history to make sure it
# # gets a little more connected

# # parts = bp.sets(graph)

# # comps = girvan_newman(graph)

# print(DEBUG)

# nx.write_gexf(graph, "pol_300_year_00_20_new.gexf")
# print("gefx file written.")