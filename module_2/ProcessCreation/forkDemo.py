#!/usr/bin/python

## fork demo
## importing os module for pid functionailities
import os

# write a function where the child process needs to execute

# to get the pid of a process use: os.getpid() of the current context of the process
def child_process():
	print "I AM THE CHILD PROCESS and my PID is: %d" %os.getpid() #returns child pid
	print "The child exiting...."



# write a parent process
def parent_process():
	print "I am the parent process with PID: %d" %os.getpid() # should return parent pid
	
	#fork a child, this will duplicate the exact replica of the parent process, one parent, one child
	childpid = os.fork() 
	if childpid == 0: #in the child fork,  fork will return 0
		# we are inside the child
		print "we are inside the child process"
		child_process() #calling child func, and returning childpid from that func 
	else:	# inside the parent fork, childpid will return child's pid
		# we are inside the parent process
		print "We are inside the parent process"
		print "Our child has the PID: %d" %childpid # this should return the child pid
	
	# next we keep this function running with infinite loop below
	while True:
		pass


## running the parent process function
parent_process()




