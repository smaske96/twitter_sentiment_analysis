import emoji
import re
from nltk.tokenize import TweetTokenizer


class Tweet:
    def __init__(self, tweet_str):
        tknzr = TweetTokenizer()
        self.tweet = tweet_str
        tokens = tknzr.tokenize(self.tweet)
        
        self.emoji = [c for c in tokens if c in emoji.UNICODE_EMOJI]
        self.hashtags = set(c for c in tokens if c.startswith('#'))
        self.mentions = set(c for c in tokens if c.startswith('@'))
        url_regex = re.compile(r'(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
        self.url = set(url_regex.findall(tweet_str))
        
        not_text = set(self.emoji).union(self.hashtags).union(self.mentions).union(self.url)
        not_text.add('RT')
        self.text = [c.lower() for c in tokens if c not in not_text]
