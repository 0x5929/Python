#!/usr/bin/env python


# importing necessary modules
from pydbg import *
from pydbg.defines import *
import sys
import struct

# global parameters
__DEBUGGER__ = pydbg()

# function definitions
def main():
    usage()
    attach_echoServ()
    try:
        bp = resolve_breakpoint_loc()
        set_breakPoint(bp)
    except:
        # this is when the echo server is not attached, and will generate exception
        msg = 'Did not Successfully set breakpoint'
        error(msg)
        print Exception
        print "[!] Exiting..."
        sys.exit(1)

    __DEBUGGER__.run()

def error(message):
    print "########################################"
    print '\n[!] ERROR: %s\n' % message
    print '########################################'

def usage():
    print '####################################################################'
    print '\n[!] WELCOME TO SEND API MONITOR OF OUR ECHO SERVER, a.exe'
    print '[!] USAGE: Please make sure a.exe aka is running on host'
    print '[!] As this send api monitor would not work if a.exe is not running\n'
    print '####################################################################'

def attach_echoServ():
    for pid, name in __DEBUGGER__.enumerate_processes():
        if name == 'a.exe':
            __DEBUGGER__.attach(pid)

def resolve_breakpoint_loc():
    list_of_bp = []
    bp1 = __DEBUGGER__.func_resolve("ws2_32", "send")
    list_of_bp.append((bp1, send_bp))

    return list_of_bp

def set_breakPoint(bp_list):
    for bp, handler in bp_list:
        __DEBUGGER__.bp_set(bp, description="BREAKPOINT", handler=handler)

def send_bp(__DEBUGGER__):
    # after some testing, the read_process_method in this x86 little endian format processor
    # the method will read upward, meaning from end point to the bytes requested, which is 4
    print_data = []

    print '\n[+] Send has been called!!\n'
    parameters_endloc = get_param_loc()
    
    for arg_loc in parameters_endloc:
        processed_mem = __DEBUGGER__.read_process_memory(arg_loc, 4)
        unpacked_data = struct.unpack('<L', processed_mem)[0]
        print_data.append(unpacked_data) 
    
    stdo(print_data)
    
    return DBG_CONTINUE

def get_param_loc():
    first_arg = __DEBUGGER__.context.Esp + 4
    second_arg = __DEBUGGER__.context.Esp + 8
    third_arg = __DEBUGGER__.context.Esp + 12
    fourth_arg = __DEBUGGER__.context.Esp + 16
    
    return (first_arg, second_arg, third_arg, fourth_arg)

def stdo(datas):
    count = 1

    print "The send function sends data on a connected socket."
    print "\nSyntax:\n"
    print "int send("

    for data in datas:
        if len(str(data)) > 3:          # this is only for the third argument, as the unpacked data is a memory location unlike the others
            data = __DEBUGGER__.smart_dereference(data, print_dots=True, hex_dump=True)
        if count == 1:
            print "_In_     SOCKET s: A descriptor identifiying a connected socket: ", data
        elif count == 2:
            print "_In_ const char *buf: A pointer to a buffer containing the data to be transmitted: ", data
        elif count == 3:        # we had to minus 2 from length to subtract the new line from file descriptor, and null term
            print "_In_       int len: The length in bytes of the data in buffer pointed to by the buf parameter: ", data - 2
        elif count == 4:
            print "_In_       int flags: A set of flags that specify the way which the call is made: ", data

        count = count + 1
    print ");"

# script execution
if __name__ == '__main__':
    main()
    print'[!] Exiting...'
    sys.exit(0)
