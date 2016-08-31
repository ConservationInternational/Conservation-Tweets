# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:46:55 2016

@author: mcooper
"""

import tweepy
import datetime
import json

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        s3 = boto3.resource('s3')
        s3.Bucket('ci-tweets').put_object(Key=str(datetime.datetime.now())+'.json',  Body=data)
        
        return True

    def on_error(self, status):
        f = open('errorlog.txt', 'w')
        f.write()
        print(status)


l = StdOutListener()
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

filt = []
f = open('keywords.txt', 'r')
for i in f:
    filt.append(i.rstrip('\n'))
f.close()
    
filt = ','.join(filt)

stream = tweepy.Stream(auth, l)
stream.filter(track=[filt])