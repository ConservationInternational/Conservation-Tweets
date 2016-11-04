import os
import boto3
import datetime
import json

files = os.listdir('temp_tweets')

data = []
for i in files:
    try:
        f = open('temp_tweets/' + i, 'r')
        out = json.loads(f.read())
        f.close()
        twt = [out.get('text'),
                out.get('id_str'),
                out.get('coordinates'),
                out.get('created_at'),
                out.get('favorite_count'),
                out.get('favorited'),
                out.get('geo'),
                out.get('place'),
                out.get('retweet_count'),
                out.get('retweeted'),
                out.get('lang'),
                out.get('user').get('favourites_count'),
                out.get('user').get('friends_count'),
                out.get('user').get('geo_enabled'),
                out.get('user').get('location'),
                out.get('user').get('name'),
                out.get('user').get('statuses_count')]
        twt = '@^@#%*^&%*$('.join(map(unicode, twt))
        twt = twt.replace(',', ' ').replace('\n', ' ').replace('\r', ' ').replace('@^@#%*^&%*$(', ',')
        data.append(twt)
    except:
        pass

    #os.remove('temp_tweets/' + i)
    
f = open('keywords.txt', 'r')
keywords = f.read().splitlines()
f.close()

for k in keywords:
    tempdat = ['text,id_str,coordinates,created_at,favorite_count,favorited,geo,place,retweet_count,retweeted,lang,user.favourites_count,user.friends_count,user.geo_enabled,user.location,user.name,user.statuses_count']
    
    ks = k.split('&')
       
    for t in data:
        if all(x.lower() in t[:t.find(',')].lower() for x in ks):
            tempdat.append(t)
    if len(tempdat) > 1:    
        s3 = boto3.resource('s3')
        s3.Bucket('ci-tweets').put_object(Key='ByKeyword/' + k.replace(' ', '.') + '-' + str(datetime.datetime.now())[:10] + '.csv',  Body='\n'.join(tempdat))
