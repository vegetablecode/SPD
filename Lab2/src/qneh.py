from timeit import default_timer as timer
import numpy as np
import copy
from makespan import makespan

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

def critical_path_creating(solution_order,tasks,numb_of_machines):
    times_table = get_times_table(solution_order, tasks, numb_of_machines)
    path_out_table = get_path_out_table(times_table)
    path_in_table = get_path_in_table(times_table)
    #Critical path with o and 1 matrix
    i = 0
    j = 0
    criticalMatrix = np.zeros((numb_of_machines, len(solution_order)))
    criticalMatrix.astype(int)
    criticalMatrix[0,0] = 1
    while i < len(solution_order) and j < numb_of_machines:
        criticalMatrix[j,i] = 1
        if j == len(solution_order) and i == numb_of_machines: break
        if i < len(solution_order)-1 and j < numb_of_machines-1:
            if path_out_table[j][i+1] < path_out_table[j+1][i]: j += 1
            else: i += 1
        else:
            if j == numb_of_machines-1: i += 1
            else:
                if i == len(solution_order)-1: j += 1
    return times_table,criticalMatrix

def IR1_mod(times_table, criticalMatrix, solution_order):
    maxValue = 0
    maxObj = -1
    for i in range(0, len(times_table)):
        for j in range(0, len(solution_order)):
            if times_table[i][j] > maxValue and criticalMatrix[i][j] == 1:
                maxValue = times_table[i][j]
                maxObj = j
    return solution_order[j]

def IR2_mod(times_table, criticalMatrix, solution_order):
    maxValue = 0
    for j in range(0, len(solution_order)):
        for i in range(0, len(times_table)):
            if criticalMatrix[i][j] == 1:
                temp = times_table[i][j]
        if temp > maxValue:
            maxValue = temp
            maxTask = j
    return solution_order[maxTask]

def IR3_mod(times_table, criticalMatrix, solution_order):
    maxValue = 0
    for j in range(0, len(solution_order)):
        temp = 0
        for i in range(0, len(times_table)):
            if criticalMatrix[i][j] == 1:
                temp += 1
        if temp > maxValue:
            maxValue = temp
            maxTask = j
    return solution_order[maxTask]

def IR4_mod(tasks,solution_order, numb_of_machines):
    maxDiff = 0
    baseTime = makespan(solution_order,tasks, numb_of_machines)
    for i in solution_order:
        idx = solution_order.index(i)
        solution_order.remove(i)
        tempTime = makespan(solution_order, tasks, numb_of_machines)
        if baseTime - tempTime > maxDiff:
            maxDiff = baseTime - tempTime
            maxTask = i
        solution_order.insert(idx, i)
    return maxTask

def qneh(tasks, numb_of_machines,neh_type):
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
        # step5: IR methods implementation
        objectToRemove = i
        if neh_type == 1:
            #IR1
            times_table, criticalMatrix = critical_path_creating(solution_order,tasks,numb_of_machines)
            objectToRemove = IR1_mod(times_table, criticalMatrix,solution_order)

        if neh_type == 2:
            #IR2
            times_table, criticalMatrix = critical_path_creating(solution_order,tasks,numb_of_machines)
            objectToRemove = IR2_mod(times_table, criticalMatrix,solution_order)

        if neh_type == 3:
            #IR3
            times_table, criticalMatrix = critical_path_creating(solution_order,tasks,numb_of_machines)
            objectToRemove = IR3_mod(times_table, criticalMatrix,solution_order)

        if neh_type == 4:
            #IR4
            objectToRemove = IR4_mod(tasks, solution_order, numb_of_machines)

        if i != objectToRemove:
            solution_order.remove(objectToRemove)
            times_table = get_times_table(solution_order, tasks, numb_of_machines)
            path_out_table = get_path_out_table(times_table)
            path_in_table = get_path_in_table(times_table)
            best_insertion_position = find_best_insertion_position(tasks, numb_of_machines, objectToRemove, solution_order, times_table, path_in_table, path_out_table)
            solution_order.insert(best_insertion_position, objectToRemove)

    stop = timer()
    return solution_order, (stop - start) * 1000
