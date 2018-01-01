#!/usr/bin/python

## you can import package by their directory name
## then the import function will look for the __init__.py file
## within that file, it is the entry point and it will import all scripts needed

import package

cal = package.Calculator(10,20)

value = cal.add()


print "Simple Addition from the calculator package, 10 + 20 = %d " %value 
