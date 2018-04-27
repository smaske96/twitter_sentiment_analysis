import pandas as pd
from src.TSA_Test import TSA_Test
from nltk import PorterStemmer
import numpy as np

print('Evaluating model using SemEval Subtask A...')
df = pd.read_csv('dataset/SemEval 2017 - Subtask_A/twitter-2016test-A.txt',sep='\t',encoding='cp1252')
#df = df[df['sentiment'] != 'neutral']
    
test = TSA_Test('out\output.json', stemmer=PorterStemmer()) 
t1 = -3.167e-5
t2 = 2.390e-5   
cnf_matrix = np.zeros((3,3))
for index, row in df.iterrows():
    s = test.getSentiment(row['tweet'])
    if row['sentiment'] == 'positive': c = 0
    elif row['sentiment'] == 'neutral': c = 1
    else: c = 2
    
    if s > t2: r = 0
    elif s >= t1 and s <= t2: r = 1
    else: r = 2 
    
    cnf_matrix[r][c] += 1

sum_r = cnf_matrix.sum(axis=0)
sum_c = cnf_matrix.sum(axis=1)

print(cnf_matrix)

pie_p = cnf_matrix[0][0] / sum_r[0]
sig_p = cnf_matrix[0][0] / sum_c[0]
F_p = 2 * pie_p * sig_p / (pie_p + sig_p)

pie_n = cnf_matrix[2][2] / sum_r[2]
sig_n = cnf_matrix[2][2] / sum_c[2]
F_n = 2 * pie_n * sig_n / (pie_n + sig_n)

F_pn = 0.5 * (F_p + F_n)
sig_pn = 0.5 * (sig_p + sig_n)


print('F1-score F1_pn = ', round(F_pn,3)) 
print('Macroaveraged recall (sigma_PN) = ', round(sig_pn,3))


print('\nEvaluating model using SemEval Subtask B...')
df = pd.read_csv('dataset/Subtasks_BD/twitter-2016test-BD.txt',sep='\t',encoding='cp1252')


cnf_matrix = np.zeros((2,2))
for index, row in df.iterrows():
    s = test.getSentiment(row['tweet'])
    
    if row['sentiment'] == 'positive': c = 0
    else: c = 1
    
    if s > 0: r = 0
    else: r = 1
    
    cnf_matrix[r][c] += 1

sum_r = cnf_matrix.sum(axis=0)
sum_c = cnf_matrix.sum(axis=1)

print(cnf_matrix)

pre = cnf_matrix[0][0]/sum_r[0]
rec = cnf_matrix[0][0]/sum_c[0]
acc = (cnf_matrix[0][0] + cnf_matrix[1][1])/sum(sum_r)
fsc = 2 * pre * rec /(pre + rec)

sig_p = cnf_matrix[0][0]/sum_c[0]
sig_n = cnf_matrix[1][1]/sum_c[1]
sig_pn = 0.5 * (sig_p + sig_n)

print('Accuracy = ', round(acc,3))
print('F-Score = ', round(fsc,3))
print('Sig_pn = ', round(sig_pn,3))
