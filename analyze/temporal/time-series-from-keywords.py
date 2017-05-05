import boto3
import pandas as pd
import csv

keywords = ["climate.change", "climatechange", "globalwarming", "global.warming"]


users = ['@realDonaldTrump','@SenSanders','@BernieSanders',
'@ReinaDeAfrica_','@CNN','@kitharingstons','@HillaryClinton','@salcidocees','@wikileaks','@AltNatParkSer','@nytimes','@BuzzFeedNews','@climatehawk1',
'@GeorgeTakei','@BarackObama','@MaiaMitchell','@Alex_Edelman','@thehill','@billmaher','@StephenSchlegel','@Jakee_and_bakee','@Greenpeace','@DrJillStein',
'@BillNye','@Descriptions','@ClimateCentral','@ClimateReality','@RogueNASA','@narendramodi','@POTUS','@washingtonpost','@NatGeoChannel','@UN','@girlposts',
'@KamalaHarris','@WhiteHouse','@ajplus','@billmckibben','@chrislhayes','@adamjohnsonNYC','@WorldfNature','@SteveSGoddard','@LeoDiCaprio','@iansomerhalder',
'@FoxNews','@guardian','@thinkprogress','@Picswithastory','@UNFCCC', '@NRDC']



#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
files = []

for k in keywords:
    pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword/' + k)
    for p in pages:
        for x in p['Contents']:
            files.append(x['Key'])


values = ['sum']*len(users)
agdict = dict(zip(users, values))
agdict['TOTAL'] = 'sum'

accumdf = pd.DataFrame()
already = []
for f in files:
    print(f)
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    df = df[~df['id_str'].isin(already)]
    
    for u in users:
        df[u] = df['text'].str.contains(u)
        
    df['TOTAL'] = True
        
    df['date'] = f[-14:-4]
    
    already = already + df['id_str'].tolist()    
    
    df = df.groupby(['date']).agg(agdict)  
    
    accumdf = pd.concat([accumdf, df])

accumdf['date'] = accumdf.index

dfnew = accumdf.groupby(['date']).agg(agdict)    

dfnew.to_csv('keywords.csv')
