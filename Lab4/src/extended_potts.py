import copy
import numpy as np
from schrage import get_column, get_min


# Implementation of NI-P algorithm
# https://www.researchgate.net/publication/241080533_Approximation_algorithms_for_no_idle_time_scheduling_on_a_single_machine_with_release_times_and_delivery_times
# Page: 5


def nip_schrage(tasks):
    W_tasks = []  # temporary order
    G_tasks = []  # ready to order tasks
    N_tasks = copy.deepcopy(tasks)
    t = get_min(get_column(N_tasks, 0))
    cmax = 0
    critical_task = 0

    while len(N_tasks) != 0 or len(G_tasks) != 0:
        while len(N_tasks) != 0 and get_min(get_column(N_tasks, 0)) <= t:
            j = np.argmin(get_column(N_tasks, 0))
            G_tasks.append(N_tasks[j])
            del N_tasks[j]
        if len(G_tasks) == 0:
            t = get_min(get_column(N_tasks, 0))
        else:
            j = np.argmax(get_column(G_tasks, 2))
            tasks_j = copy.deepcopy(G_tasks[j])
            del G_tasks[j]
            t += tasks_j.times[1]
            W_tasks.append(tasks_j)
            if cmax < t + tasks_j.times[2]:
                cmax = t + tasks_j.times[2]
                critical_task = tasks_j

    g = np.argmin(get_column(W_tasks, 2))
    task_min_q = copy.deepcopy(W_tasks[g])

    # if critical task has the shortest q -> interference task does not exist
    if task_min_q == critical_task.times[2]:
        interference_task_index = -1
    else:
        interference_task = W_tasks[0]
        for i in range(W_tasks.index(critical_task)+1):
            for j in range(W_tasks.index(interference_task)+1, W_tasks.index(critical_task)+1):
                if W_tasks[j].times[2] < critical_task.times[2]:
                    interference_task = W_tasks[j]
                    break
        interference_task_index = W_tasks.index(interference_task)

    return cmax, W_tasks, W_tasks.index(critical_task), interference_task_index

