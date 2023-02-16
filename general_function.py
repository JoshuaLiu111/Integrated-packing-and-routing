# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:21:24 2023

@author: Joshua Liu
"""
import numpy as np
from typing import Any
from statistics import mean
import copy
###GENERRAL FUNCTION###

def Totaldistance(route:list,desmap:list) -> float:
    totaldis = 0
    #add distance within the route
    for i in range(len(route)-1):
        totaldis += desmap[route[i]+1][route[i+1]+1]
    #add distance involving depot
    totaldis += desmap[0][route[0]+1] + desmap[route[-1]+1][0]
    return totaldis

def Min_distance(cur:int,route:list,desmap:list) -> float:
    #distance between current location and each choice of destination
    dist_record = [desmap[cur+1][route[i]+1] for i in range(len(route))]
    return min(dist_record)

def Min_distanceID(cur:int,route:list,desmap:list) -> int:
    dist_record = [desmap[cur+1][route[i]+1] for i in range(len(route))]
    return route[dist_record.index(min(dist_record))]

def Min_Bestpalletfit(Dlist_A:list,Dlist_B:list,desmap:list) -> float:
    #for each des in A, find its average distance to all des in B
    Cost_vector = []
    for i in Dlist_A:
        mean_distance = mean(desmap[i+1][j+1] for j in Dlist_B)
        Cost_vector.append(mean_distance)
    #record the minimum des in A
    Min_cost = min(Cost_vector)
    return Min_cost
            
def Pallet_cost(sol_package:list,Pallet_list:list) -> float:
    used_pallet = [i for i, j in enumerate(sol_package) if j]
    P_cost = sum(Pallet_list[i].c for i in used_pallet)
    return P_cost
    
def Truck_cost(sol_load:list,Truck_list:list) -> float:
    used_truck = [i for i, j in enumerate(sol_load) if j]
    T_cost = sum(Truck_list[i].C for i in used_truck)
    return T_cost

def Insert_cost(D_a:int,D_b:int,D_c:int,desmap:list) -> float:
    I_cost = desmap[D_a+1][D_c+1] + desmap[D_c+1][D_b+1] - desmap[D_a+1][D_b+1]
    return I_cost

def Swapneigh_cost(D_a:int,D_b:int,D_c:int,D_d,desmap:list) -> float:
    I_cost = Insert_cost(D_a,D_b,D_c,desmap) - Insert_cost(D_b,D_d,D_c,desmap)
    return I_cost

def Total_cost(sol_package:list,sol_load:list,sol_route:list,Pallet_list:list \
               ,Truck_list:list,desmap:list) -> float:
    P_cost = Pallet_cost(sol_package,Pallet_list)
    T_cost = Truck_cost(sol_load,Truck_list)
    used_truck = [i for i, j in enumerate(sol_route) if j]
    D_cost = sum(Totaldistance(sol_route[i],desmap) for i in used_truck) 
    return P_cost + T_cost + D_cost

def find_element(x:Any, lst:list) -> int:
    #find element in list of lists
    for i, row in enumerate(lst):
        for j, element in enumerate(row):
            if element == x:
                return i
    return -1

def Cluster_BoxFit (k:int,dimension:bool,Box_list_temp:list \
                    ,Pallet_list_temp:list,desmap:list) -> list:
    # similar to SDC_BoxFit, but one cluster could contain more destination
    sol_package = [[] for i in range(len(Pallet_list_temp))]
    sol_pacposition = [[] for i in range(len(Pallet_list_temp))]
    des_list=range(len(desmap)-1)
    #divided all the destination into k group
    splits = np.array_split(des_list, k)
    k_des_list = [list(q) for q in splits]
    # group box by clusters
    cluster_list=[[] for i in range(len(k_des_list))]
    for i in range(len(Box_list_temp)):
        for j in range(len(k_des_list)):
            if Box_list_temp[i].D in k_des_list[j]:
                cluster_list[j].append(Box_list_temp[i])
    # packing box in the same cluster into pallet
    Pallet_index = [i for i,j in enumerate(Pallet_list_temp)]
    for c in range(len(cluster_list)):
        for i in range(len(cluster_list[c])):
            if dimension==False:
                for j in Pallet_index:
                   #Check pallet capacity
                   if cluster_list[c][i].v <= Pallet_list_temp[j].rest_V:
                       #put box i into the first pallet (j) which can contain it
                       sol_package[j].append(cluster_list[c][i].ID)
                       #Calculate the rest capacity of pallet j
                       Pallet_list_temp[j].rest_V -= cluster_list[c][i].v
                       #Add destination into pallet list
                       if cluster_list[c][i].D not in Pallet_list_temp[j].D:
                           Pallet_list_temp[j].D.append(cluster_list[c][i].D)
                       break
                # once the box of one destination all packed, remove the index of the packed pallet
                # box with different destination have to pack in a new pallet
                if i == len(cluster_list[c])-1:
                    Pallet_index = [pal for pal in Pallet_index if sol_package[pal] == []]
            else:
                for j in Pallet_index:
                   indicator = False
                   #Check pallet capacity
                   if cluster_list[c][i].v <= Pallet_list_temp[j].rest_V:
                       #3d capacity
                       eps = sorted(Pallet_list_temp[j].eps_list, 
                                    key=lambda ep: (ep[0], ep[1], ep[2]))
                       for ep in eps:
                           size_condition = False
                           for ep2 in eps:
                               if ep2 != ep:
                                   if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                       if ep[0] + cluster_list[c][i].l > ep2[0]:
                                           size_condition = True
                                           break
                                   elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                       if ep[1] + cluster_list[c][i].w > ep2[1]:
                                           size_condition = True
                                           break
                           if ep[0] + cluster_list[c][i].l <= Pallet_list_temp[j].L and \
                               ep[2] + cluster_list[c][i].h <= Pallet_list_temp[j].H and \
                                ep[1] + cluster_list[c][i].w <= Pallet_list_temp[j].W and not size_condition:
                                    #PUT box i into the first pallet (j) which can contain it
                                    indicator = True
                                    sol_package[j].append(cluster_list[c][i].ID)
                                    sol_pacposition[j].append(ep)
                                    #Calculate the rest capacity of pallet j
                                    Pallet_list_temp[j].rest_V -= cluster_list[c][i].v
                                    #Add destination into pallet list
                                    if cluster_list[c][i].D not in Pallet_list_temp[j].D:
                                        Pallet_list_temp[j].D.append(cluster_list[c][i].D)
                                    #record eps    
                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1], ep[2])) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1], ep[2]))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1], ep[2]))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2])) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2]))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2]))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1], ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0], ep[1], ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0], ep[1], ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1] + cluster_list[c][i].w, ep[2])) < 1:
                                        Pallet_list_temp[j].eps_list.append((ep[0], ep[1] + cluster_list[c][i].w, ep[2]))
                                    else:
                                        Pallet_list_temp[j].eps_list.remove((ep[0], ep[1] + cluster_list[c][i].w, ep[2]))
                                        
                                    Pallet_list_temp[j].eps_list.remove(ep)
                                    break
                       #break out the pallet loop 
                       if indicator == True:
                           break
                if i == len(cluster_list[c])-1:
                    Pallet_index = [pal for pal in Pallet_index if sol_package[pal] == []]
    return sol_package,sol_pacposition,Box_list_temp,Pallet_list_temp

#GREEDY ROUTE            
def Greedyroute(T_list:list,desmap:list) -> list:
    Truck_list = copy.deepcopy(T_list)
    sol_route = [[] for i in range(len(Truck_list))]
    for i in range(len(sol_route)):
        for j in range(len(Truck_list[i].D)):
            #get next destination
            if j == 0:
                Next_destination = Min_distanceID(-1,Truck_list[i].D,desmap)
            else:
                Next_destination = Min_distanceID(sol_route[i][-1],Truck_list[i].D,desmap)
            #record destination
            sol_route[i].append(Next_destination)
            Truck_list[i].D.remove(Next_destination)           
    return sol_route            
    
#Routing with insertion
def RoutingwithInsertion(T_list:list,desmap:list) -> list:
    Truck_list = copy.deepcopy(T_list)
    sol_route = [[] for i in range(len(Truck_list))]
    for i in range(len(sol_route)):
        for j in range(len(Truck_list[i].D)):
            if j == 0:
                Next_destination = Min_distanceID(-1,Truck_list[i].D,desmap)
                sol_route[i].append(Next_destination)
                Truck_list[i].D.remove(Next_destination)
            else:
                I_cost = 10**9
                for k in range(len(sol_route[i]) + 1):
                    if k == 0:
                        new_cost = Insert_cost(-1,sol_route[i][k],Truck_list[i].D[0],desmap)
                    elif k == len(sol_route[i]):
                        new_cost = Insert_cost(sol_route[i][k-1],-1,Truck_list[i].D[0],desmap)
                    else:
                        new_cost = Insert_cost(sol_route[i][k-1],sol_route[i][k],Truck_list[i].D[0],desmap)
                    if new_cost <= I_cost:
                        I_cost = new_cost
                        I_index = k    
                #insert & remove
                sol_route[i] = sol_route[i][:I_index] + [Truck_list[i].D[0]] + sol_route[i][I_index:]
                Truck_list[i].D.pop(0)
    return sol_route

def route_remove(des:int,route:list,desmap:list) -> list:
    if len(route) == 1:
        new_route = []
        remove_cost = -Insert_cost(-1,-1,des,desmap)
    else:
        ind = route.index(des)
        if ind == 0:
            new_route = route[1:]
            remove_cost = -Insert_cost(-1,route[ind+1],des,desmap)
        elif ind == len(route)-1 :
            new_route = route[:-1]
            remove_cost = -Insert_cost(route[ind-1],-1,des,desmap)
        else:
            new_route = route[:ind] + route[ind+1:]
            remove_cost = -Insert_cost(route[ind-1],route[ind+1],des,desmap)
    
    return new_route,remove_cost

def best_insert(des:int,route:list,desmap:list) -> list:
    I_cost = 10**9
    if route == []:
        route = [des]
        I_cost = Insert_cost(-1,-1,des,desmap)
    elif des in route:
        I_cost = 0
    else:
        for k in range(len(route) + 1):
            if k == 0:
                new_cost = Insert_cost(-1,route[k],des,desmap)
            elif k == len(route):
                new_cost = Insert_cost(route[k-1],-1,des,desmap)
            else:
                new_cost = Insert_cost(route[k-1],route[k],des,desmap)
            if new_cost <= I_cost:
                I_cost = new_cost
                I_index = k    
        #insert
        route = route[:I_index] + [des] + route[I_index:]
    return route,I_cost