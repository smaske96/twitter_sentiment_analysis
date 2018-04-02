# Preprocessor class with a public .process() function to pre-process a list of Tweet instances
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')


class Preprocessor:
    """
    Constructor with settings:
        treshold<number>: we only consider words that appear in at least treshold tweets, defaults to 2%
        stem<boolean>: whether we use stemming, defaults to False
        stopwords<boolean>: whether we remove stopwords, defaults to True
    """
    def __init__(self, treshold=0.02, stem=False, removestopwords=True):
        self.__treshold = treshold
        self.__stemmer = None if not stem else PorterStemmer
        self.__stopwords = None if not removestopwords else stopwords.words("english")
        self.__meta = {}
        self.__stemwords = {}

    """
    Takes a list of Tweet and returns a processed list of Tweet
    WARNING: This mutates the Tweet instances
    """
    def process(self, tweets):
        self.__reset()
        self.__createMeta(tweets)
        self.__filterFrequent(tweets)
        return tweets

    # Private functions
    """
    Build meta object from a list of Tweet
    In this step, stopwords are removed and other words stemmed and meta object with following signature is created:
    self.__meta = {
        [word]: { 
            tweets: set of tweet indexes where the word appears,
            isFrequent: True/False,
            ...other properties for each word can be added later...
        }
    }
    """
    def __createMeta(self, tweets):
        idx = 0
        for tweet in tweets:
            tweet.text = self.__processWords(tweet.text, idx)
            idx += 1

    """
    Resets meta and stopwordCache. Useful when we want to call process on different sets of tweets.
    """
    def __reset(self):
        self.__meta = {}
        self.__stemwords = {}

    """
    Filters frequent words from tweets
    """
    def __filterFrequent(self, tweets):
        total = float(len(tweets))
        for tweet in tweets:
            frequent = [word for word in tweet.text if self.__isFrequent(word, total)]
            if len(frequent) > 0:
                tweet.text = frequent
            else:
                # randomly pick one word
                if len(tweet.text) > 0:
                    tweet.text = [tweet.text[0]]

    """
    Removes stopwords if necessary and stems if necessary
    Puts word to meta object or adds tweet number to meta set of word
    """
    def __processWords(self, words, tweetnum):
        ret = []
        for word in words:
            if not self.__isStopword(word):
                stemmed = self.__stem(word)
                if stemmed in self.__meta:
                    self.__meta[stemmed]['tweets'].add(tweetnum)
                else:
                    self.__meta[stemmed] = {"tweets": set([tweetnum])}
                ret.append(stemmed)
        return ret

    # Whether a word is a stopword
    def __isStopword(self, word):
        if self.__stopwords is None:
            return False
        else:
            return word in self.__stopwords

    # Whether a word is frequent (number of tweets containing the word >= treshold)
    def __isFrequent(self, word, total):
        if word in self.__meta:
            if "isFrequent" not in self.__meta[word]:
                isfrequent = len(self.__meta[word])/total >= self.__treshold
                self.__meta[word]["isFrequent"] = isfrequent
            return self.__meta[word]["isFrequent"]
        else:
            return False

    # Run stemmer on a word if necessary
    def __stem(self, word):
        if self.__stemmer is None:
            return word
        if word in self.__stemwords:
            return self.__stemwords[word]
        else:
            w = self.__stemmer().stem(word)
            self.__stemwords[word] = w
            return w