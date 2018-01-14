#!/usr/bin/python

# this will be the udp client aka victim of the dns spoof attack

# import socket module

import socket
#import time


# create client udp socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# setting a timeout function to 1 second
	# is not necessary so commented out
# clientSocket.settimeout(1)

# setting the address to be my fedora host at dns port 53
num = 1
while num < 10000:
	addr = ("192.168.1.30", 53)
	message = "SPOOF ME POR FAVOR!!!"

	print "SENDING TO FEDORA #%d" %num
	clientSocket.sendto(message, addr)
	num = num + 1

# closing connection
print "closing socket connection"
clientSocket.close()

###################################################################################################################

## ABOVE METHOD WILL ONLY SEND THE A SOCKET PACKET TO THE BINDED ADDRESS AND PORT
## HOWEVER IS NOT A DNS PACKET, UNLESS I PACK IT UP WITH STRUCT AND SEND IT 
## WE ARE NOW GOING TO USE SCAPY TO DO THE TASK ABOVE IN A MUCH SIMPLER WAY


#from scapy.all import *


#DNSpacket = IP()/UDP()/DNS() 






