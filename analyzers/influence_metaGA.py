
from numpy import average, std

import matplotlib.pyplot as plt
from __init__ import make_job, job_data, Analyzer


class Analyzer_MetaGA(Analyzer):
    '''
    Analyses the influence of MetaGA on the runs.
    '''

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

                'repetitions': 30,

                'population': 20,
                'generations': 500,
                'cxpb': 0.80,
                'mutpb': 0.2,
                },
            }

    def compare(self, jobs):
        'Runs and compares the results of two jobs.'
        results_jobs = self.launch(jobs)

        def adjust(stats_list):
            'Transforms the list found in stats to a plottable list.'
            return [fit[0] for fit in stats_list[0]]

        plt.figure()

        # Color sets for the graphics:
        color_sets = [('y', 'r'), ('g', 'b')]

        for job in results_jobs:
            data = job_data(job)
            size = len(data['stats'][0]['min'][0])

            color_run, color_avg = color_sets.pop()

            # Plotting individual runs:
            for d in data['stats']:
                d = adjust(d['min'])
                plt.plot(d, color_run + '--')

            # Plotting average:
            plt.plot(
                [average([adjust(d['min'])[i]
                          for d in data['stats']])
                 for i in xrange(size)],
                color_avg + '-',
                linewidth=2.0)

        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.show()

    def go(self):
        '''
        '''
        print 'Go go go'

        print 'Small population'
        jobs = [
            make_job(self.base_job,
                     {'population': 5,
                      'generations': 20,
                      'mutate': ('insert_mut', {'indpb': 0.05}),
                      }),
            make_job(self.base_job,
                     {'population': 5,
                      'generations': 20,
                      'mutate': ('meta_insert', {'indpb': 0.05}),
                      }),
        ]

        self.compare(jobs)

        print 'Done'


if __name__ == '__main__':
    analyzer = Analyzer_MetaGA()
    analyzer.go()
