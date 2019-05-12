def get_order(tasks):
    order = []
    for item in tasks:
        order.append(item.index)
    return order


def set_order(tasks, order):
    for i in range(0, len(tasks)):
        tasks[i].index = order[i]


def makespan(order, tasks):
    r_times = []  # the moment after finishing preparing task
    p_times = []  # the moment after finishing executing task
    q_times = []  # the moment after finishing transporting task
    for i in order:
        r_times.append(tasks[i].times[0])
        # calculate p_time
        if len(p_times) > 0:
            # append max of (r_time from this task, p_time from prev one) + execution time
            p_times.append(max(r_times[-1], p_times[-1]) + tasks[i].times[1])
        else:
            p_times.append(r_times[-1] + tasks[i].times[1])
        q_times.append(p_times[-1] + tasks[i].times[2])

    if len(q_times) > 0:
        return max(q_times)
    else:
        return 0


def to_natural_order(order):
    natural_order = []
    for i in range(0, len(order)):
        natural_order.append(order[i] + 1)
    return natural_order
