#!/usr/bin/python

## for loops are for iterating through an object
## for something(varaible name) in an object


print "printing name lists, which are arrays in js: "

names = ["kevin", "ricky", "bbq", "jlee"]

for friendNames in names:
	print friendNames

print "printing hybridList, another list, but hybrid with diff obj data types"
hybridList = [1, "kevin", 2, "bbq", [1, 2, 3]]

for item in hybridList:
	print item

print "printing a tuple list using for loop watch for syntax"
tupleList = [("kevin", 24), ("ricky", 25)]

for (a, b) in tupleList:
	print "name " + a 
	print "is " + str(b) + " years old"
else: 
##using else statement
	print "andddd no more names and ages on the tuple list"


## for emulating C style for loops: for (i=1; i< 10; i++)
## use for with combination with range function
## example shown below

## range function takes three arguements, where the latter two are optional
## range(first number inclusive, last number exclusive, step)
## returns a list of items that can be iterated through using for loop

print "using for and range together: "
for item in range(0,10, 2):
	print item

## above is equal to in js for (var i = 0; i< 10; i=i+2){print i}
