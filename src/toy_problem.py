'''
T1: A B C +ve
T2: B C D -ve
T3: A C D -ve
T4: C C D +ve
Minimize s0 + s1 + s2 + s3 
subject to
x0 + x1 + x2 + s0 > 0       => -1 * (x0 + x1 + x2 + s0) < 0
x1 + x2 + x3 + s1 < 0
x0 + x2 + x3 + s2 < 0
2*x2 + x3 + s3 > 0          => -1 * (2*x2 + x3 + s3) < 0
'''

import numpy as np
from scipy.optimize import linprog
N = 4 #Number of tweets
X = np.matrix([[1,1,1,0],[0,1,1,1],[1,0,1,1],[0,0,2,1]]) #Term frequency
S = np.eye(N)
result = [1, -1, -1, 1] # Sentiment 1 if positive, -1 if negative


A = np.concatenate((X,S),axis=1)
A = [-result[i]* A[i].A1 for i in range(N)]
b = [0] * N

F = np.concatenate((np.zeros(X.shape[1]), np.ones(N)))

bound = [(-5,5)] * len(A[0])
res = linprog(F, A_ub=A, b_ub=b, bounds = bound,  options={"disp": True})
print(res.x[:X.shape[1]])