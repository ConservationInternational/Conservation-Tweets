# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:46:55 2016

@author: mcooper
"""

import tweepy
import datetime

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        f = open('temp_tweets/' + str(datetime.datetime.now()).replace(':', '.') + '.json', 'w')
        f.write(data)
        f.close()
        
        return True

    def on_error(self, status):
		f = open('errorlong.txt', 'w')
		f.write(str(datetime.datetime.now())+str(status))
        f.close()


l = StdOutListener()
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

filt = []
f = open('keywords.txt', 'r')
for i in f:
    filt.append(i.rstrip('\n'))
f.close()

filt = set(filt)
filt = ','.join(filt)

stream = tweepy.Stream(auth, l)
stream.filter(langauges=['en'], track=[filt])