#!/usr/bin/python

## opening up a file using the open function
## first argument is the file name
## second is the mode: w for write, it will open a new file if non exist
## w will also overwrite an exist one, if you want to write to an existing one
## use "a" for append
## use "r" for read
## third argument is optional for buffer
## this will write the file onto its current directory
## to rename or to delete files, we need to import the os module

import os


#fdescription = open("sample.txt", "w")
#fdescription = open("sample.txt", "a")

## file.write() will write to the file using the its string arguments
#for count in range(100, 200):
#	fdescription.write(str(count) +  "\n")


## using read function
fdescription = open("renamedSample.txt", "r")
## readlinefunction can be used af the file is open in read mode
## it will read each of the lines of the file
for line in fdescription.readlines() :
## strip() method will strip off the /n on each line
	print line.strip()

## close method will close the file
# using the read function instead 



os.rename("renamedSample.txt", "renamedSample.txt")


fdescription.close()









