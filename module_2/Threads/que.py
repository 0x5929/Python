#!/usr/bin/python


## in this tutorial we will be learning how to execute Queue with threads
# this time we will be using threading module instead of the simple thread last time
# it seems like thread module is simplier
# we will also import queue module, to create task queues
# also time for timeouts

import threading
import Queue
import time


# we need a worker class to be fetching queue from queue 
# note this class inherit from threading.Thread class
class WorkerThread(threading.Thread):
	# contructor method, takes in an arg called queue
	def __init__(self, queue):
		# calls the parent class constructor method with the self object created
		# this basically initailizes the thread obj from threading class that we imported
		# this will make self object as a thread worker 
		threading.Thread.__init__(self)	
		#sets queue to the given arg
		self.queue = queue

	# run method of the workerThread class
	# NOTE: This method could contain any task you want to do with the queue by the threads
	# could be a password cracking tool, network port scanning tool....
	def run(self):
		print "WE ARE IN THE WORKER'S THREAD!!!"
		while True:	# getting a value from queue as counter
			counter = self.queue.get()
			print "We are ordered to sleep for %d seconds!!!" %counter
			time.sleep(counter)
			print "Yawn! Finished sleeping for %d seconds.." %counter
			self.queue.task_done()	# rememeber to finish the task


# creating a task queue by calling the queue method

queue = Queue.Queue()


# setting the thread workers
for i in range(10):
	print "We are now creating WorkerThread: %d" %i
	worker = WorkerThread(queue) # initializing worker thread class
	worker.setDaemon(True)	# setting daemon to be true so thread can exit after main program exits
	worker.start()	# starting the thread
	print "Worker Slave Thread %d is now Created" %i


# inputting task into queue, by putting a range of number in it
for j in range(20):
	queue.put(j) # putting range 1-10 into queue

# wait until tasks in queue are empty by:
# when there is no more queues to be get by queue.get(), queue.join() will complete
queue.join()
## from documentation: 
## blocks until all items in the queue have been gotten and processed
## when the count of unfinished tasks drops to zero, join() unblocks



# execute final message
print "ALL TASKS ARE NOW OVER, ALL WERE COMPLETED BY OUR SLAVE THREADS!!!!"







