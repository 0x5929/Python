#!/usr/bin/python

## handling exception in python using try block


## if there is an exception in the try block
## the except block will execute, and if there is no exception
## else block is executed
## finally block will be executed no matter what

try: 
	a = 0/0
except:
	print "Exception handled"
else: 
	print "no exceptions"
finally: 
	print "finally clean up"


try: 
	a = 1/1
except:
	print "Exception handled"
else: 
	print "no exceptions"
finally: 
	print "finally clean up"


## except block can also take a error message as an arugment as well
## this is for handling specific errs
## below is an example


## this way we can set the exception as any variable, and we can handle
## that specific exception

try: 
	a = 1/0
except Exception as exceptionVariable:
	print exceptionVariable
else: 
	print "no exceptions"
finally: 
	print "finally clean up"


## OKAY LETS DEFINE OUR OWN EXCEPTIONS
## by defining a base err class, with parent of Exception
## Any other exceptions can have this bass err class

class Error(Exception):
	"""Base 
		Class
			for all Exceptions"""
	pass
class evenErr(Error):
	"""raised when even"""
	pass
class oddErr(Error):
	"""Raised when odd"""
	pass

num = 1
while num < 5:
	try: 
		if num % 2 == 0:
			num = num + 1
			raise evenErr
		else:
			num = num + 1
			raise oddErr
	except evenErr:
		print "ERROR ITS EVEN!"
	except oddErr:
		print "ERROR ITS ODD!!"
	else:
		print "this should never print"
	finally:
		print "this should always print"
