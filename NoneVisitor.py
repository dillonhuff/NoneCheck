import ast
from _ast import *

from ControlFlowNode import *
from SyntaxUtils import *

class NoneVisitor(ast.NodeVisitor):

    def __init__(self):
        self.errors = set()
        self.currentFile = 'NO_FILE'

    def numErrors(self):
        return len(self.errors)

    def visit_Module(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        body = node.body
        cftRoot = ControlFlowNode(self.currentFile, node.name)
        self.execBody(cftRoot, body)
        self.addErrors(cftRoot)

    def execBody(self, cfNode, stmtNodes):
        nextCFTNode = cfNode
        for stmt in stmtNodes:
            nextCFTNode = self.execNode(nextCFTNode, stmt)
        return nextCFTNode

    def execNode(self, cfNode, stmtNode):
        if isinstance(stmtNode, Assign):
            return self.execAssign(cfNode, stmtNode)
        elif isinstance(stmtNode, Return):
            return self.execReturn(cfNode, stmtNode)
        elif isinstance(stmtNode, Call):
            return self.execCall(cfNode, stmtNode)
        elif isinstance(stmtNode, Name):
            return self.execName(cfNode, stmtNode)
        elif isinstance(stmtNode, If):
            return self.execIf(cfNode, stmtNode)
        elif isinstance(stmtNode, Expr):
            return self.execNode(cfNode, stmtNode.value)
        elif isinstance(stmtNode, Num):
            return cfNode.newChild()
        elif isinstance(stmtNode, Print):
            return cfNode.newChild()
        elif isinstance(stmtNode, BinOp):
            return cfNode.newChild()
        elif isinstance(stmtNode, Str):
            return cfNode.newChild()
        elif isinstance(stmtNode, List):
            return cfNode.newChild()
        elif isinstance(stmtNode, Call):
            return cfNode.newChild()
        elif isinstance(stmtNode, Dict):
            return cfNode.newChild()
        elif isinstance(stmtNode, Assert):
            return cfNode.newChild()
        elif isinstance(stmtNode, Attribute):
            return cfNode.newChild()
        elif isinstance(stmtNode, BoolOp):
            return cfNode.newChild()
        elif isinstance(stmtNode, UnaryOp):
            return cfNode.newChild()
        elif isinstance(stmtNode, For):
            return cfNode.newChild()
        elif isinstance(stmtNode, While):
            return cfNode.newChild()
        elif isinstance(stmtNode, IfExp):
            return cfNode.newChild()
        elif isinstance(stmtNode, TryExcept):
            return cfNode.newChild()
        elif isinstance(stmtNode, Subscript):
            return cfNode.newChild()
        elif isinstance(stmtNode, TryFinally):
            return cfNode.newChild()
        elif isinstance(stmtNode, FunctionDef):
            return cfNode.newChild()
        elif isinstance(stmtNode, Pass):
            return cfNode.newChild()
        elif isinstance(stmtNode, Compare):
            return cfNode.newChild()
        elif isinstance(stmtNode, ListComp):
            return cfNode.newChild()
        elif isinstance(stmtNode, With):
            return cfNode.newChild()
        elif isinstance(stmtNode, Lambda):
            return cfNode.newChild()
        elif isinstance(stmtNode, Delete):
            return cfNode.newChild()
        elif isinstance(stmtNode, Raise):
            return cfNode.newChild()
        elif isinstance(stmtNode, ImportFrom):
            return cfNode.newChild()
        elif isinstance(stmtNode, Import):
            return cfNode.newChild()
        elif isinstance(stmtNode, GeneratorExp):
            return cfNode.newChild()
        elif isinstance(stmtNode, Yield):
            return cfNode.newChild()
        elif isinstance(stmtNode, AugAssign):
            return cfNode.newChild()
        elif isinstance(stmtNode, Tuple):
            return cfNode.newChild()
        elif isinstance(stmtNode, ClassDef):
            return cfNode.newChild()
        elif isinstance(stmtNode, Global):
            return cfNode.newChild()
        else:
            raise ValueError('execNode: unsupported stmt\n' + ast.dump(stmtNode))

    def execName(self, cfNode, nameNode):
        cfNode.deref(nameNode.id)
        return cfNode.newChild()

    def execAssign(self, cfNode, assignNode):
        newNode = cfNode.newChild()
        valNode = assignNode.value
        if isNone(valNode):
            for idNode in assignNode.targets:
                if isinstance(idNode, Name):
                    newNode.setNone(idNode.id)
            return newNode
        else:
            for idNode in assignNode.targets:
                if isinstance(idNode, Name):
                    newNode.setNotNone(idNode.id)
            return self.execNode(newNode, valNode)

    def execIf(self, cfNode, ifNode):
        test = ifNode.test
        tBody = ifNode.body
        fBody = ifNode.orelse
        return self.execCond(cfNode, test, tBody, fBody)
    
    def execCond(self, cfNode, test, tBody, fBody):
        testResNode = self.execTest(cfNode, test)
        resultNodes = [self.execBody(testResNode, tBody), self.execBody(testResNode, fBody)]
        resNode = ControlFlowNode(testResNode.fileName, testResNode.funcName)
        map(lambda n: n.children.add(resNode), resultNodes)
        return resNode

    def execTest(self, cfNode, testExpr):
        testResNode = cfNode.newChild()
        if isNoneTest(testExpr):
            v = extractTestVars(testExpr)[0]
            testResNode.checkNone(v)
        return testResNode

    def execReturn(self, cfNode, retNode):
        return self.execNode(cfNode, retNode.value)

    def callerShouldntBeNone(self, cfNode, callNode):
        if isinstance(callNode.func, Attribute):
            attr = callNode.func
            if isinstance(attr.value, Name):
                callerName = attr.value.id
                cfNode.deref(callerName)

    def execCall(self, cfNode, callNode):
        self.callerShouldntBeNone(cfNode, callNode)
        resNodes = self.execBody(cfNode.newChild(), callNode.args)
        return resNodes

    def addErrors(self, cft):
        for error in cft.computeErrors():
            self.errors.add(error)

    def printErrors(self):
        print ''
        print '--------------- ERROR REPORT --------------'
        print 'Number of errors:', str(len(self.errors))
        for error in self.errors:
            print error
        print '-------------------------------------------'
        print ''
