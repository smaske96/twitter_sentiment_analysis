import json
from collections import defaultdict
from src.tweet import Tweet
from nltk.corpus import stopwords
import random

random.seed(42)

class TSA_Test:
    
    def __init__(self, output_file, **kwargs):
        self.word_sentiment = defaultdict(lambda: 0, json.load(open(output_file)))
        self.stemmer = kwargs['stemmer'] if 'stemmer' in kwargs else None
        self.ngrams = kwargs['ngrams'] if 'ngrams' in kwargs else True
        
    def getSentiment(self, tweet):
        tw = Tweet(tweet)
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tw.text + tw.emoji if not w in stop_words]
        if self.stemmer:
            tokens = [ self.stemmer.stem(w) for w in tokens ]
            
        if self.ngrams: tokens += [" ".join(z) for y in tw.n_grams for z in y[random.randrange(len(y))]]
        
        
        sentiment = 0
        if len(tokens) == 0: return sentiment
        for t in tokens:
            sentiment += self.word_sentiment[t]
        return sentiment/len(tokens)
        
        
        
        
        
        
            