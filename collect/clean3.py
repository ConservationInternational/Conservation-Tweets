#rename colnames

#Run on 1-12-2017

import boto3
import pandas
import csv

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])   

for f in files[1:]:
    if f[-14:-4]=='2017-01-10':
        print(f)
        out = s3client.get_object(Bucket='ci-tweets', Key=f)
        df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)

        df = df.rename(columns={'user.location.country': 'country', 'user.location.state': 'state', 'user.location.county': 'county', 'user.location.city': 'city', 'user.location.latitude': 'latitude', 'user.location.longitude': 'longitude'})
        				
        s3resource.Bucket('ci-tweets').put_object(Key=f.replace('ByKeyword', 'Test'),  Body=df.to_csv(None, encoding='utf-8', index=False))