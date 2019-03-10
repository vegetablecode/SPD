from bruteforce import bruteforce
from prettytable import PrettyTable
from makespan import makespan
from johnson import johnson
from task import Task
import random
import copy

def generating(iter):
    number_of_machines = int(input("Ile maszyn?: "))
    number_of_tasks = int(input("Ile zadan?: "))
    times = []
    durationBruteforce = []
    durationJohnson = []
    i = 0
    while i < iter:
        generatedTasks = []
        cnt_tasks =0
        cnt_machines = 0
        for cnt_tasks in range(0, number_of_tasks):
            rows = []
            for cnt_machines in range(0, number_of_machines):
                rows.append(int(random.uniform(1,10)))
            print("{}".format(rows))
            generatedTasks.append(Task(cnt_tasks, rows))
        bruteforceOrder, timeBruteforce = bruteforce(copy.deepcopy(generatedTasks), number_of_machines)
        johnsonOrder, timeJohnson = johnson(copy.deepcopy(generatedTasks), number_of_machines)
        durationBruteforce.append(timeBruteforce)
        durationJohnson.append(timeJohnson)
        bruteforceMakespan = makespan(bruteforceOrder, generatedTasks, number_of_machines)
        johnsonMakespan = makespan(johnsonOrder, generatedTasks, number_of_machines)
        i += 1
        if johnsonMakespan == bruteforceMakespan:
            times.append(johnsonMakespan)
        else:
            times.append(-1)
    x = PrettyTable()
    print("")
    print("----------------------------------------------------------")
    x.field_names = ["l.p.", "Johnson Makespan", "Poprawnosc", "Czas Bruteforce [ms]", "Czas Johnson [ms]"]

    k = 0
    for k in range(0, iter):
        if times[k] == -1:
            x.add_row([k+1,"{}".format(times[k]), "Nie", "{}".format(durationBruteforce[k]), "{}".format(durationJohnson[k])])
        else:
            x.add_row([k+1,"{}".format(times[k]), "Tak", "{}".format(durationBruteforce[k]), "{}".format(durationJohnson[k])])
    print(x)
