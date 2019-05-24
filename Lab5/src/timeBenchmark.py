from schrage import schrage, schrage_pmtn, schrage_n2, schrage_n2_pmtn
import copy
from timeit import default_timer as timer
from datareader import get_data
import numpy as np
from makespan import makespan, get_order, create_instances


def calculate_b(u, pi):
    b = 0
    cmax = 0
    for i in range(0, len(pi)):
        cmax = max(cmax, max(pi[i].times[0], cmax) + pi[i].times[1])
        if u == cmax + pi[i].times[2]:
            b = i
    return b


def calculate_a(b, u, pi):
    a = 0
    sum_tasks = 0
    for i in range(b, -1, -1):
        sum_tasks += pi[i].times[1]
        if u == sum_tasks + pi[i].times[0] + pi[b].times[2]:
            a = i
            break
    return a


def calculate_c(b, a, pi):
    c = -1
    for i in range(a, b + 1):
        if pi[i].times[2] < pi[b].times[2]:
            c = i
    return c


# deep left
def carlier_dl(tasks):
    global ub
    global pi

    u, pi = schrage(copy.deepcopy(tasks))

    if u < ub:
        ub = u

    # find b, a, c values
    b = calculate_b(u, pi)
    a = calculate_a(b, u, pi)
    c = calculate_c(b, a, pi)

    #  if c doesn't exist
    if c < 0:
        return ub

    # calculate r1, p1, q1
    r_1 = pi[c + 1].times[0]
    p_1 = 0
    q_1 = pi[c + 1].times[2]

    for i in range(c + 1, b + 1):
        p_1 += pi[i].times[1]
        if r_1 > pi[i].times[0]:
            r_1 = pi[i].times[0]
        if q_1 > pi[i].times[2]:
            q_1 = pi[i].times[2]

    # LEFT NODE
    r_pi_c = pi[c].times[0]
    pi[c].times[0] = max(pi[c].times[0], r_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, ptmn_order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)

    if lb < ub:
        ub = carlier_dl(copy.deepcopy(pi))
    pi[c].times[0] = r_pi_c

    # RIGHT NODE
    r_pi_c = pi[c].times[2]
    pi[c].times[2] = max(pi[c].times[2], q_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)

    if lb < ub:
        ub = carlier_dl(copy.deepcopy(pi))
    pi[c].times[2] = r_pi_c

    return ub


def sort_tasks(pi_list, lb_list):
    order = np.argsort(lb_list)
    new_pi_list = []
    new_lb_list = []
    for i in order:
        new_pi_list.append(pi_list[i])
        new_lb_list = [lb_list[i]]
    pi_list = copy.deepcopy(new_pi_list)
    lb_list = copy.deepcopy(new_lb_list)


# wide left
def carlier_greedy(tasks):
    # ----- "GLOBAL" VARIABLES DECLARATION ----- #
    # u: cmax for schrage
    # pi: tasks sorted with schrage
    # ub: upper border
    # lb: lower border

    global u
    global pi
    global ub
    global lb
    global pi_list
    global lb_list

    u, pi = schrage(copy.deepcopy(pi_list[0]))
    if u < ub:
        ub = u

    # find b, a, c values
    b = calculate_b(u, pi)
    a = calculate_a(b, u, pi)
    c = calculate_c(b, a, pi)

    #  if c doesn't exist
    if c < 0:
        return ub

    # calculate r1, p1, q1
    r_1 = pi[c + 1].times[0]
    p_1 = 0
    q_1 = pi[c + 1].times[2]

    for i in range(c + 1, b + 1):
        p_1 += pi[i].times[1]
        if r_1 > pi[i].times[0]:
            r_1 = pi[i].times[0]
        if q_1 > pi[i].times[2]:
            q_1 = pi[i].times[2]

    # LEFT NODE
    r_pi_c = pi[c].times[0]
    pi[c].times[0] = max(pi[c].times[0], r_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, ptmn_order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)
    if lb < ub:
        pi_list.append(copy.deepcopy(pi))
        lb_list.append(lb)
    pi[c].times[0] = r_pi_c

    # RIGHT NODE
    r_pi_c = pi[c].times[2]
    pi[c].times[2] = max(pi[c].times[2], q_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)

    if lb < ub:
        pi_list.append(copy.deepcopy(pi))
        lb_list.append(lb)
    pi[c].times[2] = r_pi_c

    # remove checked node from the list
    pi_list.pop(0)
    lb_list.pop(0)

    # sort tasks
    sort_tasks(pi_list, lb_list)
    if len(pi_list) > 0:
        return carlier_greedy(tasks)


# wide left
def carlier_wl(tasks):
    # ----- "GLOBAL" VARIABLES DECLARATION ----- #
    # u: cmax for schrage
    # pi: tasks sorted with schrage
    # ub: upper border
    # lb: lower border

    global u
    global pi
    global ub
    global lb
    global pi_list

    u, pi = schrage(copy.deepcopy(pi_list[0]))
    if u < ub:
        ub = u

    # find b, a, c values
    b = calculate_b(u, pi)
    a = calculate_a(b, u, pi)
    c = calculate_c(b, a, pi)

    #  if c doesn't exist
    if c < 0:
        return ub

    # calculate r1, p1, q1
    r_1 = pi[c + 1].times[0]
    p_1 = 0
    q_1 = pi[c + 1].times[2]

    for i in range(c + 1, b + 1):
        p_1 += pi[i].times[1]
        if r_1 > pi[i].times[0]:
            r_1 = pi[i].times[0]
        if q_1 > pi[i].times[2]:
            q_1 = pi[i].times[2]

    # LEFT NODE
    r_pi_c = pi[c].times[0]
    pi[c].times[0] = max(pi[c].times[0], r_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, ptmn_order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)
    if lb < ub:
        pi_list.append(copy.deepcopy(pi))
    pi[c].times[0] = r_pi_c

    # RIGHT NODE
    r_pi_c = pi[c].times[2]
    pi[c].times[2] = max(pi[c].times[2], q_1 + p_1)

    p_2 = 0
    r_2 = pi[c].times[0]
    q_2 = pi[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi[i].times[1]
        if r_2 > pi[i].times[0]:
            r_2 = pi[i].times[0]
        if q_2 > pi[i].times[2]:
            q_2 = pi[i].times[2]

    lb, order = schrage_pmtn(copy.deepcopy(pi))
    lb = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb)

    if lb < ub:
        pi_list.append(copy.deepcopy(pi))
    pi[c].times[2] = r_pi_c

    # remove checked node from the list
    pi_list.pop(0)
    if len(pi_list) > 0:
        return carlier_wl(tasks)


schrage_makespans = []
schrage_pmtn_makespans = []
wide_left_makespans = []
deep_left_makespans = []
greedy_makespans = []

schrage_times = []
schrage_pmtn_times = []
wide_left_times = []
deep_left_times = []
greedy_times = []

taskset = []
x = []

for i in range(5, 300):
    taskset.append(create_instances(i))
    x.append(i)

iter = 0
for i in range(0, len(taskset)):
    tasks = copy.deepcopy(taskset[i])

    # ------------------------------------------------ SCHRAGE
    # SCHRAGE ORDER
    schrage_n2_order, schrage_n2_time = schrage_n2(tasks)
    shrage_n2_makespan = makespan(schrage_n2_order, tasks)
    # print("[SHRAGE N^2] order: ", schrage_n2_order)

    schrage_makespans.append(shrage_n2_makespan)
    schrage_times.append(schrage_n2_time)
    # ------------------------------------------------ SCHRAGE
    # SCHRAGE ORDER N2 PMTN
    schrage_n2_ptmn_makespan, schrage_n2_ptmn_order, schrage_n2_ptmn_time = schrage_n2_pmtn(tasks)

    schrage_pmtn_makespans.append(schrage_n2_ptmn_makespan)
    schrage_pmtn_times.append(schrage_n2_ptmn_time)
    # ------------------------------------------------ DEEP LEFT
    ub = 999999999
    u, pi = schrage(copy.deepcopy(tasks))

    # ALGORITHM
    start = timer()
    carlier_makespan = carlier_dl(copy.deepcopy(tasks))
    stop = timer()
    carlier_time = (stop-start)*1000
    deep_left_makespans.append(carlier_makespan)
    deep_left_times.append(carlier_time)
    # ------------------------------------------------ WIDE LEFT
    u, pi = schrage(copy.deepcopy(tasks))
    ub = 999999999
    lb = 0

    pi_list = [pi]

    # ALGORITHM
    start = timer()
    carlier_wl(copy.deepcopy(tasks))
    stop = timer()
    carlier_time = (stop - start) * 1000

    wide_left_makespans.append(ub)
    wide_left_times.append(carlier_time)

    # ------------------------------------------------ WIDE GREEDY
    u, pi = schrage(copy.deepcopy(tasks))
    ub = 999999999
    lb = 0

    pi_list = [pi]
    lb_list = [lb]

    # ALGORITHM
    start = timer()
    carlier_greedy(copy.deepcopy(tasks))
    stop = timer()
    carlier_time = (stop - start) * 1000

    greedy_makespans.append(ub)
    greedy_times.append(carlier_time)
    #print(iter)
    iter += 1

print("Finished")
