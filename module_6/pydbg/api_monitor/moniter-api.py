#!/usr/bin/env python


from pydbg import *
from pydbg.defines import *
import sys


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
    print dbg.dump_context(dbg.context)
    
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

