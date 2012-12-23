'''
Used to compare the performance of different workers.
'''

import time

from __init__ import make_job, job_data, Analyzer


class Performance(Analyzer):

    # Default values for job parameters:
    base_job = {
            'status': 'available',
            'data': 'bcl380.tsp',
            'metaga': 4,

            'operators': {
                'name': 'default',

                'evaluate': 'eval_simple',
                'select': ('selTournament', {'tournsize': 1}),
                'mutate': ('insert_mut', {'indpb': 0.05}),
                'mate': 'cxSCX',

                'repetitions': 1,

                'population': 20,
                'generations': 500,
                'cxpb': 0.80,
                'mutpb': 0.2,
                },
            }

    def go(self):
        t0 = time.time()
        jobs = [make_job(self.base_job, {})]
        self.launch(jobs)
        print 'TIME:', time.time() - t0


if __name__ == '__main__':
    analyzer = Performance()
    analyzer.go()
