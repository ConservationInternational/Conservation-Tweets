keys = ['climate.change', 'global.warming', 'climatechange', 'globalwarming']
target = 3000

import boto3
import pandas as pd
import random
import csv

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')

files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

sel_files = []        
for f in files[1:]:
    for k in keys:
        if k in f:
            sel_files.append(f)

pd.set_option('max_colwidth', 4000)

accum = ['text']
while len(accum) < target:
    f = random.sample(sel_files, 1)[0]
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    accum.append(df.sample(1).to_string(columns=['text'], header=False, index=False))
    print(len(accum))
    
string = '\n'.join(accum)
s3resource.Bucket('ci-tweets-sentiment').put_object(Key='Climate_trainingdata.csv',  Body=string)


