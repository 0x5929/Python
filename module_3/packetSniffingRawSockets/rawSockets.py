#!/usr/bin/python

# raw sockets, NOTE: REMEMBER, YOU NEED TO BE ROOT TO CREATE RAW SOCKETS
# EXERCISE: FIND OUT HOW TO GRANT A NON ROOT USER TO CREATE RAW SOCKETS
# so for now, we need to run this py script as root user by using sudo cmd

# using raw sockets will be a shortcut and bypasses most of the layers in OSI model
# raw sockets will be inserted at the layer two, and it will bypass the rest

# struct module is to help unpack the binary data  packet from rawSocket
# struct can pack and unpack data to its necessary pack format
# for networking, the format or Network Byte Order is Big-Endian, represented by "!" first
# stuct.unpack => into tuple form
import socket
import struct
import binascii

# SIDE NOTE:
	# there is 8 bits in 1 byte of data
	# each of the packet header specifications is 32 bits across, so four bytes across
	# Ethernet header is 14 bytes, first 6 is the destination mac, and next 6 bytes is the source mac
	# and the last 2 bytes are the ethernet type, 0800 for IP protocol type ethernet

	# the ip packet, we are interested in the first its total 20 bytes without options, and 24 bytes with options
	# according to diagram, first 12 bytes contain version, type of service, identification, time to live, protoc
	# headerchecks.....
	# the 13th byte to the 16th byte is the souce ip, and 17th byte to the 20th byte is the destination ip 	


# create raw socket with PF_PACKET
	# first arg states we are using the packet interface
	# second arg states that we want raw sockets
	# third arg states that the protocol we want, 0x0800 is the IP protocol
	# find out the protocol number by cat /usr/include/linux/if_ether.h file 
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

# recieving and read a packet
pkt = rawSocket.recvfrom(2048) #limits to 2 kB per socket
# this will return a tuple to us, where the first value is the raw packet we are interested in


# ethernet header of packet
# fixed size of 14 bytes of the first part of the packet tuple
# the way we get first 14 bytes of a string is [0:14] in python, interesting...
ethernetHeader = pkt[0][0:14]

# unpack it using struct, we want the first 6 bytes of dest mac address
# second 6 bytes of the source mac address
# last two bytes of the eth type
# all using big-endian network byte order form
eth_hdr = struct.unpack("!6s6s2s", ethernetHeader)
# this will still spit out the bytes in tuple form

# using hexlify on each of the values, and it prints out the final hex form of each value
destMac = binascii.hexlify(eth_hdr[0])

sourceMac = binascii.hexlify(eth_hdr[1])

etherType = binascii.hexlify(eth_hdr[2]) # for IP protocl from before, 0800

print "Destination Mac: " + destMac
print "Source Mac: " + sourceMac
print "Ethernet Type: " + etherType + " if it is 0800 it means IP Protocol Ethernet"

# ip header of packet next 20 bytes if no options
# first 12 bytes are identification, To to live, protocol, not what we want
# we want the following 2 4bytes info, which is the dest ip, and source ip
ipHeader = pkt[0][14:34]

ip_hdr = struct.unpack("!12s4s4s", ipHeader)

# using the socket.inet_nta function, we can convert the byte form into human readable ip form
print "Source IP address: " + socket.inet_ntoa(ip_hdr[1])

print "Destination IP address: " + socket.inet_ntoa(ip_hdr[2])

# initial part of the tcp header of the packet

tcpHeader = pkt[0][34:54]

tcp_hdr = struct.unpack("!HH16s", tcpHeader)

# first 2 bytes is the source port, and second 2 bytes is the dest port
print "tcp_hdr: ", tcp_hdr
print "tcp source port: ", tcp_hdr[0]
print "tcp destination port: ", tcp_hdr[1]
 

# please read up on packet headers, and understanding all fields.



