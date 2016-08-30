# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:46:55 2016

@author: mcooper
"""

import tweepy
import datetime


class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        data
        
        s3 = boto3.resource('s3')
        s3.Bucket('ci-tweets').put_object(Key=str(datetime.datetime.now())+'.txt',  Body=data)

        return True

    def on_error(self, status):
        print status


l = StdOutListener()
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

filt = 'WWF,World Wide Fund for Nature,The Nature Conservancy,The Conservancy,WCS,World Conservation Society,TNC,The GEF,RARE,Pew Trust,EDF,The Ocean Conservancy,Oceana,Conservation International,Palm Oil,Meat,Soy,shrimp,Vegetarian,Vegan,Climategate,Microplastic beads,Logging,Anthropocene,Mass Extinction,Cop22,Marrakesh,CBD Mexico,Nature/Gender,Environment/Policy,Climate change/Policy,Environment/Business,Environment/Peace(building),Conservation,Nature,Biodiversity,Sustainable,Green,Earth,Planet,Gaia,Ecosystem,Resilience,Protected areas,#IUCNcongress,WeNeedNature,NatureForAll,INeedNature,NaturalCapital,Conservation Finance,Obama/POTUS,Whitehouse,Papahanaumokuakea,Marine Monument,indigenous,REDD+,Forests,Rainforest,ValensReef,NatureIsSpeaking,#IUCNRedList,#SDG,#SDGs,marine,plastic,ClimateChange,IUU,fisheries ,CEPF,PADDD,MPA,Marine Protected Areas ,Peter Seligmann,Russ Mittermeier,Greg Stone,Aulani Wilhelm'

stream = tweepy.Stream(auth, l)
stream.filter(track=[filt])