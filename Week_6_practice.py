#IMPLICIT GRAPH IMPLEMENTATION
class puzzle(object):
    def __init__(self, order):
        self.label = order
        for index in range(9):
            if order[index] == '0':
                self.spot = index
                return None
    def transition(self, to):
        label = self.label
        blankLocation = self.spot
        newBlankLabel = str(label[to])
        newLabel = ''
        for i in range(9):
            if i == to:
                newLabel += '0'
            elif i == blankLocation:
                newLabel += newBlankLabel
            else:
                newLabel += str(label[i])
        return puzzle(newLabel)
    def __str__(self):
        return self.label



def DFSWithGeneratorShortest(start, end, path = [], shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    if start.label == end.label:
        return path
    for shift in shiftDict[start.spot]:
        new = start.transition(shift)
        if new.label not in path: #avoid cycles
            if shortest == None or len(path) < len(shortest):
                newPath = DFSWithGeneratorShortest(new,end,path,shortest)
                if newPath != None:
                    shortest = newPath
    return shortest

def BFSWithGenerator(start, end, q = []):
    initPath = [start]
    q.append(initPath)
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
        if lastNode.label == end.label:
            return tmpPath
        for shift in shiftDict[lastNode.spot]:
            new = lastNode.transition(shift)
            if notInPath(new, tmpPath):
                newPath = tmpPath + [new]
                q.append(newPath)
    return None

def DFSWithGenerator(start, end, stack = []):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    initPath = [start]
    stack.insert(0, initPath)
    while len(stack)!= 0:
        tmpPath = stack.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
        if lastNode.label == end.label:
            return tmpPath
        for shift in shiftDict[lastNode.spot]:
            new = lastNode.transition(shift)
            if notInPath(new, tmpPath): #avoid cycles
                newPath = tmpPath + [new]
                stack.insert(0, newPath)
    return None


def notInPath(node, path):
    for elt in path:
        if node.label == elt.label:
            return False
    return True


shiftDict = {}
shiftDict[0] = [1, 3]
shiftDict[1] = [0, 2, 4]
shiftDict[2] = [1, 5]
shiftDict[3] = [0, 4, 6]
shiftDict[4] = [1, 3, 5, 7]
shiftDict[5] = [2, 4, 8]
shiftDict[6] = [3, 7]
shiftDict[7] = [4, 6, 8]
shiftDict[8] = [5, 7]

goal = puzzle('012345678')
test1 = puzzle('125638047')


def printGrid(pzl):
    data = pzl.label
    print data[0], data[1], data[2]
    print data[3], data[4], data[5]
    print data[6], data[7], data[8]
    print ''

def printSolution(path):
    for elt in path:
        printGrid(elt)

path = BFSWithGenerator(test1, goal)
print printSolution(path)



#MAXIMAL CLIQUE IMPLEMENTATION
class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return str(self.src) + '->' + str(self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight = 1.0):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->(' + str(self.weight) + ')'\
            + str(self.dest)

class Digraph(object):
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)





def powerGraph(gr):
    nodes = gr.nodes
    nodesList = []
    for elt in nodes:
        nodesList.append(elt)
    pSet = powerSet(nodesList)
    return pSet

def powerSet(elts):
    if len(elts) == 0:
        return [[]]
    else:
        smaller = powerSet(elts[1:])
        elt = [elts[0]]
        withElt = []
        for s in smaller:
            withElt.append(s + elt)
        allofthem = smaller + withElt
        return allofthem

def maxClique(gr):
    candidates = powerGraph(gr)
    keepEm = []
    for candidate in candidates:
        if allConnected(gr, candidate):
            keepEm.append(candidate)
    bestLength = 0
    bestSoln = None
    for test in keepEm:
        if len(test) > bestLength:
            bestLength = len(test)
            bestSoln = test
    return bestSoln

def allConnected(gr,candidate):
    for n in candidate:
        for m in candidate:
            if not n == m:
                if n not in gr.childrenOf(m):
                    return False
    return True


def testGraph():
    nodes = []
    for name in range(5):
        nodes.append(Node(str(name)))
    g = Graph()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[1],nodes[2]))
    g.addEdge(Edge(nodes[2],nodes[0]))
    g.addEdge(Edge(nodes[2],nodes[4]))
    g.addEdge(Edge(nodes[4],nodes[3]))
    return g


trialGraph = testGraph()
myClique = maxClique(trialGraph)




        

