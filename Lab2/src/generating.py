from src.bruteforce import bruteforce
from prettytable import PrettyTable
from src.neh import neh
from src.makespan import makespan
from src.johnson import johnson
from src.task import Task
import random
import copy


def generating(iter):
    number_of_machines = int(input("Ile maszyn?: "))
    number_of_tasks = int(input("Ile zadan?: "))
    bruteforceSpan = []
    johnsonSpan = []
    nehSpan = []
    durationBruteforce = []
    durationJohnson = []
    durationNeh = []
    i = 0
    while i < iter:
        generatedTasks = []
        cnt_tasks = 0
        cnt_machines = 0
        for cnt_tasks in range(0, number_of_tasks):
            rows = []
            for cnt_machines in range(0, number_of_machines):
                rows.append(int(random.uniform(1, 10)))
            print("{}".format(rows))
            generatedTasks.append(Task(cnt_tasks, rows))
        bruteforceOrder, timeBruteforce = bruteforce(copy.deepcopy(generatedTasks), number_of_machines)
        johnsonOrder, timeJohnson = johnson(copy.deepcopy(generatedTasks), number_of_machines)
        nehOrder, timeNeh = neh(copy.deepcopy(generatedTasks), number_of_machines)
        durationBruteforce.append(timeBruteforce)
        durationJohnson.append(timeJohnson)
        durationNeh.append(timeNeh)
        bruteforceMakespan = makespan(bruteforceOrder, generatedTasks, number_of_machines)
        johnsonMakespan = makespan(johnsonOrder, generatedTasks, number_of_machines)
        nehMakespan = makespan(nehOrder, generatedTasks, number_of_machines)
        bruteforceSpan.append(bruteforceMakespan)
        johnsonSpan.append(johnsonMakespan)
        nehSpan.append(nehMakespan)
        i += 1

    x = PrettyTable()
    print("")
    print("----------------------------------------------------------")
    x.field_names = ["l.p.", "Bruteforce makespan", "Johnson makespan", "Neh makespan", "Czas bruteforce [ms]",
                     "Czas Johnson [ms]", "Czas Neh [ms]"]

    k = 0
    for k in range(0, iter):
        x.add_row([k + 1, "{}".format(bruteforceSpan[k]), "{}".format(johnsonSpan[k]), "{}".format(nehSpan[k]),
                   "{}".format(durationBruteforce[k]), "{}".format(durationJohnson[k]), "{}".format(durationNeh[k])])
    print(x)
