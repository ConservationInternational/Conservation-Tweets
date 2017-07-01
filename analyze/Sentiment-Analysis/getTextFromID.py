# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 10:45:05 2017

@author: mcooper
"""

import pandas as pd
import tweepy

us = pd.read_csv("D:\Documents and Settings\mcooper\Desktop\uniformly_sampled.tsv", sep="\t",
                 names=['lang', 'id'])

us = us.loc[us['lang'].isin(['id', 'ms']), ]

#The tweepy library uses tweepy.get_status():

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)

def getTextFromID(id):
    tweet = api.get_status(id)
    return(tweet.text)

us['text'] = us.id.apply(getTextFromID)