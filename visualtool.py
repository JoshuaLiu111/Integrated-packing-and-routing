#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:57:49 2022

@author: Joshua Liu
"""
# Import all the necessary libraries and packages in the code
import matplotlib.pyplot as plt
import numpy as np
import random


# Defining the user-defined cubes() function
def palletplot(pallet_size:tuple,position_list:list,size_list:list):
    # Defining the size of the axes
    x, y, z = np.indices((10,10,10))
    # Defining the axes and the figure object
    ax = plt.figure(figsize=(9, 9)).add_subplot(projection='3d')
    # Adding pallet size
    axes = [pallet_size[0], pallet_size[1], pallet_size[2]]
    data = np.ones(axes, dtype=np.bool)
    # Transparency
    alpha = 0.3
    colors = np.empty(axes + [4], dtype=np.float32)
    colors[:] = [1, 0, 0, alpha]
    ax.voxels(data, facecolors=colors)
    # Adding boxes
    for i in range(len(position_list)):
        # Defining the length of the sides of the box
        cube = (position_list[i][0] <= x) & (x < (size_list[i][0] + position_list[i][0])) & \
               (position_list[i][1] <= y) & (y < (size_list[i][1] + position_list[i][1])) & \
               (position_list[i][2] <= z) & (z < (size_list[i][2] + position_list[i][2]))
        # Defining the colors for the box
        colors = np.empty(cube.shape, dtype=object)
        # Random colors
        colors[cube] = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])      
        # Plotting the box in the figure
        ax.voxels(cube, facecolors=colors)
    # Displaying the graph
    plt.show()


def draw_route(sol_route:list,Depot_list:list,Destination_list:list):
    '''Draw down route plot'''
    
    #Prepare axis
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ##Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    ##Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ##Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    used_truck = [i for i, j in enumerate(sol_route) if j]
    for truck in used_truck:
        
        #To get coordinates
        point=[[Destination_list[des].x,Destination_list[des].y] for des in sol_route[truck]]
        
        #Adding the original point into the route
        point.insert(0,[Depot_list[0].x,Depot_list[0].y])
        point.append([Depot_list[0].x,Depot_list[0].y])
        
        #Transfer into a np,array
        point=np.array(point)
        
        #Plot each route
        plt.plot(point[:, 0], point[:, 1], label='truck_%s' %truck)
        plt.legend()
        
    return plt.show()