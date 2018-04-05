from src.tweet import Tweet
from src.preprocessing import Preprocessor
import pandas as pd

df = pd.read_csv('dataset/sample_sts.txt')
tweets = []
for index, row in df.iterrows():
    tweets.append(Tweet(row['tweet']))

p = Preprocessor(treshold=2/len(tweets))

p.process(tweets)

with open('dataset/processed_sample_sts.txt','w') as fp:
    for tweet in tweets:
        fp.write(str(tweet.text)+'\n')