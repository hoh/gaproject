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
# def get(names):
#     'returns values from db'


def get():
    return {
        'set1': {
            'mutate': 'mutshuf',
            }
    }


def evaluate(set):
    result = {}
    # for key in ('mutate',):
    #     nickname = set[key]
    #     result[key] = alias[nickname]
    return result
