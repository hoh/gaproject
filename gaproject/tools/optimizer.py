
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
        data = box.get('belgiumtour.tsp')

        # 1.
        s = gaproject.store.Store()
        s.runs.remove({})
        s.jobs.remove({})

        # 2. Create dictionnaries for range
        base = {
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.05}),
            'mate': 'cxERX',
            'population': 100,
            'generations': 100,
            'indices': 'path_creator',
        }

        # for pop in (10, 20, 50, 100, 200, 500, 1000, 2000):
        for pop in (10, 100, 1000):
            set_ = base.copy()
            set_['name'] = 'pop-{}'.format(pop)
            set_['population'] = pop
            set_['generations'] = 1000 / pop
            s.jobs.insert(set_)

        # 3.
        gaproject.run.main(data)

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

        print 'runned'
        # Getting best
