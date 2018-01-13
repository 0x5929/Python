#!/usr/bin/python

# this script will be a subnet scanner using the scapy library
# this script will not work in a virtual enviromnment, but will work on the host machine

from scapy.all import *


	# we know the destination ip and mac, we just want to get a response of my source ip and mac
	# sending and recieving through layer 2, since we already added a ether header layer in the arp request packet
	# we want it to time out after 1 second, and we dont want the verbose output(default its true or on or 1), just what we want to print 
	# ff:ff:ff:ff:ff:ff is the broadcash mac address in a network on the hardware lvl
	# we could have also just used scapy's default hwaddress, and not given an input
for num in range(0,256): # more specifically we want the loop to go to 192.168.1.1(MyAsusRouter), 192.168.1.30(MyFedora), 192.168.1.114(MyUbuntu)
	ip = "192.168.1." + str(num)
	arpReq = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
	arpRes = srp1(arpReq, timeout=1, verbose=0)
	if arpRes:
		print "IP: " + arpRes.psrc + " MAC: " + arpRes.hwsrc

# so when there is a response, the reponse souce mac and ip is the ones we want, and we are the destination now


