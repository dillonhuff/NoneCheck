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

    def computeErrors(self):
        errors = set()
        varValues = {}
        self.walkCFGComputingErrors(errors, varValues)
        return errors

class Actions:
    SetNone, SetNotNone, Deref, CheckNone = range(4)

class VarValues:
    MaybeNone, NotNone = range(2)
