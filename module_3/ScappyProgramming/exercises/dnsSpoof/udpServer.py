#!/usr/bin/python


# udp serer using socket module

import socket

# creating the udp socket
	# using sock datagram for udp for the type of socket we want 
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding the local host ip , and port 53 for dns
udpSocket.bind(("192.168.1.114", 53))

print "STARTING TO WAIT FOR CONNECTIONS"
message, address = udpSocket.recv(5000)


print "*"*50 + " HERE ARE THE INPUT " + "*"*50
print message
print address
print "*"*100

print "shutting down the client"
returnedInfo[0].close()

print "shutting down the socket"
udpSocket.close()



