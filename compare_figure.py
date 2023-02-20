#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:34:39 2023

@author: Joshua Liu
"""
from typing import Dict
import json
import numpy as np
import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='svg'


def dict2figure_compare(C_dict:Dict):
    

    Temp_num = len(C_dict[list(C_dict)[0]][0])
    Fun_num = 3
    
    color = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, Fun_num)]
    fun_name = ['EXT','SPR','MAN']
    
    figure_nume = 'Compare outputs with 10 boxes'
    
    x = np.concatenate([([i]*Temp_num) for i,j in sorted(C_dict.items())], axis=0).tolist()

    fig = go.Figure()

    for i in range(Fun_num):    
        combine_perform = []
        for j in list(C_dict):
            combine_perform += C_dict[j][i]
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
    

if __name__ == "__main__":
    
    #read experiment data
    with open('compare_output.json') as json_file:
        output_full = json.load(json_file)
      
    out_ = output_full['whether3d_True']['class_num_8']['box_num_10']

    dict2figure_compare(out_)