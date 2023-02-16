#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:09:46 2022

@author: Joshua Liu
"""

from visualtool import palletplot

J1_size = (8,8,8)
J1_position = [(6,0,0),(1,0,0),(0,0,6),(0,0,5),(0,0,1),(0,0,0),(4,5,0),(0,5,2),(6,1,4),(7,4,0)]
J1_boxsize = [(2,4,4),(5,1,4),(5,3,2),(6,6,3),(4,4,4),(6,3,1),(2,2,4),(4,2,3),(2,3,2),(1,4,5)]

J3_size = (10,8,5)
J3_position = [(6,0,0),(1,0,2),(5,0,0),(2,0,0),(0,2,0),(4,0,2),(1,3,0)]
J3_boxsize = [(4,5,5),(3,1,3),(1,3,3),(3,3,2),(1,3,4),(1,3,3),(2,2,4)]


J4_size = (10,7,5)
J4_position = [(0,0,0),(5,0,0)]
J4_boxsize = [(5,5,5),(5,5,5)]


palletplot(J1_size,J1_position,J1_boxsize)
palletplot(J3_size,J3_position,J3_boxsize)
palletplot(J4_size,J4_position,J4_boxsize)