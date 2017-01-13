#rename colnames

#Run on 1-12-2017

import boto3
import pandas
import csv

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='baseline')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])   

for f in files[1:]:
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    			
    s3resource.Bucket('baseline-text').put_object(Key=f,  Body=df.to_csv(None, encoding='utf-8', index=False))