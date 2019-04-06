import sys
import praw
import sqlite3

if len(sys.argv) == 3:
	# parse parameters
	DB_NAME         = sys.argv[1]
	KARMA_THRESHOLD = int(sys.argv[2])
else:
	# Defaults
	DB_NAME = "test_data.db"
	KARMA_THRESHOLD = 10

conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()
reddit = praw.Reddit('polbot')

for post in db.execute("SELECT * FROM posts WHERE processed=0").fetchall():
	print("processing post: {}".format(post[1]))
	s = reddit.submission(id=post[0])
	print("comment count: {}".format(s.num_comments))
	# Limits us to just top level comments.
	s.comments.replace_more(limit=10, threshold=1)
	for comment in s.comments:
		if comment.score > KARMA_THRESHOLD:
			if comment.author != None:
				name = comment.author.name
				print("user comment over threshold: {}".format(name))
				db.execute("INSERT OR IGNORE INTO users(user_name) VALUES ('{}')".format(name))
				conn.commit()

	db.execute("UPDATE posts SET processed=1 WHERE post_id='{}'".format(post[0]))
	conn.commit()

conn.close()
