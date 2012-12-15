'''
This file will contain or set the test sets we will want to
run.
'''

from gaproject.operators import alias
from gaproject.store import Store

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
    s = Store()
    return s.jobs.find()


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
