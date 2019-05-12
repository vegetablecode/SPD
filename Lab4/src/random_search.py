from src.makespan import get_order, makespan
import random
import time
import copy


def get_random_schedule(tasks):
    return random.sample(range(0, len(tasks)), len(tasks))



def get_column(tasks, element):
    column = []
    for item in tasks:
        column.append(item.times[element])
    return column


def random_search(tasks, max_time):
    numb_of_experiments = 100  # experiments performed per loop
    best_solution = ""
    best_cmax = 10000000

    t0 = time.time()
    total_experiments = 0

    rs = get_random_schedule(tasks)

    while True:
        start = time.time()
        for i in range(0, numb_of_experiments):
            random.shuffle(rs)
            cmax = makespan(rs, tasks)

            if cmax < best_cmax:
                best_cmax = cmax
                best_solution = copy.deepcopy(rs)

        total_experiments += numb_of_experiments

        if max_time and time.time() - t0 > max_time:
            break

        t = time.time() - start

        #if t > 0:
            #print("Best: ", best_cmax, ", time: ", time.time() - t0)

    return best_solution
