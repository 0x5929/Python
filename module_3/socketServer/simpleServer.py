#!/usr/bin/python

# a simple socket server

import socket


# we want to create a tcp  socket
# to do this we call the socket method, we pass two args
	# first arg is the address family, typically AF.INET
	# second arg is the kind of socket we require from a realiablity perspective
	# we will use SOCK_STREAM, because we are using tcp
	# if we were using UDP, we pass in datagram option
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# setting socket setting for bind ip address below to be immedately available to reuse
# if the program is stopped abrubtly
	# setting the socket.sol_socket, and so_reuseaddr option to 1
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# we will have to bind the socket to a known port in the server to listen for a client
	# socket.socket.bind method takes an arg in a tuple form
	# and the tuple needs to have two values or args, ip and port #
tcpSocket.bind(("0.0.0.0", 8000))

# we next will start listening at the specific ip and port binded above for clients
	# we accomplish this by using the listen method
	# listen takes in ONE arg, the number cocurrent client the socket can handle @ a time
tcpSocket.listen(2)

# now that the socket is listening for clients
# we need to call the accept method to start accepting clients
	# the accept method returns a tuple
	# the first element of the tuple is a client side socket
	# which the server will use to speak to a specific client 
	# everytime we call accept method, a client is connected, and a new client socket is created
	# and that is what the server socket will use to speak to that client
	# the second element is a tuple itself consisting of an ip and port number of the client
	# ip of the client and port number of the client's ip used to connect to our service
# by default the accept method is a blocking call, until the client does not come in a connect, 
# accept will just wait, and not return
## the syntax of having a tuple on the left side of assignment is just python magic
# 	essentially meaning:

#	client = tcpSocket.accept()[0]
#	ip     = tcpSocket.accept()[1][0]
#       host   = tcpSocket.accept()[1][1]
# in python you can have multiple variable initalization 
# if on the right side of assignment returns the same amount of
# returned elements
# therefore execution will stop here until a client connects
print "Waiting for a Client to connect......"
(client, (ip, port)) = tcpSocket.accept()

# after a client connects, resumes execution, and prints
print "Received connection from: ", ip

# using the client socket obj to communicate
# to send data to the client
client.send("Hello World from the server socket!!!!!")

# to receive data from the client, takes arg of buffer size
# client.recv(2048) 

print "Starting ECHO output..... "

data = 'dummy'	# dummy data
 
while len(data) : # this loop will receive data from client, and send it back to the client, until connection stops
	data = client.recv(2048)
	print "Client sent: ", data
	client.send(data)

# closing the connection
print "closing connection... "

# first lets close the client object
client.close()

print "Shutting down server...."
# then lets close the server socket obj
tcpSocket.close()

