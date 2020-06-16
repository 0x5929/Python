#!/usr/bin/env python


# importing modules
import immlib
from immlib import BpHook

DESC = "This script will set a breakpoint at strcpy and evaulate the stack at the same time"

class StrcpyBpHook (BpHook):

    def __init__(self):
        BpHook.__init__(self)

    def run(self, registers):       # each hpHook obj has a dictionary of registers and their respective values at the hook instance 
        imm = immlib.Debugger()     # for logging purpose
        imm.log("strcpy Hook Initiated")

        esp = imm.readLong(registers['ESP'])
        eip = imm.readLong(registers['EIP'])
        
        # at the beginning of any function call, after the stackframe initiates, or as part of it, 
        # the second function param is pushed to the stack first, and then the first param gets pushed in, 
        # here at the breakpoint of the beginning of the function call, it is safe to say that 
        # in a 4 byte stack frame the stack frame pointer previous 4 bytes is the first param, 
        # and at its 4 previous bytes (8 referenced to the stack pointer) is the second param 
        
        first_arg_addr = imm.readLong(registers['ESP'] + 4)
        second_arg_addr = imm.readLong(registers['ESP'] + 8)
        
        imm.log("ESP: 0x%08x, EIP: 0x%08x, first_arg: 0x%08x, second_arg: 0x%08x" % (esp, eip, first_arg_addr, second_arg_addr))

        recv_str = imm.readString(second_arg_addr)       # since the second argument is the recived string pointer in c

        imm.log("Any suspicious string with certain suspicious chars can potential cause of a buffer overflow")
        imm.log("Received String: %s" % recv_str)
        imm.log("Received String Length: %d" % len(recv_str))


## for the immmunity debugger platform, the main function must have an input list of args 
## so they can be inputted from immunity debugger gui
def main(args):

    imm = immlib.Debugger()
    function_name = "msvcrt.strcpy"             # please do a follow up investigation on that name to the function
    
    # finding out the function address in the program memory
    function_address = imm.getAddress(function_name)

    if not function_address:
        return "[!] ERROR: STRCPY FUNCTION ADDRESS NOT FOUND"
    
    # remember in python we dont need the new keyword
        # creating the hook obj from class
    bpHook = StrcpyBpHook()

        # binding/adding the strcpy function address and name to the hook
    bpHook.add(function_name, function_address)
    
    # logging
    imm.log("function: %s, at address: 0x%08x hooked successfully!" % (function_name, function_address))
    

    return "[!] spse-strcpy_focus.py has successfully executed."







## BELOW METHOD IS USED TO SET A BREAKPOINT, BUT INSTEAD WE WILL USE A BREAKPOINT HOOK 
## BECAUSE WE CAN JUST EVALUATE REGISTER VALUES WHEN THE HOOK IS TRIGGERED AT STR_CPY FUNCTION CALL AT THE BREAKPOINT
#    # first we need to find the function in the binary code 
#    function_name = "strcpy"
#    function_address = imm.seasrchFunctionByName(function_name)
#
#    if  not function_address:           # if there are no function by the name we inputted
#        imm.log("[!] Error: the strcpy function was not found..")
#
#    # next we will set the breakpoint at that function address
#    imm.setBreakpoint(function_address)
#
#    # next we need to evaluate the function arguments that is pushed to the stack
#    return "[!] spse-strcpy_focus.py has successfully executed."


