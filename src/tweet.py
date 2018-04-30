import emoji
import re
from nltk.tokenize import TweetTokenizer
from nltk import ngrams
import string

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

        self.n_grams = []
        self.n_grams.append(self.__createNGram(2))
        self.n_grams.append(self.__createNGram(3))
        self.n_grams.append(self.__createNGram(4))

    """
    Creates 2D n-gram array with following signature:
    [
        [first n-gram sequence...],
        [another n-gram sequence...],
        ...
    ]
    """
    def __createNGram(self, n):
        temp_text = [c for c in self.text if c not in string.punctuation]
    
        ret = []
        for i in range(n):
            ret.append([])
        ngs = list(ngrams(temp_text, n))
        idx = 0
        for ng in ngs:
            ret[idx%n].append(ng)
            idx += 1
        return ret

