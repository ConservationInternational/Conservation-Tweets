import os
import boto3
import datetime
import json

files = os.listdir('temp_tweets')

data = ['id_str,coordinates,created_at,favorite_count,favorited,geo,place,retweet_count,retweeted,text,user.favourites_count,user.friends_count,user.geo_enabled,user.location,user.name,user.statuses_count']

for i in files:
    try:
        f = open('temp_tweets/' + i, 'r')
        out = json.loads(f.read())
        f.close()

        twt = [out.get('id_str'),
				out.get('coordinates'),
                out.get('created_at'),
                out.get('favorite_count'),
                out.get('favorited'),
                out.get('geo'),
                out.get('place'),
                out.get('retweet_count'),
                out.get('retweeted'),
                out.get('text'),
                out.get('user').get('favourites_count'),
                out.get('user').get('friends_count'),
                out.get('user').get('geo_enabled'),
                out.get('user').get('location'),
                out.get('user').get('name'),
                out.get('user').get('statuses_count')]
        twt = '@^@#%*'.join(map(unicode, twt))
        twt = twt.replace(',', ' ').replace('\n', ' ').replace('@^@#%*', ',')
        data.append(twt)

    except:
        pass

    os.remove('temp_tweets/' + i)
	
s3 = boto3.resource('s3')
s3.Bucket('ci-tweets').put_object(Key='v2' + str(datetime.datetime.now()).replace(':', '.') + '.csv',  Body='\n'.join(data))
