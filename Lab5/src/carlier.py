from src.schrage import schrage, schrage_pmtn
import copy
from timeit import default_timer as timer
from src.datareader import get_data


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
    start = timer()

    u, pi = schrage(copy.deepcopy(tasks))

    if u < ub:
        ub = u

    # find b, a, c values
    b = calculate_b(u, pi)
    a = calculate_a(b, u, pi)
    c = calculate_c(b, a, pi)

    #  if c doesn't exist
    if c < 0:
        stop = timer()
        return ub, (stop - start) * 1000

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
        ub, time = carlier_dl(copy.deepcopy(pi))
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
        ub, time = carlier_dl(copy.deepcopy(pi))
    pi[c].times[2] = r_pi_c

    stop = timer()
    return ub, (stop - start) * 1000


# wide left
def carlier_wl(tasks):
    start = timer()

    # ----- "GLOBAL" VARIABLES DECLARATION ----- #
    # u: cmax for schrage
    # pi: tasks sorted with schrage
    # ub: upper border
    # lb: lower border

    u, pi = schrage(copy.deepcopy(tasks))
    ub = 999999999
    lb = 0

    pi_list = [pi]

    # --------- CARLIER ALGORITHM LOOP --------- #
    while True:
        u, pi = schrage(copy.deepcopy(pi_list[0]))
        if u < ub:
            ub = u

        # find b, a, c values
        b = calculate_b(u, pi)
        a = calculate_a(b, u, pi)
        c = calculate_c(b, a, pi)

        #  if c doesn't exist
        if c < 0:
            stop = timer()
            return ub, (stop - start) * 1000

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


task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
result_list = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

for i in range(0, len(task_list)):
    tasks = get_data(task_list[i])
    result = result_list[i]

    print("TEST: ", task_list[i])
    print("-")

    # ---------------- WIDE LEFT
    ub = 999999999
    u, pi = schrage(copy.deepcopy(tasks))

    # ALGORITHM
    carlier_makespan, carlier_time = carlier_dl(copy.deepcopy(tasks))
    print("[CARLIER WL] makespan: {}, time: {}".format(carlier_makespan, carlier_time))

    # VALIDATION
    test_result = ["BAD RESULT", "OK"][carlier_makespan == result]
    print("RESULT: ", test_result, " | SHOULD BE: ", result_list[i])
    print("-")

    # ---------------- WIDE LEFT
    ub = 999999999
    u, pi = schrage(copy.deepcopy(tasks))

    # ALGORITHM
    carlier_makespan, carlier_time = carlier_wl(copy.deepcopy(tasks))
    print("[CARLIER DL] makespan: {}, time: {}".format(carlier_makespan, carlier_time))

    # VALIDATION
    test_result = ["BAD RESULT", "OK"][carlier_makespan == result]
    print("RESULT: ", test_result, " | SHOULD BE: ", result_list[i])
    print("---------------------------------------------")
