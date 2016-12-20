# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:51:39 2016

@author: mcooper
"""

import pickle
import math

firstname = "climatechange-post"
secondname = "climatechange-pre"

baseline = pickle.load(open("baseline_2016-12-19.p", "rb"))
first = pickle.load(open(firstname + ".p", "rb"))
second = pickle.load(open(secondname + ".p", "rb"))
    
def merge(A, B, f):
    merged = {k: f(A[k], B[k]) for k in A.viewkeys() & B.viewkeys()}
    return merged

def pmi(A, B):
    return (math.log(A/B))

def diff(A, B):
    return (A-B)


A = merge(first, baseline, f=pmi)
C = merge(second, baseline, f=pmi)

diff = merge(A, C, f=diff)

f = open(firstname + '_results.csv', 'wb')
for i in A:
    f.write(i.encode('utf-8') + ',' + str(A[i]) + '\n')

f = open(secondname + '_results.csv', 'wb')
for i in C:
    f.write(i.encode('utf-8') + ',' + str(C[i]) + '\n')

f = open(firstname + '_' + secondname + '_results.csv', 'wb')
for i in diff:
    f.write(i.encode('utf-8') + ',' + str(diff[i]) + '\n')