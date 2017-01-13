import os
import boto3
import datetime
import json
import re
import carmen
import ast

temp_files = os.listdir('temp_tweets')

engdata = ['text']
inddata = ['text']   
enggeodata = ['id_str,user.location,country,state,county,city,latitude,longitude,gps_latitude,gps_longitude']
indgeodata = ['id_str,user.location,country,state,county,city,latitude,longitude,gps_latitude,gps_longitude']

def getLat(string):
    if string == 'None':
        return('None')
    else:
        try:
            string = string.replace('  ', ', ')
            d = ast.literal_eval(string)
            return(d['coordinates'][0])
        except:
            return('None')
    
def getLon(string):
    if string == 'None':
        return('None')
    else:
        try:
            string = string.replace('  ', ', ')
            d = ast.literal_eval(string)
            return(d['coordinates'][1])
        except:
            return('None')

resolver = carmen.get_resolver()
resolver.load_locations()
   
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
            
        geotwt = [out.get('id_str'),
                out.get('user').get('location')]
        loc = resolver.resolve_tweet(out)
        if loc is not None:
            loc = loc[1]
            geotwt += [loc.country, loc.state, loc.county, loc.city, str(loc.latitude), str(loc.longitude)]
        else:
            geotwt += ['', '', '', '', '', '']
        
        try:
            geotwt += getLat(out.get['geo'])
            geotwt += getLon(out.get['user.location'])
        except:
            geotwt += ['', '']
                            
        geotwt = '@^@#%*^&%*$('.join(map(unicode, geotwt))
        geotwt = twt.replace(',', ' ').replace('\n', ' ').replace('\r', ' ').replace('@^@#%*^&%*$(', ',')
        
        if out.get('lang')=='en':
            enggeodata.append(geotwt)
        elif out.get('lang')=='in':
            indgeodata.append(geotwt)            

    except:
        pass
  
s3 = boto3.resource('s3')
s3.Bucket('baseline-text').put_object(Key='en' + str(datetime.datetime.now()) + '.csv',  Body='\n'.join(engdata))
s3.Bucket('baseline-text').put_object(Key='id' + str(datetime.datetime.now()) + '.csv',  Body='\n'.join(inddata))
s3.Bucket('geo-baseline').put_object(Key=str(datetime.datetime.now()) + '.csv',  Body='\n'.join(enggeodata))
s3.Bucket('geo-baseline').put_object(Key=str(datetime.datetime.now()) + '.csv',  Body='\n'.join(indgeodata))

for fl in temp_files:
    try:
        os.remove('temp_tweets/' + fl)
    except:
        pass