from __future__ import print_function
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from datareader import get_data
import numpy as np

# WITI Task:
# times[0] -> P (preparation time)
# times[1] -> W (weight)
# times[2] -> D (max time)

directory = "witi"
task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008", "data.009"]
result_list = [776, 799, 742, 688, 497, 440, 423, 417, 405, 393, 897]

for i in range(len(task_list)):
    task_name = task_list[i]
    tasks = get_data(directory, task_name)

    print("----- File: ", task_name, "-----")
    print("WITI: ", result_list[i])

    # create a model
    model = cp_model.CpModel()

    # max variables value, overcounted
    variables_max_value = 0
    total_time = 0

    for task in tasks:
        total_time += task.times[0]  # p time

    for task in tasks:
        if total_time - task.times[2] > 0:
            variables_max_value += task.times[1] * (total_time - task.times[2])

    # alphas (needed to find the order)
    alphas = {}
    for i in range(len(tasks)):
        for j in range(len(tasks)):
            alphas[i, j] = model.NewIntVar(0, 1, str(i)+","+str(j))

    # task starting times
    starts = [0] * len(tasks)
    ends = [0] * len(tasks)
    delays = [0] * len(tasks)

    for i in range(len(tasks)):
        starts[i] = model.NewIntVar(0, variables_max_value, "start: " + str(i))
        ends[i] = model.NewIntVar(0, variables_max_value, "end: " + str(i))
        delays[i] = model.NewIntVar(0, variables_max_value, "delay: " + str(i))

    # witi
    cmax = model.NewIntVar(0, variables_max_value, "cmax")

    # restrictions
    for i in range(len(tasks)):
        model.Add(starts[tasks[i].index] + tasks[i].times[0] <= ends[i])
        model.Add(tasks[i].times[1] * (ends[i] - tasks[i].times[2]) == delays[i])

    for i in range(len(tasks)):
        for j in range(i+1, len(tasks)):
            model.Add(starts[i] + tasks[i].times[0] <= starts[j] + alphas[i, j] * variables_max_value)
            model.Add(starts[j] + tasks[j].times[0] <= starts[i] + alphas[j, i] * variables_max_value)
            model.Add(alphas[i, j] + alphas[j, i] == 1)

    # restrictions responsible for task order
    for i in range(0, len(tasks)):
        cmax += delays[i]

    model.Minimize(cmax)

    solver = cp_model.CpSolver()
    result_status = solver.Solve(model)

    if result_status != cp_model.OPTIMAL:
        print("Solver didn't find optimal solution")
    print("Objective value = ", solver.ObjectiveValue())
