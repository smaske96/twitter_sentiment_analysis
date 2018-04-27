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
        
        del p
        
        #Remove blank tweets
        tweets = [t for t in tweets if len(t.text) > 0]
        
        #Change n-grams to string
        for i in range(len(tweets)):
            tweets[i].n_grams = [" ".join(x) for x in tweets[i].n_grams]
        
        self.__word_list = set()
        actual_word = dict()
        for tw in tweets:
            self.__word_list = self.__word_list.union(list(map(lambda a: a[0], tw.text)) + tw.n_grams) 
            for w in tw.text:
                actual_word[w[0]] = w[1]
                
        print('tweet-size = ', len(tweets))
        print('word-size = ',len(self.__word_list))
        
        
        self.__word_list = list(self.__word_list)
        print('Sample words: ', self.__word_list[:5])
        
        term_count = defaultdict(lambda: defaultdict(lambda: 0))
        for i,tw in enumerate(tweets):
            for w in list(map(lambda a: a[0], tw.text)) + tw.n_grams: #:
                term_count[i][w] += 1
        
        self.__tweet_count = len(tweets)
        
        self.actual_words = []
        for w in self.__word_list:
            if w in actual_word: 
                self.actual_words.append(actual_word[w])
            
        
        tf = []
        for i in range(self.__tweet_count):
            tmp = []
            for w in self.__word_list:
                tmp.append(term_count[i][w])
            del term_count[i]
            tf.append(tmp)
    
        self.__term_freq = tf
        
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