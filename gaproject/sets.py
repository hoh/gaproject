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
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.05}),
            'population': 10,
            'generations': 1000,
            },

        'set1b': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.05}),
            'population': 100,
            'generations': 100,
            },

        'set1c': {
            'name': 'set1c',
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.05}),
            'population': 1000,
            'generations': 10,
            },

        # 'set2': {
        #     'evaluate': 'eval_simple',
        #     'mutate': ('invert_mut', {'indpb': 0.05}),
        #     'population': 100,
        #     'generations': 100,
        # }
    }


def evaluate(set):

    mut_func, mut_args = set['mutate']

    result = {
        'evaluate': alias[set['evaluate']],
        'mutate': (alias[mut_func], mut_args),
        }
    for key in ('population', 'generations'):
        if key in set:
            result[key] = set[key]
    return result
