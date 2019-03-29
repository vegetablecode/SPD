import copy
from datareader import get_data
from neh import neh
from makespan import makespan, to_natural_order
from qneh import qneh
from generating import generating
from nehTest import test

print "NEH, ACCELERATIONS, NEH MODYFICATIONS"
print "-------------------------------------"
print "1 -- Dzialanie algorytmu NEH"
print "2 -- Porownanie NEH, bruteforce i Johnson"
print "3 -- Akceleracja"
print "4 -- Modyfikacje NEH"
print "_________________________________________"
choise = input("Twoj wybor: ")

#Pure NEH algorithm
if choise == 1:
    tasks, numb_of_machines = get_data("data.060")
    print("[NEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))

#Comparison of NEH, brutegore and Johnson
if choise == 2:
    iter = input("Ile iteracji: ")
    generating(iter)

if choise == 3:
    tasks, numb_of_machines = get_data("data.020")
    neh_order, neh_time = neh(copy.deepcopy(tasks), numb_of_machines)
    neh_makespan = makespan(neh_order, tasks, numb_of_machines)
    print("[NEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))
    print("------------------------------------------------------------------------")
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,0)
    neh_makespan = makespan(neh_order, tasks, numb_of_machines)
    print("[qNEH] makespan: {}, time: {}" .format(neh_makespan, neh_time))

if choise == 4:
    test()
