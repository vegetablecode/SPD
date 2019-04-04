from math import exp
from makespan import get_order, makespan
import random
import copy
from timeit import default_timer as timer


def swam_random_tasks(order):
    first_index = random.randint(0, len(order)-1)
    second_index = random.randint(0, len(order) - 1)
    order[first_index], order[second_index] = order[second_index], order[first_index]
    return order


def get_probability(prev_order, new_order, tasks, numb_of_machines, temperature, move_type):
    prev_order_cmax = makespan(prev_order, tasks, numb_of_machines)
    new_order_cmax = makespan(new_order, tasks, numb_of_machines)

    if new_order_cmax < prev_order_cmax:
        return 1
    return exp((prev_order_cmax - new_order_cmax) / temperature)


def decision(probability):
    return random.random() < probability


def cool_down_fcn(temperature, u, cooling_fcn_type):
    return u * temperature


def simulated_annealing(tasks, numb_of_machines, temperature, final_temperature, u, cooling_fcn_type, move_type):
    start = timer()

    # step 1: create initial order
    order = get_order(tasks)

    iterations = 0
    while temperature > final_temperature:
        # step 2: generate movement
        new_order = copy.deepcopy(order)
        swam_random_tasks(new_order)

        # step 3: make a move or not
        probability = get_probability(order, new_order, tasks, numb_of_machines, temperature, move_type)
        if decision(probability):
            order = copy.deepcopy(new_order)

        # step 4: cooling down
        temperature = cool_down_fcn(temperature, u, cooling_fcn_type)

        iterations += 1

    stop = timer()

    return order, iterations, (stop-start)*1000
