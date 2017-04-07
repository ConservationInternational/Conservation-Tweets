# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 10:31:49 2017

@author: mcooper
"""

import os
import pandas as pd
import numpy as np
import classifier

os.chdir('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis')

df = pd.read_csv('Climate_trainingdata.csv')

df['sel'] = np.random.choice([1,2], df.shape[0], p=[0.8, 0.2])


training = df.loc[df['sel']==1]

test = df.loc[df['sel']==2]

c = Classifier(training, tokens=1)

test[c.classes] = test['text'].apply(c.classify)

test['max'] = test[c.classes].idxmax(axis=1)

test = test.dropna()

ct = pd.crosstab(test['class'], test['max'])

def kappa(ct):
    N = ct.sum().sum()
    p0 = np.diag(ct).sum()/N
    pE = (1/N**2)*(ct.sum(axis=1)*ct.sum(axis=0)).sum()
    k = (p0 - pE)/(1 - pE)
    return(k)
    
kappa(ct)