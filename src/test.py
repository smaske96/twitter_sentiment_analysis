from tweet import Tweet

with open('sample_tweets.txt','r',encoding='utf8') as f:
    for t in f.readlines():
        tweet = Tweet(t)
        print(vars(tweet))
    