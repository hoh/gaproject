'''
Distributed version of the analyzer.
'''

from numpy import average

from __init__ import make_job, Analyzer, job_data


class Optimizer(Analyzer):
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

    def tournament(self, jobs):
        'Runs the jobs and returns the best result'
        result_jobs = self.launch(jobs)
        best_job, best_data = self.best_job(result_jobs)
        self.print_job(best_job, best_data)
        del best_job['_id']

        return best_job

    def go(self):
        '''
        Launches the super uber optimizer.

        Generates a range of values for a parameter, selects
        the best result and goes to the next parameter.
        '''
        print 'Go go go !'

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
