import os
import boto3
import datetime
import json
import re

temp_files = os.listdir('temp_tweets')

engdata = ['text']
inddata = ['text']   
   
for fl in temp_files:
    try:
        f = open('temp_tweets/' + fl, 'r')
        out = json.loads(f.read())
        f.close()
        twt = out.get('text')
        if out.get('lang') == 'en':
            engdata.append(re.sub(r'[^a-z#@ ]', '', twt.lower().replace('\n', '').replace('\n', '')))
        if out.get('lang') == 'id':
            inddata.append(re.sub(r'[^a-z#@ ]', '', twt.lower().replace('\n', '').replace('\n', '')))
    except:
        pass
  
s3 = boto3.resource('s3')
s3.Bucket('ci-tweets').put_object(Key='baseline/en' + str(datetime.datetime.now()) + '.csv',  Body='\n'.join(engdata))
s3.Bucket('ci-tweets').put_object(Key='baseline/id' + str(datetime.datetime.now()) + '.csv',  Body='\n'.join(inddata))

for fl in temp_files:
    try:
        os.remove('temp_tweets/' + fl)
    except:
        pass