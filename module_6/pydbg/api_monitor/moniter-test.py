#!/usr/bin/env python


from pydbg import *
from pydbg.defines import *
import sys
import struct


# initializing debugger
dbg = pydbg()

# using the enumerate_process method to dump all the running process atm
for pid, name in dbg.enumerate_processes():
    print "============================="
    print pid, name 
    
    # we can also check if name matches the process we want 
    # and attach to it, this is if we dont want to load it with a full path
    if name == 'a.exe':
        dbg.attach(pid)



##NOTE: a.exe is strcpy-server.exe
##      lets moniter every send functions api calls in the server aka a.exe


# breakpoint callback function
def send_bp(dbg):
    # we are inspecting the program at the bp with this function
    print "Send() called!!"

    # now we can dump all the context at this moment using dump_context method
    # passing in what we want to dump, which is our context
    print dbg.dump_context(dbg.context, stack_depth=10)

    ## TESTING: 
        # first step is to processing the memory in reference to esp
            # right when the function is called, the convention is to have the caller function
            # set up and push all the arguments, and pushing the the current eip which is the return address
            # then jump to the function being called, while pushing, esp is incremented by assembly
        # second step is to unpack the processed memory data with format of little endian, and unsigned long
            # little endian since we are using x86 in win7
            # unsigned long is a regular 4 byte number which is what the processed memory data could be stored in
        # third step is to dereference the unpacked data, in order to find the string value of the data

    # first step
    ret_addr_startLoc = dbg.context.Esp
    processed_mem = dbg.read_process_memory(ret_addr_startLoc, 4)

    # second step
    unpacked_process_mem = struct.unpack('<L', processed_mem)
    print 'for testing purposes, lets see what the list look like'
    print "THIS IS WHAT UNPACK LIST: ", unpacked_process_mem

    # third step
    string = dbg.smart_dereference(unpacked_process_mem[0], print_dots=True, hex_dump=True)

    print "HELLO WORLD RETURN ADDRESS: %s" %string

    # now repeating the above steps
    # first step
    first_arg_startLoc = dbg.context.Esp + 4
    processed_mem = dbg.read_process_memory(first_arg_startLoc, 4)

    # second step
    unpacked_process_mem = struct.unpack('<L', processed_mem)
    print 'for testing purposes, lets see what the list look like'
    print "THIS IS WHAT UNPACK LIST: ", unpacked_process_mem

    # third step
    string = dbg.smart_dereference(unpacked_process_mem[0], print_dots=True, hex_dump=True)

    print "HELLO WORLD FIRST ARGUMENT:  %d" %string
    
    # first step
    second_arg_startLoc = dbg.context.Esp + 8
    processed_mem = dbg.read_process_memory(second_arg_startLoc, 4)

    # second step
    unpacked_process_mem = struct.unpack('<L', processed_mem)
    print 'for testing purposes, lets see what the list look like'
    print "THIS IS WHAT UNPACK LIST: ", unpacked_process_mem

    # third step
    string = dbg.smart_dereference(unpacked_process_mem[0], print_dots=True, hex_dump=True)

    print "HELLO WORLD SECOND ARGUMENT: %s" %string
    
    # first step
    third_arg_startLoc = dbg.context.Esp + 12
    processed_mem = dbg.read_process_memory(third_arg_startLoc, 4)

    # second step
    unpacked_process_mem = struct.unpack('<L', processed_mem)
    print 'for testing purposes, lets see what the list look like'
    print "THIS IS WHAT UNPACK LIST: ", unpacked_process_mem

    # third step
    string = dbg.smart_dereference(unpacked_process_mem[0], print_dots=True, hex_dump=True)

    print "HELLO WORLD THIRD ARGUMENT: %d" %string
    
    # first step
    fourth_arg_startLoc = dbg.context.Esp + 16
    processed_mem = dbg.read_process_memory(fourth_arg_startLoc, 4)

    # second step
    unpacked_process_mem = struct.unpack('<L', processed_mem)
    print 'for testing purposes, lets see what the list look like'
    print "THIS IS WHAT UNPACK LIST: ", unpacked_process_mem

    # third step
    string = dbg.smart_dereference(unpacked_process_mem[0], print_dots=True, hex_dump=True)

    print "HELLO WORLD FOURTH ARGUMENT: %d" %string


    # we dont want to obstruct the program from doing anything, so lets just continue the program
    # after we are done with what we need at each breakpoint

    return DBG_CONTINUE



# first we need to resolve the function name to an actual address in the program memory
# second we need to set a break point at those addresses
# third we need to analyze the program at those breakpoints

# first step: using func_resolv method
#             this will require some background knowledge of in which dll 
#             does the function reside, for our case the socket send method is in ws2_32.dll aka winsock2 library
# first param is the dll name w/o extension
# second param is the function name, send note, we could have also put recv if we wanted to intercept recv api calls
send_api_addr = dbg.func_resolve("ws2_32", "send")


# second step: setting the breakpoint using bp_set method
# first param is the memory address of the breakpoint
# second param is the description of the program 
# third param is the handler call back function for the breakpoint
dbg.bp_set(send_api_addr, description="BP on Send in WS2", handler=send_bp)

# running the program
dbg.run()

