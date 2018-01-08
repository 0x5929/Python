#!/usr/bin/python



# packet injection with raw sockets
# if you can inject random data into the network, you know you can then send anything

import socket
import struct

# creating a raw socket using the socket module
# we use the PF_PACKET address family, and SOCK_RAW as the socket type, given the ip protocol field
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

# remember when we are sniffing from packet we used: rawSocket.recvfrom(byteSize)
# BUT for packet injection we will use rawSocket.bind method
# binding the interface that we want to inject with
# and the type of protocol we want our injection to be
rawSocket.bind(("eth0", socket.htons(0x0800)))

# then we will create simple ethernet packet
# this should be the ethernet header, with destMAC, sourceMAC, and ethernet type
# using the struct.pack api, this will pack up according to given format in the first arg, and subsequent arg for each of the 
# format mentioned in the format arg
packet = struct.pack("!6s6s2s", '\xaa\xaa\xaa\xaa\xaa\xaa', '\xbb\xbb\xbb\xbb\xbb\xbb', '\x08\x00')

# injecting the packet with a random string data inside
rawSocket.send(packet + "Hello There")



