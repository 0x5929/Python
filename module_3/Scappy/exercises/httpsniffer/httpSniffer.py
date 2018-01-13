#!/usr/bin/python

# used example code from https://stackoverflow.com/questions/27551367/http-get-packet-sniffer-in-scapy
# first used a general filter, then used a more specific filter to get GET packets
# then we used prn parameter of sniff to print out the packet info
# sophiscated way to print out the info using new line.join and splitting the packet info into lists at new lines,
# and joining again with new lines. REMEMBER using raw string "r" in split method, because we are splitting a raw string, 
# and we wanted to split at the new line\r\n

# importing scapy

from scapy.all import *

# testing if scapy is imported
#ls()

# defining callback functions
def build_lfilter(pkt):	# so this filter will return either true or false for each packet, given the condition
			# we are only interested in packets that after converted to str obj, has the "GET" request
	return "GET" in str(pkt)

# the print function is very compact and interesting, we want to join each element of a tuple with a new line
# note the second element also we are joining each of the output from sprintf method from scappy with a new line
# but first we need to split each of the return carriage, and end of line of the Raw.load of the packet, which its raw packets payload
# and we will split all that into a list, which will join each element with a new line
def get_request_print(pkt):	## NOTE: remember, the r inside split(r"") means the type of string we are splitting, indicating a raw string
	return "\n".join((
			"*"*50 + "GET PACKET" + "*"*=50,
			"\n".join(pkt.sprintf("{Raw:%Raw.load%}").split(r"\r\n")),
			"*"100
		))


# using the sniff function to start sniffing for packets

# first arg, setting the interface we want to sniff with
# second arg, we are using the general filter function, because we only want application http traffic packet
	# which is by transport protocol tcp, and port 80, from our server created in this directory
# third arg is the callback function we will use to build the more specific lfilter argument
	# which is defined above
# fourth arg is another callback function we will use to print the output of the result we want
	# which is also defined above
sniff(
	iface="eth0",
	filter="tcp port 80",
	lfilter=build_lfilter,
	prn=get_request_print
)


