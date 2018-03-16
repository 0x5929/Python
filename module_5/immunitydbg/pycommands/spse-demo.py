#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time

# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "A Simple Hello World Script"               # the string stored will output on the list of pycommands as description of the script

# defining main function whereas the return value will show up on the status bar
	# the main function can take in arguments
	# the argument args is in the form of list []

def main(args):	
        imm = immlib.Debugger()		# first thing we need to do is to 
					# create an instance of the debugger from the immunity lib	

	imm.log("[!] HELLO WORLD OF LOGS!")	# this writes directly to the log

        imm.updateLog()                 # this will update the log as the program runs,
                                        # if not called the program will run first
                                        # and then prints out the output/logs to user,
                                        # calling this method ensures the log will be outputted as the program runs
        
	return "[!] HELLO WORLD!"	# the return value is to provide status to the user
					# while using the immunity debugger on the status bar
					# which is also logged into the log. View by clicking view then log

	
