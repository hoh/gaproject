'''
Operators are the main specificities of Genetic Algorithms.
This (sub-)library contains the operators used for this TSP problem.
'''

# import gaproject.operators.evaluators as evaluators
import mutators as mutators
import evaluators as evaluators

# The aliases contain the nicknames used to refer to the operators
# in the analysis.
alias = {
    'eval_simple': evaluators.evalTSP,

    'mutshuf': mutators.mutShuffleIndexes,
    'insert_mut': mutators.insertionMutation,
    'ivert_mut': mutators.inversionMutation,
    'simple_inv': mutators.simpleInversionMutation,
    }