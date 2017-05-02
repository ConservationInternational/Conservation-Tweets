import boto3
import pandas
import csv
import numpy as np

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


#also get retweets for all of the keywords above


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


s3client = boto3.client('s3')

pmi = pandas.DataFrame(index=keywords, columns=countwords).apply(pandas.to_numeric)
count = pandas.DataFrame(index=keywords, columns=countwords).apply(pandas.to_numeric)

for f in files:
    out = s3client.get_object(Bucket='ci-tweets', Key=k + '.csv')
    df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    temp = pandas.DataFrame()
    for c in countwords:
        if sum(df['word'] == c):
            pmi = pmi.set_value(k, c, float(df.loc[df['word']==c, 'PMI']))
            count = count.set_value(k, c, float(df.loc[df['word']==c, 'count']))
        else:
            pmi = pmi.set_value(k, c, np.nan)
            count = count.set_value(k, c, np.nan)


pmi.to_csv('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/Word_Tablulation.csv')
count.to_csv('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/Count.csv')