from timeit import default_timer as timer
import numpy as np
import copy


def column(matrix, i):
    return [row[i] for row in matrix]


def find_best_insertion_position(tasks, numb_of_machines, index, solution_order, times_table, path_in_table, path_out_table):
    best_insertion_position = 0
    best_cmax = float("inf")

    for i in range(0, len(solution_order)+1):
        # get left neighbours path in
        left_neighbours_path_in = np.zeros(numb_of_machines, dtype=int).tolist()
        if i>0:
            left_neighbours_path_in = column(path_in_table, i-1)
        #print(left_neighbours_path_in)

        # get right neighbours path out
        right_neighbours_path_out = np.zeros(numb_of_machines, dtype=int).tolist()
        if i < len(solution_order):
            right_neighbours_path_out = column(path_out_table, i)
        #print(right_neighbours_path_out)

        # get current path in
        current_times = []
        for j in range(0, numb_of_machines):
            current_times.append(tasks[index].times[j])
        #print(current_times)

        # get current path in + cmax
        current_path_in = []
        current_path_in.append(left_neighbours_path_in[0]+current_times[0]+right_neighbours_path_out[0])
        for j in range(1, numb_of_machines):
            #print("-> i: {} | {},  {},  {}" .format(i, left_neighbours_path_in[j], current_times[j-1], current_times[j]))
            current_path_in.append(max(left_neighbours_path_in[j], current_times[j-1])+current_times[j]+right_neighbours_path_out[j])
        #print(max(current_path_in))

        # check if this cmax is better
        if max(current_path_in) < best_cmax:
            best_cmax = max(current_path_in)
            best_insertion_position = i

    return best_insertion_position;


def get_times_table(order, tasks, numb_of_machines):
    table = []
    for i in range(0, numb_of_machines):
        temp_tasks = []
        for j in order:
            temp_tasks.append(tasks[j].times[i])
        table.append(temp_tasks)
    return table

def get_path_in_table(time_table):
    table = np.zeros((len(time_table), len(time_table[0])), dtype=int).tolist()
    temp_sums = [0]*len(time_table)
    for i in range(0, len(time_table[0])):
        temp_sums[0] += time_table[0][i]
        table[0][i] += temp_sums[0]
        for j in range(1, len(time_table)):
            if temp_sums[j] < temp_sums[j-1]:
                temp_sums[j] = temp_sums[j-1]
            temp_sums[j] += time_table[j][i]
            table[j][i] = temp_sums[j]
    return table

def get_path_out_table(time_table):
    # reverse time_table
    reversed_time_table = copy.deepcopy(time_table)
    reversed_time_table.reverse()
    for i in range(0, len(reversed_time_table)):
        reversed_time_table[i].reverse()

    table = np.zeros((len(reversed_time_table), len(reversed_time_table[0])), dtype=int).tolist()
    temp_sums = [0]*len(reversed_time_table)
    for i in range(0, len(reversed_time_table[0])):
        temp_sums[0] += reversed_time_table[0][i]
        table[0][i] += temp_sums[0]
        for j in range(1, len(reversed_time_table)):
            if temp_sums[j] < temp_sums[j-1]:
                temp_sums[j] = temp_sums[j-1]
            temp_sums[j] += reversed_time_table[j][i]
            table[j][i] = temp_sums[j]

    # reverse back table
    table.reverse()
    for i in range(0, len(table)):
        table[i].reverse()

    return table


def get_sequences(index, prev_sequence):
    if index in prev_sequence: prev_sequence.remove(index)
    sequences = []
    for i in range(0, len(prev_sequence)+1):
        new_sequence = prev_sequence[:]
        new_sequence.insert(i, index)
        sequences.append(new_sequence)
    return sequences


def qneh(tasks, numb_of_machines):
    start = timer()
    # step 1: find omegas(j)
    omegas = []
    for task in tasks:
        omegas.append(sum(task.times))

    # step 2: sort in descending order (get sorted order) [args]
    omegas_order = np.argsort(-np.array(omegas)).tolist()

    # steps 3, 4: repeat n times (n = numb of tasks)
    solution_order = []
    for i in omegas_order:  # (3) get argument of next task with the highest omega value
        # (4) insert task & pick task with the lowest makespan
        times_table = get_times_table(solution_order, tasks, numb_of_machines)
        path_out_table = get_path_out_table(times_table)
        path_in_table = get_path_in_table(times_table)
        best_insertion_position = find_best_insertion_position(tasks, numb_of_machines, i, solution_order, times_table, path_in_table, path_out_table)

        solution_order.insert(best_insertion_position, i)

    stop = timer()
    return solution_order, (stop - start) * 1000
