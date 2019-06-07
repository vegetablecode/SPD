from __future__ import print_function
from ortools.linear_solver import pywraplp
from datareader import get_data
import numpy as np

directory = "rpq"
task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]

for task_name in task_list:
    tasks = get_data(directory, task_name)
    print("----- File: ", task_name, "-----")

    # create a solver
    solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # max variables value, overcounted
    variables_max_value = 0
    for task in tasks:
        variables_max_value += task.times[0] + task.times[1] + task.times[2]

    # alphas (needed to find the order)
    alphas = np.zeros((len(tasks), len(tasks))).tolist()
    for i in range(len(tasks)):
        for j in range(len(tasks)):
            alphas[i][j] = solver.IntVar(0, 1, str(i)+","+str(j))

    # task starting times
    starts = [0] * len(tasks)
    for i in range(len(tasks)):
        starts[i] = solver.IntVar(0, variables_max_value, str(i))

    # cmax
    cmax = solver.IntVar(0, variables_max_value, "cmax")

    # restrictions
    # every task has to be prepared
    for task in tasks:
        solver.Add(starts[task.index] >= task.times[0])

    # cmax has to be lower than every finish time (q)
    for task in tasks:
        solver.Add(cmax >= starts[task.index] + task.times[1] + task.times[2])

    # restrictions responsible for task order
    for i in range(0, len(tasks)):
        for j in range(i+1, len(tasks)):
            task_1 = tasks[i]
            task_2 = tasks[j]

            solver.Add(starts[task_1.index] + task_1.times[1] <= starts[task_2.index] + alphas[task_1.index][task_2.index] * variables_max_value)
            solver.Add(starts[task_2.index] + task_2.times[1] <= starts[task_1.index] + alphas[task_2.index][task_1.index] * variables_max_value)
            solver.Add(alphas[task_1.index][task_2.index] + alphas[task_2.index][task_1.index] == 1)

    solver.Minimize(cmax)
    result_status = solver.Solve()

    if result_status != pywraplp.Solver.OPTIMAL:
        print("Solver didn't find optimal solution")
    print("Objective value = ", solver.Objective().Value())
