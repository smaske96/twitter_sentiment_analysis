from src.TSA_Train import TSA_Train
from src.TwitterCorpus import TwitterCorpus
import timeit, random


start = timeit.default_timer()
print('Creating corpus...')
corpus = TwitterCorpus('dataset/sample_sts.txt',threshold=8, stem=True)
stop = timeit.default_timer()
print("Corpus created in ", round(stop - start,2), "seconds")

start = timeit.default_timer()
model = TSA_Train(corpus)
print('Model Created. Optimizing model...')
result = model.optimize()
if result:
    print('Percent of zero slacks = ', round(model.accuracy()*100,2))
    model.saveOutput()
else:
    print("Optimization failed!")
    exit(1)
stop = timeit.default_timer()
print("Model optimization ended in ", round(stop - start,2), "seconds")

