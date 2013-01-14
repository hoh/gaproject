
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
            'data': 'xqf131.tsp',
            'metaga': 4,

            'operators': {
                'name': 'default',

                'evaluate': 'eval_simple',
                'select': ('selTournament', {'tournsize': 1}),
                'mutate': ('insert_mut', {'indpb': 0.05}),
                'mate': 'cxSCX',

                'repetitions': 30,

                'population': 10,
                'generations': 100,
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

        for job in results_jobs:
            data = job_data(job)
            size = len(data['stats'][0]['min'][0])

            # # Plotting individual runs:
            # for d in data['stats']:
            #     d = adjust(d['min'])
            #     plt.plot(d, color_run + '--')

            # Plotting average:
            plt.plot(
                [average([adjust(d['min'])[i]
                          for d in data['stats']])
                 for i in xrange(size)],
                # color_avg + '-',
                # linewidth=2.0,
                label=job['operators']['name'],
                )

        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.legend()
        plt.show()

    def go(self):
        '''
        '''
        print 'Go go go'

        jobs = []
        for pop in (100,):
            
            jobs.append(
                make_job(self.base_job,
                         {'name': '{}m'.format(pop),
                          'population': pop,
                          # 'generations': 1000,
                          'mutate': ('meta_insert', {'indpb': 0.05}),
                          'mate': 'cxSCX_meta',
                         }))
            jobs.append(
                make_job(self.base_job,
                         {'name': '{}'.format(pop),
                          'population': pop,
                          # 'generations': 1000,
                          'mutate': ('insert_mut', {'indpb': 0.05}),
                          'mate': 'cxSCX',
                         }))

        self.compare(jobs)

        print 'Done'


if __name__ == '__main__':
    analyzer = Analyzer_MetaGA()
    analyzer.go()
