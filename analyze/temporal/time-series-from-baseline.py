# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:51:25 2017

@author: mcooper
"""

import boto3

#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

#Get all files
paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='baseline-text', Prefix='')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

keys= []
f = open('D:\Documents and Settings\mcooper\GitHub\Conservation-Tweets\keywords.txt', 'r')
for k in f.readlines():
    keys.append(k.strip('\n'))
f.close()

for k in keys:
    print(k)
    t = open('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/temporal/' + k + '.csv', 'a')
    for f in files:
        print(f)
        if f[:2]=='en':
            out = s3client.get_object(Bucket='baseline-text', Key=f)
            lines = out['Body'].read().decode('utf-8').replace('\r', '').split('\n')
            count = 0        
            for l in lines:
                if k in l:
                    count += 0
            t.write(f[2:-4] + ',' + str(count) + ',' + str(len(lines)) + ',' + str(count/len(lines)) + '\n')
    t.close()
    
    
                