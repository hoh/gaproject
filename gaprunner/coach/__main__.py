'''
Coach : main way to use the client-worker-collector system.
'''

import copy

from gaprunner.coach.__init__ import Coach

default = {
        'status': 'available',
        'data': 'belgiumtour.tsp',
        'metaGA': False,

        'operators': {
            'name': 'default',
            'evaluate': 'eval_simple',
            'mutate': ('insert_mut', {'indpb': 0.05}),
            # 'mutate': ('meta_insert', {'indpb': 0.05}),
            'mate': 'cxNull',
            'population': 20,
            'generations': 100,
            'select': ('selTournament', {'tournsize': 1}),
            },
        }


def job(specific_values):
    j = copy.deepcopy(default)
    j['operators'].update(specific_values)
    return j


def main():

    jobs = [job({'population': 30}),
            job({'population': 30}),
            job({'population': 30}),
            job({'population': 30})]

    def callback(results):
        print 'Got result from coach.'

    coach = Coach(jobs, callback)
    coach.loop(bg=False)

if __name__ == '__main__':
    main()
