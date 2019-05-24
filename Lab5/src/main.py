import copy
from datareader import get_data
from makespan import makespan, get_order
from schrage import schrage_n2, schrage_n2_pmtn
from timeit import default_timer as timer
#from carlier import carlier
import carlierPure
import carlierThreads

#task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"] # working WL
#result_list = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

#task_list = ["data.000", "data.001", "data.003", "data.004", "data.006"] # WORKING DL
#result_list = [228, 3026, 3309, 3191, 3446]

task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]


for i in range(0, len(task_list)):
    tasks = get_data(task_list[i])
    #result = result_list[i]

    print("TEST: ", task_list[i])

    # SCHRAGE ORDER
    schrage_n2_order, schrage_n2_time = schrage_n2(tasks)
    shrage_n2_makespan = makespan(schrage_n2_order, tasks)
    #print("[SHRAGE] makespan: {}, time: {}" .format(shrage_n2_makespan, schrage_n2_time))

    # SCHRAGE PMTN ORDER
    schrage_n2_ptmn_makespan, schrage_n2_ptmn_order, schrage_n2_ptmn_time = schrage_n2_pmtn(tasks)
    #print("[SHRAGE PMTN] makespan: {}, time: {}" .format(schrage_n2_ptmn_makespan, schrage_n2_ptmn_time))

    # CARLIER ORDER
    carlier_makespan_pure, carlier_time_pure = carlierPure(copy.deepcopy(tasks))

    # CARLIER THREADS ORDER
    carlier_makespan_threads, carlier_time_threads = carlierThreads(copy.deepcopy(tasks))
