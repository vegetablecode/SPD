from makespan import get_order, makespan
import copy
import numpy as np
from task import Task
from binaryTree_min import BinaryHeap_blocked
from binaryTree_max import BinaryHeap_available
import time

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

def schrage_nlogn(tasks):
    start_time = time.time()
    flag = 0
    N_tasks = copy.deepcopy(tasks)
    blockedTasks = []
    availableTasks = []
    blockedTasks = BinaryHeap_blocked()
    blockedTasks.buildHeap(N_tasks)
    availableTasks = BinaryHeap_available()
    solution_order = []
    t = 0
    #blockedTasks.buildHeap(N_tasks)
    while blockedTasks.isEmpty() == 0 or availableTasks.isEmpty() == 0:
        if blockedTasks.isEmpty() == 0:
            acquiredTask = blockedTasks.delMin()
            availableTasks.insert(acquiredTask)
            if flag == 1:
                t = acquiredTask.times[0]
                flag = 0
        if availableTasks.isEmpty() == 0:
            chosenTask = availableTasks.delMax()
            solution_order.append(chosenTask)
            if t == 0:
                t = chosenTask.times[0] + chosenTask.times[1]
            else:
                t += chosenTask.times[1]
        else:
            flag = 1
    end_time = time.time()
    period = end_time - start_time
    return get_order(solution_order), period
