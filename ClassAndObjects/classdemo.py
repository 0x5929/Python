#!/usr/bin/python

## below is how you would define a class
## using Class keyword, and Uppercase first letter names
## defining a global variable:
self = 100
class Calculator:
	
	## Now we define a constructor of class
	## this is the first function, that inistantiate an object of type Class Calculator
	## note the first arg is always self in functions within a class
	## you would want to store properties of the self arg to the other variables
	## creating an self object with values 

	self = 99
	def __init__(self, ina, inb ):
		self.a = ina
		self.b = inb
		self.self = ina+1+inb

	def add(self):
		return self.a + self.b

	def mult(self):
		return self.a + self.b



## now lets use the class to create an instance of an object by running the class
## and assigning it to a variable

newCalculator = Calculator(10, 20)

print 'a + b= %d' %newCalculator.add()
print 'a * b= %d' %newCalculator.mult()

##printing class  local instance variable and global variable

## instance:
print "instance variable", newCalculator.self
## global
print "global variable", self
## class, this will only work, if there are no instance variable with the same name
print "class variable", newCalculator.self


## now to demostrate inheritance: 
## in python, a class can inherit from another by the following syntax
## by putting the parent class in the class argument like so

class Scientific(Calculator):
## the method below mult will over ride its parent class mult method
	def mult(self):
		return self.a*self.b*self.b
	def power(self):
		return self.a ** self.b

newPower = Scientific(2,3)

print 'a power b = %d' %newPower.power()
print 'overridden mult : a * b *b = %d' %newPower.mult()
