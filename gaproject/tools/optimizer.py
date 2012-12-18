from gaproject.data import Box
from gaproject.tools.launcher import Launcher


class Optimizer(object):
    'Main class for parameter optimization.'

    def __init__(self):
        self.launcher = Launcher()

    def go(self):
        '''
        Launches the super uber optimizer.

        1. Clears queue and results.
        2. Queues new results for variable range of interest
        3. Executing the queue and retrieving the best result
        4. New variable and back to [2].

        '''
        print 'Go go go !'

        # 0. Loading data
        box = Box('data/TSPBenchmark')
        data = box.get('xqf131.tsp')
        self.launcher.load_data(data)

        # 1. clear queue and results
        self.launcher.clear()

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
            job['generations'] = 10000 / pop
            jobs.append(job)

        best = self.launcher.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing cxpb'
        jobs = []
        for cxpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], cxpb / 100.)
            job['cxpb'] = cxpb / 100.
            jobs.append(job)

        best = self.launcher.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing indpb'
        jobs = []
        for mut in range(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mut / 100.)
            job['mutate'] = (job['mutate'][0], {'indpb': mut / 100.})
            jobs.append(job)

        best = self.launcher.launch_queue(jobs, plot_all=False)['set']
        del best['_id']

        print 'Optimizing mutpb'
        jobs = []
        for mutpb in xrange(1, 100, 5):
            job = best.copy()
            job['name'] = '{}-{}'.format(job['name'], mutpb / 100.)
            job['mutpb'] = mutpb / 100.
            jobs.append(job)

        best = self.launcher.launch_queue(jobs, plot_all=False)['set']
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

        best = self.launcher.launch_queue(jobs, plot_all=True)['set']
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

        best = self.launcher.launch_queue(jobs, plot_all=True)['set']
        del best['_id']

        print 'runned'
        raw_input()
        # Getting best
