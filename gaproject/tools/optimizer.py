
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
            'mutate': ('mutshuf', {'indpb': 0.05}),
            'mate': 'cxERX',
            'population': 100,
            'generations': 100,
            'indices': 'path_creator',
            'cxpb': 0.70,
            'mutpb': 0.20,
        }

        print 'Optimizing population'
        jobs = []
        for pop in range(1, 1000, 50):
            job = base.copy()
            job['name'] = 'pop-{}'.format(pop)
            job['population'] = pop
            job['generations'] = 50000 / pop
            jobs.append(job)

        best = self.launch_queue(jobs)['set']
        del best['_id']

        print 'Optimizing mutations'
        jobs = []
        for mut in range(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mut / 100.)
            job['mutate'] = (job['mutate'][0], {'indpb': mut / 100.})
            jobs.append(job)

        best = self.launch_queue(jobs)['set']
        del best['_id']

        print 'Optimizing cxpb'
        jobs = []
        for cxpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], cxpb / 100.)
            job['cxpb'] = cxpb / 100.
            jobs.append(job)

        best = self.launch_queue(jobs)['set']
        del best['_id']

        print 'Optimizing mutpb'
        jobs = []
        for mutpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mutpb / 100.)
            job['mutpb'] = mutpb / 100.
            jobs.append(job)

        best = self.launch_queue(jobs)['set']
        del best['_id']

        print 'runned'
        # Getting best

    def launch_queue(self, jobs):
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
