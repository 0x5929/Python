#!/usr/bin/env python


# importing modules

from pydbg import *
from pydbg.defines import *
import sys



# getting a debugger instance
dbg = pydbg()

# attaching the debugger to our process ID
# which we will take from cmd input

dbg.attach(int(sys.argv[1]))

# defining call back handler function
# this will need the dbg instance as a param, so can analyze with dbg's methods
def detect_overflow(dbg):
    # lets make sure we ignore first chance exceptions
    # since the dbg.run is called after the set_callback function, meaning this will run twice
    # and we will ignore the first one

    if dbg.dbg.u.Exception.dwFirstChance:           # if this is a first chance exception
        return DBG_EXCEPTION_NOT_HANDLED            # IGNORING IT
    print "Access Violation Happened!"
    
    # we can also print the EIP at the moment of the crash
    print "EIP: %0X" % dbg.context.Eip

    # returning out of the function allows execution to continue after the exception
    # obviously the first chance exception will cause any of the programs exception handlers to run
    # second chance happens when the exception is not handled by program
    # returning out of the callback function means that we want to continue our execution after the second chance violation
    # this will crash the program 
    return DBG_EXCEPTION_NOT_HANDLED

# using the set_callback method to set a callback function
# on an exception that we are interested in, and calling the function when callback is invoked
# first param is the exception we are interested in, and the second is the handler
dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, detect_overflow)

# now lets make sure the program is running
# using the run method
dbg.run()
