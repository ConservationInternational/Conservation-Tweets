# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:35:26 2016

@author: mcooper
"""

import boto3
import pickle
from collections import defaultdict
import sys

if sys.platform == 'win32':
    f = open('D:/Documents and Settings/mcooper/.aws/credentials')
    read = f.readlines()
    access_key = read[1][20:-1]
    secret_key = read[2][24:-1]
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
elif sys.platform == 'linux2':
    s3 = boto3.client('s3')


paginator = s3.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='baseline/en')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])


masterdict = defaultdict(int)
for f in files:
    print('now on file ' + f)
    out = s3.get_object(Bucket='ci-tweets', Key=f)
    file = out['Body'].read()
    lines = file.decode('utf-8').split('\n')
    for l in lines[1:]:
        words = l.split()
        for w in words:
            if w=='rt':
                pass
            elif w[:4]=='http':
                masterdict['http'] += 1
            else:
                masterdict[w] += 1
        masterdict['TOTAL'] += 1

masterdict = dict(masterdict)
total = float(masterdict['TOTAL'])
for i in masterdict:
    masterdict[i] = float(masterdict[i])/float(total)

pickle.dump(masterdict, open("baseline_2016-12-19.p", "wb"), protocol=2)