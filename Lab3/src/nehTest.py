from qneh import qneh
from datareader import get_data
import copy
from makespan import makespan
import pandas as pd
import numpy as np

import copy
from datareader import get_data
from makespan import makespan, to_natural_order, get_order
from simulated_annealing import simulated_annealing
from neh import neh

sets = ["data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008", "data.009", "data.010", "data.011", "data.021", "data.031"]

init_temp = 1000
final_temp = 0.1
u = 0.98
cooling_fcn_type = 0
insert = 0

fcn0_times = []
fcn0_cmax = []
fcn1_times = []
fcn1_cmax = []

move_type = 0

# for FCN0
for set in sets:
    tasks, numb_of_machines = get_data(set)

    cooling_fcn_type = 0

    simulated_annealing_order, iterations, sa_time = simulated_annealing(copy.deepcopy(tasks), numb_of_machines,
                                                                         init_temp, final_temp, u, cooling_fcn_type,
                                                                         move_type, insert)
    simulated_annealing_makespan = makespan(simulated_annealing_order, tasks, numb_of_machines)
    fcn0_times.append(sa_time)
    fcn0_cmax.append(simulated_annealing_makespan)

# for FCN1
for set in sets:
    tasks, numb_of_machines = get_data(set)

    cooling_fcn_type = 1

    simulated_annealing_order, iterations, sa_time = simulated_annealing(copy.deepcopy(tasks), numb_of_machines,
                                                                         init_temp, final_temp, u, cooling_fcn_type,
                                                                         move_type, insert)
    simulated_annealing_makespan = makespan(simulated_annealing_order, tasks, numb_of_machines)
    fcn1_times.append(sa_time)
    fcn1_cmax.append(simulated_annealing_makespan)


d = {'FCN0 TIMES': fcn0_times, 'FCN1 TIMES': fcn1_times, 'FCN0 CMAX': fcn0_cmax,
     'FCN1 CMAX': fcn1_cmax}
table = pd.DataFrame(data=d)

print("Average FCN0 TIMES: {}".format(np.mean(fcn0_times)))
print("Average FCN1 TIMES: {}".format(np.mean(fcn1_times)))
print("Average FCN0 CMAX: {}".format(np.mean(fcn0_cmax)))
print("Average FCN1 CMAX: {}".format(np.mean(fcn1_cmax)))

table
