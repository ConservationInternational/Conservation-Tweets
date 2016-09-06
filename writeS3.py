import os
import boto3
import datetime
import pandas
import json

files = os.listdir('temp_tweets')

columns = pandas.read_csv('collect_columns.csv', header=0)
columns = list(columns.loc[columns['select'], 'name'])

dataframes = []
for i in files:
    f = open('temp_tweets/' + i, 'r')
    out = json.loads(f.read())
    f.close()
    df = pandas.io.json.json_normalize(out)
    df = df[[c for c in columns if c in df.columns]]
    dataframes.appends(df)
    os.remove('temp_tweets/' + i)

dataframe = pandas.concat(dataframes)
	
s3 = boto3.resource('s3')
s3.Bucket('ci-tweets').put_object(Key=str(datetime.datetime.now()).replace(':', '.') + '.csv',  Body=dataframe.to_csv(None))
