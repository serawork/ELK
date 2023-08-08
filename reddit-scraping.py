import praw
from pymongo import MongoClient

# Reddit API credentials
CLIENT_ID = 'WGlSffuArAzdAxvn9g_zYQ'
CLIENT_SECRET = 'c_Ad9T1ANF9OerfSpwPprdR-lBQ2RQ'
USER_AGENT = 'Kas/1.0 by confused1290'

# Set up the Reddit API instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Set your desired maximum depth
MAX_DEPTH = 2  

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["reddit_data"]
collection = db["posts"]

# Define the subreddit and topic
subreddit_name = "all"
topic = "le décès du président Jacques Chirac"


def collect_comments(comments, depth=0):
    collected_comments = []
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            collected_comments.append(comment.body)
        elif isinstance(comment, praw.models.MoreComments):
            if depth < MAX_DEPTH:
                more_comments = comment.comments()
                collected_comments.extend(collect_comments(more_comments, depth + 1))
    return collected_comments

def main():
    # Search for posts related to the topic
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(topic, sort='relevance', time_filter='all')

    # Collect post data and comments
    for post in posts:
        post_data = {
            "title": post.title,
            "text": post.selftext,
            "num_comments": post.num_comments,
            "comments": collect_comments(post.comments)
        }
        
        # Extract image URL if applicable
        if post.url and any(ext in post.url for ext in (".jpg", ".jpeg", ".png", ".gif")):
            post_data["image_url"] = post.url
        
        # Insert post data into MongoDB
        collection.insert_one(post_data)

    # Close MongoDB connection
    client.close()

if __name__ == "__main__":
    main()