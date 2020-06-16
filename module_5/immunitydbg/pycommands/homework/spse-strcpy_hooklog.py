#!/usr/bin env python

# importing the necessary modules

import immlib
from immlib import FastLogHook

DESC = "This script will attach a hook to strcpy function and analyze its function data as the program runs"


# define main
def main(args):
    
    """
        Usage: First Run the script to install hook, then run it again to get results onto log screen
    """

    imm = immlib.Debugger()

    name = "strcpy_hook"

    # first lets try to extract the hook obj from our imm knowledge db
    fastHookObj = imm.getKnowledge(name)

    # if we do indeed already have a hook
    if fastHookObj:

        # we want to log evaulated results at the instance of the hook, and output to status bar
        logResults(imm, fastHookObj)
        
        return "[!] Please check the log window for more information"

    # if we don't already have a hooked obj, meaning this is the first run
    # get hooked function name and address
    strcpy_name = 'msvcrt.strcpy'
    strcpy_addr = imm.getAddress(strcpy_name)

    # initiate the hook
    fastHookObj = FastLogHook(imm) 

    # hook our function at its address by using the logFunction method of our hook obj
    fastHookObj.logFunction(strcpy_addr)

    # store/log our first and second arg by using the esp register and its offset for the two variables
    # in a standard 32 bit system that is esp+4 for the first arg, and esp+8 for the second arg
    fastHookObj.logBaseDisplacement("ESP", 4)   # this will be logged as the first esp value in the obj
    fastHookObj.logBaseDisplacement("ESP", 8)   # this will be logged as the second esp value in the obj

    # set the hook
    fastHookObj.Hook()

    # save the obj in the db for imformation grabbing
    # passing in our name, obj, and flag for a forceful add to elimenate errs
    imm.addKnowledge(name, fastHookObj, force_add=1)
    
    # output to status bar
    return "[!] spse-strcpy_hook.py has run successfully"


def logResults(imm, fastHookObj):

        # lets log some information about our hook
        hook_log = fastHookObj.getAllLog()

        # realistically this will only have one element in the list?
        imm.log(str(hook_log))
        
        # unpack our one item list
        # according to stackexchange answer @ https://reverseengineering.stackexchange.com/questions/2502/use-of-fastloghook-function-in-immlib
        # the data structure is:
        (func_addr, (first_arg, second_arg)) = hook_log[0] 

        # second argument's string value: by passing in the address of second argument
        string = imm.readString(second_arg)

        # logging results
        imm.log("Any suspicious string with certian suspicious chars can potential cause of a buffer overflow")
        imm.log("Received String: %s" % string)
        imm.log("Received String Length: %d" % len(string))
