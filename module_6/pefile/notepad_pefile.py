#!/usr/bin/env python


# importing necessary modules
import pefile
import pprint

# function definition
def print_seperator(message):
    if message == 'end of message':
        message = '=========='
    print '======================================================================='
    print '======================================================================='
    print '=======================     ' + message + '    ========================'
    print '======================================================================='
    print '======================================================================='

def worker(arg_tuple):
    message, print_obj = arg_tuple

    print_seperator('USING '+ message)
    
    # there are two different choices of commands issued:
    # 1. pprint
    # 2. print
    # could be added if more existed
    if message[1] == 'p':
        pprint.pprint(print_obj)
    elif message[1] == 'r':
        print print_obj 
    
    print_seperator('end of message')


def main(): 
    # lets attach a portable executable (pretty much all executables in windows i assume)
    # double \ because we need to escape it for the second one
    pe = pefile.PE('c:\\windows\\notepad.exe')
   
    # we could print out our pe object's structure like such
    worker(('pprint.pprint(dir(pe)))', dir(pe)))

    # we could also print out our DOS HEADER object's structure
    worker(('pprint.pprint(dir(pe.DOS_HEADER)))', dir(pe.DOS_HEADER)))

    # checking out if the executable have the mz signature that is in the DOS HEADER
    # mz signature means that this is a DOS executable (first two bytes stating MZ)
    worker(('print hex(pe.DOS_HEADER.e_magic)', hex(pe.DOS_HEADER.e_magic)))

    # offset to the new exe file header
    worker(('print hex(pe.DOS_HEADER.e_lfanew)', hex(pe.DOS_HEADER.e_lfanew)))

    # numbers of sections
    worker(('print pe.FILE_HEADER.NumberOfSections', pe.FILE_HEADER.NumberOfSections))

    # lets see what is a structure of one of our sections, we will take our first section for example
    worker(('pprint.pprint(dir(pe.sections[0]))', dir(pe.sections[0])))
    
    for section in pe.sections:
        print section.Name
        print section.SizeOfRawData
        print '\n'

# script execution
if __name__ == '__main__':
    main()



