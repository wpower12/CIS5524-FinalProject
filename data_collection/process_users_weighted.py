import sys
import praw
import sqlite3
import pickle

if len(sys.argv) > 1:
	DB_NAME       = sys.argv[1]
	COMMENT_LIMIT = int(sys.argv[2])
	TYPE          = sys.argv[3]
	IGNORE_SUBS   = []
	for i in range(4, len(sys.argv)):
		IGNORE_SUBS.append(sys.argv[i])
else:
	DB_NAME = "test_data.db"
	TYPE = "new"
	COMMENT_LIMIT = 5
	IGNORE_SUBS = ['politics'] 

PICKLE_FN = DB_NAME[:-2]+"p"
print(PICKLE_FN)

# This will be filled with [username, {subreddit name list}] 
user_edge_lists = []

# Reddit bot and database connection.
reddit = praw.Reddit('polbot')
conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()
user_cursor = db.execute("SELECT * FROM users") 

for user in user_cursor:
	try:
		new_counts = dict()
		print(user)
		
		if TYPE == "new":
			collection = reddit.redditor(user[1]).comments.new(limit=COMMENT_LIMIT)
		if TYPE == "controversial":
			collection = reddit.redditor(user[1]).comments.controversial(limit=COMMENT_LIMIT)
		
		for comment in collection:
			sub_name = comment.subreddit.display_name
			new_counts.setdefault(sub_name, 0)
			new_counts[sub_name] += 1

		# for s in IGNORE_SUBS:
		# 	new[s]

		# Ignore users with an empty set - Posts were all in IGNORE_SUBS
		if len(new_counts) != 0:
			user_edge_lists.append([user[1], new_counts])
			# print(new_counts)
	except Exception:
		# Not sure what is causing this. The reponse says its a
		# 403 Page Reached Exception, which i think means that the
		# user's page no longer exists. I think some users
		# will have deleted their page between username collection
		# and user processing
		print("exception raised on user {}".format(user))

pickle.dump(user_edge_lists, open("data/{}".format(PICKLE_FN), "wb"))
conn.close()