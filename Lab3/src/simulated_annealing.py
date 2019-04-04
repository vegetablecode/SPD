from math import exp
from makespan import get_order, makespan
import random
import copy
from timeit import default_timer as timer


def swap_random_tasks(order):
    first_index = random.randint(0, len(order)-1)
    second_index = random.randint(0, len(order) - 1)
    order[first_index], order[second_index] = order[second_index], order[first_index]
    return order


def get_max_iterations_number(temp, final_temp, u):
    iterations = 0
    while temp > final_temp:
        iterations += 1
        temp *= u
    return iterations


def insert_random_task(order):
    removed_task_index = random.randint(0, len(order) - 1)
    insertion_task_index = random.randint(0, len(order)-2)
    removed_element = order.pop(removed_task_index)
    order.insert(insertion_task_index, removed_element)
    return order


def get_probability(prev_order, new_order, tasks, numb_of_machines, temperature, move_type):
    prev_order_cmax = makespan(prev_order, tasks, numb_of_machines)
    new_order_cmax = makespan(new_order, tasks, numb_of_machines)

    if move_type == 0:
        if new_order_cmax < prev_order_cmax:
            return 1
        return exp((prev_order_cmax - new_order_cmax) / temperature)
    elif move_type == 1:
        if new_order_cmax < prev_order_cmax:
            return 0
        return exp((prev_order_cmax - new_order_cmax) / temperature)
    elif move_type == 2:
        if prev_order_cmax != new_order_cmax:
            if new_order_cmax < prev_order_cmax:
                return 1
            return exp((prev_order_cmax - new_order_cmax) / temperature)
        else:
            return 0
    return -1


def decision(probability):
    return random.random() < probability


def cool_down_fcn(temperature, u, cooling_fcn_type, iterations, max_iterations):
    if cooling_fcn_type == 0:
        return u * temperature
    else:
        return temperature * (iterations+1 / max_iterations+1)


def simulated_annealing(tasks, numb_of_machines, temperature, final_temperature, u, cooling_fcn_type, move_type,
                        insert, custom_order=""):

    max_iterations_number = get_max_iterations_number(temperature, final_temperature, u)

    start = timer()

    # step 1: create initial order
    if custom_order == "":
        order = get_order(tasks)
    else:
        order = copy.deepcopy(custom_order)

    iterations = 0
    for i in range(0, max_iterations_number):
        # step 2: generate movement
        new_order = copy.deepcopy(order)
        if insert == 0:
            swap_random_tasks(new_order)
        elif insert == 1:
            insert_random_task(new_order)

        # step 3: make a move or not
        probability = get_probability(order, new_order, tasks, numb_of_machines, temperature, move_type)
        if decision(probability):
            order = copy.deepcopy(new_order)

        # step 4: cooling down
        temperature = cool_down_fcn(temperature, u, cooling_fcn_type, iterations, max_iterations_number)

        iterations += 1

    stop = timer()

    return order, iterations, (stop-start)*1000
