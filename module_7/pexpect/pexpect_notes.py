#!/usr/bin/python

#NOTE: executing this script in ubuntu server (where our ftp server lives)
# importing the module we are going to use
import pexpect
import sys

def main(argv):
    # first we have to use pexpect's spawn method 
    # using it as if we were typing the command on terminal
    pex = pexpect.spawn('ftp localhost 45000')
    
    # and then we are expecting certain outputs as if it were to the terminal screen
    # expect method can also be used which can take a Regex
    pex.expect_exact('Name')  # it searches for beginning of string
    
    # once we have expected that Name string, we will have control of that specific line
    pex.sendline(argv[0])
    
    # repeat for the following steps
    pex.expect_exact('Password')
    
    pex.sendline([argv[1]])

    pex.expect_exact('ftp')

    pex.sendline('ls')

    # now we are expecting the next ftp line, so we can use the before method to see what was between giving the ls cmd and ftp
    pex.expect_exact('ftp')

    lines = pex.before.split('\n')

    # printing out the lines
    for line in lines:
        print line


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'please enter ip and port as params'
        print 'format is: python pexpect_notes.py [ftp-server-name] [pw]'
        print 'or: ./pexpect_notes.py [ftp-server-name] [pw]'
        print 'example: ./pexpect_notes.py kevin-ftp password'
        sys.exit(1)
    else:
        main((sys.argv[1], sys.argv[2]))
        sys.exit(0)
