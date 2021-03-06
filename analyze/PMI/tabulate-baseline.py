# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:35:26 2016

@author: mcooper
"""

import boto3
import pickle
from collections import defaultdict
import sys
import re
import datetime
import random

lang = 'en'

if sys.platform == 'win32':
    f = open('D:/Documents and Settings/mcooper/.aws/credentials')
    read = f.readlines()
    access_key = read[1][20:-1]
    secret_key = read[2][24:-1]
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    stopwords = []
    f = open('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/stopwords.txt')
    for i in f.readlines():
        stopwords.append(i.rstrip('\n'))
    
elif sys.platform == 'linux2':
    s3 = boto3.client('s3')
    
    stopwords = []    
    f = open('stopwords.txt')
    for i in f.readlines():
        stopwords.append(i.rstrip('\n'))


paginator = s3.get_paginator('list_objects')
pages = paginator.paginate(Bucket='baseline-text', Prefix=lang)
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])


masterdict = defaultdict(int)

if len(files) > 400:
	files = random.sample(files, 400)

for f in files:
    print(str(float((files.index(f) + 1))/ float(len(files))*100)[:5] + '% now on file ' + f)
    out = s3.get_object(Bucket='baseline-text', Key=f)
    file = out['Body'].read()
    lines = file.decode('utf-8').split('\n')
    for l in lines[1:]:
        l = re.sub(r'[^a-z#@ ]', '', l.lower())
        words = l.split()
        for w in set(words):
            if w=='rt' or w in stopwords:
                pass
            elif w[:4]=='http':
                masterdict['http'] += 1
            else:
                masterdict[w] += 1
        masterdict['TOTAL'] += 1

pickle.dump(masterdict, open("baseline_" + str(datetime.datetime.now())[:10] + "_" + lang + "raw.p", "wb"), protocol=2)

masterdict = dict(masterdict)
total = float(masterdict['TOTAL'])
for i in masterdict:
    masterdict[i] = float(masterdict[i])/float(total)

pickle.dump(masterdict, open("baseline_" + str(datetime.datetime.now())[:10] + "_" + lang + "prob.p", "wb"), protocol=2)