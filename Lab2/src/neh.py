from timeit import default_timer as timer
import numpy as np
from src.makespan import makespan


def get_sequences(index, prev_sequence):
    sequences = []
    for i in range(0, len(prev_sequence)+1):
        new_sequence = prev_sequence[:]
        new_sequence.insert(i, index)
        sequences.append(new_sequence)
    return sequences


def neh(tasks, numb_of_machines):
    start = timer()

    # step 1: find omegas(j)
    omegas = []
    for task in tasks:
        omegas.append(sum(task.times))

    # step 2: sort in descending order (get sorted order)
    omegas_order = np.argsort(-np.array(omegas)).tolist()

    # steps 3, 4: repeat n times (n = numb of tasks)
    solution_order = []
    for i in omegas_order:  # for every task
        # { pick task with the highest makespan }
        lowest_makespan = float("inf")
        lowest_makespan_sequence = []
        sequences = get_sequences(i, solution_order)

        for sequence in sequences:
            if makespan(sequence, tasks, numb_of_machines) < lowest_makespan:
                lowest_makespan = makespan(sequence, tasks, numb_of_machines)
                lowest_makespan_sequence = sequence
        solution_order = lowest_makespan_sequence

    stop = timer()
    return solution_order, (stop-start)*1000
