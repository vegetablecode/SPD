import copy
from datareader import get_data
from bruteforce import bruteforce
from johnson import johnson
from makespan import makespan

tasks, numb_of_machines = get_data("data.1")


# searching for min makespan with Bruteforce
bruteforce_order = bruteforce(copy.deepcopy(tasks), numb_of_machines)
bruteforce_makespan = makespan(bruteforce_order, tasks, numb_of_machines)

print("Best order (Bruteforce): {}" .format(bruteforce_order))
print("Best makespan (Bruteforce): {}" .format(bruteforce_makespan))


# searching for min makespan with Johnson
johnson_order = johnson(copy.deepcopy(tasks),numb_of_machines)
johnson_makespan = makespan(johnson_order, tasks, numb_of_machines)
print("Best order (Johnson): {}" .format(johnson_order))
print("Best makespan (Johnson): {}" .format(johnson_makespan))
