#!/usr/bin/python


import paramiko
import getpass
import sys

# paramiko makes it very easy to use sftp to upload and download files from a remote server
# it does this on the ssh layer

# we will start by invoking ssh client first in this case, ssh
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

# now once connected, we can invoke the sftp module by simply calling the open_sftp method
sftp = ssh.open_sftp()

print 'changing directory to root using chdir() method, passing in path'
sftp.chdir('/')

print 'printing out ls results, using listdir() method'
print sftp.listdir()

print 'going back to home directory'
sftp.chdir('/home/kevin')

print 'what is in our home directory?'
print sftp.listdir()

print 'uploading uname-pword.txt to remote server home dir'
# we use put method, with first arg as path to upload, and second arg as path and name of uploaded file
sftp.put('uname-pword.txt', 'uname-pword.txt.cpy')
print 'checking ls'
print sftp.listdir()

print 'downloading uname-pword.txt.cpy to our system'
# we use get method, with first arg as the path to download, and second arg as the path and name of downloaded file
sftp.get('uname-pword.txt.cpy', 'uname-pword.txt.cpy.cpy')
print 'exiting..'



# closing connection
ssh.close()
sys.exit(0)
