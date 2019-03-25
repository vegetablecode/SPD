import copy
from src.datareader import get_data
from src.neh import neh
from src.makespan import makespan, to_natural_order
from src.qneh import qneh

tasks, numb_of_machines = get_data("data.050")
# searching for min makespan with NEH
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines, 0)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))

neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines, 1)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH mod 1] makespan: {}, time: {}" .format(neh_makespan, neh_time))

neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines, 2)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH mod 2] makespan: {}, time: {}" .format(neh_makespan, neh_time))
print("------------------------------------------------------------------------")
neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[qNEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))
