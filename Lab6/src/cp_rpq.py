from __future__ import print_function
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from datareader import get_data
import numpy as np

directory = "rpq"
task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
result_list = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

for i in range(len(task_list)):
    task_name = task_list[i]
    tasks = get_data(directory, task_name)

    print("----- File: ", task_name, "-----")
    print("Carlier: ", result_list[i])

    # create a model
    model = cp_model.CpModel()

    # max variables value, overcounted
    variables_max_value = 0
    for task in tasks:
        variables_max_value += task.times[0] + task.times[1] + task.times[2]

    # alphas (needed to find the order)
    alphas = np.zeros((len(tasks), len(tasks))).tolist()
    for i in range(len(tasks)):
        for j in range(len(tasks)):
            alphas[i][j] = model.NewIntVar(0, 1, str(i)+","+str(j))

    # task starting times
    starts = [0] * len(tasks)
    for i in range(len(tasks)):
        starts[i] = model.NewIntVar(0, variables_max_value, str(i))

    # cmax
    cmax = model.NewIntVar(0, variables_max_value, "cmax")

    # restrictions
    # every task has to be prepared
    for task in tasks:
        model.Add(starts[task.index] >= task.times[0])

    # cmax has to be lower than every finish time (q)
    for task in tasks:
        model.Add(cmax >= starts[task.index] + task.times[1] + task.times[2])

    # restrictions responsible for task order
    for i in range(0, len(tasks)):
        for j in range(i+1, len(tasks)):
            task_1 = tasks[i]
            task_2 = tasks[j]

            model.Add(starts[task_1.index] + task_1.times[1] <= starts[task_2.index] + alphas[task_1.index][task_2.index] * variables_max_value)
            model.Add(starts[task_2.index] + task_2.times[1] <= starts[task_1.index] + alphas[task_2.index][task_1.index] * variables_max_value)
            model.Add(alphas[task_1.index][task_2.index] + alphas[task_2.index][task_1.index] == 1)

    model.Minimize(cmax)

    solver = cp_model.CpSolver()
    result_status = solver.Solve(model)

    if result_status != cp_model.OPTIMAL:
        print("Solver didn't find optimal solution")
    print("Objective value = ", solver.ObjectiveValue())
