#!/usr/bin/python


# importing modules
import socket           # for socket programming
import sys              # needed for sys.exit



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("192.168.1.86", 22000))

buf = "A" * 300
sock.send(buf)
print sock.recv(1024)

# for incremental buffers, uncomment
#try:
#    while (1):                              # infinite loop to keep sending bigger size buffers
#        sock.send(buf)
#        print 'jello world'
#        ech_re = sock.recv(1024)
#        print ech_re + "\n"
#        buf = buf * 2                       # incrementing the buff by x2 every loop        
#except KeyboardInterrupt:
#    print "\n[!] User requested shutdown..."
#    sock.close()
#
#    sys.exit(0)
while 1:
    pass
