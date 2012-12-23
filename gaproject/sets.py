'''
This file will contain or set the test sets we will want to
run.
'''

from gaproject.operators import alias
# from gaproject.store import Store
from deap import tools

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
    'cxpb': 0.70,
    'mutpb': 0.20,
    'select': (tools.selTournament, {'tournsize': 3}),
    'repetitions': 2,
}


# def get():
#     'Returns a list or generator of jobs to be executed.'
#     # s = Store()
#     # return s.jobs.find()

#     sets = [{
#         'name': 'set1',
#         'evaluate': 'eval_simple',
#         'mutate': ('insert_mut', {'indpb': 0.05}),
#         # 'mutate': ('meta_insert', {'indpb': 0.05}),
#         'mate': 'cxNull',
#         'population': 20,
#         'generations': 5000,
#         'select': ('selTournament', {'tournsize': 1}),
#         },
#         {
#         'name': 'set1-meta',
#         'evaluate': 'eval_simple',
#         # 'mutate': ('insert_mut', {'indpb': 0.05}),
#         'mutate': ('meta_insert', {'indpb': 0.05}),
#         'mate': 'cxNull',
#         'population': 20,
#         'generations': 5000,
#         'select': ('selTournament', {'tournsize': 1}),
#         }]

#     def copy_and_update(set):
#         copy = defaults.copy()
#         copy.update(set)
#         return copy

#     return [copy_and_update(set) for set in sets]


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
    for key in ('population', 'generations', 'cxpb', 'mutpb', 'repetitions'):
        if key in d:
            result[key] = d[key]

    return result
