#!/usr/bin/python
 

## in order to navigate around file directories
## we need to import the os module
## in order to do special navigation, using bash wildcards, and file location
## we needto import glob module

import os
import glob

## current working directory

print "MY CURRENT DIRECTORY: " + os.getcwd()

## creating a new directory
print "CREATING A NEW DIRECTORY, PLEASE USE ls TO CHECK"

#os.mkdir('newDirectory')
## removing a directory: os.rmdir('dirName')


## listing directories/files in a path
print "LISTING ALL THE DIRECTORIES AND FILES IN THE CWD: " 
for items in os.listdir('.'):
	## we can also test each item if its a file, or dir
	if os.path.isfile(items):
		print items + " is a file"	
	elif os.path.isdir(items):
		print items + " is a directory"
	else: 
		print "this will never appear"

print "#############################################"


## using glob
print "LISTING ALL PYTHON FILES USING WILDCARD * AND GLOB MODULE"
for item in glob.glob(os.path.join(".", "*.py")):
	print item

print "########################################################"
