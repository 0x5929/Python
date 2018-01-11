#!/usr/bin/python

import socket
import struct


#creating raw socket
raw = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))

# remember rawSocket.bind method takes the arg in tuple form
raw.bind(("eth0",socket.htons(0x0806)))

# NOTE: '/x' is the escape sequence telling python the subsequent characters are to be interpreted as hex digits
# and each hex digit is 1 byte
# please use cs.nyu.edu/courses/fall98/G22.2262-001/class9.html for reference
# ARP PACKET STRUCTURE
# bytes:   2 	         2 	     1	             1 	              2		    6	      4	      6	      4
# -----------------------------------------------------------------------------------------------------------------
# Hardware          | Protocol   | Hardware      |Protocol      | operation      | sender  | sender| target| target| 
#  type  	    | type       | address       |Address       |0001 for request| Ether   | IP    |  ether| IP    |
# 0011 for ethernet |0800 for IP |  size         | size         |0002 for reply  | Address | Addr  | addr  | addr  |
#		    |		 |06 is standard |04 is standard|                |         |       |       |       |
#-------------------------------------------------------------------------------------------------------------------
#

hardwareType = '\x00\x01'
protocolType = '\x08\x00'
hardwareSize = '\x06'
protocolSize = '\x04'
operation = '\x00\x01'

first8Bytes = hardwareType + protocolType + protocolSize + operation

senderHardAddr = '\xaa\xaa\xaa\xaa\xaa\xaa'
destHardAddr = '\x00\x00\x00\x00\x00\x00'	# because we dont know what the destination hard addr is, that is what arp is for
						# aka to translate ip to hardware
senderProtocolAddr = '\xc0\xa8\x01\x72'
destProtocolAddr = '\xc0\xa8\x01\x53'
packet = struct.pack("!8s6s4s6s4s", first8Bytes, senderHardAddr, senderProtocolAddr, destHardAddr, destProtocolAddr)

# injecting packet with string
raw.send(packet + 'ARP SENT')






