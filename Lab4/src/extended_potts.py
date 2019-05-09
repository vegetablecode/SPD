import copy
import numpy as np
from src.schrage import get_column, get_min
from src.makespan import get_order

# Implementation of NI-P algorithm
# https://www.researchgate.net/publication/241080533_Approximation_algorithms_for_no_idle_time_scheduling_on_a_single_machine_with_release_times_and_delivery_times
# Page: 5

def nip_schrage(tasks):
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
