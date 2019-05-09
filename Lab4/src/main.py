import copy
from src.datareader import get_data
from src.makespan import makespan, to_natural_order, get_order
from src.schrage import schrage_n2, schrage_n2_pmtn
from src.simulated_annealing import simulated_annealing

tasks = get_data("data.001")

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
print("[INIT] makespan: ", init_makespan)

# SCHRAGE ORDER
schrage_n2_order = schrage_n2(tasks)
shrage_n2_makespan = makespan(schrage_n2_order, tasks)
print("[SHRAGE N^2] makespan: ", shrage_n2_makespan)


schrage_n2_ptmn_makespan, schrage_n2_ptmn_order = schrage_n2_pmtn(tasks)
print("[SHRAGE N^2 PMTN] makespan:", schrage_n2_ptmn_makespan)

sa_order = simulated_annealing(copy.deepcopy(tasks), 500000, 0.0001, 0.999)
sa_makespan = makespan(sa_order, tasks)
print("[SA] makespan:", sa_makespan)