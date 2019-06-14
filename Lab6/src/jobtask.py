class JobTask:
    #index of the tasks
    #machines: sequence of the subsequent machines
    #times: sequence of the subsequent times

    def __init__(self, index, machines, times):
        self.index = index
        self.machines = machines
        self.times = times
