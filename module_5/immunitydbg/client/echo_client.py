#!/usr/bin/python


# importing modules
import socket           # for socket programming
import sys              # needed for sys.exit



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("192.168.1.81", 22000))

buf = "A" * 20

sock.send(buf)

ech_re = sock.recv(1024)

print ech_re

#sock.close()
