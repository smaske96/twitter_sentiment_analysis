import pandas as pd

d = pd.read_csv('STS_Tweets.txt',encoding='cp1252')
s = d[d['sentiment']==0].head(10000)[['sentiment','tweet']]
s1 = d[d['sentiment']==4].head(10000)[['sentiment','tweet']]


def correct(sent):
    return -1 if sent == 0 else 1
    


t = s.append(s1)
t['sentiment'] = t['sentiment'].apply(correct)
t.to_csv('sample_sts.txt',index=False)