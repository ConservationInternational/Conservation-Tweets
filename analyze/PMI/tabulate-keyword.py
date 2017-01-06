# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:19:22 2016

@author: mcooper
"""

#Paramaters to set
searchkey = 'climate.change'
searchstart = '2016-09-06'
searchend = '2016-11-07'
saveas = 'climatechange-pre'

import boto3
import pickle
from collections import defaultdict
import datetime
import sys
import pandas
import re

def generatefiles(keyword, start='2016-09-06', end=99):
    if end==99:
        end = str(datetime.datetime.now() - datetime.timedelta(1))[:10]
    
    sy = int(start[:4])
    sm = int(start[5:7])
    sd = int(start[8:10])
    
    ey = int(end[:4])
    em = int(end[5:7])
    ed = int(end[8:10])
    
    result = []    
    accum = datetime.datetime(sy, sm, sd)
    stop = datetime.datetime(ey, em, ed)
    
    while accum <= stop:
        result.append('ByKeyword/' + keyword + '-' + accum.strftime('%Y-%m-%d') + '.csv')
        accum += datetime.timedelta(1)
    
    if 'ByKeyword/' + keyword + '-2016-11-04.csv' in result:
        result.remove('ByKeyword/' + keyword + '-2016-11-04.csv')   
    
    return result

files = generatefiles(searchkey, searchstart, searchend)

#Locally connect to s3 and read stopwords
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
    f = open('~/stopwords.txt')
    for i in f.readlines():
        stopwords.append(i.rstrip('\n'))

conditionaldict = defaultdict(int)
for f in files:
    print('now on file ' + f)
    try:
        out = s3.get_object(Bucket='ci-tweets', Key=f)
        file = pandas.read_csv(out['Body'])
        lines = file["text"].tolist()
        for l in lines:
            l = re.sub(r'[^a-z#@ ]', '', l.lower())
            words = l.split()
            for w in set(words):
                if w=='rt' or w in stopwords:
                    pass
                elif w[:4]=='http':
                    conditionaldict['http'] += 1
                else:
                    conditionaldict[w] += 1
            conditionaldict['TOTAL'] += 1
    except:
        print('File ' + f + ' was skipped')


pickle.dump(conditionaldict, open(saveas + ".p", "wb"), protocol=2)