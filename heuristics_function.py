# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:47:09 2022

@author: Joshua Liu
"""

import copy
from statistics import mean
from general_function import Min_distance,Min_Bestpalletfit, \
                             Insert_cost,Total_cost, \
                             Cluster_BoxFit,Greedyroute


###3.0.0###
    
#BOX FIRST FIT
def Boxfirstfit(dimension:int,Box_list:list,Pallet_list:list) -> list:
    sol_package = [[] for i in range(len(Pallet_list))]
    sol_pacposition = [[] for i in range(len(Pallet_list))]
    for i in range(len(Box_list)):
       for j in range(len(Pallet_list)):
           #Check dimension
           if dimension==False:  
               #Check pallet capacity
               if Box_list[i].v <= Pallet_list[j].rest_V:
                   #PUT box i into the first pallet (j) which can contain it
                   sol_package[j].append(Box_list[i].ID)
                   #Calculate the rest capacity of pallet j
                   Pallet_list[j].rest_V -= Box_list[i].v
                   #record destinations
                   if Box_list[i].D not in Pallet_list[j].D:
                       Pallet_list[j].D.append(Box_list[i].D)
                   break
           else:
               indicator = False
               #Check pallet capacity
               if Box_list[i].v <= Pallet_list[j].rest_V:
                   #3d capacity
                   eps = sorted(Pallet_list[j].eps_list, 
                                key=lambda ep: (ep[0], ep[1], ep[2]))
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
                       #no overlap & no exceed
                       if ep[0] + Box_list[i].l <= Pallet_list[j].L and \
                           ep[2] + Box_list[i].h <= Pallet_list[j].H and \
                            ep[1] + Box_list[i].w <= Pallet_list[j].W and not size_condition:
                           indicator = True
                           #record position
                           sol_pacposition[j].append(ep)
                           #clean eps
                           if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                               Pallet_list[j].eps_list.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                           if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                               Pallet_list[j].eps_list.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                           if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                               Pallet_list[j].eps_list.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                           if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                               Pallet_list[j].eps_list.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                           if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                               Pallet_list[j].eps_list.append((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                           if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                               Pallet_list[j].eps_list.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                           if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                               Pallet_list[j].eps_list.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                           else:
                               Pallet_list[j].eps_list.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))

                           Pallet_list[j].eps_list.remove(ep)
                           #record packing
                           sol_package[j].append(Box_list[i].ID)
                           Pallet_list[j].rest_V -= Box_list[i].v
                           #record destinations
                           if Box_list[i].D not in Pallet_list[j].D:
                               Pallet_list[j].D.append(Box_list[i].D)
                           break
                   if indicator == True:
                       break
    return sol_package,sol_pacposition,Box_list,Pallet_list


#PALLET FIRST FIT
def Palletfirstfit(sol_package:list,Box_list:list,Pallet_list:list \
                   ,Truck_list:list) -> list:
    sol_load = [[] for i in range(len(Truck_list))]
    for i in range(len(Pallet_list)):
        #Check if the pallet is empty or not
        if sol_package[i] != []:            
            for j in range(len(Truck_list)):
                #Check truck capacity
                if Pallet_list[i].V <= Truck_list[j].rest_T:
                    #Put the pallet into the first truck which can contain it
                    sol_load[j].append(Pallet_list[i].ID)
                    #Calculate the rest capacity of truck j
                    Truck_list[j].rest_T -= Pallet_list[i].V
                    #Add destination to truck j
                    for d in Pallet_list[i].D:
                        if d not in Truck_list[j].D:
                            Truck_list[j].D.append(d)                  
                    break
    return sol_load,Truck_list

###3.1.1###
#BOX MEAN FIT
def Boxmeanbestfit(dimension:bool,Box_list:list,Pallet_list:list,desmap:list) -> list:
    sol_package = [[] for i in range(len(Pallet_list))]
    sol_pacposition = [[] for i in range(len(Pallet_list))]
    for i in range(len(Box_list)):
        Index = 0
        Position = (0,0,0)
        Mean_cost = 10**9
        Unavailable_pallet_num = 0
        #Check the num of pallet have already been used
        Pallet_Num_used = sum(p!=[] for p in sol_package)      
        if dimension==False:  
            for j in range(Pallet_Num_used):
                #Check the capacity of Pallet
                if Box_list[i].v <= Pallet_list[j].rest_V:
                    #Check the mean cost of every used available pallet and find the pallet with minial mean cost      
                    new_meancost = mean(desmap[Box_list[i].D+1][Box_list[b].D+1] for b in sol_package[j])
                    if new_meancost < Mean_cost:
                        Mean_cost = new_meancost
                        Index = j
                #If every used pallet is unavaible, add the box to a new empty pallet        
                else:
                    Unavailable_pallet_num += 1
                    if Unavailable_pallet_num == Pallet_Num_used:
                        Index = Pallet_Num_used          
            if Index <= len(Pallet_list) - 1:
                sol_package[Index].append(Box_list[i].ID)
                Pallet_list[Index].rest_V -= Box_list[i].v
                if Box_list[i].D not in Pallet_list[Index].D:
                    Pallet_list[Index].D.append(Box_list[i].D)
        else:
            for j in range(Pallet_Num_used):
                #Check the capacity of Pallet
                indicator = False
                if Box_list[i].v <= Pallet_list[j].rest_V:
                    #3d capacity
                    eps = sorted(Pallet_list[j].eps_list, 
                                 key=lambda ep: (ep[0], ep[1], ep[2]))
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
                        #no overlap & no exceed
                        if ep[0] + Box_list[i].l <= Pallet_list[j].L and \
                            ep[2] + Box_list[i].h <= Pallet_list[j].H and \
                             ep[1] + Box_list[i].w <= Pallet_list[j].W and not size_condition:
                                              
                                 indicator = True
                                 new_meancost = mean(desmap[Box_list[i].D+1][Box_list[b].D+1] for b in sol_package[j])
                                 if new_meancost < Mean_cost:
                                     Mean_cost = new_meancost
                                     Index = j
                                     Position = ep
                                 break
                if indicator == False:
                    Unavailable_pallet_num += 1
                    if Unavailable_pallet_num == Pallet_Num_used:
                        Index = Pallet_Num_used
            if Index <= len(Pallet_list) - 1:
                #record packing
                sol_package[Index].append(Box_list[i].ID)
                sol_pacposition[Index].append(Position)
                Pallet_list[Index].rest_V -= Box_list[i].v
                #record destinations
                if Box_list[i].D not in Pallet_list[Index].D:
                    Pallet_list[Index].D.append(Box_list[i].D)
                #record eps
                if Pallet_list[Index].eps_list.count((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h)) < 1:
                    Pallet_list[Index].eps_list.append((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))

                if Pallet_list[Index].eps_list.count((Position[0] + Box_list[i].l, Position[1], Position[2])) < 1:
                    Pallet_list[Index].eps_list.append((Position[0] + Box_list[i].l, Position[1], Position[2]))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0] + Box_list[i].l, Position[1], Position[2]))

                if Pallet_list[Index].eps_list.count((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2])) < 1:
                    Pallet_list[Index].eps_list.append((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2]))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2]))

                if Pallet_list[Index].eps_list.count((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h)) < 1:
                    Pallet_list[Index].eps_list.append((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h))

                if Pallet_list[Index].eps_list.count((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h)) < 1:
                    Pallet_list[Index].eps_list.append((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))

                if Pallet_list[Index].eps_list.count((Position[0], Position[1], Position[2] + Box_list[i].h)) < 1:
                   Pallet_list[Index].eps_list.append((Position[0], Position[1], Position[2] + Box_list[i].h))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0], Position[1], Position[2] + Box_list[i].h))

                if Pallet_list[Index].eps_list.count((Position[0], Position[1] + Box_list[i].w, Position[2])) < 1:
                    Pallet_list[Index].eps_list.append((Position[0], Position[1] + Box_list[i].w, Position[2]))
                else:
                    Pallet_list[Index].eps_list.remove((Position[0], Position[1] + Box_list[i].w, Position[2]))

                Pallet_list[Index].eps_list.remove(Position)
    return sol_package,sol_pacposition,Box_list,Pallet_list
        
#PALLET MEAN FIT
def Palletmeanbestfit(sol_package:list,Pallet_list:list,Truck_list:list,desmap:list) -> list:
    sol_load = [[] for i in range(len(Truck_list))]
    used_pallet = [i for i, j in enumerate(sol_package) if j]
    for i in used_pallet:
        Index = 0
        Mean_cost = 10**9
        Unavailable_truck_num = 0
        #Check the num of pallet have already been used
        Truck_Num_used = sum(tr!=[] for tr in sol_load)   
        for j in range(Truck_Num_used):
            #Check truck capacity
            if Pallet_list[i].V <= Truck_list[j].rest_T:
                #Check extra destination for the truck j after add the pallet i
                Extra_destination = [des for des in Pallet_list[i].D if des not in Truck_list[j].D]
                # if no extra destination, just put pallet i in the trcuk j
                if Extra_destination == []:
                    Index = j
                    break
                else:
                    new_cost = Min_Bestpalletfit(Extra_destination, Truck_list[j].D,desmap)
                    if new_cost < Mean_cost:
                        Mean_cost = new_cost
                        Index = j
            else:
                Unavailable_truck_num += 1
                if Unavailable_truck_num == Truck_Num_used:
                    Index = Truck_Num_used
        if Index <= len(Truck_list) - 1:
            #record packing
            sol_load[Index].append(Pallet_list[i].ID)
            Truck_list[Index].rest_T -= Pallet_list[i].V
            for d in Pallet_list[i].D:
                if d not in Truck_list[Index].D:
                    Truck_list[Index].D.append(d)
    return sol_load,Truck_list

###3.1.2###
#BOX ADJUST BEST FIT
def Boxajustbestfit(dimension:bool,Box_list:list,Pallet_list:list,desmap:list) -> list:
    sol_package = [[] for i in range(len(Pallet_list))]
    sol_pacposition = [[] for i in range(len(Pallet_list))]
    for i in range(len(Box_list)):
        #Pallet_index indicating which pallet is using for box i
        Pallet_index = 0
        Position = (0,0,0)
        Marginal_cost = 10**9
        if dimension==False:
            for j in range(len(Pallet_list)):
                if Box_list[i].v <= Pallet_list[j].rest_V:
                    #Marginalcost = the cheapest insertion + space 
                    Marginalcost_list = []
                    Addition_cost = Pallet_list[j].c*Box_list[i].v/Pallet_list[j].V
                    if Pallet_list[j].D == []:
                        new_cost = Insert_cost(-1, -1, Box_list[i].D,desmap)
                        Marginalcost_list.append(new_cost + Addition_cost)
                    else:                   
                        for p in range(len(Pallet_list[j].D) + 1):
                            if p == 0:
                                new_cost = Insert_cost(-1, Pallet_list[j].D[p], Box_list[i].D,desmap)
                            elif p == len(Pallet_list[j].D):
                                new_cost = Insert_cost(Pallet_list[j].D[p-1],-1, Box_list[i].D,desmap)
                            else:
                                new_cost = Insert_cost(Pallet_list[j].D[p-1],Pallet_list[j].D[p],Box_list[i].D,desmap)
                            Marginalcost_list.append(new_cost + Addition_cost)
                    new_marginalcost = min(Marginalcost_list)
                    if new_marginalcost < Marginal_cost:
                        Marginal_cost = new_marginalcost
                        Pallet_index = j
            #record packing
            sol_package[Pallet_index].append(Box_list[i].ID)
            Pallet_list[Pallet_index].rest_V -= Box_list[i].v
            if Box_list[i].D not in Pallet_list[Pallet_index].D:
                Pallet_list[Pallet_index].D.append(Box_list[i].D)
                
        else:
            for j in range(len(Pallet_list)):
                #Check the capacity of Pallet
                if Box_list[i].v <= Pallet_list[j].rest_V:
                    #3d capacity
                    eps = sorted(Pallet_list[j].eps_list, 
                                 key=lambda ep: (ep[0], ep[1], ep[2]))
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
                        #no overlap & no exceed
                        if ep[0] + Box_list[i].l <= Pallet_list[j].L and \
                            ep[2] + Box_list[i].h <= Pallet_list[j].H and \
                             ep[1] + Box_list[i].w <= Pallet_list[j].W and not size_condition:

                                 Marginalcost_list = []
                                 Addition_cost = Pallet_list[j].c*Box_list[i].v/Pallet_list[j].V
                                 if Pallet_list[j].D == []:
                                     new_cost = Insert_cost(-1, -1, Box_list[i].D,desmap)
                                     Marginalcost_list.append(new_cost + Addition_cost)
                                 else:                   
                                     for p in range(len(Pallet_list[j].D) + 1):
                                         if p == 0:
                                             new_cost = Insert_cost(-1, Pallet_list[j].D[p], Box_list[i].D,desmap)
                                         elif p == len(Pallet_list[j].D):
                                             new_cost = Insert_cost(Pallet_list[j].D[p-1],-1, Box_list[i].D,desmap)
                                         else:
                                             new_cost = Insert_cost(Pallet_list[j].D[p-1],Pallet_list[j].D[p],Box_list[i].D,desmap)
                                         Marginalcost_list.append(new_cost + Addition_cost)
                                 new_marginalcost = min(Marginalcost_list)
                                 if new_marginalcost < Marginal_cost:
                                     Marginal_cost = new_marginalcost
                                     Pallet_index = j
                                     Position = ep
                                 break
            #record packing
            sol_package[Pallet_index].append(Box_list[i].ID)
            sol_pacposition[Pallet_index].append(Position)
            Pallet_list[Pallet_index].rest_V -= Box_list[i].v
            #record destination
            if Box_list[i].D not in Pallet_list[Pallet_index].D:
                Pallet_list[Pallet_index].D.append(Box_list[i].D)
            #record eps
            if Pallet_list[Pallet_index].eps_list.count((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h)) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))

            if Pallet_list[Pallet_index].eps_list.count((Position[0] + Box_list[i].l, Position[1], Position[2])) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0] + Box_list[i].l, Position[1], Position[2]))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0] + Box_list[i].l, Position[1], Position[2]))

            if Pallet_list[Pallet_index].eps_list.count((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2])) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2]))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0] + Box_list[i].l, Position[1] + Box_list[i].w, Position[2]))

            if Pallet_list[Pallet_index].eps_list.count((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h)) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0] + Box_list[i].l, Position[1], Position[2] + Box_list[i].h))

            if Pallet_list[Pallet_index].eps_list.count((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h)) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0], Position[1] + Box_list[i].w, Position[2] + Box_list[i].h))

            if Pallet_list[Pallet_index].eps_list.count((Position[0], Position[1], Position[2] + Box_list[i].h)) < 1:
               Pallet_list[Pallet_index].eps_list.append((Position[0], Position[1], Position[2] + Box_list[i].h))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0], Position[1], Position[2] + Box_list[i].h))

            if Pallet_list[Pallet_index].eps_list.count((Position[0], Position[1] + Box_list[i].w, Position[2])) < 1:
                Pallet_list[Pallet_index].eps_list.append((Position[0], Position[1] + Box_list[i].w, Position[2]))
            else:
                Pallet_list[Pallet_index].eps_list.remove((Position[0], Position[1] + Box_list[i].w, Position[2]))

            Pallet_list[Pallet_index].eps_list.remove(Position)
                
    return sol_package,sol_pacposition,Box_list,Pallet_list                 
                
#PALLET ADJUST BEST FIT          
def Palletajustbestfit(sol_package:list,Pallet_list:list,Truck_list:list,desmap:list) -> list:
    sol_load = [[] for i in range(len(Truck_list))]
    used_pallet = [i for i, j in enumerate(sol_package) if j]
    for i in used_pallet:
        Truck_index = 0
        Marginal_cost = 10**9
        for j in range(len(Truck_list)):
            if Pallet_list[i].V <= Truck_list[j].rest_T:
                #compute marginal cost
                Marginalcost_list = []
                Addition_cost = Truck_list[j].C*Pallet_list[i].V/Truck_list[j].T  
                #insert cost for each new destination
                Extra_destination = [des for des in Pallet_list[i].D if des not in Truck_list[j].D]
                if Extra_destination == []:
                    Truck_index = j
                    break
                else:
                    if sol_load[j] == []:
                        new_cost = Min_distance(-1, Extra_destination,desmap)
                    else:                
                        new_cost = Min_Bestpalletfit(Extra_destination, Truck_list[j].D,desmap) 
                    Marginalcost_list.append(new_cost + Addition_cost)
                    new_marginalcost = min(Marginalcost_list)      
                    if new_marginalcost < Marginal_cost:
                        Marginal_cost = new_marginalcost
                        Truck_index = j
        #record packing
        sol_load[Truck_index].append(Pallet_list[i].ID)
        Truck_list[Truck_index].rest_T -= Pallet_list[i].V
        #record destination
        for d in Pallet_list[i].D:
            if d not in Truck_list[Truck_index].D:
                Truck_list[Truck_index].D.append(d)
            
    return sol_load,Truck_list

                

###3.2.1###
#SINGLE DESTINATION CLUSTER
def SDC_BoxFit(dimension:bool,Box_list:list,Pallet_list:list,desmap:list) -> list:
    sol_package = [[] for i in range(len(Pallet_list))]
    sol_pacposition = [[] for i in range(len(Pallet_list))]
    #convert the box in the same destination in clusters
    cluster_list = [[Box_list[i] for i in range(len(Box_list)) if Box_list[i].D == j]
                    for j in range(len(desmap)-1)]
    
    # packing box, add constraints to make sure each pallet has only one destination
    Pallet_index = [i for i in range(len(Pallet_list))]   
    for c in range(len(cluster_list)):
        for i in range(len(cluster_list[c])):
            if dimension==False:
                for j in Pallet_index:
                   #Check pallet capacity
                   if cluster_list[c][i].v <= Pallet_list[j].rest_V:
                       #PUT box i into the first pallet (j) which can contain it
                       sol_package[j].append(cluster_list[c][i].ID)
                       #Calculate the rest capacity of pallet j
                       Pallet_list[j].rest_V -= cluster_list[c][i].v
                       #Add destination into pallet list
                       if cluster_list[c][i].D not in Pallet_list[j].D:
                           Pallet_list[j].D.append(cluster_list[c][i].D)
                       break
                # once the box of one destination all packed, remove the index of the packed pallet
                # box with different destination have to pack in a new pallet
                if i == len(cluster_list[c])-1:
                    Pallet_index = [pal for pal in Pallet_index if sol_package[pal] == []]
            else:
                for j in Pallet_index:
                   indicator = False
                   #Check pallet capacity
                   if cluster_list[c][i].v <= Pallet_list[j].rest_V:
                       eps = sorted(Pallet_list[j].eps_list, 
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
                           if ep[0] + cluster_list[c][i].l <= Pallet_list[j].L and \
                               ep[2] + cluster_list[c][i].h <= Pallet_list[j].H and \
                                ep[1] + cluster_list[c][i].w <= Pallet_list[j].W and not size_condition:
                                    #PUT box i into the first pallet (j) which can contain it
                                    indicator = True
                                    sol_package[j].append(cluster_list[c][i].ID)
                                    sol_pacposition[j].append(ep)
                                    #Calculate the rest capacity of pallet j
                                    Pallet_list[j].rest_V -= cluster_list[c][i].v
                                    #Add destination into pallet list
                                    if cluster_list[c][i].D not in Pallet_list[j].D:
                                        Pallet_list[j].D.append(cluster_list[c][i].D)
                                        
                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1], ep[2])) < 1:
                                        Pallet_list[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1], ep[2]))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1], ep[2]))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2])) < 1:
                                        Pallet_list[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2]))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1] + cluster_list[c][i].w, ep[2]))

                                    if eps.count((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list[j].eps_list.append((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0] + cluster_list[c][i].l, ep[1], ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list[j].eps_list.append((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0], ep[1] + cluster_list[c][i].w, ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1], ep[2] + cluster_list[c][i].h)) < 1:
                                        Pallet_list[j].eps_list.append((ep[0], ep[1], ep[2] + cluster_list[c][i].h))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0], ep[1], ep[2] + cluster_list[c][i].h))

                                    if eps.count((ep[0], ep[1] + cluster_list[c][i].w, ep[2])) < 1:
                                        Pallet_list[j].eps_list.append((ep[0], ep[1] + cluster_list[c][i].w, ep[2]))
                                    else:
                                        Pallet_list[j].eps_list.remove((ep[0], ep[1] + cluster_list[c][i].w, ep[2]))
                                        
                                    Pallet_list[j].eps_list.remove(ep)
                                    break
                       if indicator == True:
                           break
                #remove used pallet
                if i == len(cluster_list[c])-1:
                    Pallet_index = [pal for pal in Pallet_index if sol_package[pal] == []]
                    
    return sol_package,sol_pacposition,Box_list,Pallet_list

###3.2.2###
#K DESTINATION CLUSTER
def KDC_BoxFit(dimension:bool,Box_list:list,Pallet_list:list,Truck_list:list,desmap:list) -> list:
    #loop Cluster_BoxFit with different K to compare, to choose the best K
    
    best_cost = 10**9
    #number of clusters to be considered
    for k in range(1,5):  
        
        Box_list_temp = copy.deepcopy(Box_list)
        Pallet_list_temp = copy.deepcopy(Pallet_list)
        Truck_list_temp = copy.deepcopy(Truck_list)
        
        sol_pack = Cluster_BoxFit (k,dimension,Box_list_temp,Pallet_list_temp,desmap)
        sol_package = sol_pack[0]
        sol_pacposition = sol_pack[1]
        Box_list_temp = sol_pack[2]
        Pallet_list_temp = sol_pack[3]
        
        #loading and routing first to calculate the total cost
        sol_temp = Palletfirstfit(sol_package,Box_list_temp,Pallet_list_temp,Truck_list_temp)
        sol_load = sol_temp[0]
        Truck_list_temp = sol_temp[1]
        sol_route = Greedyroute(Truck_list_temp,desmap)       
        
                            
        #compare solutions with different k
        new_cost = Total_cost(sol_package,sol_load,sol_route,Pallet_list_temp,Truck_list_temp,desmap)
        if new_cost <= best_cost:
            best_sol_package = sol_package
            best_sol_load = sol_load
            best_sol_pacposition = sol_pacposition
            best_sol_route = sol_route
            best_Box_list = Box_list_temp
            best_Pallet_list = Pallet_list_temp
            best_Truck_list = Truck_list_temp
            best_cost = new_cost    
                    
    return best_sol_package,best_sol_load,best_sol_route,best_sol_pacposition,best_Box_list,best_Pallet_list,best_Truck_list
                
###3.2.3###
#PRELOAD
def Pallet_preload(dimension:bool,Box_list:list,Pallet_list:list,Truck_list:list) -> list:
    # load pallet into truck first
    sol_package = [[] for i in range(len(Pallet_list))]
    sol_pacposition = [[] for i in range(len(Pallet_list))]
    sol_load = [[] for i in range(len(Truck_list))]
    for i in range(len(Pallet_list)):           
        for j in range(len(Truck_list)):
            if Pallet_list[i].V <= Truck_list[j].rest_T:  
                sol_load[j].append(Pallet_list[i].ID)
                Truck_list[j].rest_T -= Pallet_list[i].V
                break

    #sweep packing the box into loaded pallet           
    Box_Dsortlist = sorted(Box_list, key=lambda Box_list: (Box_list.D))
    Box_index = [b.ID for b in Box_Dsortlist]

    # using sequence index, once the box is packed, the index would be remove 
    unused_pallet = []
    for j in range(len(sol_load)):
       for k in range(len(sol_load[j])):
           for i in Box_index:
               if dimension==False:
                   if Box_list[i].v <= Pallet_list[sol_load[j][k]].rest_V:
                       sol_package[sol_load[j][k]].append(Box_list[i].ID)
                       Pallet_list[sol_load[j][k]].rest_V -= Box_list[i].v
                       if Box_list[i].D not in Pallet_list[sol_load[j][k]].D:
                           Pallet_list[sol_load[j][k]].D.append(Box_list[i].D)
                       if Box_list[i].D not in Truck_list[j].D:
                           Truck_list[j].D.append(Box_list[i].D)
                       Box_index.remove(i)
               else:
                   if Box_list[i].v <= Pallet_list[sol_load[j][k]].rest_V:
                       eps = sorted(Pallet_list[sol_load[j][k]].eps_list, 
                                    key=lambda ep: (ep[0], ep[1], ep[2]))
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
                           if ep[0] + Box_list[i].l <= Pallet_list[sol_load[j][k]].L and \
                               ep[2] + Box_list[i].h <= Pallet_list[sol_load[j][k]].H and \
                                ep[1] + Box_list[i].w <= Pallet_list[sol_load[j][k]].W and not size_condition:
                                    #PUT box i into the first pallet (j) which can contain it
                                    sol_package[sol_load[j][k]].append(Box_list[i].ID)
                                    sol_pacposition[sol_load[j][k]].append(ep)
                                    #Calculate the rest capacity of pallet j
                                    Pallet_list[sol_load[j][k]].rest_V -= Box_list[i].v
                                    if Box_list[i].D not in Pallet_list[sol_load[j][k]].D:
                                        Pallet_list[sol_load[j][k]].D.append(Box_list[i].D)
                                    if Box_list[i].D not in Truck_list[j].D:
                                        Truck_list[j].D.append(Box_list[i].D)
                                    Box_index.remove(i)
                                        
                                    if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                    if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2])) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0] + Box_list[i].l, ep[1], ep[2]))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0] + Box_list[i].l, ep[1], ep[2]))

                                    if eps.count((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2])) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0] + Box_list[i].l, ep[1] + Box_list[i].w, ep[2]))

                                    if eps.count((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h)) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0] + Box_list[i].l, ep[1], ep[2] + Box_list[i].h))

                                    if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h)) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0], ep[1] +Box_list[i].w, ep[2] + Box_list[i].h))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0], ep[1] + Box_list[i].w, ep[2] + Box_list[i].h))

                                    if eps.count((ep[0], ep[1], ep[2] + Box_list[i].h)) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0], ep[1], ep[2] + Box_list[i].h))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0], ep[1], ep[2] + Box_list[i].h))

                                    if eps.count((ep[0], ep[1] + Box_list[i].w, ep[2])) < 1:
                                        Pallet_list[sol_load[j][k]].eps_list.append((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                    else:
                                        Pallet_list[sol_load[j][k]].eps_list.remove((ep[0], ep[1] + Box_list[i].w, ep[2]))
                                        
                                    Pallet_list[sol_load[j][k]].eps_list.remove(ep)
                                    break
           #record unused pallet                     
           if sol_package[sol_load[j][k]] == []:
               unused_pallet.append(sol_load[j][k])
    #unload unused pallet            
    sol_load = [[pallet for pallet in truck if pallet not in unused_pallet] for truck in sol_load]

    return sol_package,sol_load,sol_pacposition,Box_list,Pallet_list,Truck_list






        
        

  




































