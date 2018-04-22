#!/usr/bin/env python


# importing modules

import pefile
import sys


"""
    this is ran in a windows 7 environment
"""

# function definitions
def usage():
    print "##******************************* HELP MENU ************************************##"
    print "##################################################################################"
    print "###DESCRIPTION: checks if the pe file imports the given dll ######################"
    print "##############  if so, prints out all the imports names of dll ###################"
    print '###USAGE: python import_checker.py [full name of Dll] [full path to pe file] ###'
    print "###EXAMPLE: python import_checker.py ADVAPI32.dll c:\\windows\\notepad.exe   ###"
    print "###WARNING: please remember to put two \ for escaping purposes, like such: #######"
    print "########## c:\\windows\\notepad.exe ##############################################"
    print "##******************************************************************************##"

def error(msg, location):
    print "##***********************************************************************##"
    print '###ERROR: ' + msg
    print '##LOCATION: ' + location
    print '##***********************************************************************##'

def output(entry):
    print "[+] Congrats! The dll: " + entry.dll + ' is imported by the given pe file'
    print '[+] ' + entry.dll + " has the following imports: \n"
    for entry_import in entry.imports:
        print '\t [+] ADDRESS: ' + hex(entry_import.address) + ' NAME: ' + entry_import.name

def dll_check(dll, pe):
    try:
        pe = pefile.PE(pe)
    except:
        err_msg = 'could not resolve the pe file, please check the path to file file'
        loc = 'dll_check'
        error(err_msg, loc)
        sys.exit(1)
    
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        if entry.dll == dll:
            try: 
                output(entry)
            except: 
                err_msg = 'could not output matching dll and its imports'
                loc = 'output'
                error(err_msg, loc)
                sys.exit(1)
    
    print "[!] DLL CHECK COMPLETE\n"

def main(argv):
    dll_name, pe_path = argv
    dll_check(dll_name, pe_path)
    print "[!] Exiting...\n"

# script execution
if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    print "\n[!] Welcome to Dll Checker for Portable Executables (PE)!!\n"

    dll = sys.argv[1]
    pe = sys.argv[2]
    main((dll, pe))
    sys.exit(0)


