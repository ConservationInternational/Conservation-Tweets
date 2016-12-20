# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:51:39 2016

@author: mcooper
"""

import pickle

baseline = pickle.load(open("baseline_2016-12-19.p", "rb"))

first = pickle.load(open("climatechange-post.p", "rb"))
second = pickle.load(open("climatechange-pre.p", "rb"))

btot = baseline['TOTAL']
for i in baseline:
    baseline[i] = baseline[i]/btot
    
ftot = first['TOTAL']
for i in baseline:
    first[i] = first[i]/ftot
    
stot = second['TOTAL']
for i in second:
    second[i] = second[i]/stot
    
def merge(A, B, f):
	merged = {k: f(A[k], B[k]) for k in A.keys() & B.keys())
	
def pmi(A, B):
	return math.log(A/B)
	
def diff(A, B):
	return (A-B)
	
A = merge(first, baseline, f=pmi)
C = merge(second, baseline, f=pmi)

diff = merge(A, C, f=diff)

f = open('results.csv', 'rw')
for i in diff:
	f.write(i + ',' + diff[i] + '\n')
f.close()