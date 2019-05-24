from schrage import schrage, schrage_pmtn
import copy
from timeit import default_timer as timer
from datareader import get_data
import numpy as np
from carlierPure import carlier_wl_pure
#Libraries needed for threading
import multiprocessing
import threading
from multiprocessing.pool import ThreadPool
#------------------------------


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

def rightNodeThread(pi, a, b, c, r_1, p_1, q_1):
    pi1 = pi
    r_pi1_c = pi1[c].times[2]
    pi1[c].times[2] = max(pi1[c].times[2], q_1 + p_1)

    p_2 = 0
    r_2 = pi1[c].times[0]
    q_2 = pi1[c].times[2]

    for i in range(c, b + 1):
        p_2 += pi1[i].times[1]
        if r_2 > pi1[i].times[0]:
            r_2 = pi1[i].times[0]
        if q_2 > pi1[i].times[2]:
            q_2 = pi1[i].times[2]

    lb1, order1 = schrage_pmtn(copy.deepcopy(pi1))
    lb1 = max(max(r_1 + q_1 + p_1, r_2 + q_2 + p_2), lb1)
    if lb1 < ub:
        pi_list.append(copy.deepcopy(pi1))
    pi1[c].times[2] = r_pi1_c

def leftNodeThread(pi, a, b, c, r_1, p_1, q_1):
    pi2 = pi
    r_pi2_c = pi2[c].times[0]
    pi2[c].times[0] = max(pi2[c].times[0], r_1 + p_1)

    p_3 = 0
    r_3 = pi2[c].times[0]
    q_3 = pi2[c].times[2]

    for i in range(c, b + 1):
        p_3 += pi2[i].times[1]
        if r_3 > pi2[i].times[0]:
            r_3 = pi2[i].times[0]
        if q_3 > pi2[i].times[2]:
            q_3 = pi2[i].times[2]

    lb2, ptmn_order2 = schrage_pmtn(copy.deepcopy(pi2))
    lb2 = max(max(r_1 + q_1 + p_1, r_3 + q_3 + p_3), lb2)
    if lb2 < ub:
        pi_list.append(copy.deepcopy(pi2))
    pi2[c].times[0] = r_pi2_c

# wide left
def carlier_wl_parallel(tasks):
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

    #Switching to two carlierThreads
    #---------------------------------------------------------------------------
    # RIGHT NODE
    thread1 = threading.Thread(rightNodeThread(pi, a, b, c, r_1, p_1, q_1))
    thread1.start()
    thread1.join()
    #---------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # LEFT NODE
    thread2 = threading.Thread(leftNodeThread(pi, a, b, c, r_1, p_1, q_1))
    thread2.start()
    thread2.join()
    #---------------------------------------------------------------------------
    while threading.activeCount()>1:
        time.sleep(1)

    # remove checked node from the list
    pi_list.pop(0)
    return carlier_wl_parallel(tasks)


task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
result_list = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

for i in range(0, len(task_list)):
    tasks = get_data(task_list[i])
    result = result_list[i]

    print("THREADS TEST: ", task_list[i])
    print("-")

    # ------------------------------------------------ WIDE LEFT
    u, pi = schrage(copy.deepcopy(tasks))
    ub = 999999999
    lb = 0

    pi_list = [pi]

    # ALGORITHM
    start = timer()
    carlier_wl_parallel(copy.deepcopy(tasks))
    stop = timer()
    carlier_time_parallel = (stop - start) * 1000
    print("[CARLIER DL PARALLEL] makespan: {}, time: {}".format(ub, carlier_time_parallel))

    carlier_wl_pure(copy.deepcopy(tasks))
    stop = timer()
    carlier_time_pure = (stop - start) * 1000
    print("[CARLIER DL SEQUENCE] makespan: {}, time: {}".format(ub, carlier_time_pure))
    # VALIDATION
    test_result = ["BAD RESULT", "OK"][ub == result]
    print("RESULT: ", test_result, " | SHOULD BE: ", result_list[i])
    print("-")
    if carlier_time_pure > carlier_time_parallel:
        print("SEQUENCE FASTER")
    else:
        print("PARALLEL FASTER")

    print("---------------------------------------------")
