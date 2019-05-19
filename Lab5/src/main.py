import copy
from src.datareader import get_data
from src.makespan import makespan, get_order
from src.schrage import schrage_n2, schrage_n2_pmtn
from src.carlier import carlier

tasks = get_data("in50.txt")

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
print("[INIT] makespan: ", init_makespan)

# SCHRAGE ORDER
schrage_n2_order, schrage_n2_time = schrage_n2(tasks)
shrage_n2_makespan = makespan(schrage_n2_order, tasks)
print("[SHRAGE N^2] makespan: {}, time: {}" .format(shrage_n2_makespan, schrage_n2_time))

# SCHRAGE PMTN ORDER
schrage_n2_ptmn_makespan, schrage_n2_ptmn_order, schrage_n2_ptmn_time = schrage_n2_pmtn(tasks)
print("[SHRAGE N^2 PMTN] makespan: {}, time: {}" .format(schrage_n2_ptmn_makespan, schrage_n2_ptmn_time))

# CARLIER ORDER
carlier_makespan, carlier_time = carlier(copy.deepcopy(tasks))
print("[CARLIER] makespan: {}, time: {}" .format(carlier_makespan, carlier_time))