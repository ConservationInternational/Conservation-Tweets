# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 17:10:39 2017

@author: mcooper
"""

from __future__ import division
import pandas
import math
import boto3
import pickle
import csv
import numpy as np

#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweet-wordcounts', Prefix='')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

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

en_baseline = dict(pickle.load(open("baseline_2017-04-05_enprob.p", "rb")))
in_baseline = dict(pickle.load(open("baseline_2017-04-04_idprob.p", "rb")))

lang = pandas.read_csv('lang.csv')
            
for f in files:
    print(f)
    out = s3client.get_object(Bucket='ci-tweet-wordcounts', Key=f)
    df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True, names=['word', 'count'])
    total = int(df.loc[df['word']=='TOTAL','count'])
    l = lang.loc[lang['file']==f, 'lang'].tolist()[0]
    if l == 'en':   
        df = df.loc[df['word'].isin(en_baseline),:]
    elif l == 'in':
        df = df.loc[df['word'].isin(in_baseline),:]
    df['PMI'] = np.nan
    for i in df.index:
        word = df.loc[i,'word']
        count = df.loc[i, 'count']
        if l == 'en':
            base = en_baseline[word]
        elif l == 'in':
            base = in_baseline[word]
        PMI = math.log((count/total)/base)
        df = df.set_value(i, 'PMI', PMI)
    print(f)
    s3resource.Bucket('ci-tweet-PMI').put_object(Key=f, Body=df.to_csv(None, encoding='utf-8', index=False))


