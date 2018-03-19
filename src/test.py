from tweet import Tweet

with open('sample_tweets.txt','r',encoding='utf8') as f:
    for t in f.readlines():
        tweet = Tweet(t)
        print('Actual Tweet:\t', t)
        print('Hashtags:\t', tweet.hashtags)
        print('Emojis:\t\t', tweet.emoji)
        print('Mentions:\t', tweet.mentions)
        print('URL:\t\t', tweet.url)
        print('Text only:\t',tweet.text)
        print("="*75)
    