from makespan import get_order, makespan
import copy
import numpy as np
from task import Task

def get_column(tasks, element):
    column = []
    for item in tasks:
        column.append(item.times[element])
    return column;


def get_min(list):
    if len(list) <= 0:
        return -1
    else:
        return min(list)


def schrage_n2(tasks):
    W_tasks = []  # temporary order
    G_tasks = []  # ready to order tasks
    N_tasks = copy.deepcopy(tasks)
    t = get_min(get_column(N_tasks, 0))

    while len(N_tasks) != 0 or len(G_tasks) != 0:
        while len(N_tasks) != 0 and get_min(get_column(N_tasks, 0)) <= t:
            j = np.argmin(get_column(N_tasks, 0))
            G_tasks.append(N_tasks[j])
            del N_tasks[j]
        if len(G_tasks) == 0:
            t = get_min(get_column(N_tasks, 0))
        else:
            j = np.argmax(get_column(G_tasks, 2))
            t += G_tasks[j].times[1]
            W_tasks.append(G_tasks[j])
            del G_tasks[j]
    return get_order(W_tasks)


def schrage_n2_pmtn(tasks):
    W_tasks = []  # temporary order
    G_tasks = []  # ready to order tasks
    N_tasks = copy.deepcopy(tasks)
    t = get_min(get_column(N_tasks, 0))
    q_0 = 99999999
    task_l = Task(0, [0, 0, q_0])  # current task
    cmax = 0

    while len(N_tasks) != 0 or len(G_tasks) != 0:
        while len(N_tasks) != 0 and get_min(get_column(N_tasks, 0)) <= t:
            j = np.argmin(get_column(N_tasks, 0))
            task_j = copy.deepcopy(N_tasks[j])
            del N_tasks[j]
            G_tasks.append(task_j)
            if task_j.times[2] > task_l.times[2]:
                task_l.times[1] = t - task_j.times[0]
                t = task_j.times[0]
                if task_l.times[1] > 0:
                    G_tasks.append(task_l)
        if len(G_tasks) == 0:
            t = get_min(get_column(N_tasks, 0))
        else:
            j = np.argmax(get_column(G_tasks, 2))
            task_j = copy.deepcopy(G_tasks[j])
            del G_tasks[j]
            t += task_j.times[1]
            cmax = max(cmax, t + task_j.times[2])
            task_l = copy.deepcopy(task_j)
            W_tasks.append(task_j)
    return cmax, get_order(W_tasks)
