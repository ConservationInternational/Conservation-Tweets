import pandas as pd
import boto3
import csv
import numpy as np

lang = 'in'

#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='geo-baseline', Prefix='in')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])

accum = pd.DataFrame()
for f in files:
    print(f)
    out = s3client.get_object(Bucket='geo-baseline', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    accum = accum.append(df)
    
accum_sel = accum[np.isfinite(accum['gps_longitude'])]