import pandas as pd
from collections import defaultdict
import re

class Classifier:
    def __init__(self, training_data, tokens=1):
        self.tokens=tokens
        self.training_data = training_data.dropna()
        self.classes = self.training_data['class'].unique()
        self.freq_df = self._createFreqTab(training_data)
        self.totals = self.freq_df.sum()
        self.probs = self.totals/self.totals.sum()    
    
    def _createFreqTab(self, training_data):
        '''Requires a data frame with two columns:
                1. 'text' which is the text of tweets
                2. 'class' which is the categories that each tweet falls into
            
           Returns a data frame with a column for each category and rows for each word'''
    
        #Get wordcounts for each class
        dicts = []
        for c in self.classes:
            lines = training_data.loc[training_data['class'] == c, 'text']
            masterdict = defaultdict(int)
            for l in lines:
                words = self.tokenize(l)
                for w in set(words):
                    if w=='rt':
                        pass
                    elif w[:4]=='http':
                        masterdict['http'] += 1
                    else:
                        masterdict[w] += 1
            dicts.append(masterdict)
        
        #Create a frequency table for all words
        freq_df = pd.DataFrame(dicts).T
        freq_df.columns = self.classes
        
        freq_df = freq_df.fillna(0.1)
        
        return(freq_df)
    
    def classify(self, tweet):
        '''Requires a tweet
            
           Returns a pandas series of the likelihood of the tweet falling into each category'''
    
        wds = self.tokenize(tweet)
        words = self.freq_df.ix[wds, ]
        f = (words/self.totals).product()
        likelihood = f*self.probs
        likelihood_rel = likelihood/likelihood.sum()

        return(likelihood_rel)
    
    def tokenize(self, tweet):
        #Lots of quotes to convery sarcasm. Use quotes?
        if self.tokens == 1:
            tokens = re.sub(r'[^a-z#@ ]', '', tweet.lower()).split(' ')
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

    







        
        