# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:51:39 2016

@author: mcooper
"""

import pickle
import math
import sys
import os

if sys.platform == 'win32':
    os.chdir('D:/Documents and Settings/mcooper/GitHub/Conservation-Tweets/analyze/PMI')

firstname = "vegan"
secondname = "vegetarian"

base_freq = dict(pickle.load(open("baseline_2017-01-06_prob.p", "rb")))
frst_count = dict(pickle.load(open(firstname + ".p", "rb")))
scnd_count = dict(pickle.load(open(secondname + ".p", "rb")))

def convertFreq(masterdict):
    total = float(masterdict['TOTAL'])
    newdict = {}
    for i in masterdict:
        newdict[i] = float(masterdict[i])/float(total)
    return newdict

def merge(A, B, f):
    if sys.platform == 'win32':
        merged = {k: f(A[k], B[k]) for k in A.keys() & B.keys()}
    elif sys.platform == 'linux2':
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

frst_freq = convertFreq(frst_count)
scnd_freq = convertFreq(scnd_count)

frst_pmi = merge(frst_freq, base_freq, f=pmi)
scnd_pmi = merge(scnd_freq, base_freq, f=pmi)

pmi_diff = merge(frst_pmi, scnd_pmi, f=diff)

all_count = merge(frst_count, scnd_count, f=countSum)

f = open(firstname + '_results.csv', 'w')
for i in frst_pmi:
    f.write(i + ',' + str(frst_pmi[i]) + ',' + str(frst_count[i]) + '\n')

f = open(secondname + '_results.csv', 'w')
for i in scnd_pmi:
    f.write(i + ',' + str(scnd_pmi[i]) + ',' + str(scnd_count[i]) + '\n')

f = open(firstname + '_' + secondname + '_results.csv', 'w')
for i in pmi_diff:
    f.write(i + ',' + str(pmi_diff[i]) + ',' + str(all_count[i]) + '\n')
f.close()