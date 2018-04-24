#!/usr/bin/env python


# importing modules
import pydasm


# the key thing to disassembling instructions is to feed in
# the raw hex code of the instruction
# we can use pydasm.get_instruction method
# first parameter is the hex instruction, and the second parameter is the mode
# return value is an instance of an instruction obj that has the original instruction of \x50 in hex and for 32 bit processor
# all that is stored inside the instruction variable
# with some practices, we can see that get_instruction method ONLY gets the first instruction and its operands
# and that is why offset is used in getting the instruction_string
instruction = pydasm.get_instruction('\x50', pydasm.MODE_32)

# get get the string value of the instruction, do the following:
# first param is the instruction obj, and second and third is format and offset
instruction_string = pydasm.get_instruction_string(instruction, pydasm.FORMAT_INTEL, 0)

# \x50 is push eax
print "[!] The instruction \\x50 is disassembled to:  %s" %instruction_string

print '========================================================================='

instruction = pydasm.get_instruction('\x85\xc0', pydasm.MODE_32)

# another format we can use is pydasm.FORMAT_ATT ==> this will result 'test %eax, %eax' format
instruction_string = pydasm.get_instruction_string(instruction, pydasm.FORMAT_INTEL, 0)

# \x85\xc0 is test eax, eax
print "[!] The instruction \\x85\\xc0 is disassembled to: %s" %instruction_string


print '========================================================================='

instruction = pydasm.get_instruction('\xc2\x04\x00', pydasm.MODE_32)

instruction_string = pydasm.get_instruction_string(instruction, pydasm.FORMAT_INTEL, 0)

# \xc2\x04\x00 is retn 0x4
print "[!] The instruction \\x85\\xc0 is disassembled to: %s" %instruction_string

