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
    task_list = ["data.wyklad", "data.google", "data.000", "data.001", "data.002", "data.003", "data.004", "data.005", "data.006", "data.007", "data.008"]
    answers = [18, 11, 272, 1411, 1404, 1388, 1332, 1407, 1400, 1357, 1350]

    for k in range(len(task_list)):
        tasks = get_job_data(directory, task_list[k])

        #Converting tasks to other convention
        jobs_data = []
        for task in tasks:
            jobs_data_line = []
            for i in range(0, len(task.times)):
                singleTask = []
                singleTask.append(task.machines[i]-1)
                singleTask.append(task.times[i])
                jobs_data_line.append(singleTask)
            jobs_data.append(jobs_data_line)
        print("DATASET: ", task_list[k])
        #---END OF CONVERSION----------------

        # show converted
        print("-----")
        print("initial: ")
        for i in range(len(jobs_data)):
            print(jobs_data[i])
        print("-----")

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

        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))

        # Create per machine output lines.
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job+1, assigned_task.index+1)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        if status == cp_model.OPTIMAL:
            # Finally print the solution found.
            print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
            print("Answer: ", answers[k])
            print("-----")
            print("optimal: ")
            print(output)
            print("-----")
        else:
            print('Cannot find optimal schedule')
        print('-------------------------------------')

MinimalJobshopSat();
