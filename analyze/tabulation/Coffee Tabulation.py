import boto3
import pandas as pd
import csv
from collections import defaultdict
import io

keywords = ["coffee&conservation", "coffee&fair&trade", "coffee&organic", "coffee&sustain"]


#also get most used media
def mediaGrab(df, wc):
    bigstr = df['text'].to_string(index=False).split()
    #returns a tabulation of all tokens starting with 'http' within the 'text' column of a dataframe
    for i in bigstr:
        if i[:4] == 'http' and '...' not in i:
            wc[i] += 1
    return(wc)

#also get most mentioned users
def userGrab(df, wc):
    bigstr = df['text'].to_string(index=False).split()
    #returns a tabulation of all tokens starting with 'http' within the 'text' column of a dataframe
    for i in bigstr:
        if i[:1] == '@' and '...' not in i:
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

already = []
users = defaultdict(int)
media = defaultdict(int)
accumdf = pd.DataFrame()
for f in files:
    print(f)
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    df = df[~df['id_str'].isin(already)]
    
    media = mediaGrab(df, media)
    
    users = userGrab(df, users)
    
    already = already + df['id_str'].tolist()



with io.open('coffee_media.csv', 'w', encoding='utf8') as f:
    for w in media:
        f.write(w + ',' + str(media[w]) + '\n')

with io.open('coffee_users.csv', 'w', encoding='utf8') as f:
    for w in users:
        f.write(w + ',' + str(users[w]) + '\n')