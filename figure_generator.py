# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:46:46 2023

@author: Joshua liu
"""

from typing import Dict
import json
import numpy as np
import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='svg'


def dict2figure(Class_dict:Dict,Dimen:str,Box_Num:str,Des_Num:str,Split:str):
    
    #write dimension info
    if Dimen == 'True':
        di = '3d' 
    else:
        di = '1d'

    Temp_num = len(Class_dict[list(Class_dict)[0]][0])
    Fun_num = len(Class_dict[list(Class_dict)[0]])
    
    color = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, Fun_num)]
    fun_name = ['SPR','MBF','ABF','KDC','PP']
    
    figure_nume = 'Experiment outputs for ' + di + ' with ' + Box_Num + \
        ' boxes and ' + Des_Num + ' destinations' + Split
    
    x = np.concatenate([([i]*Temp_num) for i,j in sorted(Class_dict.items())], axis=0).tolist()

    fig = go.Figure()

    for i in range(Fun_num):    
        combine_perform = []
        for j in list(Class_dict):
            combine_perform += Class_dict[j][i]
        fig.add_trace(go.Box(
            y = combine_perform,
            x = x,
            name = fun_name[i],
            marker_color = color[i]
        ))
    

    fig.update_layout(
        xaxis = dict(tickfont = dict(size=25)),
        yaxis = dict(title='Total cost',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        legend = dict(font = dict(size = 25)),
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    
    
    fig.write_image('Figures/' + figure_nume + '.png')




#Compute
if __name__ == "__main__":
    
    #read experiment data
    with open('heuristics_fulloutput.json') as json_file:
        output_full = json.load(json_file)
      
    out_1d = output_full['whether3d_False']
    
    #1d/small
    small_list_1d = {}
    for i in list(out_1d):
        if i.split('num_',1)[1] in ['6','7','8']:
            read = out_1d[i]['box_num_20']['des_num_10']
            #get rid of SDC
            read.pop(3)  
            small_list_1d[i] = read
    dict2figure(small_list_1d,'False','20','10','')
    
    #1d/large
    large_list_1d = {}
    for i in list(out_1d):
        if i.split('num_',1)[1] in ['6','7','8']:
            read = out_1d[i]['box_num_80']['des_num_50']
            #get rid of SDC
            read.pop(3)  
            large_list_1d[i] =  read
    dict2figure(large_list_1d,'False','80','50','')
    
    out_3d = output_full['whether3d_True']
    
    #3d/small
    
    #class 1-5
    small_list_3d_1 = {}
    for i in list(out_3d):
        if i.split('num_',1)[1] in ['1','2','3','4','5']:
            read = out_3d[i]['box_num_20']['des_num_10']
            #get rid of SDC
            read.pop(3)  
            small_list_3d_1[i] = read        
    dict2figure(small_list_3d_1,'True','20','10','1')
    
    #class 6-8
    small_list_3d_2 = {}
    for i in list(out_3d):
        if i.split('num_',1)[1] in ['6','7','8']:
            read = out_3d[i]['box_num_20']['des_num_10']
            #get rid of SDC
            read.pop(3)  
            small_list_3d_2[i] = read        
    dict2figure(small_list_3d_2,'True','20','10','2')
    
    #3d/large

    #class 1-5
    large_list_3d_1 = {}
    for i in list(out_3d):
        if i.split('num_',1)[1] in ['1','2','3','4','5']:
            read = out_3d[i]['box_num_80']['des_num_50']
            #get rid of SDC
            read.pop(3)  
            large_list_3d_1[i] = read        
    dict2figure(large_list_3d_1,'True','80','50','1')
    
    #class 6-8
    large_list_3d_2 = {}
    for i in list(out_3d):
        if i.split('num_',1)[1] in ['6','7','8']:
            read = out_3d[i]['box_num_80']['des_num_50']
            #get rid of SDC
            read.pop(3)  
            large_list_3d_2[i] = read        
    dict2figure(large_list_3d_2,'True','80','50','2')
    