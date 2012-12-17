
from numpy import average

import gaproject.run
from gaproject.data import Box
from gaproject.tools.results import Results, RunTable


class Optimizer(object):
    'Main class for parameter optimization.'

    def go(self):
        '''
        Launches the super uber optimizer.

        1. Clears queue and results.
        2. Queues new results for variable range of interest
        3. Executing the queue
        4. Getting best result to the queue
        5. New variable and back to [2].

        '''
        print 'Go go go !'

        # 0. Loading data
        box = Box('data/TSPBenchmark')
        self.data = box.get('xqf131.tsp')

        # 1.
        self.store = gaproject.store.Store()
        self.store.runs.remove({})
        self.store.jobs.remove({})

        # 2. Create dictionnaries for range
        base = {
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.01}),
            'mate': 'cxSCX',
            'population': 201,
            'generations': 248,
            'indices': 'path_creator',
            'cxpb': 0.80,
            'mutpb': 0.2,
        }

        print 'Optimizing population'
        jobs = []
        for pop in range(1, 1000, 50):
            job = base.copy()
            job['name'] = 'pop-{}'.format(pop)
            job['population'] = pop
            job['generations'] = 50000 / pop
            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing cxpb'
        jobs = []
        for cxpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], cxpb / 100.)
            job['cxpb'] = cxpb / 100.
            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing indpb'
        jobs = []
        for mut in range(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mut / 100.)
            job['mutate'] = (job['mutate'][0], {'indpb': mut / 100.})
            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing mutpb'
        jobs = []
        for mutpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mutpb / 100.)
            job['mutpb'] = mutpb / 100.
            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing crossover operator'
        crossovers = ['cxPMX', 'cxSCX', 'cxERX', 'cxOX', 'cxHeuristic']
        jobs = []
        for cx_operator in crossovers:
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], cx_operator)
            job['mate'] = cx_operator
            if cx_operator == 'cxHeuristic':
                job['evaluate'] = 'eval_adjacent'
                job['mutate'] = ('mutshuf_adj', {'indpb': best['mutate'][1]})
                job['indices'] = 'adj_creator'
            else:
                job['evaluate'] = 'eval_simple'
                job['mutate'] = ('mutshuf', {'indpb': best['mutate'][1]})
                job['indices'] = 'path_creator'

            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=True)['set']
        del best['_id']

        print 'Optimizing mutation operator'
        jobs = []
        if best['mate'] == 'cxHeuristic':
            mutations = ['mutshuf_adj', 'invert_mut_adj', 'insert_mut_adj', 'simple_inv_adj']
        else:
            mutations = ['mutshuf', 'invert_mut', 'insert_mut', 'simple_inv']

        for mut_operator in mutations:
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mut_operator)
            job['mutate'] = (mut_operator, {'indpb': best['mutate'][1]})

            jobs.append(job)

        best = self.launch_queue(jobs, plot_all=True)['set']
        del best['_id']

        print 'runned'
        raw_input()
        # Getting best

    def launch_queue(self, jobs, plot_all):
        'Launches a queue of jobs and returns the best result.'
        self.store.runs.remove({})
        self.store.jobs.remove({})

        for job in jobs:
            self.store.jobs.insert(job)

        # 3.
        gaproject.run.main(self.data)

        # 4.
        results = Results()
        results.print_()
        if plot_all:
            results.plotDifferentRuns()

        best = results.find_one()
        best_avg = average(best['fitness'])
        for run in results.find():
            run_avg = average(run['fitness'])
            if run_avg < best_avg:
                best = run
                best_avg = run_avg

        print 'Best run so far:'
        table = RunTable()
        table.add_run(best)
        print table

        return best
