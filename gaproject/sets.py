'''
This file will contain or set the test sets we will want to
run.
'''

from gaproject.operators import alias

# from gaproject.store import Store
# future:
# def insert(...)
#     'inserts values in db'
#


def get():
    return {

        'set1a': {
            'name': 'set1a',
            'evaluate': 'eval_adjacent',
            'mutate': ('invert_mut_adj', {'indpb': 1.0}),
            'mate': 'cxHeuristic',
            'population': 50,
            'generations': 1000,
            },

        # 'set1b': {
        #     'name': 'set1b',
        #     'evaluate': 'eval_simple',
        #     'mutate': ('invert_mut', {'indpb': 1.0}),
        #     'mate': 'cxSCX',
        #     'population': 25,
        #     'generations': 200,
        #     },

        # 'set1c': {
        #     'name': 'set1c',
        #     'evaluate': 'eval_simple',
        #     'mutate': ('invert_mut', {'indpb': 1.0}),
        #     'mate': 'cxERX',
        #     'population': 25,
        #     'generations': 200,
        #     },

        # 'set1d': {
        #     'name': 'set1d',
        #     'evaluate': 'eval_simple',
        #     'mutate': ('invert_mut', {'indpb': 1.0}),
        #     'mate': 'cxOX',
        #     'population': 30,
        #     'generations': 500,
        #     },

        # 'set1f': {
        #     'name': 'set1f',
        #     'evaluate': 'eval_simple',
        #     'mutate': ('invert_mut', {'indpb': 1.0}),
        #     'mate': 'cxESCX',
        #     'population': 50,
        #     'generations': 1000,
        #     }


    }


def evaluate(set):

    mut_func, mut_args = set['mutate']
    crossover_func = set['mate']

    result = {
        'evaluate': alias[set['evaluate']],
        'mutate': (alias[mut_func], mut_args),
        'mate': (alias[crossover_func]),
        }
    for key in ('population', 'generations'):
        if key in set:
            result[key] = set[key]
    return result
