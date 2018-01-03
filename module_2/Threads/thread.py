#!/usr/bin/python


#python threading using the thread module, we also need the time module for sleeping purpose


import thread
import time

#defining a thread function
def worker_thread(id):
		
	print "THREAD ID %d NOW ALIVE!!" %id

	count = 1
	while True:	#notice the syntax of the format, in terms of as tuple if there are multiple
		print "Thread with ID %d has counter value %d" %(id, count)
		time.sleep(2) #puts system to sleep for two seconds
		count += 1 #increment counter for each thread, to go on and on until program is stopped



# the for loop combo with range will start the threads with the func above
# and pass in 5 different id, for 5 different threads.

for i in range(5):
	# starting a new thread by: 
	# first arg is the function name which you want to threadify
	# second arg is the arg that you want want to pass to the function thread, 
	# in the form of a tuple
	thread.start_new_thread(worker_thread, (i,))

# wait on the script, this will keep the program running, hence having the worker thread to keep running
print "MAIN THREAD GOING FOR A INFINITE WAIT LOOP"
while True:
	pass
