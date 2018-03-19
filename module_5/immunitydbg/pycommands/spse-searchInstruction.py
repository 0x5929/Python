#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time


# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "Find instructions, using assemble disassemble search, find module api"

def main(args):
    # starting the debugger instance
    imm = immlib.Debugger()

    # we will find a string of commands given byh the list of arguments
    # and that string will be assembled, returning a string value of the assembled instruction
    assembledInstruction = imm.assemble(' '.join(args))

    if not assembledInstruction:                        # check if the arguments of commands were passed in for imm.assemble
        return "[!] No Instruction Given!!!"            # if not passed in, we will output to status bar

    addressList = imm.search(assembledInstruction)      # this will search the input the assembled instruction string and finds
                                                        # patterns of it in the current running script, returns a list of addresses of where the
                                                        # instructions appear

    # creating a table to output infomation from the input command search
    td = imm.createTable("Instruction Locations",['Module', 'Base Address', 'Instruction Address', 'Instruction'])

    for address in addressList:
        # wget module for this address
        module = imm.findModule(address)                # this will find the module that contains this address

        if not module:                                  # if no returned list of module info
            imm.log("Address: 0x%08X not in any module"%address)
            continue

        # Get module Object by name

        instruction = ''                                # initializing instruction variable

        numArgs = len(' '.join(args).split('\n'))       # getting the count of arugments passed in by user

        for count in range(0, numArgs):                 # iterating through the number of lines inputed as arguments, if more lines are
                                                        # supplied, meaning we need to access the next instruction memory, and increment
                                                        # through all of it, and joining all of them with ' ' 
                                                        # returns the string of the disassembled instruction starting with an address, and
                                                        # go on for however many lines in the next instructions require
                                                        
            instruction += imm.disasmForward(address, nlines=count).getDisasm() + ' '

        # adding to the table
        td.add(0, [ module[0],                          # first element from the list returned from findModule, name
                    str('0x%08X'%module[1]),             # second element from the list returned from findModule, base address
                    str('0x%08X'%address),              # address found
                    instruction])                       # the instruction searched

        
        
        
    

    return "[!] spse-findInstruction.py is finished with status 0"

