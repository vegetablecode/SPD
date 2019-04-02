import copy
from src.datareader import get_data
from src.makespan import makespan, to_natural_order, get_order
from src.simulated_annealing import simulated_annealing
from src.neh import neh


tasks, numb_of_machines = get_data("data.001")

# INITIAL ORDER
initial_order = get_order(tasks)
initial_makespan = makespan(initial_order, tasks, numb_of_machines)
print("[INIT] makespan: {}, time: {}" .format(initial_makespan, 0))

# NEH ORDER
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH ] makespan: {}, time: {}" .format(neh_makespan, neh_time))

# SIMULATED ANNEALING ORDER
initial_temperature = 5000.0
simulated_annealing_order, iterations, stop_temperature, sa_time = simulated_annealing(copy.deepcopy(tasks), numb_of_machines, initial_temperature)
simulated_annealing_makespan = makespan(simulated_annealing_order, tasks, numb_of_machines)
print("[ SA ] makespan: {}, time: {}" .format(simulated_annealing_makespan, sa_time))

print("-----")
print("Algorithm finished after: {} iterations" .format(iterations))
print("Initial temperature: {}" .format(initial_temperature))
print("Stop temperature: {}" .format(stop_temperature))
print("-----")

print("NEH and SA Cmax difference: {}" .format(neh_makespan-simulated_annealing_makespan))
