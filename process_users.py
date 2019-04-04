import praw
import sqlite3
import pickle

### Major User Set Parameters
PICKLE_FN = "user_edges.p"
DB_NAME = "user_data_2.db"

COMMENT_LIMIT = 15
IGNORE_SUBS = ['politics'] # These will be culled from the subreddit sets

# This will be filled with [username, {subreddit name list}] 
user_edge_lists = []

# Reddit bot and database connection.
reddit = praw.Reddit('polbot')
conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()
user_cursor = db.execute("SELECT * FROM users") 

for user in user_cursor:
	try:
		new_set = set()
		print(user)
		for comment in reddit.redditor(user[1]).comments.new(limit=COMMENT_LIMIT):
			new_set.add(comment.subreddit.display_name)

		for s in IGNORE_SUBS:
			new_set.discard(s)

		# Ignore users with an empty set - Posts were all in IGNORE_SUBS
		if len(new_set) != 0:
			user_edge_lists.append([user[1], new_set])

	except Exception:
		# Not sure what is causing this. The reponse says its a
		# 403 Page Reached Exception, which i think means that the
		# user's page no longer exists. I think some users
		# will have deleted their page between username collection
		# and user processing
		print("exception raised on user {}".format(user))
	
pickle.dump(user_edge_lists, open("data/{}".format(PICKLE_FN), "wb"))

conn.close()
