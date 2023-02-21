#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:34:39 2023

@author: Joshua Liu
"""
import json
import numpy as np
import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='svg'


class figure_compare():
    
    def __init__(self,path:str):
        #read experiment data
        with open(path) as json_file:
            output_full = json.load(json_file)
          
        out_ = output_full['whether3d_True']['class_num_8']['box_num_10']
        
        #get best
        Temp_num = len(out_[list(out_)[0]][0])
        for des in out_:
            read = out_[des]
            man = []
            for i in range(Temp_num):
                man.append(min(read[2][i],read[3][i],read[4][i],read[5][i],read[6][i]))
            out_[des] = [read[0],read[1],man]
        self.out_ = out_
        
    def dict2figure_hist(self):
        rate = [[],[]]
        for des in self.out_:
            base = self.out_[des][0]
            spr = self.out_[des][1]
            comp = self.out_[des][2]
            for i in range(len(base)):
                rate[0].append(100*(spr[i]-base[i])/base[i])
                rate[1].append(100*(comp[i]-base[i])/base[i])
        
        color = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, 3)]
        figure_nume = 'Compare outputs with 10 boxes_hist'
        
        fig = go.Figure()
        fig.add_trace(go.Box(y=rate[0],boxpoints='all', name='SPR',marker_color = color[1]))
        fig.add_trace(go.Box(y=rate[1],boxpoints='all', name='MAN',marker_color = color[2]))
        
        fig.update_layout(
            xaxis = dict(tickfont = dict(size=25)),
            yaxis = dict(title='Opportunity loss',
                         tickfont = dict(size=25),
                         titlefont = dict(size = 25)),
            legend = dict(font = dict(size = 25))
        )
        
        fig.write_image('Figures/' + figure_nume + '.png')

    def dict2figure_compare(self):
        

        Temp_num = len(self.out_[list(self.out_)[0]][0])
        Fun_num = 3
        
        color = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, Fun_num)]
        fun_name = ['EXT','SPR','MAN']
        
        figure_nume = 'Compare outputs with 10 boxes'
        
        x = np.concatenate([([i]*Temp_num) for i,j in sorted(self.out_.items())], axis=0).tolist()

        fig = go.Figure()

        for i in range(Fun_num):    
            combine_perform = []
            for j in list(self.out_):
                combine_perform += self.out_[j][i]
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
    
    path = 'compare_output.json'
    
    dict_set = figure_compare(path)
    dict_set.dict2figure_hist()
    dict_set.dict2figure_compare()
    
    
