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

defaults = {
    'evaluate': 'eval_simple',
    'mutate': ('mutshuf', {'indpb': 0.05}),
    'mate': 'cxERX',
    'population': 100,
    'generations': 100,
}


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

        'set1b-lm': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.01}),
            'population': 100,
            'generations': 100,
            },

        'set1b-hm': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.10}),
            'population': 100,
            'generations': 100,
            },

        'set2b': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('insert_mut', {'indpb': 0.05}),
            'population': 100,
            'generations': 100,
            },

        'set3b': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('invert_mut', {'indpb': 0.05}),
            'population': 100,
            'generations': 100,
            },

        'set4b': {
            'name': 'set1b',
            'evaluate': 'eval_simple',
            'mutate': ('simple_inv', {'indpb': 0.05}),
            'population': 100,
            'generations': 100,
            },

    }


def evaluate(set):

    # We will use the defaults, updated by the given set:
    d = defaults.copy()
    d.update(set)

    # Extracting the two parts for mutate: function and arguments,
    # the others being straightforward:
    mut_func, mut_args = d['mutate']

    result = {
        'evaluate': alias[d['evaluate']],
        'mutate': (alias[mut_func], mut_args),
        'mate': (alias[d['mate']]),
        }

    # Integer values, no need to go through alias:
    for key in ('population', 'generations'):
        if key in d:
            result[key] = d[key]

    return result
