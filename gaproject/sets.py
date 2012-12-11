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
            }
    }


def evaluate(set):
    result = {
        'mutate': (alias[set['mutate']], {'indpb': 0.05}),
        }
    return result
