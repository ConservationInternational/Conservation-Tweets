from __future__ import division
import pandas as pd
import boto3
import csv
import numpy as np

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

dates = []
sel_files = []
for f in files:
    if f[10:-15] in ['global.warming', 'globalwarming', 'climate.change', 'climatechange']:
        sel_files.append(f)
    if f[-14:-4] not in dates:
        dates.append(f[-14:-4])

exec(open('classifier.py', 'rb').read())
c = Classifier(pd.read_csv('Climate_trainingdata_classified.csv'), tokens=1)

for d in dates[1:]:
    
    print(d)
    
    date_files = []
    for f in sel_files:
        if d in f:
            date_files.append(f)
    
    df = pd.DataFrame()
    for f in date_files:
        out = s3client.get_object(Bucket='ci-tweets', Key=f)
        temp = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
        
        temp['keyword'] = f[10:-15]
        
        df = df.append(temp, ignore_index = True)
        
    df = df[pd.notnull(df['text'])]
    
    print('Classifying')
    
    df[c.classes] = df['text'].apply(c.classify)
    df['max'] = df[c.classes].idxmax(axis=1)
    
    s3resource.Bucket('ci-tweets-sentiment').put_object(Key='climate/climate' + d + '.csv', Body=df.to_csv(None, encoding='utf-8', index=False))