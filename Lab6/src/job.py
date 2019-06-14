from __future__ import print_function
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from datareader import get_job_data
import collections

def MinimalJobshopSat():
    print("Minimal JOB SHOP Problem")
    # Create the model.
    model = cp_model.CpModel()

    directory = "jobshop"
    task_list = ["data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
    for task_name in task_list:
        tasks = get_job_data(directory, task_name)

        #Converting tasks to other convention
        jobs_data = []
        for task in tasks:
            jobs_data_line = []
            for i in range(0, len(task.times)):
                singleTask = []
                singleTask.append(task.machines[i])
                singleTask.append(task.times[i])
                jobs_data_line.append(singleTask)
            jobs_data.append(jobs_data_line)
        print (task_name)
        #---END OF CONVERSION----------------

        #The number of machines
        machines_count = 1 + max(task[0] for job in jobs_data for task in job)
        #The number of machines range
        all_machines = range(machines_count)
        # Computes horizon dynamically as the sum of all durations.
        horizon = sum(task[1] for job in jobs_data for task in job)
        # Named tuple to store information about created variables.
        task_type = collections.namedtuple('task_type', 'start end interval')
        # Named tuple to manipulate solution information.
        assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')


        # Creates job intervals and add to the corresponding machine lists.
        all_tasks = {}
        machine_to_intervals = collections.defaultdict(list)

        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                duration = task[1]
                suffix = '_%i_%i' % (job_id, task_id)
                start_var = model.NewIntVar(0, horizon, 'start' + suffix)
                end_var = model.NewIntVar(0, horizon, 'end' + suffix)
                interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
                all_tasks[job_id, task_id] = task_type(
                    start=start_var, end=end_var, interval=interval_var)
                machine_to_intervals[machine].append(interval_var)

        # Create and add disjunctive constraints.
        for machine in all_machines:
            model.AddNoOverlap(machine_to_intervals[machine])

        # Precedences inside a job.
        for job_id, job in enumerate(jobs_data):
            for task_id in range(len(job) - 1):
                model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

        # Makespan objective.
        obj_var = model.NewIntVar(0, horizon, 'makespan')
        model.AddMaxEquality(obj_var, [
            all_tasks[job_id, len(job) - 1].end
            for job_id, job in enumerate(jobs_data)
        ])
        model.Minimize(obj_var)

        # Solve model.
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL:
            # Finally print the solution found.
            print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        else:
            print('Cannot find optimal schedule')
        print('-------------------------------------')

MinimalJobshopSat();
