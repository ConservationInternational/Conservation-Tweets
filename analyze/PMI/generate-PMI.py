# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 17:10:39 2017

@author: mcooper
"""

from __future__ import division
import pandas
import math
import pickle
import csv
import numpy as np
import os

os.chdir('D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/Sentiment-Analysis/palm processing results/')
#skipfiles = []
#try:
#    pages = paginator.paginate(Bucket='ci-tweet-PMI', Prefix='')
#    for p in pages:
#        for x in p['Contents']:
#            skipfiles.append(x['Key'])
#except:
#    for object in s3resource.Bucket('ci-tweet-PMI').objects.all():
#        print(object)
#
#for f in skipfiles:
#    files.remove(f)


files = ['EngPosWCt.csv', 'EngNegWCt.csv', 'IndPosWCt.csv', 'IndNegWCt.csv']

en_baseline = dict(pickle.load(open("D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI/baseline_2017-04-05_enprob.p", "rb")))
in_baseline = dict(pickle.load(open("D://Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI/baseline_2017-04-04_idprob.p", "rb")))
            
for f in files:
    print(f)
    df = pandas.read_csv(f, quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True, names=['word', 'count'])
    if f[:3] == 'Eng':   
        df = df.loc[df['word'].isin(en_baseline),:]
        total = 265138
    elif f[:3] == 'Ind':
        df = df.loc[df['word'].isin(in_baseline),:]
        total = 84731
    df['PMI'] = np.nan
    for i in df.index:
        word = df.loc[i,'word']
        count = df.loc[i, 'count']
        if f[:3] == 'Eng':
            base = en_baseline[word]
        elif f[:3] == 'Ind':
            base = in_baseline[word]
        PMI = math.log((count/total)/base)
        df = df.set_value(i, 'PMI', PMI)
    print(f)
    df.to_csv('PMI_' + f, encoding='utf-8', index=False)


