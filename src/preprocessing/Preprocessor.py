# Preprocessor class with a public .process() function to pre-process a list of Tweet instances
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import random

random.seed(42)
nltk.download('stopwords')
nltk.download('sentiwordnet')


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
    Preprocessing of ngrams enabled by default
    WARNING: This mutates the Tweet instances (Tweet.text property, in case of ngrams Tweet.n_grams)
    """
    def process(self, tweets, ngrams=True):
        self.__reset()
        self.__createMeta(tweets)
        self.__filterFrequent(tweets)
        if ngrams:
            self.__processNgrams(tweets)
            self.__filterFrequentNgrams(tweets)
        return tweets

    # Private functions
    """
    Stem/stopword removal from n-grams
    """
    def __processNgrams(self, tweets):
        n_grams_new = []
        tweetnum = 0
        for tweet in tweets:
            for ngram in tweet.n_grams:
                for seq in ngram:
                    newseq = []
                    for item in seq:
                        if not self.__isStopgram(item):
                            stemmed = self.__stemAll(item)
                            if len(stemmed) > 0:
                                newseq.append(stemmed)
                                joined = "".join(stemmed)
                                if joined in self.__meta:
                                    self.__meta[joined]['tweets'].add(tweetnum)
                                else:
                                    self.__meta[joined] = {"tweets": set([tweetnum])}
                    if len(newseq) > 0:
                        n_grams_new += newseq
                        break
            tweet.n_grams = n_grams_new
            n_grams_new = []
            tweetnum += 1

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
                    tweet.text = random.sample(tweet.text,1)

    """
    Filters frequent ngrams from tweets
    """
    def __filterFrequentNgrams(self, tweets):
        total = float(len(tweets))
        for tweet in tweets:
            tweet.n_grams = [ngram for ngram in tweet.n_grams if self.__isFrequent("".join(ngram), total)]

    """
    Removes stopwords if necessary and stems if necessary
    Puts word to meta object or adds tweet number to meta set of word
    """
    def __processWords(self, words, tweetnum):
        ret = []
        for word in words:
            if not self.__isStopword(word):
                stemmed = (self.__stem(word),word) # To preserve actual word before stemming, required for Sentiwordnet
                if stemmed in self.__meta:
                    self.__meta[stemmed[0]]['tweets'].add(tweetnum)
                else:
                    self.__meta[stemmed[0]] = {"tweets": set([tweetnum])}
                ret.append(stemmed)
        return ret

    # Whether a word is a stopword
    def __isStopword(self, word):
        if self.__stopwords is None:
            return False
        else:
            return word in self.__stopwords

    # Whether a list of words is stopwords-only
    def __isStopgram(self, words):
        if self.__stopwords is None:
            return False
        else:
            for word in words:
                if not self.__isStopword(word):
                    return False
            return True

    # Whether a word is frequent (number of tweets containing the word >= treshold)
    def __isFrequent(self, word, total):
        if word in self.__meta:
            if "isFrequent" not in self.__meta[word]:
                isfrequent = len(self.__meta[word]['tweets'])/total >= self.__treshold
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

    # Run stemmer on a list of words if necessary
    # Returns a new stemmed list
    def __stemAll(self, words):
        if self.__stemmer is None:
            return words
        ret = []
        for word in words:
            ret.append(self.__stem(word))
        return ret
