#!/usr/bin/python

import nmap


# initiating port scanner
nm = nmap.PortScanner()

# scanning local host for port 20-443
results = nm.scan('127.0.0.1', '20-443')

# printing results
print 'printing results\n'
print results
# note we could prettify the results with a custom dictionary handling fucntino

print 'printing command_line method\n'
print nm.command_line()

print 'printing scan info'
print nm.scaninfo()

print 'printing a list of all protocols using all_protocols method on the nm value of key localhost, should expect tcp'
print nm['127.0.0.1'].all_protocols

print 'printing tcp keys, should expect 22'
print nm['127.0.0.1']['tcp']

print 'printing more info on tcp port 22'
print nm['127.0.0.1']['tcp'][22]

# for more examples of automation, please visit the documentation page, and try to automate anything that will take repeatitive steps



