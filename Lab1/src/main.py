import os
import sys
import re
from task import Task
from bruteforce import permute

#Function to calculate total makespan - 2 machine version
def makespan(order1, order2):
    time1 = 0
    time2 = 0
    for i in range (0, len(order1)):
        time1 += order1[i]
        if time2 < time1:
            time2 = time1 + order2[i]
        else:
            time2 += order2[i]
    #print("Work time of machine 1: {}".format(time1))
    return time2

# open file with data
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, '../datasets/data.5')

#If the file does not exist
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

order1 = []                     #machine1
order2 = []                     #machine2
for task in tasks:
    order1.append(task.times[0])
    order2.append(task.times[1])
    #print(task.times)           #printing times of each task
makespan(order1, order2)        #makespan with normal order

#Generating indexTable
indexTable = []
for i in range(0, numb_of_items):
    indexTable.append(i)

#Searching minimum makespan with bruteforce
for p in permute(indexTable):
    tempOrder1 = []
    tempOrder2 = []
    for i in range(0, len(indexTable)-1):
        tempOrder1.append(order1[p[i]])
        tempOrder2.append(order2[p[i]])
    span = makespan(tempOrder1,tempOrder2)
    print p
    print("Total Makespan: {}".format(span))
