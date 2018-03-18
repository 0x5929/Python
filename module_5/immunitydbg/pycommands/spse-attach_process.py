#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time


# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "attach echo server process, make sure you enter the correct active PID of echo_server.exe as the input parameter"

def main(args):
    # starting the debugger instance
    imm = immlib.Debugger()

    # we can attach by ipnut PID, on cmd prompt first argument given while running the program in imm
    imm.Attach(int(args[0]))

    
    return "[!] spse-attach_process is finished with status 0"

