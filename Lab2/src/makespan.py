def get_order(tasks):
    order = []
    for item in tasks:
        order.append(item.index)
    return order


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


def to_natural_order(order):
    natural_order = []
    for i in range(0, len(order)):
        natural_order.append(order[i] + 1)
    return natural_order
