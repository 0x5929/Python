#!/usr/bin/python

from scapy.all import *

# finding protolcols and details

ls()
ls(IP)

IP().show()


# sniffing packets
	# we will use the sniff method, with first arg is the interface, and second arg as the amount  of pkts we want to sniff
	# sniff is a blocking call, and only return after sniffing the 3 packets we requested
pkts = sniff(iface="eth0", count=3)
print "pkts will be in list form"
print pkts
print "FIRST PACKET:"
print pkts[0]
print "=================================================================================================="
print 'SECOND PACKET:'
print pkts[1]
print "==================================================================================================="
print 'THIRD PACKET:'
print pkts[2]
print "===================================================================================================" 


print 'FOR BEAUTIFUL FORMATED OUTPUTS, USE PACKET.SHOW()'
print "FIRST PACKET:"
pkts[0].show()
print "==================================================================================================="
# if we wanted to show the hex format of the packet, we can use the hexdump method with the arg as the packet
print "SHOWING THE HEX FORMAT OF THE SECOND PACKET USING hexdump(packet) method"
hexdump(pkts[1])
print "===================================================================================================="


# if we wanted to write packets to a pcap file to be read and analyzed later we can use the wrpcap function...
	# first arg is the name of the pcap file, note it will be in .cap format, and second arg is the packets we want to write it to such as:
wrpcap("demo.cap", pkts)

# and to read from a certain pcap file, we use the rdpcap method with its only arg is the file name of the .cap file
# NOTE: the readpackets will be exactly the same form as pkts
print "reading from pcap file: demo.cap..."
readPackets = rdpcap("demo.cap")
print readPackets
print "==================================================================================================="
  

# adding filters to the packets we want to filter, this is very powerful
	# so this sniff method takes in another arg of the filter, we only want arp packets
arpPkts = sniff(iface="eth0", filter="arp", count=3)


# print packets as they come in, this is for if we dont want to post processing of these pkts
	# we can use the lambda function with the sniff method, as another arg of the method
	# in this particular example, we are printing the summary of the packets onto the stdout of terminal
	# for each packet x, we are printing summary() method
	# we could have used prn=lambda x: x.show() for a nicely formatted output
	# usually we can up the count to like 20 or 30, but since its a script and i want it to finish execution 
	# i changed it back to 5
icmpPkts = sniff(iface="eth0", filter="icmp", count=5, prn=lambda x: x.summary())
print "=========================================================================================================="
print "finished with on the spot printing of icmp packets using sniff of scapy..."
## NOTE: scapy will take out the hardcode aspect of rawsocket packet sniffing, so we can just worry about the sniff/anazlysis part


# convert packet as a string
stringPacket = str(pkts[0])
print "STRING PACKET: "
print stringPacket
print "=================================================================================================="

# to reconstruct a packet from string to packet format, we need to know the string formatted packet's most outtermost protocol
	# for us its the ethernet header (pretty much always)
	# so we call from the scapy library, Ether(pkt) this will convert the string pkt pkt to its original  packet form
	# scapy will do all the work underneath
convertedBackPkt = Ether(stringPacket)

print "CONVERTED BACK TO PACKET FORMAT:"
print convertedBackPkt
print "================================================================================================"


## we can export a packet as Base64 encode
	# first we need to convert packet into a string by str func
	# then we can use the export_object function
	# this will give you a base64 encoded output in the stdout terminal
export_object(str(pkts[0]))

## we can also import a packet from Base64, and this will wait for an input on the stdin terminal
	# we can copy and paste the base64 encoded string from above
	# and hit control D, to return execution, and check out newPkt
	# would work if we are in the interactive shell, other wise it wont, so i commented it out
	# becaues it is a blocking call, and it waits for a import basecode 64 str obj to return to execution 
	# so i commented the rest out
#newPkt = import_object()

#print "THE NEW PACKET WE IMPORTED FROM EARLIER: "
#print newPkt
#print "================================================================================================="
#print "RECONSTRUCTING IT USING ITS OUTTERMOST PROTOCOL: ether"
#Ether(newPkt)
#print "================================================================================================"




 



