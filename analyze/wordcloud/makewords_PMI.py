import pandas
import boto3
import csv
import numpy as np

#Read in data, skipping words already in buck


files = ['PMI_EngPosWCt.csv', 'PMI_EngNegWCt.csv', 'PMI_IndPosWCt.csv', 'PMI_IndNegWCt.csv']

for f in files:
    print(f)
    df = pandas.read_csv(f, quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
        
    #Get most outstanding words
    df = df.sort_values('PMI', ascending=False).head(300)
    df = df[df['PMI'] > 0]
    
    #Get most common outstanding words
    df = df.sort_values('count', ascending=False).head(100)    
    
    df['combo'] = df['count']*df['PMI']
    df['count'] = np.sqrt(df['combo']/df['combo'].min()).round()
    
    h = open(f[:-4] + '_words.csv', 'w')
    for i in df.index:
        ct = 0
        while ct < df.loc[i, 'count']:
            h.write(df.loc[i, 'word'] + ' ')
            ct += 1
    h.close()

            
            
    