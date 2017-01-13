#clean weird quote issue and geotag files from before 11-04-2017
#geotag those files

#Run on 1-12-2017

import boto3
import pandas
import carmen
import csv
import datetime

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

resolver = carmen.get_resolver()
resolver.load_locations()

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

dates = []    
accum = datetime.datetime(2016, 9, 6)
stop = datetime.datetime(2016, 11, 5)

while accum <= stop:
    dates.append(accum.strftime('%Y-%m-%d'))
    accum += datetime.timedelta(1)

for f in files[1:]:
    if f[-14:-4] in dates:
        print(f)
        out = s3client.get_object(Bucket='ci-tweets', Key=f)
        df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)

        df = df.assign(country='')
        df = df.assign(state='')
        df = df.assign(county='')
        df = df.assign(city='')
        df = df.assign(latitude='')
        df = df.assign(longitude='')        
        
        
        #Remove weird string issues
        cleancols = []
        for i in df.columns:
            cleancols.append(i.replace('"', ''))
        
        df.columns = cleancols
        
        for c in df.columns:
            if df[c].dtype=='O':
                df[c] = df[c].str.replace('"', '')

        if 'user.location' in df.columns:
            for i in df.index:
                try:
                    tweet = {'place': None, 'user': {'location': df.loc[i]['user.location']}}
                    loc = resolver.resolve_tweet(tweet)
                    if loc is not None:
                        df = df.set_value(i, 'country', loc[1].country)
                        df = df.set_value(i, 'state', loc[1].state)
                        df = df.set_value(i, 'county', loc[1].county)
                        df = df.set_value(i, 'city', loc[1].city)
                        df = df.set_value(i, 'latitude', loc[1].latitude)
                        df = df.set_value(i, 'longitude', loc[1].longitude)
                except:
                    pass
        				
        s3resource.Bucket('ci-tweets').put_object(Key=f.replace('ByKeyword', 'Test'),  Body=df.to_csv(None, encoding='utf-8', index=False))