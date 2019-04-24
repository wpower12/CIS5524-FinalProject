# Making a histogram of the subreddit counts. 

# Then need another script to iterate over leaving out the top 1, 2, 5, 10
# to get stats and stuff. Like for each of those, we need the average degree, 
# number of connected components...
import itertools
import pickle
import numpy as np

TOP_COUNT = 100
EDGELIST_FN = "pol_300_year_00_50_new_weighted"

el = pickle.load(open("data/{}.p".format(EDGELIST_FN), "rb"))
print("opened edgelist from: data/{}.p".format(EDGELIST_FN))

sub_counts = dict()

for user in el:
	for sub in user[1]:
		if sub not in sub_counts:
			sub_counts[sub] = 1
		else:
			sub_counts[sub] += 1

res = sorted(sub_counts.items(), key=lambda kv: -1*kv[1])[:(TOP_COUNT+1)]
for count in res:
	print("{}\t{}".format(count[0], count[1]))