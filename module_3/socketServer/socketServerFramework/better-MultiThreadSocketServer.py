#!/usr/bin/python

## multi-thread socket TCP server


import threading
import SocketServer



# creating TCP Server Handler Class
	# this class is created so we can modify each request handle, and do what we want with it, 
	# in our case, we are setting it up to be an echo server
class ThreadedServerRequestHandler(SocketServer.BaseRequestHandler):
	# the handle function comes with .request same as socket.client, 
	# and .client_address -> socket.ip from socket module	
	def handle(self):
		data = "dummy"
		while len(data):
			print "Receiving data from client: ", self.client_address
			data = self.request.recv(1024) # capped at 1kb
			print "Client Sent: ", data
			# echoing data back to client
			print "Back at ya buddy!"
			self.request.send(data)
		else:
			print "lost connection from: ", self.client_address


# creating SocketServer Class
	# this class needs to inherit from SocketSErver.ThreadingMixIn to handle threading per request
	# also inheriting the TCP Server object
class SimpleTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): 

#	def __init__ (self, address, handler):
		# setting up options for the server
#		SocketServer.ThreadingMixIn.daemon_threads = True
#		SocketServer.BaseServer.allow_reuse_address = True
#		print """Getting ready to start the TCP Server, listening at
#				IP: %s
#				PORT: %d"""%(address[0], address[1])
# calling this thread class from outside will call the __init__ contructor with args passed in
# these arg are used to call TCPServer Class, and invoking its contstuctor with __init__, this way
# we can pass in the arg passed in from the outside call along with the self instance
#		SocketServer.TCPServer.__init__(self, address, handler) 

# just using pass works because this class inheirts from TCPServer, and its constructor __init__ is automattically
# invoked when called from outside
	pass



# initializing server
	# if this is the main program running
	# and not being export to run in another program
	# run this :
if __name__ == "__main__":
	address = ("0.0.0.0", 9000)	# addr to be a tuple of localhost ip on port 9000
	server = SimpleTCPServer(address, ThreadedServerRequestHandler)
	# allow reusable ip
#	server.allow_reuse_address = True
# creating threads
	# calling the threading.Thread class directly
	# this way we dont need to create our own custom thread class
	# with custom run method
	# and to initiate threadin.Thread with self instance
	# since we can just use target=objectTobeRanWithEachThread
	# and now this will  give you a thread 
	# with server.serve_forever obj's functionality for each thread
	# essientially as if we had our own custom thread class(inherits from threading.thread)
	# calling that class with attributes to be initialized in __init__ function
	# and to invoke run in the run() by calling thread.start()
	# so we skip all that, because we already know what each thread should run with
	# and that is serve_forever obj's functionality, not needing any other attr for the thread
	threadedServer = threading.Thread(target=server.serve_forever())
	print "THIS SHOULD NEVER PRINT"















