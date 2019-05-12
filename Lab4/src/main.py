import copy
from src.datareader import get_data
from src.makespan import makespan, to_natural_order, get_order
from src.schrage import schrage_n2, schrage_n2_pmtn, schrage_nlogn, schrage_nlogn_pmtn

tasks = get_data("in50.txt")

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
#print("[INIT] makespan: ", init_makespan)

# SCHRAGE ORDER
schrage_n2_order = schrage_n2(tasks)
shrage_n2_makespan = makespan(schrage_n2_order, tasks)
#print("[SHRAGE N^2] order: ", schrage_n2_order)
print("[SHRAGE N^2] makespan: ", shrage_n2_makespan)

# SCHRAGE ORDER NLOGN
schrage_nlogn_order = schrage_nlogn(tasks)
schrage_nlogn_makespan = makespan(schrage_nlogn_order, tasks)
#print("[SHRAGE NLOGN] order: ", schrage_nlogn_order)
print("[SHRAGE NLOGN] makespan: ", schrage_nlogn_makespan)

schrage_n2_ptmn_makespan, schrage_n2_ptmn_order = schrage_n2_pmtn(tasks)
print("[SHRAGE N^2 PMTN] makespan:", schrage_n2_ptmn_makespan)


schrage_nlogn_pmtn_makespan, schrage_nlogn_pmtn_order = schrage_nlogn_pmtn(tasks)
print("[SHRAGE NLOGN PMTN] makespan:", schrage_nlogn_pmtn_makespan)