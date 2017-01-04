file = 'ambiguous.csv'

import pickle
from collections import defaultdict
import os
import re

os.chdir('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')

masterdict = defaultdict(int)
f = open(file, 'r', encoding='utf8')

for l in f.readlines():
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

pickle.dump(masterdict, open("ambiguous_wc.p", "wb"), protocol=2)

f = open("ambiguous_wc.csv", "w")
for i in masterdict:
    f.write(i + ',' + str(masterdict[i]) + '\n')
