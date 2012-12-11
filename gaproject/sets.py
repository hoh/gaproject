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
            'mutate': 'mutshuf',
            },

        'set2': {
            'evaluate': 'eval_simple',
            'mutate': 'simple_inv',
        }
    }


def evaluate(set):
    result = {
        'evaluate': alias[set['evaluate']],
        'mutate': (alias[set['mutate']], {'indpb': 0.05}),
        }
    return result
