# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:25:55 2017

@author: mcooper
"""

import os
import pickle
import pandas as pd

os.chdir('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')


believes = pickle.load(open('believes_wc.p', 'rb'))
ambiguous = pickle.load(open('ambiguous_wc.p', 'rb'))
disbelieves = pickle.load(open('disbelieves_wc.p', 'rb'))

df = pd.DataFrame([believes, ambiguous, disbelieves]).T
df.columns = ['believes', 'ambiguous', 'disbelieves']


df = df.fillna(1)

#df = df.dropna()

df = df.drop('TOTAL')




tweet = 'al gore'

wds = tweet.lower().split(' ')

totals = df.sum()

probs = totals/totals.sum()

words = df.loc[wds, ]

f = (df.loc[wds, ].dropna()/totals).product()

likelihood = f*probs

likelihood/likelihood.sum()

    