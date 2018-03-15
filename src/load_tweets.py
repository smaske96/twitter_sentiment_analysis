# Loads tweets in a text file

import tweepy
from api_keys import *

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

if (not api):
    print ("Problem connecting to API")

    
    

searchQuery = '"trump" OR #trump'    
maxTweets = 10000
tweetsPerQry = 100

tweetCount = 0

with open('trump.txt', 'w',encoding='utf8') as f:
    for tweet in tweepy.Cursor(api.search,q=searchQuery, tweet_mode='extended').items(maxTweets) :         
        if tweet.lang == 'en': # and not tweet.retweeted and ('RT @' not in tweet.full_text):
            f.write(' '.join(tweet.full_text.splitlines())  + '\n')
            tweetCount += 1

    print("Downloaded {0} tweets".format(tweetCount))