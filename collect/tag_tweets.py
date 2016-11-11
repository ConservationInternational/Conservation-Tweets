# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 01:39:09 2016

@author: mcooper
"""

import os

files = os.listdir('temp_tweets')

f = open('keywords.txt', 'r')
keywords = f.read().splitlines()
f.close()


for f in files:

    try:
        t = open('temp_tweets/' + f, 'r')
        raw = t.read()    
    
        for k in keywords:
    
            ks = k.split('&')
            
            if all(raw.lower().find(x.lower()) > -1 for x in ks):
                nf = open('tagged_tweets/' + k + f, 'w')
                nf.write(raw)
        
        os.remove('temp_tweets/' + f)
    
    except:
        pass