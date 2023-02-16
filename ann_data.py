# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 14:59:01 2023

@author: Joshua liu
"""
import pickle
import numpy as np
from heuristics_experiment import instance_gen
from heuristics_runner import runfunction

#feeding
ins_size = 1000

#random feeds
B_Num = [20,40,60,80]
D_Num = [10,25,50]
Class_range = range(6,9)

#record
record_ins = []
record_results = []
record_fun = []
for temp in range(ins_size):
    
    b_num = np.random.choice(B_Num)
    d_num = np.random.choice(D_Num)
    cl = np.random.choice(Class_range)
    ins = instance_gen(b_num,d_num,cl)
    results = []
    #four proposed algorithms
    for j in [1,2,4,5]:
        results.append(runfunction(j,False,ins,pernot=False))
    best_fun = results.index(min(results))
    
    #record output indexes
    record_ins.append(ins)
    record_results.append(results)
    record_fun.append([1 if i == best_fun else 0 for i in range(4)])
    
with open('ann_data.pkl', 'wb') as f: 
    pickle.dump([record_ins,record_results,record_fun], f)
