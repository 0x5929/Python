#!/usr/bin/python


# importing modules
import socket           # for socket programming
import sys              # needed for sys.exit



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("192.168.1.81", 22000))

buf = "A" * 20


try:
    while (1):                              # infinite loop to keep sending bigger size buffers
        sock.send(buf)
        ech_re = sock.recv(1024)
        print ech_re + "\n"
        buf = buf * 2                       # incrementing the buff by x2 every loop        
except KeyboardInterrupt:
    print "\n[!] User requested shutdown..."
    sock.close()
    sys.exit(0)
