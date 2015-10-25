from _ast import *

def extractTestVars(testExpr):
    possible_vars = [testExpr.left] + testExpr.comparators
    vars = [i.id for i in possible_vars if isinstance(i, Name)]
    return vars
            
def isNone(valNode):
    isNoneName = isinstance(valNode, Name) and valNode.id == "None"
    return isNoneName

def isNoneTest(testExpr):
    if isinstance(testExpr, Compare) and len(testExpr.ops) == 1:
        if isinstance(testExpr.ops[0], Is):
            return isNone(testExpr.left) or isNone(testExpr.comparators[0])
    return False

