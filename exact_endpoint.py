# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:28:34 2023

@author: Joshua Liu
"""
import pyomo.environ as pyo
from typing import Dict

from exact_insreader import data_reader
from exact_model import define_model

def write_vars(instance: pyo.ConcreteModel):
    """Writes decision variables to list of dicts."""

    var_outputs = [
        {"variable": v.name, "index": index, "value": pyo.value(v[index])}
        for v in instance.component_objects(pyo.Var, active=True)
        for index in v
    ]
    return var_outputs

def cal_solution_cost(instance:pyo.AbstractModel):
    """Calculates total cost of entities"""
    sol_total_cost =  sum(
            pyo.value(instance.u0[j]) * pyo.value(instance.c[j]) for j in instance.J
            ) + sum(
            pyo.value(instance.u1[k]) * pyo.value(instance.C[k]) for k in instance.K
            ) + sum(
            pyo.value(instance.gs[k,d,dp]) * pyo.value(instance.cp[d,dp])
                      for k in instance.K
                      for d in instance.DP
                      for dp in instance.DP
            )
    return sol_total_cost

def solve_least_cost(Ins_list:list, solver_options:Dict):
    """Endpoint for least cost model"""

    # Generate data
    print("bringing input data to a pyomo format...")
    data = {None: data_reader(Ins_list)}
    print(data)

    # Create abstract model
    print("creating abstract model...")
    abstract_model = define_model()

    print("creating model instance...")
    instance = abstract_model.create_instance(data)

    print("applying selected solver...")
    opt = pyo.SolverFactory(solver_options["solver"])

    if solver_options["solver"] == "gurobi":
        opt.options["ResultFile"] = "INFEASIBILITY.ilp"
        opt.options["MIPFocus"] = 1
        opt.options["Heuristics"] = 0.1
        opt.options["MIPGap"] = solver_options["mip_gap"]
        opt.options["TimeLimit"] = solver_options["time_limit"]
    if solver_options["solver"] == "glpk":
        opt.options["tmlim"] = solver_options["time_limit"]
        opt.options["mipgap"] = solver_options["mip_gap"]

    print("solving...")
    opt.solve(instance, tee=True)

    var_outputs = write_vars(instance)
    cost = cal_solution_cost(instance)

    return var_outputs,cost
