from gaproject.data import Box
from gaproject.tools.launcher import Launcher


class RComparator(object):
    'Main class for representation comparison.'

    def __init__(self):
        self.launcher = Launcher()

    def go(self):
        # '''
        # Launches the super uber optimizer.

        # 1. Clears queue and results.
        # 2. Queues new results for variable range of interest
        # 3. Executing the queue and retrieving the best result
        # 4. New variable and back to [2].

        # '''
        print 'Go go power rangers!'

        # 0. Loading data
        box = Box('data/TSPBenchmark')
        data = box.get('xqf131.tsp')
        self.launcher.load_data(data)

        # 1. clear queue and results
        self.launcher.clear()

        # 2. Create base dictionary
        base = {
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.01}),
            'mate': 'cxSCX',
            'population': 201,
            'generations': 2,
            'indices': 'path_creator',
            'cxpb': 0.80,
            'mutpb': 0.2,
        }

        adj_mutations = ['mutshuf_adj', 'invert_mut_adj', 'insert_mut_adj', 'simple_inv_adj']
        path_mutations = ['mutshuf', 'invert_mut', 'insert_mut', 'simple_inv']
        crossovers = ['cxPMX', 'cxESCX', 'cxSCX', 'cxERX', 'cxOX', 'cxHeuristic']

        for mut_operator in path_mutations:
            print 'Computing comparison for ', mut_operator
            jobs = []
            for crossover in crossovers:
                job = base.copy()
                job['name'] = '{}-{}'.format(crossover, mut_operator)
                job['mate'] = crossover
                if crossover == 'cxHeuristic':
                    job['evaluate'] = 'eval_adjacent'
                    job['indices'] = 'adj_creator'
                    # we set the adjacent mutation relying on the fact that adj mut and path mut
                    # follow the same ordering
                    index_curr_mut = path_mutations.index(mut_operator)
                    job['mutate'] = (adj_mutations[index_curr_mut], {'indpb': job['mutate'][1]['indpb']})
                else:
                    job['evaluate'] = 'eval_simple'
                    job['mutate'] = (mut_operator, {'indpb': job['mutate'][1]['indpb']})
                    job['indices'] = 'path_creator'

                jobs.append(job)
            self.launcher.launch_queue(jobs, plot_all=True)['set']
        print 'runned'
        raw_input()
        # Getting best
