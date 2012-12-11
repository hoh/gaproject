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
        'set1': {
            'evaluate': 'eval_simple',
            'mutate': ('mutshuf', {'indpb': 0.05}),
            },

        'set2': {
            'evaluate': 'eval_simple',
            'mutate': ('simple_inv', {'indpb': 0.05}),
        }
    }


def evaluate(set):

    mut_func, mut_args = set['mutate']

    result = {
        'evaluate': alias[set['evaluate']],
        'mutate': (alias[mut_func], mut_args),
        }
    return result
