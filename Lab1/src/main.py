import os
import sys
import re
from src.task import Task


def makespan(order1, order2):
    time1 = 0
    time2 = 0
    for i in range (0, len(order1)):
        time1 += order1[i]
        time2 += (time1 + order2[i])



# open file with data
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, '../datasets/data.1')

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

order1 = []
order2 = []
for task in tasks:
    order1.append(task.times[0])
    order2.append(task.times[1])
    print(task.times)

makespan(order1, order2)