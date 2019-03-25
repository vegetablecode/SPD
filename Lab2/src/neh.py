from timeit import default_timer as timer
import numpy as np
from src.makespan import makespan


def get_sequences(index, prev_sequence):
    if index in prev_sequence: prev_sequence.remove(index)
    sequences = []
    for i in range(0, len(prev_sequence)+1):
        new_sequence = prev_sequence[:]
        new_sequence.insert(i, index)
        sequences.append(new_sequence)
    return sequences

#Defining IR1 modyfication
def nehIR1(tasks_cp,solution_order_cp,lastIndexElement,numb_of_machines):
    maxValue = 0
    for index,task in enumerate(tasks_cp):
        if index in solution_order_cp:
            maxTemp = max(task.times)
            if maxTemp > maxValue:
                maxValue = maxTemp
                taskNumber = index
    if lastIndexElement == taskNumber: return solution_order_cp
    lowest_makespan = float("inf")
    lowest_makespan_sequence = []
    sequences = get_sequences(taskNumber,solution_order_cp)
    for sequence in sequences:
        if makespan(sequence, tasks_cp, numb_of_machines) < lowest_makespan:
            lowest_makespan = makespan(sequence, tasks_cp, numb_of_machines)
            lowest_makespan_sequence = sequence
    return lowest_makespan_sequence

#Defining IR2 modyfication
def nehIR2(tasks_cp,solution_order_cp,lastIndexElement,numb_of_machines):
    maxValue = 0
    for index,task in enumerate(tasks_cp):
        if index in solution_order_cp:
            maxTemp = sum(task.times)
            if maxTemp > maxValue:
                maxValue = maxTemp
                taskNumber = index
    if lastIndexElement == taskNumber: return solution_order_cp
    lowest_makespan = float("inf")
    lowest_makespan_sequence = []
    sequences = get_sequences(taskNumber,solution_order_cp)
    for sequence in sequences:
        if makespan(sequence, tasks_cp, numb_of_machines) < lowest_makespan:
            lowest_makespan = makespan(sequence, tasks_cp, numb_of_machines)
            lowest_makespan_sequence = sequence
    return lowest_makespan_sequence


#Defining IR3 modyfication
def nehIR3(void):
    print("cos")

#Defining IR4 modyfication
def nehIR4(tasks_cp,solution_order_cp,lastIndexElement,numb_of_machines):
    taskNumber = 0
    diffMax = 0
    makespanBase = makespan(solution_order_cp,tasks_cp,numb_of_machines)
    for index,task in enumerate(tasks_cp):
        if index in solution_order_cp:
            idx = solution_order_cp.index(index)
            solution_order_cp.remove(index)
            makespanTemp = makespan(solution_order_cp,tasks_cp,numb_of_machines)
            diffTemp = makespanBase - makespanTemp
            if diffTemp > diffMax: taskNumber = index
            solution_order_cp.insert(idx,index)
    if lastIndexElement == taskNumber: return solution_order_cp
    lowest_makespan = float("inf")
    lowest_makespan_sequence = []
    sequences = get_sequences(taskNumber,solution_order_cp)
    for sequence in sequences:
        if makespan(sequence, tasks_cp, numb_of_machines) < lowest_makespan:
            lowest_makespan = makespan(sequence, tasks_cp, numb_of_machines)
            lowest_makespan_sequence = sequence
    return lowest_makespan_sequence


def neh(tasks, numb_of_machines,neh_type):
    start = timer()
    # step 1: find omegas(j)
    omegas = []
    for task in tasks:
        omegas.append(sum(task.times))

    # step 2: sort in descending order (get sorted order)
    omegas_order = np.argsort(-np.array(omegas)).tolist()

    # steps 3, 4: repeat n times (n = numb of tasks)
    solution_order = []
    for i in omegas_order:  # (3) get task with the highest omega value
        # (4) insert task & pick task with the lowest makespan
        lowest_makespan = float("inf")
        lowest_makespan_sequence = []
        sequences = get_sequences(i, solution_order)

        for sequence in sequences:
            if makespan(sequence, tasks, numb_of_machines) < lowest_makespan:
                lowest_makespan = makespan(sequence, tasks, numb_of_machines)
                lowest_makespan_sequence = sequence
        solution_order = lowest_makespan_sequence

        # step5: IR methods implementation
        if neh_type == 1:
            #IR1
            solution_order = nehIR1(tasks,solution_order,i,numb_of_machines)
        if neh_type == 2:
            #IR2
            solution_order = nehIR2(tasks,solution_order,i,numb_of_machines)
        if neh_type == 3:
            #IR3
            nehIR3()
        if neh_type == 4:
            #IR4
            solution_order = nehIR4(tasks,solution_order,i,numb_of_machines)
    #print(lowest_makespan)
    stop = timer()
    return solution_order, (stop-start)*1000
