#!/usr/bin/python

# this will be a multi threaded TCP Server that will serve forever until SIGINT
## this is not the right way of doing a threaded socketServer

## after reading the documentation, the better way has path: 
# /home/kevin/Python/module_3/socketServer/socketServerFramework/better-multiThreadSocketServer.py

# reason for that is at the time of writing this script, there is a lack of general understanding of 
# python classes, and mulitple inheritence. and the flexibility of each classes, and the deeper understading 
# of the threading.Thread class, which can be called with a target=object to be run as a thread instead of creating
# custom threading classes. 

import SocketServer
import threading

## Threading Class
class SlaveThreads(threading.Thread):
	def __init__(self, i, IP, PORT, serverHandler):
		# remember to call the parent class's constructor to make this a thread
		threading.Thread.__init__(self)
		self.i = i
		self.IP = IP
		self.PORT = PORT
		self.serverHandler = serverHandler
	def run(self): #starting the server in here, because each slave threads will do the job
		print """HELLO WORLD, I AM SLAVE THREAD NUMBER: %d
				AND MY JOB IS TO CREATE A SOCKET SERVER LISTENING PATIENTLY ON 
					IP: %s
					PORT %d"""	%(self.i, self.IP, self.PORT)	
		# grabbing the info from for server creation
		address = (self.IP, self.PORT)
		# creating the server
		server = SocketServer.TCPServer(address, self.serverHandler)
		# setting reusable address to true
		server.allow_reuse_address = True
		# lets serve forever
		server.serve_forever()




## ServerHanlder Class
class multiThreadServerHandler(SocketServer.BaseRequestHandler):
	def handler(self):
		print "HEY LOOK! We got a connection from: ", self.client_address
		self.data = 'dummy'
		while len(self.data):
			# whatever data we recieve from client (within 5000 bytes)
			self.data = self.request.recv(5000) # this is equivalent to socket.client.recv(5000)
			print "The Client Sent: ", self.data
			# we echo it back to the client
			self.request.send(self.data)			
		else:
			print "Darn, connection from " + self.client_address + " has closed"




## port needs to be different each time
## aka each slave worker needs a different port to the host IP

IP = "0.0.0.0"	# localhost 
PORT = 9000	# lets start at 9000

# lets first start with 5 workers
for i in range(5):
	print "Creating Slave #: %d"%i
	slave = SlaveThreads(i, IP, PORT, multiThreadServerHandler) # always pass in the slave id first. 
	# increment PORT
	PORT = PORT + 1
	slave.start()
	print "Okay, we are done creating our slave thread number %d, next please ~~~"%i





