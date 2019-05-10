import copy
from datareader import get_data
from makespan import makespan, to_natural_order, get_order
from schrage import schrage_n2, schrage_n2_pmtn
from schrage_nlogn import schrage_nlogn
from simulated_annealing import simulated_annealing
from extended_potts import nip_schrage

tasks = get_data("data.001")

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
print("[INIT] makespan: ", init_makespan)

# SCHRAGE ORDER
schrage_n2_order = schrage_n2(tasks)
shrage_n2_makespan = makespan(schrage_n2_order, tasks)
print("[SHRAGE N^2] makespan: ", shrage_n2_makespan)

# SCHRAGE ORDER NLOGN
schrage_nlogn_order, period = schrage_nlogn(tasks)
schrage_nlogn_makespan = makespan(schrage_nlogn_order, tasks)
print("[SHRAGE NLOGN] makespan: ", schrage_nlogn_makespan)

schrage_n2_ptmn_makespan, schrage_n2_ptmn_order = schrage_n2_pmtn(tasks)
print("[SHRAGE N^2 PMTN] makespan:", schrage_n2_ptmn_makespan)

#sa_order = simulated_annealing(copy.deepcopy(tasks), 500000, 0.0001, 0.999)
#sa_makespan = makespan(sa_order, tasks)
#print("[SA] makespan:", sa_makespan)

cmax, ord, d, f = nip_schrage(tasks)
print("[NIP SHRAGE N^2] makespan: ", cmax)
