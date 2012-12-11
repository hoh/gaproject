'''
Set to be used for benchmarks.
'''
from gaproject.functions.evaluators import Evaluators
from gaproject.functions.mutators import mutShuffleIndexes, \
                                         insertionMutation, \
                                         inversionMutation, \
                                         simpleInversionMutation
from functions.mutators import insertionMutation

# alias = {
#     'dist': Evaluators(distance_map).evalTSP,
#     'mut1': (mutShuffleIndexes, {'indpb': 0.05}),
# }

# operators = {'evaluate': Evaluators(distance_map).evalTSP,

#                  #'mutate': (mutShuffleIndexes, {'indpb': 0.05}),
#                  'mutate': (insertionMutation, {'indpb': 0.05}),
#                  #'mutate': (inversionMutation, {'indpb': 0.05}),
#                  #'mutate': (simpleInversionMutation, {'indpb': 0.05}),
#                  }

bench = {0: {'genetations': 500,
             'evaluate': 'dist',
             'mutate': 'mut1',
             },
         }
