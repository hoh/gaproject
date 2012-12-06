
from deap import creator
import random

'''
Here should come the crossover functions.
'''

def cxERX(individual1,individual2):
	return  CXERXCalculator(individual1,individual2).crossover()

class CXERXCalculator:

    def __init__(self, individual1,individual2):
    	self.individual2 = individual2
    	self.individual1 = individual1
    	self.edgeMap = {} 	

	def crossover(self):
		self.buildEdgeMap()
		return self.createChild()

	def createChild(self):
	    child = creator.Individual()
	    #step1
	    currentNode = self.individual1[random.randint(0,len(self.individual1)-1)]
	    while True:
	        child.append(currentNode)
	        #extract the nodes linked to current node
	        neighborgs = self.edgeMap.pop(currentNode)
	        neighborgs = list(neighborgs)
	        #remove references to the current node
	        self.cleanupNodeFromEdgeMap(currentNode)
	        if neighborgs != []:
	            #find which neighborg node has the less edges
	            currentNeighborg = neighborgs[0]
	            currentLen = len(self.edgeMap[currentNeighborg])
	            for neighborg in neighborgs:
	                if len(self.edgeMap[neighborg]) < currentLen:
	                    currentLen = len(self.edgeMap[neighborg])
	                    currentNeighborg = neighborg
	            #the neighborg with the less edges is the next node in the child
	            currentNode = currentNeighborg
	        else:
	            if self.edgeMap == {}: 
	                break #if there are no more nodes to assign then stop
	            else:
	                #chose as next node any remaining node at random
	                currentNode = self.edgeMap.keys()[random.randint(0,len(self.edgeMap.keys())-1)]
	    return child
	
	def buildEdgeMap(self):
		 #build the edgemap
	    for node in self.individual1:
	        pos1 = self.individual1.index(node)
	        pos2 = self.individual2.index(node)
	        neighborg1 = self.individual1[(pos1-1) % len(self.individual1)]
	        neighborg2 = self.individual1[(pos1+1) % len(self.individual1)]
	        neighborg3 = self.individual2[(pos2-1) % len(self.individual2)]
	        neighborg4 = self.individual2[(pos2+1) % len(self.individual2)]
	        self.edgeMap[node]=set([neighborg1,neighborg2,neighborg3,neighborg4])

	def cleanupNodeFromEdgeMap(self,referenceNode):
	    edgeMapEntriesToBeRemoved = []
	    for node in self.edgeMap:
	        if referenceNode in self.edgeMap[node]:
	            self.edgeMap[node].remove(referenceNode)
	        if self.edgeMap[node] == set():
	            edgeMapEntriesToBeRemoved.append(node)
	    for node in edgeMapEntriesToBeRemoved:
	            edgeMapEntriesToBeRemoved.remove(node)
