import numpy as np
from scipy.optimize import linprog
from src.TwitterCorpus import TwitterCorpus
import json
from nltk.corpus import sentiwordnet as swn

"""
Class to construct a training model

Attributes:
    threshold: term threshold
    tweet_count: number of Tweets in the corpus
    word_list: list of terms in the corpus
    term_freq: list of term frequency in the corpus corresponding to the word_list
    results: List of sentiments (+1, -1) of each tweet in the corpus
"""

class TSA_Train:
    """
    Loads the parameters of the corpus
    """
    def __init__(self, corpus, **kwargs):
        self.threshold = kwargs['threshold'] if 'threshold' in kwargs else 1e-3
        self.tweet_count = corpus.getTweetCount()
        self.word_list = corpus.getWords()
        self.term_freq = corpus.getTF()
        self.results = corpus.getResult()
        self.actual_word = corpus.actual_words
    
    """
    Dump the variables A, b, F in out/
    """
    def __dump_vars(self,fnames,*args):
        for i in range(len(args)):
            if fnames[i] == 'A':
                with open('out/' + fnames[i] +'.txt','w') as fp:
                    for t in args[i]:
                        fp.write(" ".join(map(str,t)) + '\n')
            else:
                np.savetxt('out/' + fnames[i] +'.txt', args[i],fmt='%5.8g')
    
    """
    Creates the matrices required for Linear Progamming in MATLAB
    """
    def optimize(self):
        N = self.tweet_count
        #X = self.term_freq
        #S = -1*np.eye(N)
        y = self.results
        
        
        """
        Get sentiwordnet scores
        """
        swn_param = []
        for w in self.actual_word:
            if len(w.split()) > 1: 
                swn_param.append(0)
                continue
            swn_list = list(swn.senti_synsets(w))
            if len(swn_list) == 0 or (swn_list[0].pos_score() > 0 and swn_list[0].neg_score() > 0):
                swn_param.append(0)
                continue
                
            if swn_list[0].pos_score() > 0: 
                swn_param.append(1)
            elif swn_list[0].neg_score() > 0:
                swn_param.append(-1)
            else:
                swn_param.append(0)
        
        #Convert all constraint to 'less than' bound
        A = [[-y[i]* x for x in self.term_freq[i]] for i in range(N)]  
        W = len(A[0])
        
        #Right hand side of constraint
        b = [-self.threshold for i in range(N)]        
        
        
        
        F = np.concatenate((np.zeros(W), np.ones(N)))      #Objective function that contains S variables only
        
        self.__dump_vars(['F','A','b','s'],F,A,b,swn_param)
        
        solver = input("Execute out/solveLinProg.m; Success? (y/n) : ")
        #output = linprog(F, A_ub=A, b_ub=b, bounds = bound,   options=dict(disp=True, maxiter=float("inf")))
        """
        MATLAB will write the solution of the linear programming to out/x.txt
        """
        if solver == 'y':
            with open('out/x.txt','r') as fp:
                x = list(map(float,fp.readlines()))
            self.term_sentiment = x[:W]
            self.slacks = np.array(x[W:])
            return True
        else:
            return False
    """
    Saves the sentiment of each term cacluated by linear programming as a JSON file
    """
    def saveOutput(self,**kwargs):
        fname = kwargs['filename'] if 'filename' in kwargs else 'out\output.json'
        with open(fname,'w') as fp:
            json.dump(dict(zip(self.word_list, self.term_sentiment)), fp)
    
    """
    Calculates fraction of zero slacks
    """
    def accuracy(self):
        #Based on fraction of non-zero slacks
        return np.count_nonzero(self.slacks==0)/len(self.slacks)
        
        
        
        
        