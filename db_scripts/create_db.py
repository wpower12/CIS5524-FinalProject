import sqlite3

DB_NAME = "user_data_2.db"
conn = sqlite3.connect("data/{}".format(DB_NAME))
db   = conn.cursor()

db.execute('''CREATE TABLE posts (post_id TEXT, 
								  post_title TEXT,
								  processed INTEGER DEFAULT 0,
								  UNIQUE(post_id))''')

db.execute('''CREATE TABLE users (user_id INTEGER PRIMARY KEY ASC, 
								  user_name TEXT,
								  processed INTEGER DEFAULT 0,
								  UNIQUE(user_name))''')

conn.commit()
conn.close()