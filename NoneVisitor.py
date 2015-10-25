import ast
from _ast import *

from ControlFlowNode import *

class NoneVisitor(ast.NodeVisitor):

    def __init__(self):
        self.errors = set()

    def numErrors(self):
        return len(self.errors)

    def visit_Module(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        body = node.body
        cftRoot = ControlFlowNode()
        self.execStmts([cftRoot], body)
        self.addErrors(cftRoot)

    def execStmts(self, cfNodes, stmtNodes):
        if len(stmtNodes) == 0:
            return cfNodes
        nextStmt = stmtNodes[0]
        nextCFTNodes = []
        for cfNode in cfNodes:
            nextCFTNodes += self.execStmt(cfNode, nextStmt)
        return self.execStmts(nextCFTNodes, stmtNodes[1:])

    def execStmt(self, cfNode, stmtNode):
        if isinstance(stmtNode, Assign):
            return self.execAssign(cfNode, stmtNode)
        elif isinstance(stmtNode, If):
            return self.execIf(cfNode, stmtNode)
        elif isinstance(stmtNode, Return):
            return self.execReturn(cfNode, stmtNode)
        elif isinstance(stmtNode, Call):
            return self.execCall(cfNode, stmtNode)
        elif isinstance(stmtNode, Expr):
            return self.execStmt(cfNode, stmtNode.value)
        elif isinstance(stmtNode, Name):
            return self.execName(cfNode, stmtNode)
        elif isinstance(stmtNode, Num):
            return [cfNode]
        else:
            raise ValueError('execStmt: unsupported stmt\n' + ast.dump(stmtNode))

    def execName(self, cfNode, nameNode):
        cfNode.shouldntBeNone(nameNode.id)
        return [cfNode]

    def execAssign(self, cfNode, assignNode):
        newNode = cfNode.newChild()
        valNode = assignNode.value
        if self.isNone(valNode):
            for idNode in assignNode.targets:
                newNode.setNone(idNode.id)
            return [newNode]
        else:
            for idNode in assignNode.targets:
                newNode.setNotNone(idNode.id)
            return self.execStmt(cfNode, valNode)

    def execIf(self, cfNode, ifNode):
        test = ifNode.test
        tBody = ifNode.body
        fBody = ifNode.orelse
        ifNodes = self.execCond(cfNode, test, tBody, fBody)
        return self.execStmts(ifNodes, tBody) + self.execStmts(ifNodes, fBody)

    def execCond(self, cfNode, test, tBody, fBody):
        testResNode = self.execTest(cfNode, test)
        return self.execStmts([testResNode], tBody) + self.execStmts([testResNode], fBody)

    def execTest(self, cfNode, testExpr):
        testResNode = cfNode.newChild()
        if (self.isNoneTest(testExpr)):
            v = self.extractTestVars(testExpr)[0]
            testResNode.maybeNone(v)
        return testResNode

    def execReturn(self, cfNode, retNode):
        return self.execStmt(cfNode, retNode.value)

    def callerShouldntBeNone(self, cfNode, callNode):
        if isinstance(callNode.func, Attribute):
            attr = callNode.func
            callerName = attr.value.id
            cfNode.shouldntBeNone(callerName)

    def execCall(self, cfNode, callNode):
        self.callerShouldntBeNone(cfNode, callNode)
        resNodes = self.execStmts([cfNode], callNode.args)
        return resNodes

    def isNoneTest(self, testExpr):
        if isinstance(testExpr, Compare):
            return True
        return False

    def extractTestVars(self, testExpr):
        possible_vars = [testExpr.left] + testExpr.comparators
        vars = [i.id for i in possible_vars if isinstance(i, Name)]
        return vars
            
    def isNone(self, valNode):
        return isinstance(valNode, Name) and valNode.id == "None"

    def addErrors(self, cft):
        for error in cft.computeErrors():
            self.errors.add(error)

        for child in cft.children:
            self.addErrors(child)

    def printErrors(self):
        print str(len(self.errors)) + 'ERRORS'
        for error in self.errors:
            print error
        print str(len(self.errors)) + 'ERRORS'
