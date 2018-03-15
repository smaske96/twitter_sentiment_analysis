import emoji, re

class Tweet:
    def __init__(self, tweet_str):
        self.tweet = tweet_str
        
        self.emoji =  [c for c in self.tweet if c in emoji.UNICODE_EMOJI]
        self.hashtags = set(part[1:] for part in self.tweet.split() if part.startswith('#'))
        self.text = self.tweet
        for c in self.emoji:
            self.text = self.text.replace(c,"")
            
        for c in self.hashtags:
            self.text = self.text.replace("#"+c,"")
        