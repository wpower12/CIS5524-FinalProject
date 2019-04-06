import sys
import praw
import sqlite3

if len(sys.argv) > 1:
	# Parse Parameters
	DB_NAME     = sys.argv[1]
	POST_COUNT  = int(sys.argv[2])
	TIME_FILTER = sys.argv[3]
	TYPE        = sys.argv[4]
	SUBREDDITS  = []
	for i in range(5, len(sys.argv)):
		SUBREDDITS.append(sys.argv[i])
else:
	DB_NAME = "test_data.db"
	POST_COUNT = 1
	TIME_FILTER = "year"
	TYPE = "top"
	SUBREDDITS = ['politics']

print(SUBREDDITS)

conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()
reddit = praw.Reddit('polbot')

for sub in SUBREDDITS:
	print("processing subreddit: {}".format(sub))

	if TYPE == "top": 
		collection = reddit.subreddit(sub).top(time_filter=TIME_FILTER, limit=POST_COUNT)
	if TYPE == "controversial":
		collection = reddit.subreddit(sub).top(time_filter=TIME_FILTER, limit=POST_COUNT)

	for post in collection:
		print("saving post {}".format(post.title))
		title = post.title.replace('"', ' ')
		title = title.replace("'", " ")
		db.execute("INSERT INTO posts(post_id, post_title) VALUES ('{}', '{}')".format(post.id, title))
		conn.commit()

conn.close()
