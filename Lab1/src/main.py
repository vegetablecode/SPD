import copy
from src.datareader import get_data
from src.bruteforce import bruteforce
from src.johnson import johnson2
from src.makespan import makespan

tasks, numb_of_machines = get_data("data.1")


# searching for min makespan with Bruteforce
bruteforce_order = bruteforce(copy.deepcopy(tasks), numb_of_machines)
bruteforce_makespan = makespan(bruteforce_order, tasks, numb_of_machines)

print("Best order (Bruteforce): {}" .format(bruteforce_order))
print("Best makespan (Bruteforce): {}" .format(bruteforce_makespan))


# searching for min makespan with Johnson
johnson_order = johnson2(copy.deepcopy(tasks))
johnson_makespan = makespan(johnson_order, tasks, numb_of_machines)
print("Best order (Johnson): {}" .format(johnson_order))
print("Best makespan (Johnson): {}" .format(johnson_makespan))

