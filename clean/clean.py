#Remove non-english, non-indonesian tweets
#Add columns for user.location vars

#Run on 1-11-2017

import boto3
import pandas
import carmen
import csv

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

resolver = carmen.get_resolver()
resolver.load_locations()

with open('oncemore.txt') as f:
    files = f.readlines()
files = [x.replace('"', '').strip() for x in files] 

for f in files[1:]:
	print(f)
	out = s3client.get_object(Bucket='ci-tweets', Key=f)

	df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)

	df = df.assign(country='')
	df = df.assign(state='')
	df = df.assign(county='')
	df = df.assign(city='')
	df = df.assign(latitude='')
	df = df.assign(longitude='')

	#Remove non-english, non-indonesian tweets
	if 'lang' in df.columns:
		df = df.loc[(df['lang'] == 'en') | (df['lang'] == 'in')]

	if 'user.location' in df.columns:
		for i in df.index:
			try:
				tweet = {'place': None, 'user': {'location': df.loc[i]['user.location']}}
				loc = resolver.resolve_tweet(tweet)
				if loc is not None:
					df = df.set_value(i, 'country', loc[1].country)
					df = df.set_value(i, 'state', loc[1].state)
					df = df.set_value(i, 'county', loc[1].county)
					df = df.set_value(i, 'city', loc[1].city)
					df = df.set_value(i, 'latitude', loc[1].latitude)
					df = df.set_value(i, 'longitude', loc[1].longitude)
			except:
				pass
				
	s3resource.Bucket('ci-tweets').put_object(Key=f,  Body=df.to_csv(None, encoding='utf-8', index=False))