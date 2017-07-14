import boto3
import pandas as pd
import csv
from collections import defaultdict
import io

keywords = ["sawit", "palm.oil"]

#also get most mentioned users
def userGrab(t, wc):
    txt = english.tokenize1(t)
    #returns a tabulation of all tokens starting with '@' column of a dataframe
    for i in txt:
        if i[:1] == '@' and '...' not in i:
            wc[i] += 1
    return(wc)


#GetClassifiers
execfile('ClassifierWordList.py')

#Get Wordlists
f = open('negative-words.txt')
engneg = f.read().split('\n')
f = open('positive-words.txt')
engpos = f.read().split('\n')

f = open("negative.txt")
indneg = f.read().split('\r\n')
f = open("positive.txt")
indpos = f.read().split('\r\n')

#Make classifiers
english = ClassifyWordList(engpos, engneg, 'positive', 'negative', tokens=1)
bahasa = ClassifyWordList(indpos, indneg, 'positive', 'negative', tokens=12)


def writeDD(dd, filename):
    with open(filename, 'w') as f:
        for w in dd:
            f.write(w + ',' + str(dd[w]) + '\n')

DailyTot = pd.DataFrame()

EngPosUCt = defaultdict(int)
EngNegUCt = defaultdict(int)
IndNegUCt = defaultdict(int)
IndPosUCt = defaultdict(int)

EngPosWCt = defaultdict(int)
EngNegWCt = defaultdict(int)
IndPosWCt = defaultdict(int)
IndNegWCt = defaultdict(int)

Spatial = pd.DataFrame()


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


for f in files:
    print(f)
    
    date = f[-14:-4]
    k = f[10:-15]
    
    out = s3client.get_object(Bucket='ci-tweets', Key=f)
    df = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    if k == 'palm.oil':
        df['class'] = df.text.apply(english.classify)
    elif k=='sawit':
        df['class'] = df.text.apply(bahasa.classify)
    
    EngPos = 0
    EngNeg = 0
    IndPos = 0
    IndNeg = 0
    
    total = 0
    
    for t,c in zip(df['text'], df['class']):
        words = english.tokenize1(str(t))
        
        total += 1
        
        if k == 'sawit':
            if c=='positive':
                IndPos += 1
                IndPosUCt = userGrab(t, IndPosUCt)
                for w in words:
                    IndPosWCt[w] += 1 
                
            elif c=='negative':  
                IndNeg += 1
                IndNegUCt = userGrab(t, IndNegUCt)
                for w in words:
                    IndNegWCt[w] += 1 
                
        elif k == 'palm.oil':
            if c=='positive':
                EngPos += 1
                EngPosUCt = userGrab(t, EngPosUCt)
                for w in words:
                    EngPosWCt[w] += 1 
                
            elif c=='negative':
                EngNeg += 1
                EngNegUCt = userGrab(t, EngNegUCt)
                for w in words:
                    EngNegWCt[w] += 1 
    
    newdf = df.loc[df['geo']!='None']
    
    dailydf = pd.DataFrame(data={'EngPos':EngPos, 'EngNeg':EngNeg, 'IndPos':IndPos, 'IndNeg':IndNeg, 'Total':total, 'Date':date, 'Key':k}, index=[0])
    
    Spatial = pd.concat([Spatial, newdf])
    DailyTot = pd.concat([DailyTot, dailydf])

DailyTot.to_csv('PalmSawitDailyTotals.csv')
Spatial.to_csv('SpatialPalm.csv')



writeDD(EngPosUCt, 'EngPosUCt.csv')
writeDD(EngNegUCt, 'EngNegUCt.csv')
writeDD(IndNegUCt, 'IndNegUCt.csv')
writeDD(IndPosUCt, 'IndPosUCt.csv')

writeDD(EngPosWCt, 'EngPosWCt.csv')
writeDD(EngNegWCt, 'EngNegWCt.csv')
writeDD(IndPosWCt, 'IndPosWCt.csv')
writeDD(IndNegWCt, 'IndNegWCt.csv')

