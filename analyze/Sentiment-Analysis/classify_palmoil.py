import pandas as pd
import boto3
import csv
from collections import defaultdict
import random

execfile('ClassifierWordList.py')

def classifyTheme(readbucket, readprefix, classifier, writebucket, writeprefix):
    s3client = boto3.client('s3')
    s3resource = boto3.resource('s3')
    
    paginator = s3client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=readbucket, Prefix=readprefix)
    files = []
    for p in pages:
        for x in p['Contents']:
            files.append(x['Key'])
    
    if len(files) > 200 and readbucket == 'baseline-text':
        files = random.sample(files, 200)

    dd = defaultdict(int)
    for i in files:
        print(i)
        out = s3client.get_object(Bucket=readbucket, Key=i)
        temp = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
        
        temp['class'] = temp.text.apply(classifier.classify)
        
        vc = temp['class'].value_counts()
        
        s3resource.Bucket(writebucket).put_object(Key=i.replace(readprefix, writeprefix), Body=temp.to_csv(None, encoding='utf-8', index=False))        
    
        if 'tie' in vc.index:
            dd['tie'] += vc['tie']
        if 'positive' in vc.index:
            dd['positive'] += vc['positive']
        if 'negative' in vc.index:
            dd['negative'] += vc['negative']
    
    return(dd)

def writeDict(dictionary, name):
    string = ''
    for i in dictionary:
        string += i
        string += ','
        string += str(dictionary[i])
        string += '\n'
    f = open(name, 'w+')
    f.write(string)
    f.close()


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
#english = ClassifyWordList(engpos, engneg, 'positive', 'negative')
bahasa = ClassifyWordList(indpos, indneg, 'positive', 'negative')

#Classify English Baseline
#eng_base_dd = classifyTheme('baseline-text', 'en', english, 'ci-tweets-sentiment', 'engbase/en')
#writeDict(eng_base_dd, 'eng_base_dd.csv')

#Classify Bahasa Baseline
ind_base_dd = classifyTheme('baseline-text', 'in', bahasa, 'ci-tweets-sentiment', 'indbase/in')
writeDict(ind_base_dd, 'ind_base_dd.csv')

#Classify Sawit
ind_dd = classifyTheme('ci-tweets', 'ByKeyword/sawit', bahasa, 'ci-tweets-sentiment', 'sawit/sawit')
writeDict(ind_dd, 'ind_dd.csv')

#Classify PalmOil
#eng_dd = classifyTheme('ci-tweets', 'ByKeyword/palm.oil', english, 'ci-tweets-sentiment', 'palmoil/palm.oil')
#writeDict(eng_dd, 'eng_dd.csv')







