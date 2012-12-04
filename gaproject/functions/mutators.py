
'''
Here should come the mutation functions.
'''
import random


def insertionMutation(individual,indpb):
    """
    chose an individual randomly and insert it at a random position
    """
    if(random.random()>indpb):
        indexRandomNode = random.randint(0, len(individual)-1)
        insertionPoint = random.randint(0, len(individual)-1)
        removedValue=individual.pop(indexRandomNode)  
        individual.insert(insertionPoint,removedValue)
    return individual

def inversionMutation(individual,indpb):
    """
    chose a Subtour then insert it reversed at a different part of the individual
    """
    if(random.random()>indpb):
        #compute the beginning and end of the Subtour.
        begSubtour = random.randint(0, len(individual)-1)
        endSubtour = random.randint(begSubtour, len(individual)-1)

        #extract the Subtour and reverse it
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #remove Subtour from individual
        del individual[begSubtour:endSubtour]

        #compute where to insert it
        insertionPos = random.randint(0, len(individual)-1)

        #create the new individual by inserting the Subtour at the insertion position
        individual[:] = individual[0:insertionPos] + Subtour + individual[insertionPos:]

    return individual

def simpleInversionMutation(individual, indpb):
    """
    chose a Subtour then reverse it at a different part of the individual
    """
    if(random.random()>indpb):
        begSubtour = random.randint(0, len(individual)-1)
        endSubtour = random.randint(begSubtour, len(individual)-1)

        #extract the Subtour
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #create the new individual
        individual[:] = individual[0:begSubtour] + Subtour + individual[endSubtour:]

    return individual
