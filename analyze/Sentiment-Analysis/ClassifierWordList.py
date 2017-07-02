# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 11:23:30 2017

@author: mcooper
"""

import re

class ClassifyWordList:
    def __init__(self, a, b, a_name, b_name, tokens=1):
        '''Takes two lists of words, on in category a and one in category b'''
        self.a = a
        self.b = b
        self.a_name = a_name
        self.b_name = b_name
        self.tokens = tokens
        
        
    def validateUnique(self, a, b):
        intersection = [val for val in a if val in b]
        if len(intersection) > 0:
            print('Warning: Some words appear in both lists')
    
    def tokenize(self, tweet):
        if not isinstance(tweet, str):
            tweet = ''
        #Lots of quotes to convery sarcasm. Use quotes?
        if self.tokens == 1:
            tokens = re.sub(r'[^a-z#@ ]c', '', tweet.lower()).split(' ')
            while '' in tokens:
                tokens.remove('')
        elif self.tokens == 2:
            #get bigrams for words and phrases, but treat @ and # as monograms
            tokens = []
            words = re.sub(r'[^0-9a-z#@ ]', '', tweet.lower()).split(' ')
            words = ['' if x=='rt' else x for x in words]
            while '' in words:
                words.remove('')
            words = ['http' if x[:4]=='http' else x for x in words]        
            for i in range(len(words)-1):
                if words[i][0] in ['#', '@']: 
                    tokens.append(words[i])
                elif words[i+1][0] in ['@', '#']:
                    pass
                else:
                    tokens.append(words[i] + ' ' + words[i+1])
        return(tokens)

    def classify(self, tweet):
        tokens = self.tokenize(tweet)
        a_ct = 0
        b_ct = 0
        for t in tokens:
            if t in self.a:
                a_ct += 1
            elif t in self.b:
                b_ct += 1
        if a_ct > b_ct:
            return(self.a_name)
        elif b_ct > a_ct:
            return(self.b_name)
        else:
            return('tie')