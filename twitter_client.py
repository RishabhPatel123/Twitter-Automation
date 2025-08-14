import os,tweepy
from dotenv import load_dotenv
load_dotenv("token.env")
USER_ID = os.getenv("USER_ID")
def get_client():
    api_key=os.getenv("api_key")
    api_secret = os.getenv("api_secret")
    access_token = os.getenv("access_token")
    access_token_secret = os.getenv("access_token_secret")
    bearer_token = os.getenv("bearer_token")
    client = tweepy.Client(consumer_key=api_key,consumer_secret=api_secret,access_token=access_token,access_token_secret=access_token_secret,bearer_token=bearer_token)
    return client
