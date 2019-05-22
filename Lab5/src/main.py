import copy
from src.datareader import get_data
from src.makespan import makespan, get_order
from src.schrage import schrage_n2, schrage_n2_pmtn
from src.carlier import carlier


task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
result_list = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

for i in range(0, len(task_list)):
    tasks = get_data(task_list[i])
    result = result_list[i]

    print("TEST: ", task_list[i])

    # SCHRAGE ORDER
    schrage_n2_order, schrage_n2_time = schrage_n2(tasks)
    shrage_n2_makespan = makespan(schrage_n2_order, tasks)
    #print("[SHRAGE] makespan: {}, time: {}" .format(shrage_n2_makespan, schrage_n2_time))

    # SCHRAGE PMTN ORDER
    schrage_n2_ptmn_makespan, schrage_n2_ptmn_order, schrage_n2_ptmn_time = schrage_n2_pmtn(tasks)
    #print("[SHRAGE PMTN] makespan: {}, time: {}" .format(schrage_n2_ptmn_makespan, schrage_n2_ptmn_time))

    # CARLIER ORDER
    carlier_makespan, carlier_time = carlier(copy.deepcopy(tasks))
    #print("[CARLIER] makespan: {}, time: {}" .format(carlier_makespan, carlier_time))

    # VALIDATION
    test_result = ["BAD RESULT", "OK"][carlier_makespan == result]
    print("RESULT: ", test_result)
    print("---------------")

