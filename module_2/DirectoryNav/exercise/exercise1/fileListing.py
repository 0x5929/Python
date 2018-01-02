#!/usr/bin/python

import os

# working directory, initialized at cwd
global wd
wd  = os.getcwd()
# level, initialized at 1
global lvl 
lvl = 1
# do we have a deeper level?
global deeperLvl 
deeperLvl = False

# function to check if file is a directory
# if it is, the function will return back to the iterate function with deeperLvl updated
def check(itemDirectory):
	## has to be a full abs path for the check, if not it would check this files cwd
	if os.path.isdir(itemDirectory):
		global deeperLvl	
		deeperLvl = True	#switching deepLvl check to be true
		return
	else:
		return
# function to print results
# depending on its level
def Print(item, lvl):
	if lvl == 1:
		print "-- " + item
	elif lvl == 2:
		print "---- " + item
	elif lvl == 3:
		print "------- " + item
	elif lvl == 4: 
		print "--------- " + item
	else:
		print "Uh oh, error, this should never happen!!"

# function to iterate
# the main function
def iterate(level, cwd):
	# iterates through the current working directory	
	for item in os.listdir(cwd):
		# grabbing the full abs path of item, and sending it to check
		itemDir = os.path.join(cwd, item)
		check(itemDir)
		## if the item checked is a directory, hence having another lvl
		if deeperLvl == True:
			## print the directory with its appropriate lvl
			Print(item, lvl)
			## updating the level, working directory, and deeperLvl
			global lvl
			lvl = lvl + 1
			global wd
			wd = wd + '/' + item
			global deeperLvl
			deeperLvl = False
			# recursively calling itself for the deeper level
			return iterate(lvl, wd)
		else:	# if not a directory, sending the item to print
			Print(item, lvl)
	return

## calling the main iterate function
iterate(lvl, wd)





