import ast

from NoneVisitor import *

def testAssert(assertion, testName):
    if assertion:
        print testName + '\t\t\t' + 'passed'
    else:
        print testName + '\t\t\t' + 'FAILED'

def countErrors(fileName):
    parsedFile = ast.parse(open(fileName, 'r').read())
    x = NoneVisitor()
    x.visit(parsedFile)
    return x.numErrors()

def setNone():
    fileName = './cases/Test3.py'
    parsedFile = ast.parse(open(fileName, 'r').read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 1, 'setNone')
    
def basicTest():
    fileName = './cases/Test1.py'
    parsedFile = ast.parse(open(fileName, 'r').read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 1, 'basicTest')

def twoErrors():
    fileName = './cases/Test2.py'
    parsedFile = ast.parse(open(fileName, 'r').read())
    x = NoneVisitor()
    x.visit(parsedFile)
    testAssert(x.numErrors() == 2, 'twoErrors')

def noError():
    numErrors = countErrors('./cases/Test4.py')
    testAssert(numErrors == 0, 'noError')

def noErrorIs():
    testAssert(countErrors('./cases/Test5.py') == 0, 'noErrorIs')

def oneFuncallNoError():
    testAssert(countErrors('./cases/Test6.py') == 0, 'oneFuncallNoError')

def oneForwardError():
    testAssert(countErrors('./cases/Test7.py') == 1, 'oneForwardError')

def allTests():
    setNone()
    basicTest()
    twoErrors()
    noError()
    noErrorIs()
    oneFuncallNoError()
    oneForwardError()

allTests()
