# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:47:54 2016

@author: mcooper
"""

import os
import boto3
import datetime

files = os.listdir('temp_tweets')

data = []
for i in files:
    f = open ('temp_tweets/' + i)
    data.append(f.read())
    f.close()
    os.remove('temp_tweets/' + i)

s3 = boto3.resource('s3')
s3.Bucket('ci-tweets').put_object(Key=str(datetime.datetime.now()).replace(':', '.') + '.txt',  Body='\n'.join(data))
