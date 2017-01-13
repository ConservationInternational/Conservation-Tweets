#Separate out geographic tweets
#Keep only columns id_str, geo, country, state, county, city, latitude, longitude
#Split coords into exact.latitude & exact.longitude
#maybe also a any.latitude and any.longitude file
#group by keyword and write

#Run on 1-12-2017

import boto3
import pandas
import csv
import ast

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])
        
keys = []
for f in files[1:]:
    new = f[10:-15]
    if new not in keys:
        keys.append(new)
        
def getLat(string):
    if string == 'None':
        return('None')
    else:
        try:
            string = string.replace('  ', ', ')
            d = ast.literal_eval(string)
            return(d['coordinates'][0])
        except:
            return('None')
    
def getLon(string):
    if string == 'None':
        return('None')
    else:
        try:
            string = string.replace('  ', ', ')
            d = ast.literal_eval(string)
            return(d['coordinates'][1])
        except:
            return('None')
    
for k in keys:
    df = pandas.DataFrame()
    for f in files[1:]:
        if k in f:
            print(f)
            out = s3client.get_object(Bucket='ci-tweets', Key=f)
            dfsub = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)

            df = pandas.concat([df, dfsub.loc[(dfsub['latitude'].notnull()) | (dfsub['geo']!='None'),['id_str', 'created_at', 'geo', 'country', 'state', 'city', 'latitude', 'longitude']]])
    
    df = df.assign(gps_latitude='')
    df = df.assign(gps_longitude='')
        
    df['gps_latitude'] = df['geo'].apply(getLat)
    df['gps_longitude'] = df['geo'].apply(getLon) 
    
    dfgps = df.loc[df['gps_longitude']!='None',['id_str', 'created_at', 'gps_longitude', 'gps_latitude']]

    s3resource.Bucket('tweets-place').put_object(Key=(k + '.csv'),  Body=df.to_csv(None, encoding='utf-8', index=False))
    s3resource.Bucket('tweets-geo').put_object(Key=(k + '.csv'),  Body=dfgps.to_csv(None, encoding='utf-8', index=False))