def johnson2(tasks):
    list1 = []
    list2 = []
    while (len(list1)+len(list2)) < len(tasks):
        shortest_index = [99, 99]
        shortest_task = [999, 999]
        for i in range(0, len(tasks)):
            if tasks[i].times[0] < shortest_task[0]:
                shortest_task[0] = tasks[i].times[0]
                shortest_index[0] = i
            if tasks[i].times[1] < shortest_task[1]:
                shortest_task[1] = tasks[i].times[1]
                shortest_index[1] = i
        if shortest_task[0] == shortest_task[1]:
            tasks[shortest_index[0]].times = [999, 999]
            list1.append(shortest_index[0])
        elif shortest_task[0] < shortest_task[1]:  # shortest task belongs to 1. machine
            tasks[shortest_index[0]].times = [999, 999]
            list1.append(shortest_index[0])
        else:  # shortest task belongs to 2. machine
            tasks[shortest_index[1]].times = [999, 999]
            list2.insert(0, shortest_index[1])

    return list1+list2

