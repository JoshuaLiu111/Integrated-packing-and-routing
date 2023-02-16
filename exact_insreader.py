# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:28:34 2023

@author: Joshua Liu
"""
from typing import Dict, Any

def data_reader(Ins_list:list) -> dict:
    
    # Setup
    De_list,B_list,P_list,T_list,D_list,desmap = Ins_list
    
    # Transfer
    Goto_list = [[] for i in range(len(B_list))]
    for i in range(len(B_list)):
        for d in range(len(D_list)):
            if d == B_list[i].D:
                Goto_list[i].append(1)
            else:
                Goto_list[i].append(0)
        Goto_list[i].insert(0,1)
    
    # Initialise data_dict
    data_dict: Dict[str, Dict[Any, Any]] = {}

    # Set general parameters
    data_dict["epsilon"] = {None: 0.01}
    data_dict["Upsilon"] = {None: 100}

    # Sets
    data_dict["I"] = {
        None: [i for i in range(len(B_list))]
    }
    data_dict["J"] = {
        None: [j for j in range(len(P_list))]
    }
    data_dict["K"] = {
        None: [k for k in range(len(T_list))]
    }
    data_dict["DP"] = {
        None: [d for d in range(len(De_list + D_list))]
    }
    
    # Paras
    data_dict["d0"] = {
        None: 0
    }
    
    # Boxes
   
    data_dict["v"] = {
        i : B_list[i].v for i in range(len(B_list))
    }
    data_dict["l"] = {
        i : B_list[i].l for i in range(len(B_list))
    }
    data_dict["w"] = {
        i : B_list[i].w for i in range(len(B_list))
    }
    data_dict["h"] = {
        i : B_list[i].h for i in range(len(B_list))
    }
    data_dict["g0"] = {
            (i,d) : Goto_list[i][d]
            for i in range(len(B_list))
            for d in range(len(De_list + D_list))
        }
    
    # Pallets
    
    data_dict["V"] = {
        j : P_list[j].V for j in range(len(P_list))
    }
    data_dict["c"] = {
        j : P_list[j].c for j in range(len(P_list))
    }
    data_dict["L"] = {
        j : P_list[j].L for j in range(len(P_list))
    }
    data_dict["W"] = {
        j : P_list[j].W for j in range(len(P_list))
    }
    data_dict["H"] = {
        j : P_list[j].H for j in range(len(P_list))
    }
    
    # Trucks
    
    data_dict["T"] = {
        k : T_list[k].T for k in range(len(T_list))
    }
    data_dict["C"] = {
        k : T_list[k].C for k in range(len(T_list))
    }

    
    # Distance
    data_dict["cp"] = {
            (d, dp) : desmap[d][dp]
            for d in range(len(De_list + D_list))
            for dp in range(len(De_list + D_list))
        }
 
    return data_dict
