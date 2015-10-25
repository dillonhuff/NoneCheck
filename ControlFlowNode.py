from copy import *

class ControlFlowNode():
    def __init__(self):
        self.errors = set()
        self.children = set()
        self.varValues = {}

    def setNone(self, val):
        self.varValues[val] = set()
        self.varValues[val].add('none')

    def setNotNone(self, val):
        self.varValues[val] = set()
        self.varValues[val].add('not-none')

    def maybeNone(self, var):
        if var in self.varValues:
            self.varValues[var].add('maybe-none')
        else:
            self.varValues[var] = set()
            self.varValues[var].add('maybe-none')

    def shouldntBeNone(self, var):
        if var in self.varValues:
            self.varValues[var].add('shouldnt-be-none')
        else:
            self.varValues[var] = set()
            self.varValues[var].add('shouldnt-be-none')

    def newChild(self):
        newChild = ControlFlowNode()
        for var in self.varValues:
            newChild.varValues[var] = set()
            for val in self.varValues[var]:
                newChild.varValues[var].add(val)
        self.children.add(newChild)
        return newChild

    def possiblyNone(self, var):
        return 'none' in self.varValues[var] or 'maybe-none' in self.varValues[var]

    def shouldNotBeNone(self, var):
        return 'shouldnt-be-none' in self.varValues[var]

    def computeErrors(self):
        errors = set()
        for var in self.varValues:
            if self.possiblyNone(var) and self.shouldNotBeNone(var):
                errors.add(var + ' may be none')
        return errors
