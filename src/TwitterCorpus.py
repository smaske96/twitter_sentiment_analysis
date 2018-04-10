# This is a dummy corpus to test TSA_Train.
# This should be modified to load a Twitter Corpus
#
# Sample:
# T1: A B C +ve
# T2: B C D -ve
# T3: A C D -ve
# T4: C C D +ve
#
import pandas as pd
from src.tweet import Tweet
from src.preprocessing import Preprocessor
from collections import defaultdict
class TwitterCorpus:
    def __init__(self, file, stem=False, **kwargs):
        df = pd.read_csv(file)
        tweets = []
        for index, row in df.iterrows():
            tweets.append(Tweet(row['tweet']))
            
        p = Preprocessor(stem=stem) if 'threshold' not in kwargs else Preprocessor(stem=stem,treshold=kwargs['threshold']/len(tweets))
        p.process(tweets)
        
        #Remove blank tweets
        tweets = [t for t in tweets if len(t.text) > 0]
        
        
        self.__word_list = set()
        for tw in tweets:
            self.__word_list = self.__word_list.union(tw.text)
        print('tweet-size = ', len(tweets))
        print('word-size = ',len(self.__word_list))
        self.__word_list = list(self.__word_list)
        term_count = defaultdict(lambda: defaultdict(lambda: 0))
        for i,tw in enumerate(tweets):
            for w in tw.text:
                term_count[i][w] += 1
                
        tf = []
        for i in range(len(tweets)):
            tmp = []
            for w in self.__word_list:
                tmp.append(term_count[i][w])
            tf.append(tmp)
    
        self.__term_freq = tf
        self.__tweet_count = len(tweets)
        self.__results = list(df['sentiment']) # Sentiment 1 if positive, -1 if negative
    
    # Returns total number of tweets in the corpus
    def getTweetCount(self): 
        return self.__tweet_count
        
    # Returns the word list on which term frequency is based
    def getWords(self):
        return self.__word_list
        
    # Returns a 2D list of integers as term frequency of words in word list for each tweet
    def getTF(self):
        return self.__term_freq
        
    # Returns the array of sentiment of each tweet. It should correspond to the term freq list.
    def getResult(self):
        return self.__results