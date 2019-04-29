import itertools
import pickle
import random
import sys
import numpy as np
import igraph as ig

if len(sys.argv) > 1:
	COUNT = int(sys.argv[1])
	SAVE_FN = sys.argv[2]
else:
	COUNT = 10000
	SAVE_FN = "test_gviz_01"

EDGELIST_FN = "pol_300_year_00_50_new_weighted"
edge_list = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))

# Top 20 is our best data. so ignoring that amount.
IGNORE_SUBS = ["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF"]	

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

# Second pass builds the sub map
u_id = s_id
for user in el:
	un = user[0]
	subs = user[1]
	for sub_name in subs:
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1

m_size = len(user_map)+len(subs_map)
A = np.zeros((m_size, m_size), dtype=np.int8)

for user in el:
	un = user[0]
	user_id = user_map[un]
	subs = user[1]
	for sub_name in subs:
		sub_id = subs_map[sub_name]
		if sub_name not in IGNORE_SUBS:
			A[user_id][sub_id] = 1.0

bigraph = ig.Graph.Adjacency(A.tolist(), mode=ig.ADJ_MAX)

# save the vertex names?
for user in user_map:
	u_id = user_map[user]
	bigraph.vs[u_id]["type"] = "user"
	bigraph.vs[u_id]["name"] = user

for sub in subs_map:
	s_id = subs_map[sub]
	bigraph.vs[s_id]["type"] = "sub"
	bigraph.vs[s_id]["name"] = sub

bigraph.write("{}.dot".format(SAVE_FN), format="dot")
print("saved file")
