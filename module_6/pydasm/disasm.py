#!/usr/bin/env python

"""
    THIS WILL BE EXECUTED ON A FEDORA SYSTEM

"""


# importing modules

import pydasm
import sys

# global variables initialization
__BYTECOUNT__ = 0

# function definitions
def usage():
    print "##******************************* HELP MENU ************************************##"
    print "##################################################################################"
    print "###DESCRIPTION: disassembles a hex executable ####################################"
    print "##############  with an option of how many bytes to disasm #######################"
    print '###USAGE: [stdin of executable hex code] ./diasm.py [optional bytes to parse]#####'
    print "###EXAMPLE: cat shellcode | ./diasm.py 200 #######################################"
    print "########## for disassembling first 200 bytes of shell code, output would be like:#"
    print "########## [snip]... [hex executable] [assembly instruction]######################"
    print "##******************************************************************************##"
    print "[!] Exiting..."

def error(msg, location):
    print "##***********************************************************************##"
    print '###ERROR: ' + msg
    print '##LOCATION: ' + location
    print '##***********************************************************************##'
    print '[!] Exiting...' 

def disassemble(buf):
    # the actual diassembly process
    # we need an offset to keep track of each instruction in the given shell executable
    # we also need a list of tuples to be outputted
    offset = 0
    output = []

    # now we have to loop through all the executable hex and and parse each instruction, increment offset
    # get_instruction method only gets the first instruction in the first input argument 
    while offset < len(buf):
        # check if bytecount was inputted by user, and return function once reached byte count
        if __BYTECOUNT__ is not 0 and offset >= __BYTECOUNT__:
            print '[+] Byte count was given, and all is parsed until bytecount'
            return output
        
        # get instruction
        instruction = pydasm.get_instruction(buf[offset:], pydasm.MODE_32)
        if not instruction:
            print '[+] Cannot find intructions in the given buffer at offset: ', offset
            return output
        instruction_string = pydasm.get_instruction_string(instruction, pydasm.FORMAT_INTEL, offset)
        
        # increment offset, while keeping track of old one
        old_offset = offset
        offset = offset + instruction.length

        # append to output
        output.append((buf[old_offset:offset + 1], instruction_string))
    
    return output

def stdo_print(listOfPrintables):
    """
        Param format: [(hex, instruction)]
    """
    print "#####################################################"
    print "PRINTING OUT INPUT HEX AND OUTPUT DISASSEMBLY INSTRUCTION: \n"
    for h, i in listOfPrintables:
        print '========================='
        print 'hex: ', h
        print 'instruction: %s' %i
    print "[+] Finished printing all instructions"

def main(buf):
    # given the buffer as input param
    # we will disassemble first, and print out the output
    output = disassemble(buf)
    stdo_print(output)

    print '[!] Exiting...'


# script execution
if __name__ == '__main__':
    if sys.stdin.isatty():                              # meaning no executable hex code in the standard input file descriptor
        usage()                                         # run usage function
        sys.exit(1)                                     # then gracefully exits with status code of 1
    else:                                               # meaning we have an input in the stdin file descriptor
        buf = sys.stdin.read()
        buf = buf[:-1]                                  # eliminating the last char, which is a line feed
        
        if len(sys.argv) == 2:                          # given an input byte count to parse
            try:
                __BYTECOUNT__ = int(sys.argv[1])        # lets try to parse the byte count from input
            except ValueError:
                err_msg = 'Could not parse the byte count from terminal user input, please run the program without any input for help menu'
                loc = 'script execution'
                error(err_msg, loc)
                sys.exit(1)
        main(buf)
        sys.exit(0)                                     # gracefully exits with status code of 0 for success
