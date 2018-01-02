#!/usr/bin/python

## in order to find out a file's stats, such as its size, creation and etc
## we need to import os module

import os

## first lets open up a test file, and write to it

testFile = open("testFile.txt", "w")

for i in range(0, 100):
	testFile.write("the number increment is: " + str(i)+ '\n')

testFile.close()


## next lets look at its stats
print "testFile has a size of: " + str(os.stat("testFile.txt").st_size)+ " bytes"

## location
print "testFile has a location of: " + os.path.abspath("testFile.txt")

## modification time
print "testFile was last modified: ",  os.path.getmtime(os.path.abspath("testFile.txt"))

## creation time
print "testFile was created: ", os.stat("testFile.txt").st_ctime



