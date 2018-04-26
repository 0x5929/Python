#!/usr/bin/env python


# importing modules

from pydbg import *
from pydbg.defines import *
import utils                                                # to analyze and print crash reports
import sys
import time


# global definitions
__DEBUGGER__ = pydbg()

# function definitions
def main(path):

    debugger_setup(path)


def debugger_setup(path):
    
    try:    # using load method to load our path to exe
        __DEBUGGER__.load(path)
    except:
        err_msg = '\n[+] Could not properly load the given path, please ensure path to exe is correct'
        loc = 'FUNCTION: debugger_generation'
        error(err_msg, loc)
        sys.exit(1)
    
    __DEBUGGER__.set_callback(EXCEPTION_ACCESS_VIOLATION, overflow_detector)
    
    __DEBUGGER__.run()


def overflow_detector(__DEBUGGER__):
    
    # ignoring the first chance exception
    if __DEBUGGER__.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED
    
    crash_reporter()

    return DBG_EXCEPTION_NOT_HANDLED


def crash_reporter():
    print '\n[+] Access Violation Happened!!'

    # using utils module to record the crash
    crash_info = utils.crash_binning.crash_binning()                # the crash_binning class from crash_binning file in the module
    crash_info.record_crash(__DEBUGGER__)
    print crash_info.crash_synopsis()


def usage():
    print "  ##*************************************** HELP MENU **************************************************##\n"
    print "  ########################################################################################################"
    print "  ### DESCRIPTION: analyzes a buffer overflow crash with a crash report ##################################"
    print "  ##############  when loaded with the executable path  ##################################################"
    print '  ### USAGE: python pydbg_memoryAccessViolation_crashReport.py [full path to exe] ########################'
    print "  ### EXAMPLE: python pydbg_memoryAccessViolation_crashReport.py c:\\Users\\kevin\\Desktop\\a.exe ########"
    print "  ########## REMEMBER: to put double backslashes in path so escape  ######################################"
    print "  ########## FOR THIS PARTICULAR SYSTEM: I ran this in the same path as the utils module addon directory #"
    print "  ########## path: c:\\Python27\\Libs\\paimei ############################################################"
    print "\n  ##****************************************************************************************************##"
    print "[!] Exiting..."


def error(msg, location):
    print " ##***********************************************************************##\n"
    print ' ### ERROR: ' + msg
    print ' ## LOCATION: ' + location
    print '\n ##***********************************************************************##'
    print '[!] Exiting...'


# script execution
if __name__ == '__main__':
    if len(sys.argv) < 2 :
        usage()
        sys.exit(1)
    else:
        start_time = time.time()
        main(sys.argv[1])
        end_time = time.time() - start_time
        print '\n[+] Main Execution Finished in %f seconds' % end_time
        print '[!] Exiting...'
        sys.exit(0)
        











