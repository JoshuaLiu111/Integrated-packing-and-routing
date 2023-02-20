# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:28:34 2023

@author: Joshua Liu
"""

from typing import Dict
import numpy as np
import time
from exact_endpoint import solve_least_cost
from generator import depotgen,boxgen,palletgen,truckgen,desgen,desmapgen



def run_least_cost_opt(Ins_list:list, solver_options:Dict):

    #record start time
    start = time.time()
    # Run model endpoint and retrieve results
    var_outputs,cost_outputs = solve_least_cost(Ins_list, solver_options)
    #record end time
    end = time.time()
    runtime = end - start
    print('Variable values are:',var_outputs)
    print('Total cost is:',cost_outputs)
    print('Running time of the algorithm is:', round(runtime,2), 's')
    
    return cost_outputs


if __name__ == "__main__":
    
    #Seed
    np.random.seed(6)
    #Input
    Depot_Num = 1
    Box_Num = 8
    Pallet_Num = 8
    Truck_Num = 8
    Destination_Num = 4
    Dimen = True
    Class = 5
    #List
    De_list = depotgen(Depot_Num)
    B_list = boxgen(Box_Num,Destination_Num,Class)
    P_list = palletgen(Pallet_Num,Class)
    T_list = truckgen(Truck_Num,Class)
    D_list = desgen(Destination_Num)

    #Map
    desmap = desmapgen(De_list,D_list,triangle=False)
    
    #Combine
    Ins_list = [De_list,B_list,P_list,T_list,D_list,desmap]
    
    solver_options = {"solver": "gurobi", "mip_gap": 0.00001, "time_limit": 1000}
    
    #Run
    run_least_cost_opt(Ins_list, solver_options)