'''
Operators are the main specificities of Genetic Algorithms.
This (sub-)library contains the operators used for this TSP problem.
'''

# import gaproject.operators.evaluators as evaluators
import mutators as mutators
import evaluators as evaluators
import crossovers as crossovers
import creators

# The aliases contain the nicknames used to refer to the operators
# in the analysis.
alias = {
    'path_creator': creators.path_creator,
    'adj_creator': creators.adj_creator,

    'eval_simple': evaluators.evalTSP,
    'eval_adjacent': evaluators.evalTSPAdjacentEdges,

    'mutshuf': mutators.mutShuffleIndexes,
    'insert_mut': mutators.insertionMutation,
    'invert_mut': mutators.inversionMutation,
    'simple_inv': mutators.simpleInversionMutation,

    'invert_mut_adj': mutators.inversionMutationAdj,
    'insert_mut_adj': mutators.insertionMutationAdj,
    'simple_inv_adj': mutators.simpleInversionMutationAdj,
    'mutshuf_adj': mutators.mutShuffleIndexesAdj,

    'meta_insert': mutators.insertionMutationMetaGA,

    'cxOX': crossovers.cxOrdered,
    'cxHeuristic': crossovers.cxHeuristic,
    'cxSCX': crossovers.cxSimpleSCX,
    'cxESCX': crossovers.cxEnhancedSCX,
    'cxERX': crossovers.cxERX,
    'cxPMX': crossovers.cxPMX,
    }
