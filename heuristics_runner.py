# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:28:34 2023

@author: Joshua Liu
"""
from visualtool import palletplot,draw_route
import copy
import time
import numpy as np
from generator import depotgen,boxgen,palletgen,truckgen,desgen,desmapgen
from general_function import Pallet_cost,Truck_cost,Greedyroute,RoutingwithInsertion, \
                             Totaldistance
from heuristics_function import Boxfirstfit,Palletfirstfit,Boxmeanbestfit,Palletmeanbestfit, \
                          Boxajustbestfit,Palletajustbestfit,SDC_BoxFit,KDC_BoxFit, \
                          Pallet_preload
from heuristics_perturbative import perturbbox,perturbdes

#RUN PROGRAMME
def runfunction(function_code:int,dimension:bool,Ins_list:list,Print:bool=False,
                plot:bool=False,routing_method:int=1,pernot:bool=True) -> float:
    
    Depot_list = copy.deepcopy(Ins_list[0])
    Box_list = copy.deepcopy(Ins_list[1])
    Pallet_list = copy.deepcopy(Ins_list[2])
    Truck_list = copy.deepcopy(Ins_list[3])
    Destination_list = copy.deepcopy(Ins_list[4])
    desmap = copy.deepcopy(Ins_list[5])
    
    #record start time
    start = time.time()
    
    ### 3.0.0 Firstfit (0)
    if function_code == 0:
        sol_pack = Boxfirstfit(dimension,Box_list,Pallet_list)
        sol_package = sol_pack[0]
        sol_pacposition = sol_pack[1]
        sol_Blist = sol_pack[2]
        sol_Plist = sol_pack[3]
        sol_lo = Palletfirstfit(sol_package,sol_Blist,sol_Plist,Truck_list)
        sol_load = sol_lo[0]
        sol_Tlist = sol_lo[1]
        if routing_method == 0:
            sol_route = Greedyroute(sol_Tlist,desmap)
        else:
            sol_route = RoutingwithInsertion(sol_Tlist,desmap)

    ### 3.1.1 Meanbestfit (1)
    if function_code == 1:
        sol_pack = Boxmeanbestfit(dimension,Box_list,Pallet_list,desmap)
        sol_package = sol_pack[0]
        sol_pacposition = sol_pack[1]
        sol_Blist = sol_pack[2]
        sol_Plist = sol_pack[3]
        sol_lo = Palletmeanbestfit(sol_package,sol_Plist,Truck_list,desmap)
        sol_load = sol_lo[0]
        sol_Tlist = sol_lo[1]
        if routing_method == 0:
            sol_route = Greedyroute(sol_Tlist,desmap)
        else:
            sol_route = RoutingwithInsertion(sol_Tlist,desmap)

    ### 3.1.2 Adjustbestfit (2)
    if function_code == 2:
        sol_pack = Boxajustbestfit(dimension,Box_list,Pallet_list,desmap)
        sol_package = sol_pack[0]
        sol_pacposition = sol_pack[1]
        sol_Blist = sol_pack[2]
        sol_Plist = sol_pack[3]
        sol_lo = Palletajustbestfit(sol_package,sol_Plist,Truck_list,desmap)
        sol_load = sol_lo[0]
        sol_Tlist = sol_lo[1]
        if routing_method == 0:
            sol_route = Greedyroute(sol_Tlist,desmap)
        else:
            sol_route = RoutingwithInsertion(sol_Tlist,desmap)

    ### 3.2.1 Single-destination cluster (3)
    if function_code == 3:
        sol_pack = SDC_BoxFit(dimension,Box_list,Pallet_list,desmap)
        sol_package = sol_pack[0]
        sol_pacposition = sol_pack[1]
        sol_Blist = sol_pack[2]
        sol_Plist = sol_pack[3]
        sol_lo = Palletfirstfit(sol_package,sol_Blist,sol_Plist,Truck_list)
        sol_load = sol_lo[0]
        sol_Tlist = sol_lo[1]
        if routing_method == 0:
            sol_route = Greedyroute(sol_Tlist,desmap)
        else:
            sol_route = RoutingwithInsertion(sol_Tlist,desmap)

    ### 3.2.2 K-destination cluster (4)
    if function_code == 4:
        sol = KDC_BoxFit(dimension,Box_list,Pallet_list,Truck_list,desmap)
        sol_package = sol[0]
        sol_load = sol[1]
        sol_route = sol[2]
        sol_pacposition = sol[3]
        sol_Blist = sol[4]
        sol_Plist = sol[5]
        sol_Tlist = sol[6]

    ### 3.2.3 Pre-loaded packing (5)
    if function_code == 5:
        sol = Pallet_preload(dimension,Box_list,Pallet_list,Truck_list)
        sol_package = sol[0]
        sol_load = sol[1]
        sol_pacposition = sol[2]
        sol_Blist = sol[3]
        sol_Plist = sol[4]
        sol_Tlist = sol[5]
        if routing_method == 0:
            sol_route = Greedyroute(sol_Tlist,desmap)
        else:
            sol_route = RoutingwithInsertion(sol_Tlist,desmap)
            
    ###pertub###
    if pernot == True and function_code != 0:
        persol_1 = perturbbox(dimension,sol_package,sol_pacposition,sol_load,sol_route, \
                         sol_Blist,sol_Plist,sol_Tlist,desmap)
        persol_2 = perturbdes(dimension,persol_1[0],persol_1[1],persol_1[2],persol_1[3],sol_Plist,sol_Tlist,desmap)
        sol_package,sol_pacposition,sol_load,sol_route = persol_2

    end = time.time()
    runtime = end - start
    
    P_cost = Pallet_cost(sol_package,Pallet_list)
    T_cost = Truck_cost(sol_load,Truck_list)
    D_cost = 0
    Distancecost_bytruck = []
    for route in sol_route:
        if route != []:    
            route_cost = Totaldistance(route,desmap)
            D_cost += route_cost
            Distancecost_bytruck.append(route_cost)
            
    Total_cost = P_cost + T_cost + D_cost

    if Print == True:
        if len([box for pallet in sol_package for box in pallet]) != len(Box_list):
            print('PALLET INFEASIBALE!!!')
        
        elif len([pallet for truck in sol_load for pallet in truck]) != \
                 len([pallet for pallet in sol_package if pallet != []]):
                     print('TRUCK INFEASIBALE!!!')
        
        else:
            used_pallet = [i for i, j in enumerate(sol_package) if j]
            used_truck = [i for i, j in enumerate(sol_load) if j]
            print('Packaging solution (Box in Pallet):',sol_package[:max(used_pallet)+1])
            print('Packaging position (Box in Pallet):',sol_pacposition[:max(used_pallet)+1])
            print('Loading solution (Pallet in Truck):',sol_load[:max(used_truck)+1])
            print('routing solution (Destination in Truck):',sol_route[:max(used_truck)+1])
            print('Pallet cost:',P_cost)
            print('Truck cost:',T_cost)
            print('Total travel cost:',D_cost)
            print('Travel cost by each truck(In truck ID order):', Distancecost_bytruck)
            print('Total cost:', Total_cost)
            print('Running time of the algorithm is:', round(runtime,2), 's')

            if plot == True:
                #plot 3d packing
                if dimension == True:
                    for j in used_pallet:
                        size_list = []
                        pallet_size = (Pallet_list[j].L,Pallet_list[j].W,Pallet_list[j].H)
                        for i in sol_package[j]:
                            size_list.append((Box_list[i].l,Box_list[i].w,Box_list[i].h))
                        palletplot(pallet_size,sol_pacposition[j],size_list)
                
                #plot route
                draw_route(sol_route,Depot_list,Destination_list)
   
    return Total_cost

#Test
if __name__ == "__main__":
    
    #Seed
    np.random.seed(6)
    #Input
    Depot_Num = 1
    Box_Num = 40
    Pallet_Num = 40
    Truck_Num = 40
    Destination_Num = 25
    Dimen = True
    Class = 5
    fun = 2
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
    
    #Run
    runfunction(fun,Dimen,Ins_list,Print=True,plot=False)

