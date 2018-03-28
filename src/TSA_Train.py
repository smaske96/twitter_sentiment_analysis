import numpy as np
from scipy.optimize import linprog
from TwitterCorpus import TwitterCorpus

class TSA_Train:
    def __init__(self, corpus, **kwargs):
        self.threshold = kwargs['threshold'] if 'threshold' in kwargs else 1e-3        
        self.tweet_count = corpus.getTweetCount()
        self.word_list = corpus.getWords()
        self.term_freq = corpus.getTF()
        self.results = corpus.getResult()
        
        
    def optimize(self):
        N = self.tweet_count
        X = np.matrix(self.term_freq)
        S = np.eye(N)
        y = self.results
        
        A = np.concatenate((X,S),axis=1)
        A = np.matrix([-y[i]* A[i].A1 for i in range(N)])      #Convert all constraint to 'less than' bound
        b = [-y[i] * self.threshold for i in range(N)]         #Right hand side of constraint
        
        F = np.concatenate((np.zeros(X.shape[1]), np.ones(N)))      #Objective function that contains S variables only
        bound = [(-1,1)] * X.shape[1] + [(0,None)] * len(S[0])      #Bound for each x_i is [-1,1] and s_i is [0, inf)
        
        output = linprog(F, A_ub=A, b_ub=b, bounds = bound,  options={"disp": True})
        self.term_sentiment = output.x[:X.shape[1]]
        self.slacks = output.x[X.shape[1]:]
        
    def saveOutput(self,**kwargs):
        fname = kwargs['filename'] if 'filename' in kwargs else 'output.json'
        with open(fname,'w') as fp:
            fp.write(str(dict(zip(self.word_list, self.term_sentiment))))
            
    def accuracy(self):
        #Based on fraction of non-zero slacks
        return np.count_nonzero(self.slacks==0)/len(self.slacks)
        
        
            
        
        
        