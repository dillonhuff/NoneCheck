import ast

from NoneVisitor import *

def testAssert(assertion, testName):
    if assertion:
        print testName + '\t\t\t' + 'passed'
    else:
        print testName + '\t\t\t' + 'FAILED'

def setNone():
    fileName = "./cases/Test3.py"
    parsedFile = ast.parse(open(fileName, "r").read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 1, "setNone")
    
def basicTest():
    fileName = "./cases/Test1.py"
    parsedFile = ast.parse(open(fileName, "r").read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 1, "basicTest")

def twoErrors():
    fileName = "./cases/Test2.py"
    parsedFile = ast.parse(open(fileName, "r").read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 2, "twoErrors")

def allTests():
    setNone()
    basicTest()
    twoErrors()

allTests()
