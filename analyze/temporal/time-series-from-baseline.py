import boto3

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

#Get all files
paginator = s3client.get_paginator('list_objects')
pages = paginator.paginate(Bucket='baseline-text', Prefix='')
files = []
for p in pages:
    for x in p['Contents']:
        files.append(x['Key'])
        
beginfile = 'en2016-11-24 10:01:58.032584.csv'
files = files[files.index(beginfile):]

keys= []
f = open('keywords.txt', 'r')
for k in f.readlines():
    keys.append(k.strip('\n'))
f.close()

for f in files:
    print(f)
    if f[:2]=='en':
        for k in keys:
            t = open(k + '.csv', 'a')
            
            out = s3client.get_object(Bucket='baseline-text', Key=f)
            lines = out['Body'].read().decode('utf-8').replace('\r', '').split('\n')
            count = 0        
            for l in lines:
                if k in l:
                    count += 1
            t.write(f[2:-4] + ',' + str(count) + ',' + str(len(lines)) + ',' + str(count/len(lines)) + '\n')
            t.close()
    
    
                