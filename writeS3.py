# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:47:54 2016

@author: mcooper
"""

import os
import boto3

os.chdir('~/temp_tweets')

files = os.listdir()

s3 = boto3.resource('s3')
s3.Bucket('ci-tweets').put_object(Key=str(datetime.datetime.now())+'.txt',  Body=data)
