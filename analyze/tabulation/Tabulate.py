import boto3
import pandas
import csv
import numpy as np

keywords = ["climate.change", "mass.extinction", "deforestation", "fracking", "pesticides", "overfishing"]

countwords = ["fear", "afraid", "worried", "scared", "nervous", "worry", "anxiety", "scary", "bad", "sad", "crisis", "threat", "problem", "real", "issue", "gross"]

s3client = boto3.client('s3')

pmi = pandas.DataFrame(index=keywords, columns=countwords).apply(pandas.to_numeric)
count = pandas.DataFrame(index=keywords, columns=countwords).apply(pandas.to_numeric)

for k in keywords:
    out = s3client.get_object(Bucket='ci-tweet-PMI', Key=k + '.csv')
    df = pandas.read_csv(out['Body'], quoting=csv.QUOTE_NONE, error_bad_lines=False, warn_bad_lines=True)
    
    for c in countwords:
        if sum(df['word'] == c):
            pmi = pmi.set_value(k, c, float(df.loc[df['word']==c, 'PMI']))
            count = count.set_value(k, c, float(df.loc[df['word']==c, 'count']))
        else:
            pmi = pmi.set_value(k, c, np.nan)
            count = count.set_value(k, c, np.nan)


pmi.to_csv('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/Word_Tablulation.csv')
count.to_csv('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/tabulation/Count.csv')