'''
Operators are the main specificities of Genetic Algorithms.
This (sub-)library contains the operators used for this TSP problem.
'''

# import gaproject.operators.evaluators as evaluators
import mutators as mutators
import evaluators as evaluators
import crossovers as crossovers

# The aliases contain the nicknames used to refer to the operators
# in the analysis.
alias = {
    'eval_simple': evaluators.evalTSP,
    'eval_adjacent': evaluators.evalTSPAdjacentEdges,

    'mutshuf': mutators.mutShuffleIndexes,
    'insert_mut': mutators.insertionMutation,
    'invert_mut': mutators.inversionMutation,
    'simple_inv': mutators.simpleInversionMutation,

    'invert_mut_adj': mutators.inversionMutationAdj,
    'inset_mut_adj': mutators.insertionMutationAdj,
    'simple_inv_adj': mutators.simpleInversionMutationAdj,
    'mutshuf_adj': mutators.mutShuffleIndexesAdj,

    'cxOX': crossovers.cxOrdered,
    'cxHeuristic': crossovers.cxHeuristic,
    'cxSCX': crossovers.cxSimpleSCX,
    'cxESCX': crossovers.cxEnhancedSCX,
    'cxERX': crossovers.cxERX,
    'cxPMX': crossovers.cxPMX
    }
