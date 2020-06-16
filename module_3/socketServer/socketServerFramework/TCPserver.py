#!/usr/bin/python

## TCP server using SocketServer Framework

import SocketServer


# your custom class has to inherit from the framework's baseRequestHandler to handle requests
# note in this class we dont have the constructor __init__, this is not required if we dont have 
# anything to do in the beginning, other than passing this whole class as a handler to another method as an arg
class EchoServerHandler(SocketServer.BaseRequestHandler):
	# we want to override the handle call
	def handle(self): # this is where all the requests are routed and handled, very important func
		print "Got Connection from: ", self.client_address
		data = 'dummy'

		while len(data):
			# self.request = socket.client, so we can call recv or send on it
			data = self.request.recv(1024)	# this is what is received from  the request  client
			print "The Client Sent: " + data
			self.request.send(data)	# and the server will send the data back to the client aka echo
		else: # if there are no more client data
			print "AWWWW..... The Client Left!!"

serverAddr = ("0.0.0.0", 9000)	# tuple form, localhost ip, and port 9000

print "THE SOCKETSERVER IS LISTENING ON: 192.168.1.114 PORT 9000, come thru with connections ~~~~"

# creating the TCP Server
# using the socketServer framework, and specifying a TCP Server
# first argument is a tuple that has the server info: IP and PORT
# second arugment needs to be a class/object that inherits from the framework's
# baseRequestHandler, so the second arg is a handler obj
server = SocketServer.TCPServer(serverAddr, EchoServerHandler)

# letting the server run and serve forever by invoking method
server.serve_forever()

