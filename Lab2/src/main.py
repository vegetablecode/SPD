import copy
from src.datareader import get_data
from src.gantt import draw_gantt
from src.neh import neh

tasks, numb_of_machines = get_data("data.1")

# searching for min makespan with NEH
neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines)

plt = draw_gantt(neh_order, tasks, numb_of_machines, neh_time, "Podzial zadan")
plt.show()
