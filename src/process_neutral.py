import pandas as pd
from src.TSA_Test import TSA_Test
from nltk import PorterStemmer
from collections import defaultdict

import matplotlib.pyplot as plt

print('Running the model on training set...')
df = pd.read_csv('dataset/STS_Tweets.txt',sep=',',encoding='cp1252')
neg = df[df['sentiment']==0].head(10000)[['sentiment','tweet']]
#neu = df[df['sentiment']==2].head(10000)[['sentiment','tweet']]
pos = df[df['sentiment']==4].head(10000)[['sentiment','tweet']]

test = TSA_Test('out\output.json', stemmer=PorterStemmer())  
df = pd.concat([neg, pos])

sentiment = defaultdict(lambda: [])
for index, row in df.iterrows():
    sentiment[row['sentiment']].append(test.getSentiment(row['tweet']))
    
d = [sentiment[i] for i in sentiment]
bplot = plt.boxplot(d,showfliers=False)
#print(len(bplot['fliers'][0].get_ydata()))
#print(len(bplot['fliers'][1].get_ydata()))

print('Mean -ve: ', sum(d[0])/len(d[0]))
print('Mean +ve: ', sum(d[1])/len(d[1]))
plt.show()    
    