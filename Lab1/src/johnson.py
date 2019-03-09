from src.task import Task


# Johnson main function
def johnson(tasks, numb_of_machines):
    if numb_of_machines == 2:
        print("Model dwumaszynowy")
        return johnson2(tasks)
    else:
        print("Model trzymaszynowy")
        return johnson3(tasks)


# Johnson in case of two machines
def johnson2(tasks):
    list1 = []
    list2 = []
    while len(tasks) > 0:
        shortest_index_1 = 0  # index of shortest task for 1st machine
        shortest_index_2 = 0  # index of shortest task for 2st machine
        for i in range(0, len(tasks)):
            if tasks[i].times[0] < tasks[shortest_index_1].times[0]:
                shortest_index_1 = i
            if tasks[i].times[1] < tasks[shortest_index_2].times[1]:
                shortest_index_2 = i
        # if the shortest task is for 1st machine OR both of machines have the shortest task with the same time
        if (shortest_index_1 == shortest_index_2) | (shortest_index_1 == shortest_index_2):
            list1.append(tasks[shortest_index_1].index)
            del tasks[shortest_index_1]
        else:
            list2.insert(0, tasks[shortest_index_2].index)
            del tasks[shortest_index_2]
    return list1+list2


# Johnson in case of three machines
def johnson3(tasks):
    # Creating 2 virtual machines
    virtual_tasks = []
    for i in range(0, len(tasks)):
        first_comp = tasks[i].times[0] + tasks[i].times[1]
        second_comp = tasks[i].times[1] + tasks[i].times[2]
        virtual_tasks.append(Task(i, [first_comp, second_comp]))
    return johnson2(virtual_tasks)
