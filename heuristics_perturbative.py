# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:34:47 2023

@author: Joshua Liu
"""
import copy
import numpy as np
import math
from general_function import Insert_cost,best_insert, \
    Total_cost,find_element,route_remove,Swapneigh_cost

def perturbbox(dimension:bool,sol_package:list,sol_pacposition:list,
               sol_load:list,sol_route:list,B_list:list,P_list:list,
               T_list:list,desmap:list) -> list:
    Box_list = copy.deepcopy(B_list)
    Pallet_list = copy.deepcopy(P_list)
    Truck_list = copy.deepcopy(T_list)
    #current cost
    sol_cost = Total_cost(sol_package,sol_load,sol_route,Pallet_list,Truck_list,desmap)
    for temp in range(1000):
        rannum = np.random.randint(6)
        #box packing swap
        if rannum < 1:
            #generate swap
            used_pallet = [i for i, j in enumerate(sol_package) if j]
            if len(used_pallet) > 1:
                j_1,j_2 = np.random.choice(used_pallet,2,replace=False)
                i_1 = np.random.choice(sol_package[j_1])
                i_2 = np.random.choice(sol_package[j_2])
                if dimension==False:  
                    #check capacity
                    if Box_list[i_1].v <= Pallet_list[j_2].rest_V + Box_list[i_2].v and \
                        Box_list[i_2].v <= Pallet_list[j_1].rest_V + Box_list[i_1].v:
                            temp_package = copy.deepcopy(sol_package)
                            temp_route = copy.deepcopy(sol_route)
                            temp_cost = sol_cost
                            #find destinations of truck
                            j1_truck = find_element(j_1,sol_load)
                            j2_truck = find_element(j_2,sol_load)
                            j1i1_truckbox = [box for pal in sol_load[j1_truck] for box in sol_package[pal] if box !=i_1]
                            j2i2_truckbox = [box for pal in sol_load[j2_truck] for box in sol_package[pal] if box !=i_2]
                            j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                            j2i2_des = [Box_list[box].D for box in j2i2_truckbox]
                            #move destinations & update cost
                            if j1_truck != j2_truck:
                                if Box_list[i_1].D not in j1i1_des:
                                    j1_remove = route_remove(Box_list[i_1].D,temp_route[j1_truck],desmap)
                                    temp_route[j1_truck] = j1_remove[0]
                                    temp_cost += j1_remove[1]
                                j1_insert = best_insert(Box_list[i_2].D,temp_route[j1_truck],desmap)
                                temp_route[j1_truck] = j1_insert[0]
                                temp_cost += j1_insert[1]
                                if Box_list[i_2].D not in j2i2_des:
                                    j2_remove = route_remove(Box_list[i_2].D,temp_route[j2_truck],desmap)
                                    temp_route[j2_truck] = j2_remove[0]
                                    temp_cost += j2_remove[1]
                                j2_insert = best_insert(Box_list[i_1].D,temp_route[j2_truck],desmap)
                                temp_route[j2_truck] = j2_insert[0]
                                temp_cost += j2_insert[1]
                            temp_package[j_1] = [i_2 if item == i_1 else item for item in temp_package[j_1]]
                            temp_package[j_2] = [i_1 if item == i_2 else item for item in temp_package[j_2]]
                            if temp_cost < sol_cost:
                                Pallet_list[j_1].rest_V += Box_list[i_1].v - Box_list[i_2].v
                                Pallet_list[j_2].rest_V += Box_list[i_2].v - Box_list[i_1].v
                                sol_package = temp_package
                                sol_route = temp_route
                                sol_cost = temp_cost
                else:
                    if Box_list[i_1].v <= Pallet_list[j_2].rest_V + Box_list[i_2].v and \
                        Box_list[i_2].v <= Pallet_list[j_1].rest_V + Box_list[i_1].v:
                            temp_package = copy.deepcopy(sol_package)
                            temp_package[j_1] = [i_2 if item == i_1 else item for item in temp_package[j_1]]
                            temp_package[j_2] = [i_1 if item == i_2 else item for item in temp_package[j_2]]
                            temp_pos = copy.deepcopy(sol_pacposition)
                            temp_pos[j_1] = []
                            temp_pos[j_2] = []
                            eps_1 = [(0, 0, 0)]
                            eps_2 = [(0, 0, 0)]
                            #check 3d capacity of pallet j_1
                            for i in temp_package[j_1]:
                                eps = sorted(eps_1, key=lambda ep: (ep[0], ep[1], ep[2]))
                                for ep in eps:
                                    size_condition = False
                                    for ep2 in eps:
                                        if ep2 != ep:
                                            if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                                if ep[0] + Box_list[i].l > ep2[0]:
                                                    size_condition = True
                                                    break
                                            elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                                if ep[1] + Box_list[i].w > ep2[1]:
                                                    size_condition = True
                                                    break
                                    if ep[0] + Box_list[i].l <= Pallet_list[j_1].L and \
                                        ep[2] + Box_list[i].h <= Pallet_list[j_1].H and \
                                         ep[1] + Box_list[i].w <= Pallet_list[j_1].W and not size_condition:
                                             temp_pos[j_1].append(ep)
                                                 
                                             if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                                 eps_1.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                             else:
                                                 eps_1.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                                 eps_1.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                             else:
                                                 eps_1.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                                 eps_1.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                             else:
                                                 eps_1.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                                 eps_1.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                             else:
                                                 eps_1.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                                 eps_1.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                             else:
                                                 eps_1.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                                 eps_1.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                             else:
                                                 eps_1.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                                 eps_1.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                             else:
                                                 eps_1.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                                 
                                             eps_1.remove(ep)
                                             break
                            #check 3d capacity of pallet j_2
                            for i in temp_package[j_2]:
                                eps = sorted(eps_2, key=lambda ep: (ep[0], ep[1], ep[2]))
                                for ep in eps:
                                    size_condition = False
                                    for ep2 in eps:
                                        if ep2 != ep:
                                            if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                                if ep[0] + Box_list[i].l > ep2[0]:
                                                    size_condition = True
                                                    break
                                            elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                                if ep[1] + Box_list[i].w > ep2[1]:
                                                    size_condition = True
                                                    break
                                    if ep[0] + Box_list[i].l <= Pallet_list[j_2].L and \
                                        ep[2] + Box_list[i].h <= Pallet_list[j_2].H and \
                                         ep[1] + Box_list[i].w <= Pallet_list[j_2].W and not size_condition:
                                             temp_pos[j_2].append(ep)
                                                 
                                             if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                                 eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                             else:
                                                 eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                                 eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                             else:
                                                 eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                                 eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                             else:
                                                 eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                             if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                                 eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                             else:
                                                 eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                                 eps_2.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                             else:
                                                 eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                                 eps_2.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                             else:
                                                 eps_2.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                             if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                                 eps_2.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                             else:
                                                 eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                                 
                                             eps_2.remove(ep)
                                             break
                            if len(temp_package[j_1]) == len(temp_pos[j_1]) and len(temp_package[j_2]) == len(temp_pos[j_2]):
                                temp_route = copy.deepcopy(sol_route)
                                temp_cost = sol_cost
                                j1_truck = find_element(j_1,sol_load)
                                j2_truck = find_element(j_2,sol_load)
                                j1i1_truckbox = [box for pal in sol_load[j1_truck] for box in sol_package[pal] if box !=i_1]
                                j2i2_truckbox = [box for pal in sol_load[j2_truck] for box in sol_package[pal] if box !=i_2]
                                j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                                j2i2_des = [Box_list[box].D for box in j2i2_truckbox]
                                #move destinations
                                if j1_truck != j2_truck:
                                    if Box_list[i_1].D not in j1i1_des:
                                        j1_remove = route_remove(Box_list[i_1].D,temp_route[j1_truck],desmap)
                                        temp_route[j1_truck] = j1_remove[0]
                                        temp_cost += j1_remove[1]
                                    j1_insert = best_insert(Box_list[i_2].D,temp_route[j1_truck],desmap)
                                    temp_route[j1_truck] = j1_insert[0]
                                    temp_cost += j1_insert[1]
                                    if Box_list[i_2].D not in j2i2_des:
                                        j2_remove = route_remove(Box_list[i_2].D,temp_route[j2_truck],desmap)
                                        temp_route[j2_truck] = j2_remove[0]
                                        temp_cost += j2_remove[1]
                                    j2_insert = best_insert(Box_list[i_1].D,temp_route[j2_truck],desmap)
                                    temp_route[j2_truck] = j2_insert[0]
                                    temp_cost += j2_insert[1]
                                if temp_cost < sol_cost:
                                    Pallet_list[j_1].rest_V += Box_list[i_1].v - Box_list[i_2].v
                                    Pallet_list[j_2].rest_V += Box_list[i_2].v - Box_list[i_1].v
                                    Pallet_list[j_1].eps_list = eps_1
                                    Pallet_list[j_2].eps_list = eps_2
                                    sol_package = temp_package
                                    sol_pacposition = temp_pos
                                    sol_route = temp_route
                                    sol_cost = temp_cost
                                
        #pallet packing swap
        elif rannum < 2:
            #generate swap
            used_truck = [i for i, j in enumerate(sol_load) if j]
            if len(used_truck) > 1:
                j_1,j_2 = np.random.choice(used_truck,2,replace=False)
                i_1 = np.random.choice(sol_load[j_1])
                i_2 = np.random.choice(sol_load[j_2])
                if Pallet_list[i_1].V <= Truck_list[j_2].rest_T + Pallet_list[i_2].V and \
                    Pallet_list[i_2].V <= Truck_list[j_1].rest_T + Pallet_list[i_1].V:
                        temp_load = copy.deepcopy(sol_load)
                        temp_route = copy.deepcopy(sol_route)
                        temp_cost = sol_cost
                        #get destinatons of pallets and trucks
                        i1_des = list(set([Box_list[box].D for box in sol_package[i_1]]))
                        i2_des = list(set([Box_list[box].D for box in sol_package[i_2]]))
                        j1i1_truckbox = [box for pal in sol_load[j_1] for box in sol_package[pal] if pal !=i_1]
                        j2i2_truckbox = [box for pal in sol_load[j_2] for box in sol_package[pal] if pal !=i_2]
                        j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                        j2i2_des = [Box_list[box].D for box in j2i2_truckbox]
                        #move destinations
                        for des in i1_des:
                            if des not in j1i1_des:
                                j1_remove = route_remove(des,temp_route[j_1],desmap)
                                temp_route[j_1] = j1_remove[0]
                                temp_cost += j1_remove[1]
                        for des in i2_des:
                            if des not in j2i2_des:
                                j2_remove = route_remove(des,temp_route[j_2],desmap)
                                temp_route[j_2] = j2_remove[0]
                                temp_cost += j2_remove[1]
                            j1_insert = best_insert(des,temp_route[j_1],desmap)
                            temp_route[j_1] = j1_insert[0]
                            temp_cost += j1_insert[1]
                        for des in i1_des:
                            j2_insert = best_insert(des,temp_route[j_2],desmap)
                            temp_route[j_2] = j2_insert[0]
                            temp_cost += j2_insert[1]
                        temp_load[j_1] = [i_2 if item == i_1 else item for item in temp_load[j_1]]
                        temp_load[j_2] = [i_1 if item == i_2 else item for item in temp_load[j_2]]
                        if temp_cost < sol_cost:
                            Truck_list[j_1].rest_T += Pallet_list[i_1].V - Pallet_list[i_2].V
                            Truck_list[j_2].rest_T += Pallet_list[i_2].V - Pallet_list[i_1].V
                            sol_load = temp_load
                            sol_route = temp_route
                            sol_cost = temp_cost
                        
        #box packing insert
        elif rannum < 3:
            #generate insert choice
            used_pallet = [i for i, j in enumerate(sol_package) if j]
            if len(used_pallet) > 1:
                j_1,j_2 = np.random.choice(used_pallet,2,replace=False)
                i_1 = np.random.choice(sol_package[j_1])
                if dimension==False:  
                    #check capacity
                    if Box_list[i_1].v <= Pallet_list[j_2].rest_V:
                        temp_package = copy.deepcopy(sol_package)
                        temp_load = copy.deepcopy(sol_load)
                        temp_route = copy.deepcopy(sol_route)
                        temp_cost = sol_cost
                        #get truck destinations
                        j1_truck = find_element(j_1,sol_load)
                        j2_truck = find_element(j_2,sol_load)
                        j1i1_truckbox = [box for pal in sol_load[j1_truck] for box in sol_package[pal] if box != i_1]
                        j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                        #move destination
                        if j1_truck != j2_truck:
                            if Box_list[i_1].D not in j1i1_des:
                                j1_remove = route_remove(Box_list[i_1].D,temp_route[j1_truck],desmap)
                                temp_route[j1_truck] = j1_remove[0]
                                temp_cost += j1_remove[1]
                            j2_insert = best_insert(Box_list[i_1].D,temp_route[j2_truck],desmap)
                            temp_route[j2_truck] = j2_insert[0]
                            temp_cost += j2_insert[1]
                        temp_package[j_1].remove(i_1)
                        temp_package[j_2].append(i_1)
                        #get rid of empty pallet
                        if temp_package[j_1] == []:
                            temp_load[j1_truck].remove(j_1)
                            temp_cost -= Pallet_list[j_1].c
                        if temp_cost < sol_cost:
                            Pallet_list[j_1].rest_V += Box_list[i_1].v
                            Pallet_list[j_2].rest_V -= Box_list[i_1].v
                            sol_package = temp_package
                            sol_load = temp_load
                            sol_route = temp_route
                            sol_cost = temp_cost
                else:
                    if Box_list[i_1].v <= Pallet_list[j_2].rest_V:
                        temp_package = copy.deepcopy(sol_package)
                        temp_package[j_1].remove(i_1)
                        temp_package[j_2].append(i_1)
                        temp_pos = copy.deepcopy(sol_pacposition)
                        temp_pos[j_1] = []
                        temp_pos[j_2] = []
                        eps_1 = [(0, 0, 0)]
                        eps_2 = [(0, 0, 0)]
                        #check 3d capacity for j_1
                        for i in temp_package[j_1]:
                            eps = sorted(eps_1, key=lambda ep: (ep[0], ep[1], ep[2]))
                            for ep in eps:
                                size_condition = False
                                for ep2 in eps:
                                    if ep2 != ep:
                                        if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                            if ep[0] + Box_list[i].l > ep2[0]:
                                                size_condition = True
                                                break
                                        elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                            if ep[1] + Box_list[i].w > ep2[1]:
                                                size_condition = True
                                                break
                                if ep[0] + Box_list[i].l <= Pallet_list[j_1].L and \
                                    ep[2] + Box_list[i].h <= Pallet_list[j_1].H and \
                                     ep[1] + Box_list[i].w <= Pallet_list[j_1].W and not size_condition:
                                         temp_pos[j_1].append(ep)
                                             
                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_1.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_1.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                             eps_1.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                         else:
                                             eps_1.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_1.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_1.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_1.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_1.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_1.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_1.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_1.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_1.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_1.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_1.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                             
                                         eps_1.remove(ep)
                                         break
                        #check 3d capacity for j_2
                        for i in temp_package[j_2]:
                            eps = sorted(eps_2, key=lambda ep: (ep[0], ep[1], ep[2]))
                            for ep in eps:
                                size_condition = False
                                for ep2 in eps:
                                    if ep2 != ep:
                                        if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                            if ep[0] + Box_list[i].l > ep2[0]:
                                                size_condition = True
                                                break
                                        elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                            if ep[1] + Box_list[i].w > ep2[1]:
                                                size_condition = True
                                                break
                                if ep[0] + Box_list[i].l <= Pallet_list[j_2].L and \
                                    ep[2] + Box_list[i].h <= Pallet_list[j_2].H and \
                                     ep[1] + Box_list[i].w <= Pallet_list[j_2].W and not size_condition:
                                         temp_pos[j_2].append(ep)
                                             
                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_2.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                             
                                         eps_2.remove(ep)
                                         break
                        if len(temp_package[j_1]) == len(temp_pos[j_1]) and len(temp_package[j_2]) == len(temp_pos[j_2]):
                            temp_route = copy.deepcopy(sol_route)
                            temp_load = copy.deepcopy(sol_load)
                            temp_cost = sol_cost
                            j1_truck = find_element(j_1,sol_load)
                            j2_truck = find_element(j_2,sol_load)
                            j1i1_truckbox = [box for pal in sol_load[j1_truck] for box in sol_package[pal] if box != i_1]
                            j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                            #move destinations
                            if j1_truck != j2_truck:
                                if Box_list[i_1].D not in j1i1_des:
                                    j1_remove = route_remove(Box_list[i_1].D,temp_route[j1_truck],desmap)
                                    temp_route[j1_truck] = j1_remove[0]
                                    temp_cost += j1_remove[1]
                                j2_insert = best_insert(Box_list[i_1].D,temp_route[j2_truck],desmap)
                                temp_route[j2_truck] = j2_insert[0]
                                temp_cost += j2_insert[1]
                            #get rid of empty pallet
                            if temp_package[j_1] == []:
                                temp_load[j1_truck].remove(j_1)
                                temp_cost -= Pallet_list[j_1].c
                            if temp_cost < sol_cost:
                                Pallet_list[j_1].rest_V += Box_list[i_1].v
                                Pallet_list[j_2].rest_V -= Box_list[i_1].v
                                Pallet_list[j_1].eps_list = eps_1
                                Pallet_list[j_2].eps_list = eps_2
                                sol_package = temp_package
                                sol_pacposition = temp_pos
                                sol_load = temp_load
                                sol_route = temp_route
                                sol_cost = temp_cost
                            
        #pallet packing insert
        elif rannum < 4:
            #generate insert index
            used_truck = [i for i, j in enumerate(sol_load) if j]
            if len(used_truck) > 1:
                j_1,j_2 = np.random.choice(used_truck,2,replace=False)
                i_1 = np.random.choice(sol_load[j_1])
                #check capacity
                if Pallet_list[i_1].V <= Truck_list[j_2].rest_T:
                    temp_load = copy.deepcopy(sol_load)
                    temp_route = copy.deepcopy(sol_route)
                    temp_cost = sol_cost
                    #get destination info
                    i1_des = list(set([Box_list[box].D for box in sol_package[i_1]]))
                    j1i1_truckbox = [box for pal in sol_load[j_1] for box in sol_package[pal] if pal !=i_1]
                    j1i1_des = [Box_list[box].D for box in j1i1_truckbox]
                    #move destinations
                    for des in i1_des:
                        if des not in j1i1_des:
                            j1_remove = route_remove(des,temp_route[j_1],desmap)
                            temp_route[j_1] = j1_remove[0]
                            temp_cost += j1_remove[1]
                        j2_insert = best_insert(des,temp_route[j_2],desmap)
                        temp_route[j_2] = j2_insert[0]
                        temp_cost += j2_insert[1]
                    temp_load[j_1].remove(i_1)
                    temp_load[j_2].append(i_1)
                    #get rid of empty truck
                    if temp_load[j_1] == []:
                        temp_cost -= Truck_list[j_1].C
                    if temp_cost < sol_cost:
                        Truck_list[j_1].rest_T += Pallet_list[i_1].V
                        Truck_list[j_2].rest_T -= Pallet_list[i_1].V
                        sol_load = temp_load
                        sol_route = temp_route
                        sol_cost = temp_cost

        #box degrading
        elif rannum < 5:
            #generate degrading index
            used_pallet = [i for i, j in enumerate(sol_package) if j]
            unused_pallet = [i for i, j in enumerate(sol_package) if not j]
            if len(unused_pallet) != 0:
                j_1 = np.random.choice(used_pallet)
                j_2 = np.random.choice(unused_pallet)
                
                if dimension==False:  
                    #check capacity
                    j1_truck = find_element(j_1,sol_load)
                    if Pallet_list[j_1].V - Pallet_list[j_1].rest_V <= Pallet_list[j_2].rest_V \
                        and Pallet_list[j_2].V <= Truck_list[j1_truck].rest_T + Pallet_list[j_1].V:
                        temp_package = copy.deepcopy(sol_package)
                        temp_load = copy.deepcopy(sol_load)
                        temp_package[j_2] = temp_package[j_1]
                        temp_package[j_1] = []
                        temp_load[j1_truck] = [pal if pal != j_1 else j_2 for pal in temp_load[j1_truck]]
                        temp_cost = sol_cost - Pallet_list[j_1].c + Pallet_list[j_2].c
                        if temp_cost < sol_cost:
                            Truck_list[j1_truck].rest_T += Pallet_list[j_1].V - Pallet_list[j_2].V
                            Pallet_list[j_2].rest_V -= Pallet_list[j_1].V - Pallet_list[j_1].rest_V
                            Pallet_list[j_1].rest_V = Pallet_list[j_1].V
                            sol_package = temp_package
                            sol_load = temp_load
                            sol_cost = temp_cost
                else:
                    #check capacity
                    j1_truck = find_element(j_1,sol_load)
                    if Pallet_list[j_1].V - Pallet_list[j_1].rest_V <= Pallet_list[j_2].rest_V \
                        and Pallet_list[j_2].V <= Truck_list[j1_truck].rest_T + Pallet_list[j_1].V:
                        temp_package = copy.deepcopy(sol_package)
                        temp_load = copy.deepcopy(sol_load)
                        temp_pos = copy.deepcopy(sol_pacposition)
                        temp_package[j_2] = temp_package[j_1]
                        temp_package[j_1] = []
                        temp_pos[j_1] = []
                        temp_pos[j_2] = []
                        eps_1 = [(0, 0, 0)]
                        eps_2 = [(0, 0, 0)]
                        #check 3d capacity of pallet j_2
                        for i in temp_package[j_2]:
                            eps = sorted(eps_2, key=lambda ep: (ep[0], ep[1], ep[2]))
                            for ep in eps:
                                size_condition = False
                                for ep2 in eps:
                                    if ep2 != ep:
                                        if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                            if ep[0] + Box_list[i].l > ep2[0]:
                                                size_condition = True
                                                break
                                        elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                            if ep[1] + Box_list[i].w > ep2[1]:
                                                size_condition = True
                                                break
                                if ep[0] + Box_list[i].l <= Pallet_list[j_2].L and \
                                    ep[2] + Box_list[i].h <= Pallet_list[j_2].H and \
                                     ep[1] + Box_list[i].w <= Pallet_list[j_2].W and not size_condition:
                                         temp_pos[j_2].append(ep)
                                             
                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                         if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                             eps_2.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                         else:
                                             eps_2.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                         if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                             eps_2.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                         else:
                                             eps_2.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                             
                                         eps_2.remove(ep)
                                         break
                        if len(temp_package[j_2]) == len(temp_pos[j_2]):
                            temp_load[j1_truck] = [pal if pal != j_1 else j_2 for pal in temp_load[j1_truck]]
                            temp_cost = sol_cost - Pallet_list[j_1].c + Pallet_list[j_2].c
                            if temp_cost < sol_cost:
                                Truck_list[j1_truck].rest_T += Pallet_list[j_1].V - Pallet_list[j_2].V
                                Pallet_list[j_2].rest_V -= Pallet_list[j_1].V - Pallet_list[j_1].rest_V
                                Pallet_list[j_1].rest_V = Pallet_list[j_1].V
                                Pallet_list[j_1].eps_list = eps_1
                                Pallet_list[j_2].eps_list = eps_2
                                sol_package = temp_package
                                sol_pacposition = temp_pos
                                sol_load = temp_load
                                sol_cost = temp_cost
        
        #pallet degrading
        elif rannum < 6:
            #generate degrading index
            used_truck = [i for i, j in enumerate(sol_load) if j]
            unused_truck = [i for i, j in enumerate(sol_load) if not j]
            if len(unused_truck) != 0:
                j_1 = np.random.choice(used_truck)
                j_2 = np.random.choice(unused_truck)
                #check capacity
                if Truck_list[j_1].T - Truck_list[j_1].rest_T <= Truck_list[j_2].rest_T:
                    temp_load = copy.deepcopy(sol_load)
                    temp_route = copy.deepcopy(sol_route)
                    temp_load[j_2] = temp_load[j_1]
                    temp_load[j_1] = []
                    temp_route[j_2] = temp_route[j_1]
                    temp_route[j_1] = []
                    temp_cost = sol_cost - Truck_list[j_1].C + Truck_list[j_2].C
                    if temp_cost < sol_cost:
                        Truck_list[j_2].rest_T -= Truck_list[j_1].T - Truck_list[j_1].rest_T
                        Truck_list[j_1].rest_T = Truck_list[j_1].T
                        sol_load = temp_load
                        sol_route = temp_route
                        sol_cost = temp_cost
            
    return sol_package,sol_pacposition,sol_load,sol_route




#destination swap
def perturbdes(dimension:bool,sol_package:list,sol_pacposition:list,
               sol_load:list,sol_route:list,P_list:list,
               T_list:list,desmap:list) -> list:
    Pallet_list = copy.deepcopy(P_list)
    Truck_list = copy.deepcopy(T_list)
     
    sol_cost = Total_cost(sol_package,sol_load,sol_route,Pallet_list,Truck_list,desmap)
    Record_cost=[sol_cost]
    Record_route=[sol_route]
    for temperature in np.logspace(0,6,1000)[::-1]:
        #get swapable truck index
        swapable_truck = [tr for tr in range(len(sol_route)) if len(sol_route[tr]) >= 2]
        j_1 = np.random.choice(swapable_truck)
        temp_route = copy.deepcopy(sol_route)
        j1_route = temp_route[j_1]
        [i_1,i_2]=sorted(np.random.choice(len(j1_route),2,replace=False))
        temp_route[j_1] = j1_route[:i_1]+j1_route[i_2:i_2+1]+j1_route[i_1+1:i_2] \
                +j1_route[i_1:i_1+1]+j1_route[i_2+1:]
        if i_2 == i_1+1:
            if i_1 == 0:
                if i_2 == len(j1_route)-1:
                    temp_cost = sol_cost + Swapneigh_cost(-1,j1_route[i_1],j1_route[i_2],-1, desmap)
                else:
                    temp_cost = sol_cost + Swapneigh_cost(-1,j1_route[i_1],j1_route[i_2],j1_route[i_2+1], desmap)
            else:
                if i_2 == len(j1_route)-1:
                    temp_cost = sol_cost + Swapneigh_cost(j1_route[i_1-1],j1_route[i_1],j1_route[i_2],-1, desmap)
                else:
                    temp_cost = sol_cost + Swapneigh_cost(j1_route[i_1-1],j1_route[i_1],j1_route[i_2],j1_route[i_2+1], desmap)
        else:
            if i_1 == 0:
                if i_2 == len(j1_route)-1:
                    temp_cost = sol_cost - Insert_cost(-1,j1_route[i_1+1],j1_route[i_1],desmap) \
                        - Insert_cost(j1_route[i_2-1],-1,j1_route[i_2],desmap) \
                            + Insert_cost(-1,j1_route[i_1+1],j1_route[i_2],desmap) \
                                + Insert_cost(j1_route[i_2-1],-1,j1_route[i_1],desmap)
                else:
                    temp_cost = sol_cost - Insert_cost(-1,j1_route[i_1+1],j1_route[i_1],desmap) \
                        - Insert_cost(j1_route[i_2-1],j1_route[i_2+1],j1_route[i_2],desmap) \
                            + Insert_cost(-1,j1_route[i_1+1],j1_route[i_2],desmap) \
                                + Insert_cost(j1_route[i_2-1],j1_route[i_2+1],j1_route[i_1],desmap)
            else:
                if i_2 == len(j1_route)-1:
                    temp_cost = sol_cost - Insert_cost(j1_route[i_1-1],j1_route[i_1+1],j1_route[i_1],desmap) \
                        - Insert_cost(j1_route[i_2-1],-1,j1_route[i_2],desmap) \
                            + Insert_cost(j1_route[i_1-1],j1_route[i_1+1],j1_route[i_2],desmap) \
                                + Insert_cost(j1_route[i_2-1],-1,j1_route[i_1],desmap)
                else:
                    temp_cost = sol_cost - Insert_cost(j1_route[i_1-1],j1_route[i_1+1],j1_route[i_1],desmap) \
                        - Insert_cost(j1_route[i_2-1],j1_route[i_2+1],j1_route[i_2],desmap) \
                            + Insert_cost(j1_route[i_1-1],j1_route[i_1+1],j1_route[i_2],desmap) \
                                + Insert_cost(j1_route[i_2-1],j1_route[i_2+1],j1_route[i_1],desmap)
        delta = sol_cost - temp_cost
        if math.exp((delta)/temperature) > np.random.rand():
            sol_route = temp_route
            sol_cost = temp_cost
            #Record
            Record_cost.append(sol_cost)
            Record_route.append(sol_route)
        
    sol_route = Record_route[Record_cost.index(min(Record_cost))]
            
    return sol_package,sol_pacposition,sol_load,sol_route