from jobtask import JobTask
from task import Task
import os
import sys
import re


def get_data(directory, dataset_name):
    # open file with data
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, '../datasets/' + directory + '/' + dataset_name)

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
                #  numb_of_items = n[0]
                numb_of_columns = n[1]
            else:
                tasks.append(Task(cnt - 1, n))
            cnt += 1
    return tasks


def get_job_data(directory, dataset_name):
    # open file with data
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, '../datasets/' + directory + '/' + dataset_name)

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
                numb_of_machines = n[0]
                numb_of_tasks = n[1]
            else:
                machines_list = [0] * n[0]
                times_list = [0] * n[0]
                j = 1
                for i in range(0, n[0]):
                    machines_list[i] = n[j]
                    times_list[i] = n[j+1]
                    j += 2
                tasks.append(JobTask(cnt - 1, machines_list, times_list))
            cnt += 1
    
    return tasks
