from math import exp
from src.makespan import get_order, makespan
import random
import copy

def swam_random_tasks(order):
    first_index = random.randint(0, len(order)-1)
    second_index = random.randint(0, len(order) - 1)
    order[first_index], order[second_index] = order[second_index], order[first_index]
    return order


def get_probability(prev_order, new_order, tasks, temperature):
    prev_order_cmax = makespan(prev_order, tasks)
    new_order_cmax = makespan(new_order, tasks)

    if new_order_cmax < prev_order_cmax:
        return 1
    return exp((prev_order_cmax - new_order_cmax) / temperature)


def decision(probability):
    return random.random() < probability


def cool_down_fcn(temperature, u):
    return u * temperature


def simulated_annealing(tasks, temperature, min_temperature, u):
    # step 1: create initial order
    order = get_order(tasks)

    while temperature > min_temperature:
        # step 2: generate movement
        new_order = copy.deepcopy(order)
        swam_random_tasks(new_order)

        # step 3: make a move or not
        probability = get_probability(order, new_order, tasks, temperature)
        if decision(probability):
            order = copy.deepcopy(new_order)

        # step 4: cooling down
        temperature = cool_down_fcn(temperature, u)

    return order
