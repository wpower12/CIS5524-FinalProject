import subprocess

# TODO - The subreddits list stuff is broken. IDK if I care that much. but w.e

# Each data-gathering needs the following parameters
# create_db
#  - DB_NAME
# fetch_posts
#  - DB_NAME     = sys.argv[1]
#  - POST_COUNT  = int(sys.argv[2])
#  - TIME_FILTER = sys.argv[3]
#  - TYPE        = sys.argv[4]
#  - SUBREDDITS  = [] (5, ...)
# fetch_users
#  - DB_NAME         = sys.argv[1]
#  - KARMA_THRESHOLD = sys.argv[2]
# process_users
#  - DB_NAME       = sys.argv[1]
#  - COMMENT_LIMIT = sys.argv[2]
#  - TYPE          = sys.argv[3]
#  - IGNORE_SUBS   = []

# So in total, thats:
# 0 DB_NAME         - Used by all scripts, where the posts and users are stored.
# 1 POST_COUNT      - Number of posts to grab, from which users are pulled
# 2 TIME_FILTER     - [day, month, year] -   Time sort for the posts     
# 3 TYPE_POSTS      - [top, controversial] - Type sort for the posts
# 4 SUBREDDITS      - list of the subreddits to find posts in, also used to exclude subreddits during processing
# 5 KARMA_THRESHOLD - To decide what user names to gather from the posts
# 6 COMMENT_LIMIT   - Number of comments per user to look for subreddits in.
# 7 TYPE_USERS      - [new, controversial] - Type sort for user comments

runs = [
		# ["pol_300_year_05_20_new.db", 300, "year", "top", ["politics"], 5, 20, "new"],
		# ["pol_300_year_05_20_con.db", 300, "year", "top", ["politics"], 5, 20, "controversial"],
		# ["pol_300_year_10_20_new.db", 300, "year", "top", ["politics"], 10, 20, "new"],
		# ["pol_300_year_10_20_con.db", 300, "year", "top", ["politics"], 10, 20, "controversial"],
		# ["pol_300_year_00_20_new.db", 300, "year", "top", ["politics"], 0, 20, "new"],
		["pol_300_year_00_20_new.db", 300, "year", "top", ["politics"], 0, 50, "new"],]

for run in runs:
	# Create the database for the posts/users
	subprocess.run(["python",
					"data_collection/create_db.py",
					run[0]])
   
	# Build string of subreddits
	subs = ""
	for s in run[4]:
		subs = subs + s + " "
	subs = subs[:-1]
	
	# Fetch Posts
	# subprocess.run(["python",
	# 				"data_collection/fetch_posts.py",
	# 				run[0],
	# 				str(run[1]),
	# 				run[2],
	# 				run[3],
	# 				subs])

	# # Fetch Users
	# subprocess.run(["python",
	# 				"data_collection/fetch_users.py",
	# 				run[0],
	# 				str(run[5])])

	# Process Users - This will save out a pickle file with a user-subreddit list
	subprocess.run(["python",
					"data_collection/process_users_weighted.py",
					run[0],
					str(run[6]),
					run[7],
					subs])