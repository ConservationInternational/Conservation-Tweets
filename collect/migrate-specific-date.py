# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:33:51 2016

@author: mcooper
"""

import os
import boto3
import json
today = '2016-11-14'
tagged_files = os.listdir('tagged_tweets')
f = open('keywords.txt', 'r')
keywords = f.read().splitlines()
keywords = keywords
f.close()
for k in keywords:
    data = ['text,id_str,coordinates,created_at,favorite_count,favorited,geo,place,retweet_count,retweeted,lang,user.favourites_count,user.friends_count,user.geo_enabled,user.location,user.name,user.statuses_count']
    for fl in tagged_files:
        if k in fl and today in fl:                        
            try:
                f = open('tagged_tweets/' + fl, 'r')
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
    if len(data) > 1:    
        s3 = boto3.resource('s3')
        s3.Bucket('ci-tweets').put_object(Key='ByKeyword/' + k.replace(' ', '.') + '-' + today + '.csv',  Body='\n'.join(data))

for fl in tagged_files:
    if today in fl:
        os.remove('tagged_tweets/' + fl)