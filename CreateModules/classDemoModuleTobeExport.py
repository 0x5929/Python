#!/usr/bin/python

class Calculator:
	def __init__(self, ina, inb ):
		self.a = ina
		self.b = inb
	def add(self):
		return self.a + self.b

	def mult(self):
		return self.a + self.b



class Scientific(Calculator):
## the method below mult will over ride its parent class mult method
	def mult(self):
		return self.a*self.b*self.b
	def power(self):
		return self.a ** self.b


def quickAdd(a,b):
	return a + b	




