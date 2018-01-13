#!/usr/bin/python


# this will be a sniffer that will sniff out all the local ap ssid using scapy


# used example code from http://hackoftheday.securitytube.net/2013/03/wi-fi-sniffer-in-10-lines-of-python.html


# importing scapy

from scapy.all import *

# defining a list of APs, so we dont print out the same ssid
ap_list = []

# the packet handler will filter through packets that has layer of Dot11 which is 802.11, which is set of wifi standard or protocols
# then we futhur filter through the packets, and if the packet has type 0, meaning network management packets
# AND if they have the subtype of 8, which is beacon frame, which tells clients that AP exist, which is exactly what we want
# and we if havent seen the packet before, we will put the packet into the ap_list, and print out its info
def packetHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                return "AP MAC: %s with SSID %s " %(pkt.addr2, pkt.info)



# utilizing the sniff method of scapy
# every packet sniffed will go through the packethandler to be outputted on stdout on terminal screen
# we will bind the iface here, instead of changing it like the interactive shell, via conf.iface
sniff(iface="wlp0s20u9u2", prn=packetHandler)

