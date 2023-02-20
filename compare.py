#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:34:22 2023

@author: Joshua Liu
"""
from heuristics_runner import runfunction
from exact_runner import run_least_cost_opt
import json
from heuristics_experiment import instance_gen

if __name__ == "__main__":
    B_Num = [10]
    D_Num = [5,10]
    Dimen = [True]
    Class_range = [8]
    Function_code = range(6)
    Run_temp = 10
    solver_options = {"solver": "gurobi", "mip_gap": 0.00001, "time_limit": 1000}
    
    #average over temp
    dict_all = {}
    for di in Dimen:
        dict_cl = {}
        for cl in Class_range:
            dict_b = {}
            for b_num in B_Num:
                dict_d = {}
                for d_num in D_Num:
                    perform_run = []
                    for run in range(Run_temp):
                        #generate instance
                        Ins_list = instance_gen(b_num,d_num,cl,Pallet_Num=20,Truck_Num=20)
                        #record performance
                        perform = []
                        perform.append(run_least_cost_opt(Ins_list,solver_options))
                        for fun in Function_code:
                            perform.append(runfunction(fun,di,Ins_list))
                        #recorf over run
                        perform_run.append(perform)
                    #flip list of lists
                    perform_fullrun = [list(i) for i in zip(*perform_run)]
                    #add to dict level d
                    dict_d['des_num_%s' % d_num] = perform_fullrun
                #add to dict level b
                dict_b['box_num_%s' % b_num] = dict_d
            #add to dict level cl
            dict_cl['class_num_%s' % cl] = dict_b
        #add to dict level di
        dict_all['whether3d_%s' % di] = dict_cl
    
    with open('compare_output.json','w') as fp:
        json.dump(dict_all, fp)