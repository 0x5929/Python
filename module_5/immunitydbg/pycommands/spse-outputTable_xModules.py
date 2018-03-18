#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time


# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "printing out a table with all the current running process's executable loaded modules and their info"

def main(args):
    # starting the debugger instance
    imm = immlib.Debugger()

    td = imm.createTable("Module Information", ["Name", "Base", "Entry", "Size", "File_Version"])
    # getAllModules will return a dictionary of all loaded executable modules
    xModules = imm.getAllModules()

    # immlib.Debugger has a getALlModules method, and that will return a list of module obj which is a
    # class with methods in the lib.immDebugger.Modules, methods like getName()...
    for entity in xModules.values():            # we are interested in the values part of each module obj
        # with hex formatting
        td.add(0, [ entity.getName(),
                    '%08X'%entity.getBaseAddress(),
                    '%08X'%entity.getEntry(),
                    '%08X'%entity.getSize(),
                    entity.getVersion()
                    ])
    ## ADDITIONALLY: logging current register info at this given instance moment of the running exe file
    imm.log(str(imm.getRegs()))
    imm.updateLog()
    
    return "[!] spse-outputTable_xModules.py is finished with status 0"

