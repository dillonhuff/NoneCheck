from _ast import *

def extractTestVars(testExpr):
    possible_vars = [testExpr.left] + testExpr.comparators
    vars = [i.id for i in possible_vars if isinstance(i, Name)]
    return vars
            
def isNone(valNode):
    return isinstance(valNode, Name) and valNode.id == "None"

def isNoneTest(testExpr):
    if isinstance(testExpr, Compare):
        return True
    return False

