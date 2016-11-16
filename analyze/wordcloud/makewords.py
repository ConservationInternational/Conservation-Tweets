import boto3
import re
import sys

def find_nth(haystack, needle, n):
    if n==0:
        return 0
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start     


def getWordsFromFile(body):
    lines = body.split('\n')
    text = lines[0].find('text')
    comstart = lines[0][:text].count(',')
    comstop = comstart + 1
    result = ''
    for line in lines[1:]:
        start = find_nth(line, ',', comstart)
        stop = find_nth(line, ',', comstop)
        text = line[start:stop]
        result = result + ' ' + re.sub(r'[^a-z#@ ]', '', text.lower())
    return result 

if __name__ == '__main__':
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ci-tweets')    
    for i in sys.argv[1:]:
        body = ''
        for obj in bucket.objects.all():
            if i in obj.key:
                file = obj.get()['Body'].read().decode('utf-8')
                body = body + getWordsFromFile(file)
        f = open(i + '_words.txt', 'w')
        f.write(body)
        f.close()    
    
