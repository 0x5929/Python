#!/usr/bin/python


# IN THIS SCRIPT, WE LEARNED HOW TO SEND PACKETS TO A DISTANT HOST, AND HOW TO RECEIVE, AND CHANGE UP SCAPY'S ROUTING TABLE IF NECESSARY


# importing the whole scapy library

from scapy.all import *

# in order to create false or forged packets with scapy, you just have to remember
# to create the packet in a protocol header sequence 
# ie. ether()/IP()/TCP()/HTTPOrApplicationData

# in order to create an IP packet, just call the IP() method, with param of destiantion to any ip, or website such as google.com
pkt = IP(dst="google.com")

# in order to send/inject packets, we have two options:
	# layer 2 sending (at IP/ICMP/IGMP/ARP) internet layer
		# we will use spendp(), and need to specify the right interface and have to give an ethernet header yourself for the layer1
	# sending packets at layer 3 (TCP/UDP) tansport layer
		# we will use send() method, routing decided based on local table from your pc, taken care by scapy
		# loop on the same packet? 
		# inter: time interval in seconds?



# we are re directing the pkt variable to another packet, here we will add the icmp protocol header for echo request
# note if you do icmp instead of with IP header before, you dont have dest ip to send the echo request to
# thus, ICMP although lies in the same layer at IP, it is a intergral part of the IP Protocol, it uses services
# of IP to delivery its messagers
# ICMP is usually encapsulated WITHIN an IP datagram

# using sendp layer 2 sending
# HERE WE HAVE IP/ICMP/RAW DATA
pkt = Ether()/IP(dst="google.com")/ICMP()/"kevin was here"
	# first arg is the packet, notice we had to add a Ether() layer
	# second arg is the interface, we have specify with sendp, layer 2 sending
	# third arg is loop, set to 1 if we want to keep sending the packets over and over again, like in a loop
	# fourth arg is inter for time interval in seconds for each loop send a packet 
	# i deleted the third and fourth arg because i dont want the loop to mess up this scripts execution after
print "SENDING PACKETS FROM ETH0"
sendp(pkt, iface="eth0")



# SEND AND RECEIVE PACKETS
	# important to use because the replies can be seen in scapy, and we dont have to use another program like tcpdump to see replies
	# layer 2
		# srp() method, returns answers and unanswered packets
		# srp1() mthod, returns only answered packet
	# layer 3
		# sr() method, returns answers and unanswered packets
		# sr1() mthod, returns only answered packets

# if we were using layer 3, we dont need to add in the etherheader, as scapy will do that for us
# note we added a ttyl for ip header, it states it will travel through 22 routers/switches/bridges or layer 2 of OSI
print "Sending and receving ICMP requets to  google.com, using scapy send and receive at layer 2"
srp1(Ether()/IP(dst="google.com", ttl=22)/ICMP()/"hello world")
print "="*50


print "Sending just IP packet to google.com, using scapy at layer 3, timing out after 3 seconds "
# sending and receiving using layer 3, we dont need a ether header, but just IP packet will never get a reponse, unlike ICMP echo request
# so we need to set a timout param in seconds, of how long to try before getting a resposne
sr1(IP(dst="google.com"), timeout=3)
print "="*50
 

# how to do routing with scapy
	# this is to add the route of any host, to go through the any gateway ip you want
	# this will only change the routing table inside scapy, and will not affect global ip table of your host machine
	# use conf.route.resync() to reset the table to original 
	# all is commented out because we dont need to add to our table, everything we need already exist in the way we want
#conf.route.add(host="192.168.1.114", gw="192.168.1.1")
#conf.route.resync()
















