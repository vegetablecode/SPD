import math


def swap(t, left, right):
    t[left], t[right] = t[right], t[left]


def get_parent_node(n):
    return math.floor((n-1)//2)


def get_left_node(n):
    return 2*n+1


def get_right_node(n):
    return 2*n+2


def perc_up(tasks, i):
    p = get_parent_node(i)
    while i > 0 and tasks[p].times[2] < tasks[i].times[2]:
        swap(tasks, p, i)
        i = p
        p = get_parent_node(i)


def perc_down(tasks, i):
    n = len(tasks) - 1  # last element
    while True:
        left = get_left_node(i)
        right = get_right_node(i)
        if left < n and tasks[left].times[2] > tasks[i].times[2]:
            m = left
        else:
            m = i
        if right < n and tasks[right].times[2] > tasks[m].times[2]:
            m = right
        if m == i:
            break
        else:
            swap(tasks, m, i)
            i = m


class Heap:
    def __init__(self):
        self.tasks = []

    def __str__(self):
        return str(self.tasks)

    def is_empty(self):
        return not self.tasks

    def insert(self, task):
        self.tasks.append(task)
        perc_up(self.tasks, len(self.tasks)-1)

    def remove(self):
        # move max to end
        swap(self.tasks, 0, len(self.tasks) - 1)
        perc_down(self.tasks, 0)
        return self.tasks.pop()

    def count(self):
        return len(self.tasks)

    def root(self):
        return self.tasks[0]
