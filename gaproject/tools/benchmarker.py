from gaproject.data import Box
from gaproject.tools.launcher import Launcher


class Benchmarker(object):
    'Main class for benchmarker.'

    def __init__(self):
        self.launcher = Launcher()

    def go(self):
        '''
        Launches the benchmarker.

        1.loads problem
        1. Clears queue and results.
        2. create new job
        3. Executes the queue and retrieves the best result
        4. New variable and back to [2].

        '''
        print 'Go benchmarker go!'

        #base is a job based on the results of the optimizer
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

        problems = ['belgiumtour.tsp', 'xqf131.tsp', 'bcl380.tsp', 'xql622.tsp']

        for problem in problems:

            #1. load problem
            box = Box('data/TSPBenchmark')
            data = box.get(problem)
            self.launcher.load_data(data)

            #2. clear
            self.launcher.clear()

            #3. create job
            print 'Attacking problem: ', problem
            job = base.copy()
            job['name'] = 'bmark-{}'.format(problem)

            #4. launch job
            self.launcher.launch_queue([job])

        print 'done!'
        raw_input()
