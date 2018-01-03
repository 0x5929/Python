#!/usr/bin/python


# mutli thread socket server

import socket
import threading
import Queue


## USAGE: 
#	can be connected to as many echo servers as there are threads
# 	server will not close until all connections are made and closed after



# threading worker class

class SlaveThreads(threading.Thread):
	def __init__(self, i, queue): # think about what each thread will recieve as args
		threading.Thread.__init__(self)	#calling parent thread class for thread workers
		self.i = i
		self.queue = queue
	def run(self):
		print "HELLOO WORLD, I AM SLAVE NUMBER: %d" %self.i
		# extract data from queue
		queueData = self.queue.get()
		client = queueData[0]
		clientIP = queueData[1]
		clientPORT = queueData[2]
		data = 'dummy'
		print """SLAVE ID: %d will now perform ECHO server with a client of 
				IP: %s 
				PORT: %s""" %(self.i, clientIP, clientPORT)
		while data: # this will keep running until connection is closed
			data = client.recv(6000)
			print "Client Sent: ", data
			client.send(data)
		else:	# if client closes connection
			print """SLAVE ID: %d now closing Client Connection
					with client IP: %s
						client PORT: %s""" %(self.i, clientIP, clientPORT)
			client.close() 
			self.queue.task_done()


# starting up the queue
queue = Queue.Queue()

		
# starting up the tcp socket server

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSocket.bind(("0.0.0.0", 8000))
print "Server listening on 192.168.1.114:8000"
tcpSocket.listen(5)

# assigning echo server to each threads
for i in range(3):
	print "Waiting for a client to connect~~~"
	(client, (ip, port)) = tcpSocket.accept()
	print "Starting to Create Slave Number %d" %i
	queue.put([client, ip, port])
	newSlave = SlaveThreads(i, queue)
	newSlave.start()

# this will be blocking to execute until all tasks are done
queue.join()

print "Closing The Server Socket ......"
tcpSocket.close()

