import pandas as pd
import os
from collections import defaultdict
import re

os.chdir('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')

df = pd.read_csv('Climate_trainingdata.csv')

classes = df['class'].unique()

dicts = []
for c in classes:
    lines = df.loc[df['class'] == c, 'text']
    masterdict = defaultdict(int)
    for l in lines:
        l = re.sub(r'[^a-z#@ ]', '', l.lower())
        words = l.split()
        for w in set(words):
            if w=='rt':
                pass
            elif w[:4]=='http':
                masterdict['http'] += 1
            else:
                masterdict[w] += 1
        masterdict['TOTAL'] += 1
    dicts.append(masterdict)
    
df = pd.DataFrame(dicts).T
df.columns = classes

file = 'ambiguous.csv'


df = df.fillna(1)

#df = df.dropna()

df = df.drop('TOTAL')




tweet = 'test'

wds = tweet.lower().split(' ')

totals = df.sum()

probs = totals/totals.sum()

words = df.loc[wds, ]

f = (df.loc[wds, ].dropna()/totals).product()

likelihood = f*probs

likelihood/likelihood.sum()

    