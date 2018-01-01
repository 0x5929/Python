#!/usr/bin/python

## below is an example of user input
## using the raw_input function with the argument of
## the system question, prompting user for an input

name = raw_input("What is your name?")

## using the printing statement with the variable storing user input
## and using string contactnation

print "Your name is " + name

## then we use an if statement depending on the user input
## python recongizes the blocks of code  by indentation
## so it is very important to have clean and clear code 
## where each block has its uniform indentation
## notice the syntax for the if/else if statements

if name == "kevin":
	print "You are Kevin!!"	
	print "The computer Admin"
elif name == "john":
	print "You are John"
	print "A regular dummy user"
else : 
	print "Unknown user"


