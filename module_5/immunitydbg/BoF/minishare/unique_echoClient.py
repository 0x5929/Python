#!/usr/bin/python


# importing necessary modules
import sys
import argparse
import socket

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
    string = 'GET '
    for i in range(len(upper_alpha)):
        for j in range(len(lower_alpha)):
            for k in range(len(digits)):
                string = string + upper_alpha[i] + lower_alpha[j] + digits[k]

    print "The string sent to echo server at %s, port: %d is: %s" %(ip, port, string[:size])
    string = string[:size]
    string = string + ' HTTP/1.1\r\n\r\n'
    return string
    

def socket_setup((ip, port, size)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP socket
    s.connect((ip, port))
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
