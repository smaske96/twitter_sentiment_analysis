import numpy as np
from scipy.optimize import linprog
from src.TwitterCorpus import TwitterCorpus
import json

class TSA_Train:
    def __init__(self, corpus, **kwargs):
        self.threshold = kwargs['threshold'] if 'threshold' in kwargs else 1e-3
        self.tweet_count = corpus.getTweetCount()
        self.word_list = corpus.getWords()
        self.term_freq = corpus.getTF()
        self.results = corpus.getResult()
        
    def __dump_vars(self,fnames,*args):
        for i in range(len(args)):
            if fnames[i] == 'A':
                with open('out/' + fnames[i] +'.txt','w') as fp:
                    for t in args[i]:
                        fp.write(" ".join(map(str,t)) + '\n')
            else:
                np.savetxt('out/' + fnames[i] +'.txt', args[i],fmt='%5.8g')
    
    
    def optimize(self):
        N = self.tweet_count
        #X = self.term_freq
        #S = -1*np.eye(N)
        y = self.results
        #print(self.word_list)
        #print(X)
        
        A = [[-y[i]* x for x in self.term_freq[i]] for i in range(N)]  
        W = len(A[0])
        #A = np.concatenate((A,S),axis=1)
        
        #print(A)
        #Convert all constraint to 'less than' bound
        b = [-self.threshold for i in range(N)]        
        #print(b)
        #Right hand side of constraint
        
        F = np.concatenate((np.zeros(W), np.ones(N)))      #Objective function that contains S variables only
        #bound = [(None,None)] * X.shape[1] + [(0,None)] * len(S[0])      #Bound for each x_i is [-1,1] and s_i is [0, inf)
        
        self.__dump_vars(['F','A','b'],F,A,b)
        
        solver = input("Use MATLAB solver. Success? (y/n) : ")
        #output = linprog(F, A_ub=A, b_ub=b, bounds = bound,   options=dict(disp=True, maxiter=float("inf")))
        if solver == 'y':
            with open('out/x.txt','r') as fp:
                x = list(map(float,fp.readlines()))
            self.term_sentiment = x[:W]
            self.slacks = np.array(x[W:])
            return True
        else:
            return False
        
    def saveOutput(self,**kwargs):
        fname = kwargs['filename'] if 'filename' in kwargs else 'out\output.json'
        with open(fname,'w') as fp:
            json.dump(dict(zip(self.word_list, self.term_sentiment)), fp)
            
    def accuracy(self):
        #Based on fraction of non-zero slacks
        return np.count_nonzero(self.slacks==0)/len(self.slacks)
        
        
        
        
        