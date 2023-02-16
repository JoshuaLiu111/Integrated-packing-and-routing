# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:11:19 2023

@author: Joshua Liu
"""
import numpy as np
import math

#DEPOT INFO (ID,location)
class Depot():
    def __init__(self,ID,x,y):
        self.ID =ID
        self.x = x
        self.y = y       
        
#BOX INFO (ID, destination, volumn, measurements)
class Box():
    def __init__(self,ID,D,v,l,w,h):
        self.ID = ID
        self.D = D
        self.v = v
        self.l = l
        self.w = w
        self.h = h

#PALLET INFO (ID, capacity, measurements, rest capacity, cost)
class Pallet():
    def __init__(self,ID,V,L,W,H,rest_V,eps_list,c,D):
        self.ID = ID
        self.V = V
        self.L = L
        self.W = W
        self.H = H
        self.eps_list = eps_list
        self.c = c
        self.rest_V = rest_V
        self.D = D

#TRUCK INFO (ID, capacity, rest capacity, cost)
class Truck():
    def __init__(self,ID,T,rest_T,C,D):
        self.ID = ID
        self.T = T
        self.rest_T = rest_T
        self.C = C
        self.D = D
 
#Destination INFO (ID, axis, polar)
class Destination():
    def __init__(self,ID,x,y,angle,r):
        self.ID =ID
        self.x = x
        self.y = y
        self.angle = angle
        self.r = r

#GENERATE DEPOT LIST
def depotgen(Depot_Num:int) -> list:
    Depot_list = []
    for i in range(Depot_Num):
        Depot_list.append(Depot(i, np.random.uniform(-1,1), np.random.uniform(-1,1))) 
    return Depot_list

#GENERATE BOX LIST
def boxgen(Box_Num:int,Destination_Num:int,Class:int) -> list:
    Box_list = []
    Box_Num10p = Box_Num // 10
    for i in range(Box_Num):
        Box_list.append(Box('unrank', np.random.randint(0,Destination_Num), 'computing', 
                            'generating','generating','generating'))
        if Class == 6:
            Box_list[i].l = np.random.randint(1,3)
            Box_list[i].w = np.random.randint(1,3)
            Box_list[i].h = np.random.randint(1,3)
        elif Class == 7:
            Box_list[i].l = np.random.randint(1,5)
            Box_list[i].w = np.random.randint(1,5)
            Box_list[i].h = np.random.randint(1,5)
        elif Class == 8:
            Box_list[i].l = np.random.randint(1,9)
            Box_list[i].w = np.random.randint(1,9)
            Box_list[i].h = np.random.randint(1,9)
    if Class == 1:
        #type 1
        for i in range(4*Box_Num10p,Box_Num):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(6,10)
        #type 2
        for i in range(Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(1,6)
        #type 3
        for i in range(Box_Num10p,2*Box_Num10p):
            Box_list[i].l = np.random.randint(1,7)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(6,10)
        #type 4
        for i in range(2*Box_Num10p,3*Box_Num10p):
            Box_list[i].l = np.random.randint(5,10)
            Box_list[i].w = np.random.randint(5,10)
            Box_list[i].h = np.random.randint(5,10)
        #type 5
        for i in range(3*Box_Num10p,4*Box_Num10p):
            Box_list[i].l = np.random.randint(1,6)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(1,6)
    elif Class == 2:
        #type 1
        for i in range(Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(6,10)
        #type 2
        for i in range(4*Box_Num10p,Box_Num):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(1,6)
        #type 3
        for i in range(Box_Num10p,2*Box_Num10p):
            Box_list[i].l = np.random.randint(1,7)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(6,10)
        #type 4
        for i in range(2*Box_Num10p,3*Box_Num10p):
            Box_list[i].l = np.random.randint(5,10)
            Box_list[i].w = np.random.randint(5,10)
            Box_list[i].h = np.random.randint(5,10)
        #type 5
        for i in range(3*Box_Num10p,4*Box_Num10p):
            Box_list[i].l = np.random.randint(1,6)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(1,6)
    elif Class == 3:
        #type 1
        for i in range(Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(6,10)
        #type 2
        for i in range(Box_Num10p,2*Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(1,6)
        #type 3
        for i in range(4*Box_Num10p,Box_Num):
            Box_list[i].l = np.random.randint(1,7)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(6,10)
        #type 4
        for i in range(2*Box_Num10p,3*Box_Num10p):
            Box_list[i].l = np.random.randint(5,10)
            Box_list[i].w = np.random.randint(5,10)
            Box_list[i].h = np.random.randint(5,10)
        #type 5
        for i in range(3*Box_Num10p,4*Box_Num10p):
            Box_list[i].l = np.random.randint(1,6)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(1,6)
    elif Class == 4:
        #type 1
        for i in range(Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(6,10)
        #type 2
        for i in range(Box_Num10p,2*Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(1,6)
        #type 3
        for i in range(2*Box_Num10p,3*Box_Num10p):
            Box_list[i].l = np.random.randint(1,7)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(6,10)
        #type 4
        for i in range(4*Box_Num10p,Box_Num):
            Box_list[i].l = np.random.randint(5,10)
            Box_list[i].w = np.random.randint(5,10)
            Box_list[i].h = np.random.randint(5,10)
        #type 5
        for i in range(3*Box_Num10p,4*Box_Num10p):
            Box_list[i].l = np.random.randint(1,6)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(1,6)
    elif Class == 5:
        #type 1
        for i in range(Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(6,10)
        #type 2
        for i in range(Box_Num10p,2*Box_Num10p):
            Box_list[i].l = np.random.randint(6,10)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(1,6)
        #type 3
        for i in range(2*Box_Num10p,3*Box_Num10p):
            Box_list[i].l = np.random.randint(1,7)
            Box_list[i].w = np.random.randint(6,10)
            Box_list[i].h = np.random.randint(6,10)
        #type 4
        for i in range(3*Box_Num10p,4*Box_Num10p):
            Box_list[i].l = np.random.randint(5,10)
            Box_list[i].w = np.random.randint(5,10)
            Box_list[i].h = np.random.randint(5,10)
        #type 5
        for i in range(4*Box_Num10p,Box_Num):
            Box_list[i].l = np.random.randint(1,6)
            Box_list[i].w = np.random.randint(1,6)
            Box_list[i].h = np.random.randint(1,6)  
    for i in range(Box_Num):
        Box_list[i].v = Box_list[i].l * Box_list[i].w * Box_list[i].h
    #sort and label by volume
    Box_list=sorted(Box_list, key=lambda Box_list: (Box_list.v), reverse=True)
    for i in range(Box_Num):
        Box_list[i].ID = i
    return Box_list

#GENERATE PALLET LIST
def palletgen(Pallet_Num:int,Class:int) -> list:
    Pallet_list = []
    for i in range(Pallet_Num):
        Pallet_list.append(Pallet('unrank','computing','generating','generating', 
                                  'generating','generating',[(0, 0, 0)],
                                  'generating',[]))
        if Class == 6:
            Pallet_list[i].L = np.random.randint(2,4)
            Pallet_list[i].W = np.random.randint(2,4)
            Pallet_list[i].H = np.random.randint(2,4)
            Pallet_list[i].c = np.random.randint(2,5)
        elif Class == 7:
            Pallet_list[i].L = np.random.randint(4,6)
            Pallet_list[i].W = np.random.randint(4,6)
            Pallet_list[i].H = np.random.randint(4,6)
            Pallet_list[i].c = np.random.randint(10,13)
        else:
            Pallet_list[i].L = np.random.randint(8,11)
            Pallet_list[i].W = np.random.randint(8,11)
            Pallet_list[i].H = np.random.randint(8,11)
            Pallet_list[i].c = np.random.randint(20,31)
        Pallet_list[i].V = Pallet_list[i].L * Pallet_list[i].W * Pallet_list[i].H
        Pallet_list[i].rest_V = Pallet_list[i].V
    #sort and label by unit space cost
    Pallet_list=sorted(Pallet_list, key=lambda Pallet_list: Pallet_list.V/Pallet_list.c, reverse=True)
    for i in range(Pallet_Num):
        Pallet_list[i].ID = i
    return Pallet_list

#GENERATE TRUCK LIST
def truckgen(Truck_Num:int,Class:int) -> list:
    Truck_list = []
    for i in range(Truck_Num):
        Truck_list.append(Truck('unrank','generating', 'generating', 
                                'generating',[]))
        if Class == 6:
            Truck_list[i].T = np.random.randint(31,63)
            Truck_list[i].C = np.random.randint(9,16)
        elif Class == 7:
            Truck_list[i].T = np.random.randint(182,365)
            Truck_list[i].C = np.random.randint(33,56)
        else:
            Truck_list[i].T = np.random.randint(1458,2917)
            Truck_list[i].C = np.random.randint(75,126)
        Truck_list[i].rest_T = Truck_list[i].T
    #sort and label by unit space cost
    Truck_list=sorted(Truck_list, key=lambda Truck_list: Truck_list.T/Truck_list.C, reverse=True)  
    for i in range(Truck_Num):
        Truck_list[i].ID = i
    return Truck_list

#Destination INFO
def desgen(Destination_Num:int) -> list:
    Destination_list = []
    for i in range(Destination_Num):
        Destination_list.append(Destination('unrank', 'computing', 'computing' ,np.random.uniform(0,360), np.random.uniform(0,11)))
        Destination_list[i].x = Destination_list[i].r*math.cos(Destination_list[i].angle)
        Destination_list[i].y = Destination_list[i].r*math.sin(Destination_list[i].angle)
    #sort and label by polar
    Destination_list=sorted(Destination_list, key=lambda Destination_list: (Destination_list.angle,Destination_list.r),reverse=False)
    for i in range(Destination_Num):
        Destination_list[i].ID = i   
    return Destination_list

#Distance map INFO
def desmapgen(De_list:list,D_list:list,triangle:bool=True) -> list:
    #combine depot and destinations
    com_list = De_list+D_list
    desmap = [[] for D in com_list]
    for i in range(len(com_list)):
        for j in range(len(com_list)):
            #newtonian distance with random amplifier (if triangle == True)
            dist = (((com_list[i].x-com_list[j].x)**2+(com_list[i].y-com_list[j].y)**2)**0.5) \
                *(1 + triangle*np.random.randint(0,2))
            #add random traffic parameter (if triangle == True)
            if i != j:
                dist += triangle*np.random.randint(0,2)
            desmap[i].append(dist)
    return desmap