import os
import sys

from NoneVisitor import *

dirName = '/Users/dillon/PythonWorkspace/pandas'

x = NoneVisitor()
numExceptions = 0
for root, dirs, files in os.walk(dirName):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            print path
            try:
                parsedFile = ast.parse(open(path, "r").read())
                x.currentFile = path
                x.visit(parsedFile)
            except Exception, e:
                numExceptions += 1
                print 'Error: Could not parse file, exception: %s' % e

x.printErrors()
print ''
print 'Number of exceptions', numExceptions
