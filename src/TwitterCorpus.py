# This is a dummy corpus to test TSA_Train.
# This should be modified to load a Twitter Corpus
#
# Sample:
# T1: A B C +ve
# T2: B C D -ve
# T3: A C D -ve
# T4: C C D +ve
#

class TwitterCorpus:
    def __init__(self):
        self.__term_freq = [[1,1,1,0],[0,1,1,1],[1,0,1,1],[0,0,2,1]]
        self.__word_list = ['A','B','C','D']
        self.__tweet_count = 4
        self.__results = [1, -1, -1, 1] # Sentiment 1 if positive, -1 if negative
    
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