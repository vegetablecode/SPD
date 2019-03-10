import copy
from datareader import get_data
from bruteforce import bruteforce
from johnson import johnson
from makespan import makespan, get_order
from gantt import draw_gantt

def ta000Instance(choice):
    #Loading a ta000 instance
    if choice == 1:
        tasks, numb_of_machines = get_data("ta000_2")
    elif choice == 2:
        tasks, numb_of_machines = get_data("ta000_3")

    # searching for min makespan with Bruteforce
    bruteforce_order = bruteforce(copy.deepcopy(tasks), numb_of_machines)
    bruteforce_makespan = makespan(bruteforce_order, tasks, numb_of_machines)

    # searching for min makespan with Johnson
    johnson_order = johnson(copy.deepcopy(tasks),numb_of_machines)
    johnson_makespan = makespan(johnson_order, tasks, numb_of_machines)


    # descriptions
    print("---------------------------")
    print("Best order (Bruteforce): {}" .format(bruteforce_order))
    print("Best makespan (Bruteforce): {}" .format(bruteforce_makespan))

    print("Best order (Johnson): {}" .format(johnson_order))
    print("Best makespan (Johnson): {}" .format(johnson_makespan))


    # plot figures
    plt = draw_gantt(bruteforce_order, tasks, numb_of_machines, "Podzial zadan (przeglad zupelny)")
    plt = draw_gantt(johnson_order, tasks, numb_of_machines, "Podzial zadan (algorytm Johnsona)")
    plt.show()


#MAIN INTERFACE DEFINED
print ("")
print("BRUTEFORCE and JOHNSON algorithm program")
print("----------------------------------------")
print("1 - Dzialanie na podstawie ta000 2-maszynowego")
print("2 - Dzialanie na podstawie ta000 3-maszynowego")
print("3 - Generowanie losowe danych i przedstawienie wynikow w tabeli")
print("4 - Wyjscie")
print("---------------------------------------------------------------")
choice = int(input("Enter a number: "))

if choice == 1 or choice == 2:
    ta000Instance(choice)
elif choice ==3:
    #Generating function
    print("Generating:")
elif choice == 4:
    exit()
#----------------------
