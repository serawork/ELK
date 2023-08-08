import requests
from pymongo import MongoClient

#Facebook Graph API token
FACEBOOK_TOKEN = "FACEBOOK_TOKEN"

# Instagram Graph API token
INSTAGRAM_TOKEN = "INSTAGRAM_TOKEN"

# Set up MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["social_media"]
collection = db["posts"]

# Function to collect Facebook posts
def collect_facebook_posts(query):
    url = f"https://graph.facebook.com/v12.0/search?q={query}&type=post&access_token={FACEBOOK_TOKEN}"
    response = requests.get(url)
    data = response.json()
    posts = data.get("data", [])
    return posts

# Function to collect Instagram posts
def collect_instagram_posts(query):
    url = f"https://graph.instagram.com/v12.0/ig_hashtag_search?user_id=YOUR_USER_ID&q={query}&access_token={INSTAGRAM_TOKEN}"
    response = requests.get(url)
    data = response.json()
    hashtag_id = data.get("data", [])[0].get("id")
    
    if hashtag_id:
        url = f"https://graph.instagram.com/v12.0/{hashtag_id}/recent_media?access_token={INSTAGRAM_TOKEN}"
        response = requests.get(url)
        data = response.json()
        posts = data.get("data", [])
        return posts
    
    return []

# Main function to collect and store posts
def main():
    query = "le décès du président Jacques Chirac"
    
    # Collect Facebook posts
    facebook_posts = collect_facebook_posts(query)
    
    # Collect Instagram posts
    instagram_posts = collect_instagram_posts(query)
    
    # Combine and store posts in MongoDB
    all_posts = facebook_posts + instagram_posts
    for post in all_posts:
        collection.insert_one(post)
    
    print("Posts collected and stored successfully!")

if __name__ == "__main__":
    main()