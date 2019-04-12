import copy
from datareader import get_data
from makespan import makespan, to_natural_order, get_order
from simulated_annealing import simulated_annealing
from improved_simulated_annealing import improved_simulated_annealing
from neh import neh


tasks, numb_of_machines = get_data("data.001")

# INITIAL ORDER
init_order = get_order(tasks)
init_makespan = makespan(init_order, tasks, numb_of_machines)
print("[INIT] makespan: {}, time: {}" .format(init_makespan, 0))

# NEH ORDER
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines)
neh_makespan = makespan(neh_order, tasks, numb_of_machines)
print("[NEH ] makespan: {}, time: {}" .format(neh_makespan, neh_time))

# SIMULATED ANNEALING ORDER
init_temp = 5000
final_temp = 0.1
u = 0.98
cooling_fcn_type = 0
move_type = 0
insert = 0

simulated_annealing_order, iterations_sa, sa_time = simulated_annealing(copy.deepcopy(tasks), numb_of_machines, init_temp,
                                                                     final_temp, u, cooling_fcn_type, move_type, insert)
simulated_annealing_makespan = makespan(simulated_annealing_order, tasks, numb_of_machines)

improved_simulated_annealing_order, iterations_isa, isa_time = improved_simulated_annealing(copy.deepcopy(tasks), numb_of_machines, init_temp,
                                                                     final_temp, u, cooling_fcn_type, move_type, insert)
improved_simulated_annealing_makespan = makespan(improved_simulated_annealing_order, tasks, numb_of_machines)
print("[ SA ] makespan: {}, time: {}" .format(simulated_annealing_makespan, sa_time))
print("[ ISA ] makespan: {}, time: {}" .format(improved_simulated_annealing_makespan, isa_time))

print("-----")
print("Algorithm finished after: {} iterations" .format(iterations_sa))
print("Initial temperature: {}" .format(init_temp))
print("Stop temperature: {}" .format(final_temp))
print("-----")

print("NEH and SA Cmax difference: {}" .format(neh_makespan-simulated_annealing_makespan))
