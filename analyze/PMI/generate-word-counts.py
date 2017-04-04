import boto3
import pandas
import csv
from collections import defaultdict
import re

skip_already_written = False

#Read in data, skipping words already in buck
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='ci-tweets', Prefix='ByKeyword')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])


if skip_already_written:
	skipfiles = []
	try:
		pages = paginator.paginate(Bucket='ci-tweet-wordcounts', Prefix='')
		for p in pages:
			for x in p['Contents']:
				skipfiles.append(x['Key'])
	except:
		for object in s3resource.Bucket('ci-tweet-wordcounts').objects.all():
			print(object)

	skipkeys = []
	for f in skipfiles:
		skipkeys.append(f[:-4])

	keys = []
	for f in files[1:]:
		new = f[10:-15]
		if (new not in keys) and (new not in skipkeys):
			keys.append(new)
			
else:
	keys = []
	for f in files[1:]:
		new = f[10:-15]
		if (new not in keys) :
			keys.append(new)	

#get stopwords
stopwords = []
f = open('stopwords.txt')
for i in f.readlines():
    stopwords.append(i.rstrip('\n'))

for k in keys:
    wc = defaultdict(int)
    for f in files[1:]:
        if k==f[10:-15]:
            try:
                print(f)
                out = s3client.get_object(Bucket='ci-tweets', Key=f)
                df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
                
                lines = df["text"].tolist()
                for l in lines:
                    l = re.sub(r'[^a-z#@ ]', '', l.lower())
                    words = l.split()
                    for w in set(words):
                        if w=='rt' or w in stopwords:
                            pass
                        elif w[:4]=='http':
                            wc['http'] += 1
                        else:
                            wc[w] += 1
                    wc['TOTAL'] += 1
            except:
                w = open('wc-fail.txt')
                w.write(f + '\n')
                w.close()   
    string = ''
    for i in wc:
        string += i
        string += ','
        string += str(wc[i])
        string += '\n'
    s3resource.Bucket('ci-tweet-wordcounts').put_object(Key=(k + '.csv'),  Body=string)


