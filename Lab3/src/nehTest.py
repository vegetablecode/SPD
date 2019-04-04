from qneh import qneh
from datareader import get_data
import copy
from makespan import makespan


def test():
    tasks, numb_of_machines = get_data("data.090")
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,0)
    print ("Neh time: {}".format(neh_time))
    print ("Makespan {}".format(makespan(neh_order, tasks, numb_of_machines)))
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,1)
    print ("Neh mod1 time: {}".format(neh_time))
    print ("Makespan {}".format(makespan(neh_order, tasks, numb_of_machines)))
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,2)
    print ("Neh mod2 time: {}".format(neh_time))
    print ("Makespan {}".format(makespan(neh_order, tasks, numb_of_machines)))
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,3)
    print ("Neh mod3 time: {}".format(neh_time))
    print ("Makespan {}".format(makespan(neh_order, tasks, numb_of_machines)))
    neh_order, neh_time = qneh(copy.deepcopy(tasks), numb_of_machines,4)
    print ("Neh mod4 time: {}".format(neh_time))
    print ("Makespan {}".format(makespan(neh_order, tasks, numb_of_machines)))
