#!/usr/bin/python

## below is the syntax of how to define a function in python
## using the def keyword, remember indentation means that function body

## importing a module called sys, to be used as a command line argument passed by user
## this will be used at the end of the script to call the function with
import sys

def print5times(string_to_print):
	
	for count in range(0,5):
		print string_to_print
	## functions DONT have to return anything

## calling that function
## sys.argv[1] meaning the seoncd  argument given from the command line by the user 
## will be the argument, the first command line argument being the ./function.py itself

print5times(sys.argv[1])
## this function will print the user input 5 times


