'''
Distributed version of the analyzer.
'''

import os.path
import copy
import json

from numpy import average

from gaprunner.coach import Coach
from gaproject.tools.launcher import Launcher
from gaproject.tools.results import RunTable


def job_data(job):
    # Directory where the results have been saved:
    RESULTS_DIRECTORY = os.path.expanduser('~/GAP_results')
    data_path = os.path.join(RESULTS_DIRECTORY, str(job['_id']), 'data.json')
    return json.load(open(data_path))


def make_job(base, new_operators):
    job = copy.deepcopy(base)
    # Resetting the status of the job, in case we reuse a result:
    job['status'] = 'available'
    job['operators'].update(new_operators)
    return job


class Optimizer(object):
    'Main class for parameter optimization.'

    # Default values for job parameters:
    base_job = {
            'status': 'available',
            'data': 'belgiumtour.tsp',
            'metaga': False,

            'operators': {
                'name': 'default',

                'evaluate': 'eval_simple',
                'select': ('selTournament', {'tournsize': 1}),
                'mutate': ('insert_mut', {'indpb': 0.05}),
                'mate': 'cxSCX',

                'repetitions': 4,

                'population': 20,
                'generations': 500,
                'cxpb': 0.80,
                'mutpb': 0.2,
                },
            }

    def __init__(self):
        self.launcher = Launcher()

    def launch(self, jobs):
        coach = Coach(jobs)
        return coach.loop(bg=False)

    def best_job(self, jobs):
        best_job = jobs[0]
        best_data = job_data(best_job)
        best_avg = average(best_data['fitness'])

        for run in jobs:
            run_data = job_data(run)
            run_avg = average(run_data['fitness'])
            if run_avg < best_avg:
                best_job = run
                best_data = run_data
                best_avg = run_avg
        return best_job, best_data

    def print_job(self, job, data):
        print 'Best run so far:'
        table = RunTable()
        table.add_run(job, data)
        print table

    def tournament(self, jobs):
        'Runs the jobs and returns the best one'
        result_jobs = self.launch(jobs)
        best_job, best_data = self.best_job(result_jobs)
        self.print_job(best_job, best_data)
        del best_job['_id']

        return best_job

    def go(self):
        '''
        Launches the super uber optimizer.

        1. Clears queue and results.
        2. Queues new results for variable range of interest
        3. Executing the queue and retrieving the best result
        4. New variable and back to [2].

        '''
        print 'Go go go !'

        # self.launcher.load_data(data)

        # 1. clear queue and results
        # self.launcher.clear()

        # 2. Create dictionnaries for range

        print 'Optimizing population'
        jobs = []
        for pop in range(1, 1000, 20):
            job = make_job(self.base_job,
                           {'name': 'pop-{}'.format(pop),
                            'population': pop,
                            'generations': 10000 / pop,
                           })
            jobs.append(job)

        best_job = self.tournament(jobs)

        print 'Optimizing cxpb'
        jobs = []
        for cxpb in xrange(1, 100, 5):
            job = make_job(best_job,
                           {'name': '{}-{}'.format(best_job['operators']['name'], cxpb / 100.),
                            'cxpb': cxpb / 100.,
                           })
            jobs.append(job)

        best_job = self.tournament(jobs)

        return

        print 'Optimizing indpb'
        jobs = []
        for mut in range(1, 100, 5):
            job = make_job(best_job,
                           {'name': '{}-{}'.format(job['name'], mut / 100.),
                            'mutate': (job['mutate'][0], {'indpb': mut / 100.}),
                            })
            jobs.append(job)

        best_job = self.tournament(jobs)

        print 'Optimizing mutpb'
        jobs = []
        for mutpb in xrange(1, 100, 5):
            job = make_job(best_job,
                           {'name': '{}-{}'.format(job['name'], mutpb / 100.),
                           'mutpb': mutpb / 100.,
                           })
            jobs.append(job)

        best_job = self.tournament(jobs)

        print 'Optimizing crossover operator'
        crossovers = ['cxPMX', 'cxSCX', 'cxERX', 'cxOX', 'cxHeuristic']
        jobs = []
        for cx_operator in crossovers:
            job = make_job(best_job,
                           {'name': '{}-{}'.format(job['name'], cx_operator),
                            'mate': cx_operator,
                           })
            if cx_operator == 'cxHeuristic':
                job['evaluate'] = 'eval_adjacent'
                job['mutate'] = ('mutshuf_adj', {'indpb': best_job['mutate'][1]})
                job['indices'] = 'adj_creator'
            else:
                job['evaluate'] = 'eval_simple'
                job['mutate'] = ('mutshuf', {'indpb': best_job['mutate'][1]})
                job['indices'] = 'path_creator'

            jobs.append(job)

        best_job = self.tournament(jobs)

        print 'Optimizing mutation operator'
        jobs = []
        if best_job['mate'] == 'cxHeuristic':
            mutations = ['mutshuf_adj', 'invert_mut_adj', 'insert_mut_adj', 'simple_inv_adj']
        else:
            mutations = ['mutshuf', 'invert_mut', 'insert_mut', 'simple_inv']

        for mut_operator in mutations:
            job = make_job(best_job,
                           {'name': '{}-{}'.format(job['name'], mut_operator),
                            'mutate': (mut_operator, {'indpb': best_job['mutate'][1]}),
                           })

            jobs.append(job)

        best_job = self.tournament(jobs)

        print 'runned'
        raw_input()
        # Getting best

if __name__ == '__main__':
    optimizer = Optimizer()
    optimizer.go()
