import pandas as pd
from src.TSA_Test import TSA_Test
from nltk import PorterStemmer

print('Evaluating model...')
df = pd.read_csv('dataset/SemEval 2017 - Subtask_A/twitter-2016train-A.txt',sep='\t')
df = df[df['sentiment'] != 'neutral']
    
test = TSA_Test('out\output.json', stemmer=PorterStemmer())    
tp, tn, fp, fn = 0, 0, 0, 0
for index, row in df.iterrows():
    s = test.getSentiment(row['tweet'])
    if s > 0 and row['sentiment'] == 'positive': tp += 1
    if s < 0 and row['sentiment'] == 'negative': tn += 1
    if s > 0 and row['sentiment'] == 'negative': fp += 1
    if s < 0 and row['sentiment'] == 'positive': fn += 1
    
pre = tp/(tp + fp)
rec = tp/(tp + fn)
acc = (tp + tn)/(tp + tn + fp + fn)
fsc = 2 * pre * rec /(pre + rec)
print('Precision = ', round(pre,2))
print('Recall = ', round(rec,2))
print('Accuracy = ', round(acc,2))
print('F-Score = ', round(fsc,2))
