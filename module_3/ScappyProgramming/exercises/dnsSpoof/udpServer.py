#!/usr/bin/python


# udp serer using socket module

import socket

# creating the udp socket
	# using sock datagram for udp for the type of socket we want 
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# allowing reusable address, good for quick rebinding
udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding the local loopback host ip , and port 53 for dns
udpSocket.bind(('', 53))

while True:
    print "STARTING TO WAIT FOR CONNECTIONS"
    message, address = udpSocket.recvfrom(512) # the method call is recvfrom


    print "*"*50 + " HERE IS THE SPOOFED PACKET " + "*"*50
    print message
    print address
    print "*"*100
    break

print "shutting down the client"

print "shutting down the socket"
udpSocket.close()



