import copy
from src.datareader import get_data
from src.makespan import makespan, to_natural_order, get_order

tasks = get_data("rpq_500.txt")  # cmax -> 5.446

# print all tasks
for task in tasks:
    print(task.index, " ", task.times)

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
print("[INIT] makespan: ", init_makespan)