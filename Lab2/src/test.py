from src.datareader import get_data
from src.qneh import get_times_table, get_path_out_table, get_path_in_table, find_best_insertion_position

tasks, numb_of_machines = get_data("data.000")

simple_order = [0, 2, 1, 3]
task_index = 4

times_table = get_times_table(simple_order, tasks, numb_of_machines)
path_out_table = get_path_out_table(times_table)
path_in_table = get_path_in_table(times_table)
best_insertion_index = find_best_insertion_position(tasks, numb_of_machines, task_index, simple_order, times_table, path_in_table, path_out_table)
print(best_insertion_index)

#print(get_path_out_table(times_table))