import praw
import sqlite3

DB_NAME = "user_data_2.db"
conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()

reddit = praw.Reddit('polbot')
subreddits = ['politics']

post_count = 200

for sub in subreddits:
	print("processing subreddit: {}".format(sub))
	for post in reddit.subreddit(sub).top(time_filter="year", limit=post_count):
		print("saving post {}".format(post.title))
		title = post.title.replace('"', ' ')
		title = title.replace("'", " ")
		db.execute("INSERT INTO posts(post_id, post_title) VALUES ('{}', '{}')".format(post.id, title))
		conn.commit()

conn.close()
