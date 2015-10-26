from copy import *

class ControlFlowNode():
    def __init__(self, fileName, funcName):
        self.fileName = fileName
        self.funcName = funcName
        self.actions = []
        self.children = set()
        self.varValues = {}

    def newChild(self):
        newChild = ControlFlowNode(self.fileName, self.funcName)
        self.children.add(newChild)
        return newChild

    def possiblyNone(self, var):
        return 'none' in self.varValues[var] or 'maybe-none' in self.varValues[var]

    def checkNone(self, var):
        self.actions.append((Actions.CheckNone, var))

    def deref(self, var):
        self.actions.append((Actions.Deref, var))

    def setNone(self, var):
        self.actions.append((Actions.SetNone, var))

    def setNotNone(self, var):
        self.actions.append((Actions.SetNotNone, var))

    def errorString(self, var):
        return self.fileName + ': ' + self.funcName + ': ' + var + ' may be none'

    def collectNodes(self, added, nodes):
        if not self in nodes:
            nodes.add(self)
            added.add(self)
        for child in self.children:
            if not child in added:
                child.collectNodes(added, nodes)

    def computeErrors(self):
        allNodes = set()
        added = set()
        self.collectNodes(added, allNodes)
        allNodes = list(allNodes)
        print 'Number of nodes', len(allNodes)
        liveInLiveOut = noneDataFlowAnalysis(allNodes)
        maybeNoneIn = liveInLiveOut[0]
        maybeNoneOut = liveInLiveOut[1]
        errors = set()
        for node in allNodes:
            for var in maybeNoneIn[node]:
                if var in node.use():
                    errors.add(node.errorString(var))
        return errors

    def use(self):
        varsUsed = set()
        for action in self.actions:
            if action[0] == Actions.Deref:
                varsUsed.add(action[1])
        return varsUsed

    def define(self):
        varsDefined = set()
        for action in self.actions:
            if action[0] == Actions.SetNone or action[0] == Actions.CheckNone:
                varsDefined.add(action[1])
        return varsDefined

class Actions:
    SetNone, SetNotNone, Deref, CheckNone = range(4)

class VarValues:
    MaybeNone, NotNone = range(2)

def noneDataFlowAnalysis(nodes):
    liveIn = {}
    liveOut = {}
    for node in nodes:
        liveIn[node] = set()
        liveOut[node] = set()
    oldLiveIn = {}
    oldLiveOut = {}
    while True:
        for node in nodes:
            oldLiveIn[node] = copy(liveIn[node])
            oldLiveOut[node] = copy(liveOut[node])
            liveIn[node] = node.use().union(liveOut[node].difference(node.define()))
            liveOut[node] = freshLiveOut(liveIn, node)
        if noChange(oldLiveIn, oldLiveOut, liveIn, liveOut):
            break
    return (liveIn, liveOut)

def freshLiveOut(liveIn, node):
    newLiveOut = set()
    for child in node.children:
        newLiveOut.union(liveIn[child])
    return newLiveOut

def noChange(oldIn, oldOut, newIn, newOut):
    return oldIn == newIn and oldOut == newOut
