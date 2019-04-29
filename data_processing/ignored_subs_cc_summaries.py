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
	LOG_FN = sys.argv[3]
	TOP_N_COMPS = int(sys.argv[4])	
	NUM_USERS_FOR_SUM = int(sys.argv[5])
else:
	COUNT          = 500 
	MIN_EDGE_VALUE = 3
	LOG_FN = "cc_summary_res"
	TOP_N_COMPS = 5	
	NUM_USERS_FOR_SUM = 3000

EDGELIST_FN = "pol_300_year_00_50_new_weighted"

IGNORE_SUBS_LISTS = [
	    # ["politics", "AskReddit", "worldnews", "news", "funny", "pics"]]	
	    ["politics"],
	    ["politics", "AskReddit", "worldnews", "news", "funny", "pics"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF", "mildlyinteresting", "trashy", "unpopularopinion", "BlackPeopleTwitter", "technology"],
		["politics", "AskReddit", "worldnews", "news", "funny", "pics", "todayilearned", "gaming", "aww", "videos", "movies", "gifs", "PoliticalHumor", "Showerthoughts", "interestingasfuck", "WTF", "mildlyinteresting", "trashy", "unpopularopinion", "BlackPeopleTwitter", "technology", "science", "PublicFreakout", "OldSchoolCool", "AmItheAsshole", "nottheonion", "relationship_advice", "MurderedByWords", "RoastMe", "WhitePeopleTwitter", "oddlysatisfying", "atheism", "AdviceAnimals", "insanepeoplefacebook", "memes", "television", "nba", "AskMen", "nfl", "Futurology", "Damnthatsinteresting"]]

def plog(str, fo):
	print(str)
	fo.write(str+"\n")

log_file = open("results/{}.txt".format(LOG_FN), "w")
edge_list = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
plog("opened edgelist from: data/{}.p".format(EDGELIST_FN), log_file)
plog("random draw of {}, threshold {}".format(COUNT, MIN_EDGE_VALUE), log_file)

el = random.sample(edge_list, COUNT)

#### Building The Projection Graph
### These steps are the same for each iteration
user_map = dict()
subs_map = dict()
uid_uname_map = []
sid_sname_map = []

# First pass builds the user map
u_id = 0
s_id = 0
for user in el:
	un = user[0]
	user_map[un] = u_id
	u_id += 1
	uid_uname_map.append(un)

# Second pass builds the sub map
s_id = 0
for user in el:
	un = user[0]
	subs = user[1]
	for sub_name in subs:
		if sub_name not in subs_map:
			subs_map[sub_name] = s_id
			s_id += 1
			sid_sname_map.append(sub_name)

# Bi-Adj Matrix for each set of ignored sups
for IGNORE_SUBS in IGNORE_SUBS_LISTS:
	plog("ignoring top {} subs:".format(len(IGNORE_SUBS)-1), log_file)

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

	plog("\tbuilding projection: {}".format(np.count_nonzero(B)), log_file)

	# Actual User-User Projection
	padj = np.matmul(B, B.transpose()) 
	np.fill_diagonal(padj, 0)
	clip_padj = np.where( padj > MIN_EDGE_VALUE, 1, 0)

	uuproj_graph = ig.Graph.Adjacency(clip_padj.tolist(), mode=ig.ADJ_MAX) 
	components = uuproj_graph.components()

	# Need the CC's sorted by size.
	# cc_sizes = components.sizes()
	# print(cc_sizes)
	# print(list(components[0]))
	components = sorted(list(components), key=lambda kv: len(kv))
	components.reverse()

	# Need to go from the user ID to a username, and then pull
	# the users row in the edge list, find their subs, then
	# remove the IGNORED_SUBS and print it out. 
	plog("\ttop {} connected components (by size):".format(TOP_N_COMPS), log_file)
	cc_num = 0
	for cc in itertools.islice(components,TOP_N_COMPS):
		i = 0
		non_ignored_subs = dict()
		for user_id in cc:
			user_id = cc[0]
			un = uid_uname_map[user_id]
			subs = None
			for user in el:
				if user[0] == un:
					subs = user[1]
					break

			for s in subs:
				if s in IGNORE_SUBS:
					break
				if s not in non_ignored_subs:
					non_ignored_subs[s] = 1
				else:
					non_ignored_subs[s] += 1
			i += 1
			if i >= NUM_USERS_FOR_SUM:
				break

		plog("\t  representative subs for cc # {}, {} nodes:".format(cc_num, len(cc)), log_file)
		for s in non_ignored_subs:
			plog("\t   {}, {}".format(s, non_ignored_subs[s]), log_file)
		cc_num += 1

log_file.close()
