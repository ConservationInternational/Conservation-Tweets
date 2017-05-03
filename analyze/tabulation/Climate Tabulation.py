import boto3
import pandas as pd
import csv
from collections import defaultdict

keywords = ["climate.change", "climatechange", "globalwarming", "global.warming"]
 
#Energy Words
energy = ['energy', 'renewable', 'clean', 'tech', 'transportation', 'industry', 'oil', 'gas', 'wind', 'solar', 'fossil', 'fuel', 
 'efficiency', 'geothermal', 'nuclear', 'cars', 'hydropower', 'air', 'frack', 'battery', 'burn', 'power', 'wind', 'solar', 'electri']
#Nature Words
nature = ['forest', 'ecosystem', 'land', 'food', 'ecosystems', 'vegtarian', 'vegan', 'ocean', 'mangrove', 'fish', 'coral', 'reefs', 'restoration',
          'reforestation', 'degradation', 'rehabilitation', 'adapt', 'mitigat', 'resilien', 'nature', 'water', 'livestock', 'sink', 'redd', 'extinct',
          'peat']

#Conflict Words
conflict = ['fight', 'isis', 'war', 'military', 'conflict', 'syria', 'army', 'navy', 'security', 'terror', 'poverty']

#Health Words
health = ['sick', 'death', 'disease', 'health', 'illness', 'pandemic', 'malaria', 'died', 'dying',  'die']

#Financial Words
finance = ['stock', 'market', 'finance', 'investment', 'fund', 'money']

#also get most used media
def mediaGrab(df, wc):
    bigstr = df['text'].to_string(index=False).split()
    #returns a tabulation of all tokens starting with 'http' within the 'text' column of a dataframe
    for i in bigstr:
        if i[:4] == 'http' and '...' not in i:
            wc[i] += 1
    return(wc)

#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
files = []

for k in keywords:
    pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword/' + k)
    for p in pages:
        for x in p['Contents']:
            files.append(x['Key'])

keys = nature + energy + conflict + health + finance + ['ENERGY', 'NATURE', 'CONFLICT', 'HEALTH', 'FINANCE']
values = ['sum']*len(keys)
agdict = dict(zip(keys, values))
agdict['RT'] = 'count'

wc = defaultdict(int)
accumdf = pd.DataFrame()
for f in files:
    print(f)
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    for w in nature + energy + conflict + health + finance:
        df[w] = df['text'].str.lower().str.contains(w)
    
    df['RT'] = df['text'].str.contains('^RT', regex=True)    
    
    df['ENERGY'] = df[energy].apply(func=any, axis=1)
    df['NATURE'] = df[nature].apply(func=any, axis=1)
    df['CONFLICT'] = df[conflict].apply(func=any, axis=1)
    df['HEALTH'] = df[health].apply(func=any, axis=1)
    df['FINANCE'] = df[finance].apply(func=any, axis=1)
    
    df['keyword'] = f[10:-15]
    df['date'] = f[-14:-4]
    
    dfnew = df.groupby(['keyword', 'date', 'RT']).agg(agdict)
    
    accumdf = pd.concat([accumdf, dfnew])
    
    wc = mediaGrab(df, wc)
    
accumdf.to_csv('keywords.csv')
with open('media.csv', 'w') as f:
    for w in wc:
        f.write(w + ',' + str(wc[w]) + '\n')