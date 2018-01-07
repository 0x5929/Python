#!/usr/bin/python



# import modules

import socket
import struct
import binascii


# first we need to create a websever for us to connect to

# we need to run both this script % ./webServer.py to get this to work


# creating raw socket

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))


while True: 
# 5kB  packet

	pkt = rawSocket.recvfrom(5000)


# if the tcp header destination port is 80
# or source port is 80, then we do data dump

	tcpHeader = pkt[0][34:54]

	tcp_hdr = struct.unpack("!HH16s", tcpHeader)

	if (tcp_hdr[0] == 80 or tcp_hdr[1] == 80):
	# do the data dump
		# ethernet header
		ethHeader = pkt[0][0:14]
		eth_hdr = struct.unpack("!6s6s2s", ethHeader)
		destMAC = binascii.hexlify(eth_hdr[0])	
		sourceMAC = binascii.hexlify(eth_hdr[1])
		EthType = binascii.hexlify(eth_hdr[2])
		print """
			The Destination MAC Address: %s
			The Source MAC Address: %s
			The Ethernet type: %s
			NOTE: 0800 means IP Type 
			"""%(destMAC, sourceMAC, EthType)
		# ip header
		ipHeader = pkt[0][14:34]
		ip_hdr = struct.unpack("!12s4s4s", ipHeader)
		sourceIP = socket.inet_ntoa(ip_hdr[1])	
		destIP = socket.inet_ntoa(ip_hdr[2])
		print """
			The Destination IP Address: %s
			The Source IP Address: %s	
			"""%(destIP, sourceIP)
			# TCP Data
		print "========================================================"
		sourcePORT = tcp_hdr[0]
		destinationPORT = tcp_hdr[1]
		print """
			Destination Port: %d
			Source Port: %d
			"""%(destinationPORT, sourcePORT)
		print 'DATA:'
		print "#############################"
		data = pkt[0][58:62]
		if data:
			unpackedData = struct.unpack("!4c", data)
			print unpackedData 
		else:
			print "THERE IS NO DATA IN THIS HTTP REQUEST" 






