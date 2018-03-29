import json
from collections import defaultdict
from tweet import Tweet
from nltk.corpus import stopwords

class TSA_Test:
    def __init__(self, output_file, **kwargs):
        self.word_sentiment = defaultdict(lambda: x, json.load(open(output_file)))
        #Add stemming option
        
    def getSentiment(self, tweet):
        tw = Tweet(tweet)
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tw.text + tw.emoji if not w in stop_words]
        
        sentiment = 0
        for t in tokens:
            sentiment += self.word_sentiment[t]
        return sentiment/len(tokens)
        
        
        
        
        
        
            