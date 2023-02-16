# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:52:52 2023

@author: Joshua liu
"""

from typing import Dict
import json

def dict2table(Box_Des_dict:Dict,Dimen:str,Class:str):
    
    #write dimension info
    if Dimen == 'True':
        di = '3d' 
    else:
        di = '1d'
        
    #record readings
    with open("./latex_table/" + di + '_class' + Class + '.tex', "w") as f:
        backreturn = "\\\\\n" + " "*8

        content = backreturn.join([
            f"{ins} & {' & '.join(map(str,read))}"
            for ins, read in sorted(Box_Des_dict.items()) 
        ])
        
        title = '{Experiment outputs in detail for ' + di + '/class' + str(Class) + '}'
        
        #write table
        f.write(f"""
\\begin{{table}}[ht!]
    \\caption{title}
    \\centering
    \\begin{{tabular}}{{@{{}}ccccccc@{{}}}}
        \\toprule
        {{\\bfseries Instance}} & {{\\bfseries SPR}} & {{\\bfseries MBF}}
        & {{\\bfseries ABF}} & {{\\bfseries SDC}} & {{\\bfseries KDC}} & {{\\bfseries PP}}\\\\
        \\midrule
        {content}\\\\
        \\bottomrule
    \\end{{tabular}}
\\end{{table}}
        """.strip())

#Compute
if __name__ == "__main__":
    
    #read experiment data
    with open('heuristics_output.json') as json_file:
        output_all = json.load(json_file)
    
    Dimen_list = [i for i,j in sorted(output_all.items())]
    Class_list = [i for i,j in sorted(output_all[Dimen_list[0]].items())]
    for i in Dimen_list:
        for j in Class_list:
            temp_output = output_all[i][j]
            Boxnum_list = [i for i,j in sorted(temp_output.items())]
            Desnum_list = [i for i,j in sorted(temp_output[Boxnum_list[0]].items())]
            di = i.split('_',1)[1]
            cl = j.split('num_',1)[1]
            
            Box_Des_dict = {}
            for b in Boxnum_list:
                for d in Desnum_list:
                    read_b = b.split('num_',1)[1]
                    read_d = d.split('num_',1)[1]
                    read_b_d = read_b + '/' + read_d
                    Box_Des_dict[read_b_d] = [round(elem,2) for elem in temp_output[b][d]]
                    
            dict2table(Box_Des_dict,di,cl)
