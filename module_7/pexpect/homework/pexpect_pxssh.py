#!/usr/bin/python


# this script is run on fedora to test ssh connection to ubuntu server
# using pxssh class of the pexpect module

from pexpect import pxssh
import getpass
import sys

try: 
    ssh_session = pxssh.pxssh()
    
    hostname = raw_input('hostname/IP: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    
    # log in could be implemented with login method
    ssh_session.login(hostname, username, password)
    
    # sending first command
    ssh_session.sendline('uptime')

    ssh_session.prompt()        # prompt is like expect method, but already uses the usual and unique prompt chars like # or $
    print ssh_session.before

    # sending second command
    ssh_session.sendline('ls -la')
    ssh_session.prompt()

    for line in ssh_session.before.split('\n'):
        print line
    
    ssh_session.logout()
    sys.exit(0)

except pxssh.ExceptionPxssh as e:
    print 'pxssh has failed on login'
    print e
    sys.exit(1)
