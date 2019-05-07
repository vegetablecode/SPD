from src.makespan import get_order, makespan
import copy
import numpy as np

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
