#!/usr/bin/env python

##### this python script is saved under pycommand inside immdbg directory
##### this script can be run along side with immdbg to automate debugging binary tasks
##### and print out useful results for analysis at a later time

# importing necessary modules

import immlib		# this lib is shipped with the immunity framework


DESC = "this script will output a tabulated window with results we need"

def main(args):
    imm = immlib.Debugger()

    # creating table data
        # arg => first argument is string of the name of table,
        # second argument is another list of column names
    td = imm.createTable("my_table", ["PID", "Name"])

    # now we have to populate the table
     # the method add takes args=> first arg is 0 for writing to table
     # second arg is a tuple of the row data
    td.add(0, ["26", "kevin"])
