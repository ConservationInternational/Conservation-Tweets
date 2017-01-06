# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:51:39 2016

@author: mcooper
"""

import pickle
import math

firstname = "climatechange-post"
secondname = "climatechange-pre"

base_count = dict(pickle.load(open("baseline_2016-12-19.p", "rb")))
frst_count = dict(pickle.load(open(firstname + ".p", "rb")))
scnd_count = dict(pickle.load(open(secondname + ".p", "rb")))

def convertFreq(masterdict):
    total = float(masterdict['TOTAL'])
    newdict = {}
    for i in newdict:
        newdict[i] = float(newdict[i])/float(total)
    return newdict
    
def merge(A, B, f):
    merged = {k: f(A[k], B[k]) for k in A.viewkeys() & B.viewkeys()}
    return merged

def pmi(A, B):
    return (math.log(A/B))

def diff(A, B):
    return (A-B)
    
def countSum(A, B):
    return sum([A, B])

def valueConcat(A, B):
    return ([A, B])

base_freq = convertFreq(base_count)
frst_freq = convertFreq(frst_count)
scnd_freq = convertFreq(scnd_count)

frst_pmi = merge(frst_freq, base_freq, f=pmi)
scnd_pmi = merge(scnd_freq, base_freq, f=pmi)

pmi_diff = merge(frst_pmi, scnd_pmi, f=diff)

all_count = merge(frst_count, scnd_count, f=countSum)

frst_pmi_count = merge(frst_pmi, frst_count)
scnd_pmi_count = merge(scnd_pmi, scnd_count)
pmi_diff_count = merge(pmi_diff, all_count)


f = open(firstname + '_results.csv', 'wb')
for i in frst_pmi_count:
    f.write(i + ',' + str(frst_pmi_count[i][0]) + str(frst_pmi_count[i][1]) + '\n')

f = open(secondname + '_results.csv', 'wb')
for i in scnd_pmi_count:
    f.write(i + ',' + str(scnd_pmi_count[i][0]) + str(scnd_pmi_count[i][1]) + '\n')

f = open(firstname + '_' + secondname + '_results.csv', 'wb')
for i in pmi_diff_count:
    f.write(i + ',' + str(pmi_diff_count[i][0]) + str(pmi_diff_count[i][1]) + '\n')