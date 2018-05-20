#!/usr/bin/python


import paramiko
import getpass
import sys

# starting by invoking the client we want
# in this case, ssh
ssh = paramiko.SSHClient()

# for first time connections, we need to auto add host key
# by calling the  set missing host key policy, and passing in 
# the auto add policy
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connecting to ssh server at ip, username, and password
ip = raw_input('Host name/IP: ')
username = raw_input('Username: ')
password = getpass.getpass('Password: ')

ssh.connect(ip, username=username, password=password)

# now once connected, we can execute commands as if we were on a terminal shell for remote ssh
# using the exec command method, and it returns a tuple of all three standard file descriptors
stdin, stdout, stderr = ssh.exec_command('ls -la')

# standard output from the return of exec command as a readline method
for line in stdout.readlines():
    print line.strip()      # each line has a strip property to get content
                

# closing connection
ssh.close()
sys.exit(0)
