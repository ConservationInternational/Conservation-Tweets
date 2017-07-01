import os
import pandas as pd
import boto3
import csv
from collections import defaultdict

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

    dd = defaultdict(int)
    for i in files:
        print(i)
        out = s3client.get_object(Bucket='ci-tweets', Key=i)
        temp = pd.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
        
        temp['class'] = temp.text.apply(classifier.classify)
        
        vc = temp['class'].value_counts()
        
        s3resource.Bucket(writebucket).put_object(Key=i.replace(readprefix, writeprefix), Body=temp.to_csv(None, encoding='utf-8', index=False))        
    
        dd['tie'] += vc['tie']
        dd['positive'] += vc['positive']
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

f = open('negative-words.txt')
engneg = f.read().split('\n')
f = open('positive-words.txt')
engpos = f.read().split('\n')


#Make english classifier
english = ClassifyWordList(engpos, engneg, 'positive', 'negative')

#Classify PalmOil
eng_dd = classifyTheme('ci-tweets', 'ByKeyword/palm.oil', english, 'ci-tweets-sentiment', 'palmoil/palm.oil')
writeDict(eng_dd, 'eng_dd.csv')

#Classify English Baseline
eng_base_dd = classifyTheme('baseline-text', 'en', english, 'ci-tweets-sentiment', 'engbase/en')
writeDict(eng_base_dd, 'eng_base_dd.csv')

f = open("negative.txt")
indneg = f.read().split('\n')
f = open("positive.txt")
indpos = f.read().split('\n')

#Make Bahasa classfier
bahasa = ClassifyWordList(indpos, indneg, 'positive', 'negative')

#Classify Sawit
ind_dd = classifyTheme('ci-tweets', 'ByKeyword/sawit', bahasa, 'ci-tweets-sentiment', 'sawit/sawit')
writeDict(ind_dd, 'ind_dd.csv')

#Classify Bahasa Baseline
ind_base_dd = classifyTheme('baseline-text', 'in', bahasa, 'ci-tweets-sentiment', 'indbase/in')
writeDict(ind_base_dd, 'ind_base_dd.csv')


