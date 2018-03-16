#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time

#NOTE: this script will create the same table as the attach table in the immdbg gui

# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "this script will output a tabulated window with results of process info"

def main(args):
    imm = immlib.Debugger()

    # creating table data
        # arg => first argument is string of the name of table,
        # second argument is another list of column names   
    td = imm.createTable("my_table", ["PID", "Name", "Path", "Services"])
    
    # now we have to populate the table
     # the method add takes args=> first arg is 0 for writing to table
     # second arg is a list of the row data

    psList = imm.ps()   # first we are getting a list of current processes

    for process in psList:
        td.add(0, [str(process[0]), process[1], process[2], str(process[3])])

    return "[!] HELLO WORLD PROCESS INFO TABLE CREATED"
