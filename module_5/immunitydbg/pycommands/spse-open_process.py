#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time


# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "start echo server process"

def main(args):
    # starting the debugger instance
    imm = immlib.Debugger()

    # first we need to open/start the process
    imm.openProcess("c:\\Documents and Settings\\kevin\\Desktop\\Echo_Server\\echo_server.exe")
    
    return "[!] spse-open_process is finished with status 0"

