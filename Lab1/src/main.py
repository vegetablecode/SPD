import os
import sys
import re
import copy
from src.task import Task
from src.bruteforce import permute
from src.johnson import johnson2


def makespan(order, tasks, numb_of_machines):
    times = []
    for j in range(0, numb_of_machines):
        times.append(0)
    for i in order:
        times[0] += tasks[i].times[0]
        for j in range(1, numb_of_machines):
            if times[j] < times[j-1]:
                times[j] = times[j-1]
            times[j] += tasks[i].times[j]

    return max(times)


# open file with data
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, '../datasets/data.1')

# if the file does not exist
if not os.path.isfile(filename):
    print("File path {} does not exist. Exiting...".format(filename))
    sys.exit()

# convert file to list of tasks
tasks = []
with open(filename) as fp:
    cnt = 0
    for line in fp:
        n = list(map(int, re.findall(r'\d+', line)))
        if cnt == 0:
            numb_of_items = n[0]
            numb_of_machines = n[1]
        else:
            tasks.append(Task(n))
        cnt += 1

# generating index table
index_table = []
for i in range(0, numb_of_items):
    index_table.append(i)


# searching for min makespan with bruteforce
best_order = index_table
best_makespan = makespan(best_order, tasks, numb_of_machines)

for p in permute(index_table):
    if makespan(p, tasks, numb_of_machines) < best_makespan:
        best_order = list(p)
        best_makespan = makespan(p, tasks, numb_of_machines)

print("Best order: {}" .format(best_order))
print("Best makespan: {}" .format(best_makespan))


# searching for min makespan with Johnson
johnson_order = johnson2(copy.deepcopy(tasks))
johnson_makespan = makespan(johnson_order, tasks, numb_of_machines)
print("Best order (Johnson): {}" .format(johnson_order))
print("Best makespan (Johnson): {}" .format(johnson_makespan))