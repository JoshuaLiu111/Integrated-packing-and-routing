# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 13:23:51 2023

@author: Joshua Liu
"""

from heuristics_runner import runfunction
import numpy as np
import json
from generator import depotgen,boxgen,palletgen,truckgen,desgen,desmapgen



#Instance
def instance_gen(Box_Num:int,Destination_Num:int,Class:int,
                 Depot_Num:int=1,Pallet_Num:int=80,
                 Truck_Num:int=50,triangle:bool=True) -> list:
    #List
    De_list = depotgen(Depot_Num)
    B_list = boxgen(Box_Num,Destination_Num,Class)
    P_list = palletgen(Pallet_Num,Class)
    T_list = truckgen(Truck_Num,Class)
    D_list = desgen(Destination_Num)

    #Map
    desmap = desmapgen(De_list,D_list)
    
    return De_list,B_list,P_list,T_list,D_list,desmap



#Compute
if __name__ == "__main__":
    B_Num = [20,40,60,80]
    D_Num = [10,25,50]
    Dimen = [False,True]
    Class_range = range(1,9)
    Function_code = range(6)
    Run_temp = 10
    
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
                        Ins_list = instance_gen(b_num,d_num,cl)
                        #record performance
                        perform = []
                        for fun in Function_code:
                            perform.append(runfunction(fun,di,Ins_list))
                        #recorf over run
                        perform_run.append(perform)
                    #compute average over runs
                    perform_overrun = np.average(np.array(perform_run), axis=0).tolist()
                    #add to dict level d
                    dict_d['des_num_%s' % d_num] = perform_overrun
                #add to dict level b
                dict_b['box_num_%s' % b_num] = dict_d
            #add to dict level cl
            dict_cl['class_num_%s' % cl] = dict_b
        #add to dict level di
        dict_all['whether3d_%s' % di] = dict_cl
    
    with open('heuristics_output.json','w') as fp:
        json.dump(dict_all, fp)
    
    ''' Don't run this unless absolutely necessary
    #full output
    dict_full = {}
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
                        Ins_list = instance_gen(b_num,d_num,cl)
                        #record performance
                        perform = []
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
        dict_full['whether3d_%s' % di] = dict_cl
    
    with open('heuristics_fulloutput.json','w') as fp:
        json.dump(dict_full, fp)
    '''