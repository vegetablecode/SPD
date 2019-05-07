import copy
from src.datareader import get_data
from src.makespan import makespan, to_natural_order, get_order
from src.schrage_n2 import schrage_n2

tasks = get_data("data.004")

# print all tasks
#for task in tasks:
#    print(task.index, " ", task.times)

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks)
print("[INIT] makespan: ", init_makespan)

# SCHRAGE ORDER
schrage_n2_order = schrage_n2(tasks)
shrage_n2_makespan = makespan(schrage_n2_order, tasks)
print("[SHRAGE N^2] makespan: ", shrage_n2_makespan)
