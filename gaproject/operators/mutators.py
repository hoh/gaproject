
'''
Here should come the mutation functions.
'''

import random

from gaproject.operators.optimizers import loop_removal
from gaproject.tools.adjacent import fromAdjacentToPath
from gaproject.tools.adjacent import fromPathToAdjacent
from gaproject.tools.adjacent import checkIfValidAdjacent

# Importing the mutator from DEAP
from deap import tools
mutShuffleIndexes = loop_removal(tools.mutShuffleIndexes)


def mutationFromAdjacentToPath(function):
    'Allows use of a Path representation based mutator on Adjascent representation.'

    def wrapped(individual, indpb):
        # print 'mut from:', individual
        if not checkIfValidAdjacent(individual):
            raise ValueError('Invalid error.')
        # print 'individual', type(individual), individual
        indi = fromAdjacentToPath(individual)
        # print 'indi', type(indi), indi
        result = function(indi, indpb)
        # print 'result', type(result), result
        individual[:] = fromPathToAdjacent(result[0])
        # print 'individual', type(individual), individual
        # print '\n'*5
        return individual
    return wrapped

mutShuffleIndexesAdj = mutationFromAdjacentToPath(mutShuffleIndexes)


@loop_removal
def insertionMutation(individual, indpb):
    """
    Chosing an node randomly and inserting it at a random position.
    """
    if (random.random() < indpb):
        indexRandomNode = random.randint(0, len(individual) - 1)
        insertionPoint = random.randint(0, len(individual) - 1)
        removedValue = individual.pop(indexRandomNode)
        individual.insert(insertionPoint, removedValue)

    return individual,

insertionMutationAdj = mutationFromAdjacentToPath(insertionMutation)


@loop_removal
def inversionMutation(individual, indpb):
    """
    Chosing a Subtour then inserting it reversed at a different part of the individual.
    """
    if(random.random() < indpb):
        #compute the beginning and end of the Subtour.
        begSubtour = random.randint(0, len(individual) - 1)
        endSubtour = random.randint(begSubtour, len(individual) - 1)

        #extract the Subtour and reverse it
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #remove Subtour from individual
        del individual[begSubtour:endSubtour]

        #compute where to insert it
        insertionPos = random.randint(0, len(individual) - 1)

        #create the new individual by inserting the Subtour at the insertion position
        individual[:] = individual[0:insertionPos] + Subtour + individual[insertionPos:]

    return individual,

inversionMutationAdj = mutationFromAdjacentToPath(inversionMutation)


@loop_removal
def simpleInversionMutation(individual, indpb):
    """
    Reversing a Subtour.
    """
    if(random.random() < indpb):
        begSubtour = random.randint(0, len(individual) - 1)
        endSubtour = random.randint(begSubtour, len(individual) - 1)

        #extract the Subtour
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #create the new individual
        individual[:] = individual[0:begSubtour] + Subtour + individual[endSubtour:]

    return individual,

simpleInversionMutationAdj = mutationFromAdjacentToPath(simpleInversionMutation)


__all__ = (mutShuffleIndexes,
           insertionMutation,
           inversionMutation,
           simpleInversionMutation,
           insertionMutationAdj,
           inversionMutationAdj,
           simpleInversionMutationAdj,
           mutShuffleIndexesAdj
           )
