#!/usr/bin/env python


# importing necessary modules
from pydbg import *
from pydbg.defines import *
import sys
import struct

## NOTE: COULD NOT FIND A WAY TO MONITOR REGISTRY WRITES TO LOGIN AND BOOT
##          THIS SCRIPT IS TO MONITOR SEND, RECV, FILE OPEN AND WRITES A PROGRAM USES

# global parameters
__DEBUGGER__ = pydbg()

# function definitions
#######################################################################################################

def main(pid):
    try:
        __DEBUGGER__.attach(pid)
    except Exception as sys_msg:
        msg = 'Did not Successfully attach pe with given pid'
        error((msg, sys_msg))
        print '\n[!] Exiting...'
        sys.exit(1)
    
    bp = resolve_breakpoint_loc()
    set_breakPoint(bp)

    __DEBUGGER__.run()
#######################################################################################################

def error(messages):
    """
    messages --> (app err, sys err)
    
    """
    print "#######################################################################"
    print '\n[!] APPLICATION ERROR: %s' % messages[0]
    print '\n[!] SYSTEM ERROR: %s\n' % str(messages[1])
    print '#######################################################################'
#######################################################################################################

def usage():
    print '#######################################################################'
    print '\n[!] WELCOME TO API MONITOR'
    print '[!] USAGE: Please make sure the full path of the pe is given as an arg'
    print '[!] EXAMPLE: python fileopenWrite-moniter.py c:\\windows\\notepad.exe'
    print '[!] NOTE: Please remember to use double back slashes in path\n'
    print '#######################################################################'
    print '\n[!] Exiting...'
######################################################################################################

def resolve_breakpoint_loc():
    # returned list
    list_of_bp = []

    # resolving each breakpoint locations
    bp1 = __DEBUGGER__.func_resolve("ws2_32", "send")
    bp2 = __DEBUGGER__.func_resolve("ws2_32", "recv")
    bp3 = __DEBUGGER__.func_resolve("kernel32", "CreateFileA")
    bp4 = __DEBUGGER__.func_resolve("kernel32", "CreateFileW")
    bp5 = __DEBUGGER__.func_resolve("kernel32", "WriteFile")

    # appending to our returned list of bp and handlers
    list_of_bp.append((bp1, send_bp, 'send'))
    list_of_bp.append((bp2, recv_bp, 'recv'))
    list_of_bp.append((bp3, createFileBp, 'CreateFileA'))
    list_of_bp.append((bp4, createFileBp, 'CreateFileW'))
    list_of_bp.append((bp5, writeFileBp, 'WriteFile'))
    
    return list_of_bp
#####################################################################################################

def set_breakPoint(bp_list):
    for bp, handler, name in bp_list:
        try:
            __DEBUGGER__.bp_set(bp, description="breakpoint", handler=handler)
        except Exception as sys_msg:
            err_msg = 'Could not successfully set a breakpoint at: ' + name + ' api function call'
            error((err_msg, sys_msg))
#####################################################################################################

# handler and related function definitions
def send_bp(__DEBUGGER__):
    # after some testing, the read_process_method in this x86 little endian format processor
    # the method will read upward, meaning from end point to the bytes requested, which is 4
    print_data = []

    print '\n~~[+] send api from winsock2_32.dll has been called!!~~\n'
    
    parameter_desc = {
                        '1': 'File descriptor used for transmission',
                        '2': 'Buffer pointer for data to be trasmitted',
                        '3': 'length of buffer',
                        '4': 'additional flags, optional'
                     }

    interested_params = (2, 3)
    parameters_details = get_param_loc(interested_params)
    
    for arg_num, arg_loc in parameters_details:
        processed_mem = __DEBUGGER__.read_process_memory(arg_loc, 4)
        unpacked_data = struct.unpack('<l', processed_mem)[0]
        
        if arg_num == 3:    # if buffer length, we need to minus the null term and new line by file descriptor
            unpacked_data = unpacked_data - 2
      
        if arg_num == 2:    # and we need to dereference our second param since it is a pointer to string buffer
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, True))
        else:
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, False)) 
    
    stdo('SEND_API', print_data)
    
    return DBG_CONTINUE
#########################################################################################################################

def recv_bp(__DEBUGGER__):
    print_data = []

    print '\n~~[+] recv api from winsock2_32.dll has been called!!\n~~'
    
    parameter_desc = {
                        '1': 'File descriptor used for transmission',
                        '2': 'Buffer pointer for data to be trasmitted',
                        '3': 'length of buffer allocated, minus 2 bytes of newline and null term',
                        '4': 'additional flags, optional'
                     }

    interested_params = (3,)
    parameters_details = get_param_loc(interested_params)
   
    # remember how memory is read from low to high in our case 
    for arg_num, arg_loc in parameters_details:
        processed_mem = __DEBUGGER__.read_process_memory(arg_loc, 4)
        unpacked_data = struct.unpack('<l', processed_mem)[0]
        
        if arg_num == 3:    # if buffer length, we need to minus the null term and new line by file descriptor
            unpacked_data = unpacked_data - 2
        
        if arg_num == 2:    # and we need to dereference our second param since it is a pointer to string buffer
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, True))
        else:
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, False))
    
    stdo('RECV API', print_data)
    
    return DBG_CONTINUE
##########################################################################################################################

def createFileBp(__DEBUGGER__):
    print_data = []

    print '\n~~[+] create file api from kernel32.dll has been called!!~~\n'
    
    parameter_desc = {
                        '1': 'Pointer to file name',
                        '2': 'Desired access',
                        '3': 'share mode',
                        '4': 'security attributes , optional'
                     }

    interested_params = (1, )
    parameters_details = get_param_loc(interested_params)
   
    # remember how memory is read from low to high in our case 
    for arg_num, arg_loc in parameters_details:
        processed_mem = __DEBUGGER__.read_process_memory(arg_loc, 4)
        unpacked_data = struct.unpack('<l', processed_mem)[0]
        
        if arg_num == 1:    # and we need to dereference our first param since it is a pointer to string buffer
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, True))
        else:
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, False)) 
    
    stdo('CREATEFILE API', print_data)
    
    return DBG_CONTINUE
################################################################################################################################

def writeFileBp(__DEBUGGER__):
    print_data = []

    print '\n~~[+]writeFile api from kernel32.dll has been called!!~~\n'
    
    parameter_desc = {
                        '1': 'handle to file or I/O device',
                        '2': 'buffer to be written',
                        '3': 'length of buffer in bytes to write',
                        '4': 'a pointer to an overlapped structure'
                     }

    interested_params = (2, 3)
    parameters_details = get_param_loc(interested_params)
   
    # remember how memory is read from low to high in our case 
    for arg_num, arg_loc in parameters_details:
        processed_mem = __DEBUGGER__.read_process_memory(arg_loc, 4)
        unpacked_data = struct.unpack('<l', processed_mem)[0]
        
        if arg_num == 3:    # if buffer length, we need to minus the null term and new line by file descriptor
            unpacked_data = unpacked_data - 2
        
        if arg_num == 2:    # and we need to dereference our second param since it is a pointer to string buffer
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, True))
        else:
            print_data.append((parameter_desc[str(arg_num)], unpacked_data, False)) 
    
    stdo('WRITEFILE API', print_data)
    
    return DBG_CONTINUE
######################################################################################################################

def get_param_loc(params):

    """
    We can get up to 4 paramters of interested function
    params type: tuple
    params description: each element is the number of the arg wanted

    return type: list of tuples 
    return description: each element is the number of arg and the location of the arg wanted

    """

    return_params = []

    first_arg = __DEBUGGER__.context.Esp + 4
    second_arg = __DEBUGGER__.context.Esp + 8
    third_arg = __DEBUGGER__.context.Esp + 12
    fourth_arg = __DEBUGGER__.context.Esp + 16
    
    for paramWanted in params:
        if paramWanted == 1:
            return_params.append((1, first_arg))
        elif paramWanted == 2:
            return_params.append((2, second_arg))
        elif paramWanted == 3:
            return_params.append((3, third_arg))
        elif paramWanted == 4:
            return_params.append((4, fourth_arg))

    return return_params
#####################################################################################################

def stdo(title, datas):
    """
    prints to standard output
    
    title type: string
    title description: the title of the output data
    datas type: list of tuples
    datas description: list of data, descriptions to be evaluated/printed, passed in from bp handler functions
    
    return type: none
    return description: writes to standard output

    """

    print "\n===================================================="
    print '\n[+] ' + title + '\n'

    for desc, data, evaluate in datas:
        if evaluate:          # this is only for the data that needs to be dereferenced
            data = __DEBUGGER__.smart_dereference(data, print_dots=True, hex_dump=True)

        print "[+] Description: " + desc + ' Data: ', data
    print "====================================================\n"

###############################################################################################################################################

# script execution
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        print '\n[!] Exiting...'
        sys.exit(1)
    try: 
        pid = int(sys.argv[1])
    except:
        usage()
        print '\n[!] Exiting...'
        sys.exit(1)
    main(pid)
    print'[!] Exiting...'
    sys.exit(0)
