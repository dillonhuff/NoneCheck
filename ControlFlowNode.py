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

    def executeAction(self, action, errors, varValues):
        instr = action[0]
        var = action[1]
        if instr == Actions.SetNone:
            varValues[var] = VarValues.MaybeNone
        elif instr == Actions.SetNotNone:
            varValues[var] = VarValues.NotNone
        elif instr == Actions.CheckNone:
            if var in varValues and varValues[var] == VarValues.NotNone:
                errors.add(self.errorString(var))
            varValues[var] = VarValues.MaybeNone
        elif instr == Actions.Deref:
            if var in varValues and varValues[var] == VarValues.MaybeNone:
                errors.add(self.errorString(var))
            else:
                varValues[var] = VarValues.NotNone
        else:
            raise ValueException('ExecuteAction: Unsupported action')

    def walkCFGComputingErrors(self, errors, varValues):
        for action in self.actions:
            self.executeAction(action, errors, varValues)
        valsCopy = copy(varValues)
        for childNode in self.children:
            childNode.walkCFGComputingErrors(errors, valsCopy)
        return errors

    def collectNodes(self):
        allNodes = [self]
        for child in self.children:
            allNodes += child.collectNodes()
        return allNodes

    def computeErrors(self):
        allNodes = self.collectNodes()
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
        if noChange(oldLiveIn, oldLiveOut, liveIn, liveOut):
            break
    return (liveIn, liveOut)

def noChange(oldIn, oldOut, newIn, newOut):
    return oldIn == newIn and oldOut == newOut
