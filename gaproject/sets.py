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
    'indices': 'path_creator',
    'cxpb': 0.73,
    'mutpb': 0.23,
}


def get():
    'Returns a list or generator of jobs to be executed.'
    s = Store()
    return s.jobs.find()

    # return [{
    #     'name': 'set1adj',
    #     'evaluate': 'eval_adjacent',
    #     'mutate': ('mutshuf_adj', {'indpb': 0.05}),
    #     'population': 10,
    #     'generations': 1000,
    #     'indices': 'adj_creator',
    #     'mate': 'cxHeuristic',
    #     }]

    # return [{
    #     'name': 'set1a',
    #     'evaluate': 'eval_simple',
    #     'mutate': ('mutshuf', {'indpb': 0.05}),
    #     'population': 10,
    #     'generations': 1000,
    #     }]


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
        'indices': alias[d['indices']],
        }

    # Integer values, no need to go through alias:
    for key in ('population', 'generations', 'cxpb', 'mutpb'):
        if key in d:
            result[key] = d[key]

    return result
