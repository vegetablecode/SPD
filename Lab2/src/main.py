import copy
from datareader import get_data
from neh import neh
from makespan import makespan, to_natural_order
from qneh import qneh

tasks, numb_of_machines = get_data("data.010")
# searching for min makespan with NEH
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))

print("------------------------------------------------------------------------")
neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,4)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[qNEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))
