import numpy as np
from matplotlib import pyplot as plt


def draw_gantt(order, tasks, numb_of_machines, time, label):
    # setup
    bar_size = 90
    machines = ["Maszyna 1", "Maszyna 2", "Maszyna 3"]
    colors = plt.cm.rainbow(np.linspace(0, 1, len(tasks)))

    # figure options
    plt.figure(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.grid(color='k', linestyle='-', linewidth=0.2, axis='x')
    plt.xlabel('Czas')
    plt.title(label, fontsize=20)
    plt.margins(y=0.3)
    plt.gca().invert_yaxis()

    # draw labels
    for i in range(0, 3):
        plt.hlines(machines[i], 0, 0)

    # calculate blocks
    times = []
    for j in range(0, numb_of_machines):
        times.append(0)
    for i in order:
        times[0] += tasks[i].times[0]
        for j in range(1, numb_of_machines):
            if times[j] < times[j - 1]:
                times[j] = times[j - 1]
            times[j] += tasks[i].times[j]
        for j in range(0, numb_of_machines):
            plt.hlines(machines[j], times[j] - tasks[i].times[j]-0.1, times[j]+0.1, colors="black", lw=bar_size)  # border
            plt.hlines(machines[j], times[j] - tasks[i].times[j]+0.1, times[j]-0.1, colors=colors[i], lw=bar_size)  # fill

    # how order
    natural_order = []
    for i in range(0, len(order)):
        natural_order.append(order[i]+1)

    text = "Kolejność: " + ','.join(map(str, natural_order)) + " | Cmax: " + str(max(times)) + " | Czas: " + str(round(time, 3)) + " ms"

    plt.figtext(.13, .02, text, fontsize=14)
    plt.xticks(np.arange(0, max(times)+1, step=1))

    return plt

