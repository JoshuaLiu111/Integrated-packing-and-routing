# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 09:59:47 2023

@author: Joshua liu
"""
from heuristics_runner import runfunction
import time
import numpy as np
from heuristics_experiment import instance_gen
import plotly.express as px
import plotly.io as io
io.renderers.default='svg'

if __name__ == "__main__":
    B_Num = range(20,81)
    D_Num = range(10,51)
    di = True
    cl = 1
    fun = 1
    Run_temp = 3
    
    #Fix B
    b_num = 80
    time_fixb = [[] for d_num in D_Num]
    for i in range(len(D_Num)):
        for run in range(Run_temp):
            #generate instance
            Ins_list = instance_gen(b_num,D_Num[i],cl)
            start = time.time()
            runfunction(fun,di,Ins_list)
            end = time.time()
            time_fixb[i].append(end-start)
    
    #Fix D
    d_num = 50
    time_fixd = [[] for b_num in B_Num]
    for i in range(len(B_Num)):
        for run in range(Run_temp):
            #generate instance
            Ins_list = instance_gen(B_Num[i],d_num,cl)
            start = time.time()
            runfunction(fun,di,Ins_list)
            end = time.time()
            time_fixd[i].append(end-start)
            
    time_D = np.average(np.array(time_fixb), axis=1).tolist()
    time_B = np.average(np.array(time_fixd), axis=1).tolist()
    
    fig = px.scatter(x=B_Num, y=time_B)
    fig.update_layout(
        xaxis = dict(title='Box number',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        yaxis = dict(title='Run time',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25))
    )
    fig.write_image('Figures/' + 'box_runtime' + '.png')
    
    fig = px.scatter(x=D_Num, y=time_D)
    fig.update_layout(
        xaxis = dict(title='Destination number',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        yaxis = dict(title='Run time',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25))
    )
    fig.write_image('Figures/' + 'destination_runtime' + '.png')

    
    