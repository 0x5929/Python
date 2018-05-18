#!/usr/bin/python


#NOTE: executing this script in fedora ssh into 192.168.1.114 ubuntuserver16
# importing the module we are going to use
import pexpect
import sys

def main(argv):
    # first we have to use pexpect's spawn method 
    # using it as if we were typing the command on terminal
    pex = pexpect.spawn('ssh kevin@192.168.1.114')
    
    # and then we are expecting certain outputs as if it were to the terminal screen
    # expect method can also be used which can take a Regex
    pex.expect_exact('password')  # it searches for beginning of string
    
    # once we have expected that Name string, we will have control of that specific line
    pex.sendline(argv)
    
    user_host_home_dir = 'kevin@ubuntuServer:~$'
    # repeat for the following steps
    pex.expect_exact(user_host_home_dir)

    pex.sendline('ls')

    # now we are expecting the next ftp line, so we can use the before method to see what was between giving the ls cmd and ftp
    pex.expect_exact(user_host_home_dir)

    lines = pex.before.split('\n')

    # printing out the lines
    for line in lines:
        print line


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'please enter ssh password as cmd line param'
        print 'format is: python pexpect_ssh.py [pw-IP]'
        print 'or: ./pexpect_notes.py [pw-IP]'
        print 'example: ./pexpect_ssh.py password'
        sys.exit(1)
    else:
        main(sys.argv[1])
        sys.exit(0)
