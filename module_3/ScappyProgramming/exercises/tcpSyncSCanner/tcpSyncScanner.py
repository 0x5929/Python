#!/usr/bin/python


# this script will act as a syn scanner for tcp ports, and will do so silently
# by sending a reset flag after being notifed that the port is open, so the connection will be closed
# and not logged
# referenced using https://null-byte.wonderhowto.com/how-to/build-stealth-port-scanner-with-scapy-and-python-0164779/

# importing necessary modules

import sys			# for shutting down the script, or giving bash cmds in script
from datetime import datetime	# for datetime.now() function
from time import strftime	# for strftime() function to format time into a string we want
from scapy.all import *		# importing the scapy lib

# importing development and testing module
#import traceback

##################################	USER INPUT	###################################

# for testing purpose
#targetIP = "192.168.1.30"
#min_port = 25
#max_port = 25

try: 
	targetIP = raw_input("[*] Please Enter the Target IP Address for the Scan: ")
	min_port = raw_input("[*] Please Enter the Minimum Port to be Scanned: ")
	max_port = raw_input("[*] Please Enter the Maximum Port to be Scanned: ")
	# we have to test the user input
	try: 
		if int(min_port) >= 0 and int(max_port) >= 0 and int(max_port >= int(min_port)):
			# all three conditions need to be met
			pass
		else:	# if not we will shutdown the script
			print "\n[!] Invalid Range of Ports"
			print "[!] Exiting....."
			sys.exit(1)
	except Exception:
		print "\n[!] Invalid Range of Ports, err coming from outside of the if block"
		print "[!] Exiting....."
		sys.exit(1)
	pass
except KeyboardInterrupt:
	print "\n[!] User Has Requested Shutdown...."
	print "[!] Exiting..."
	sys.exit(1)

#####################################################################################################

####################################	 SETTING CONSTANTS	#######################################

# the range of ports needs to be inclusive at the end
ports = range(int(min_port), int(max_port) + 1)
# starting clock using datetime.now func
startingClock = datetime.now()
# setting hex values for the flags we need\
	# really we would only need the synack flag to test against later on
SYNACK = 0x12
RSTACK = 0x14

#######################################################################################################



#################################	FUNCTION DEFINITION	#######################################

# defining the check host function
	# used to see if host IP is up
def checkHost(ip):
	# we are going to check by pinping the host
	conf.verb = 0
	try: # by using the layer 3 send and receive for 1 answer packet name ping
		ping = sr1(IP(dst=ip)/ICMP())
		print "\n[*] Target IP is Up. Starting the Scan Now ~~~"
	except Exception:
		traceback.print_exc()
		print "\n[!] Could not Resolve Target IP"
		print "[!] Exiting...."
		sys.exit(1)

# defining the scan port function
	# responsible for all the port scanning logic
def portScanner(port):
	# randomly choosing a source port from scapy for the sr1 function
	srcPort = RandShort()
	conf.verb = 0	# setting verbose to 0, so unnesscary info wont output
	# the syn packet with the flag for tcp to be S for syn for synchronize
		# this will ask the server if the port is open depending on answer
	SYNPkt = IP(dst=targetIP)/TCP(sport=srcPort, dport=port, flags="S")
        print "THIS IS THE SYN PKT: ", SYNPkt
        SYNACKPkt = sr1(SYNPkt)
	print "THIS IS THE SYNACK PKT", SYNACKPkt
        responseFlag = SYNACKPkt.getlayer(TCP).flags # setting the response packet flag to a variable
	# lets test for the flag, and see if ports are open
        print "this is the response flag", responseFlag
	if responseFlag == SYNACK:	# constant hex set earlier this script
		return True
	else:
		return False
	# after test, no matter whether port is open or closed, we will send a RST for RESET
	# to the server, this way they will not log connection if the port is open
	RSTPkt = IP(dst=targetIP)/TCP(sport=srcPort, dport=port, flags="R")
	# sending the RSTPkt, note there will not be an anticipated response for this flag tcp packet
	send(RSTPkt)

######################################################################################################



######################################	RUNNING SCRIPT	##########################################
	
# running script as the main script and not as a dependency
if __name__ == "__main__":
	#checking if host is up and alive
	checkHost(targetIP)
	print "Scanning Start at " + strftime("%H:%M:%S") + "!! \n"	# using the format time string func
	for port in ports:
		status = portScanner(port)	# port scanner will return true or false, for open/close ports
		if status == True:
			print "Port " + str(port) + " is open!"
		else:
			print "Port " + str(port) + " is closed :("
	stopClock = datetime.now()
	totalTime = stopClock - startingClock
	print "\n[*] Scan Finished"
	print "[*] Total Scan Duration: " + str(totalTime)


###################################################################################################




























