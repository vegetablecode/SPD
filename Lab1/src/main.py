import copy
from src.datareader import get_data
from src.bruteforce import bruteforce
from src.johnson import johnson
from src.makespan import makespan, get_order
from src.gantt import draw_gantt

tasks, numb_of_machines = get_data("data.8")


# searching for min makespan with Bruteforce
bruteforce_order, bruteforce_time = bruteforce(copy.deepcopy(tasks), numb_of_machines)
bruteforce_makespan = makespan(bruteforce_order, tasks, numb_of_machines)

# searching for min makespan with Johnson
johnson_order, johnson_time = johnson(copy.deepcopy(tasks),numb_of_machines)
johnson_makespan = makespan(johnson_order, tasks, numb_of_machines)


# descriptions
print("---------------------------")
print("Best order (Bruteforce): {}" .format(bruteforce_order))
print("Best makespan (Bruteforce): {}" .format(bruteforce_makespan))

print("Best order (Johnson): {}" .format(johnson_order))
print("Best makespan (Johnson): {}" .format(johnson_makespan))


# plot figures
plt = draw_gantt(bruteforce_order, tasks, numb_of_machines, bruteforce_time, "Podział zadań (przegląd zupełny)")
plt = draw_gantt(johnson_order, tasks, numb_of_machines, johnson_time, "Podział zadań (algorytm Johnsona)")
plt = draw_gantt(get_order(tasks), tasks, numb_of_machines, 0, "Podział zadań (naturalna kolejność)")
plt.show()
