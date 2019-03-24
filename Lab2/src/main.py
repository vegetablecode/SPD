import copy
from datareader import get_data
from gantt import draw_gantt
from neh import neh

tasks, numb_of_machines = get_data("data.1")

# searching for min makespan with NEH
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines,0)
print ("")
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines,1)
print ("")
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines,2)

#plt = draw_gantt(neh_order, tasks, numb_of_machines, neh_time, "Podzial zadan")
#plt.show()
