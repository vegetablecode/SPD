from makespan import makespan
from makespan import get_order
from timeit import default_timer as timer


def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p
            xs[low], xs[i] = xs[i], xs[low]


def bruteforce(tasks, numb_of_machines):
    start = timer()
    best_order = get_order(tasks)
    best_makespan = makespan(best_order, tasks, numb_of_machines)

    for p in permute(get_order(tasks)):
        print("order: {}" .format(p))
        print("makespan: {}" .format(makespan(p, tasks, numb_of_machines)))
        print("---")
        if makespan(p, tasks, numb_of_machines) < best_makespan:
            best_order = list(p)
            best_makespan = makespan(p, tasks, numb_of_machines)
    stop = timer()
    return best_order, (stop-start)*1000
